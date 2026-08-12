#!/usr/bin/env python3
"""
brand-readme onboard script
Extracts design tokens from a target URL and proposes a style-guide.md update.

Usage:
    python3 scripts/onboard.py https://yoursite.com
    python3 scripts/onboard.py https://yoursite.com --apply
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser


# --- Color Utilities ---

def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    return int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB tuple to hex string."""
    return f"#{r:02X}{g:02X}{b:02X}"


def relative_luminance(r: int, g: int, b: int) -> float:
    """Calculate relative luminance per WCAG 2.1."""
    def linearize(c: int) -> float:
        c_norm = c / 255.0
        return c_norm / 12.92 if c_norm <= 0.03928 else ((c_norm + 0.055) / 1.055) ** 2.4

    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(fg: tuple[int, int, int], bg: tuple[int, int, int]) -> float:
    """Calculate WCAG contrast ratio between two colors."""
    l1 = relative_luminance(*fg)
    l2 = relative_luminance(*bg)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def adjust_for_contrast(fg: tuple[int, int, int], bg: tuple[int, int, int], min_ratio: float = 4.5) -> tuple[int, int, int]:
    """Adjust foreground luminance until contrast ratio meets minimum."""
    ratio = contrast_ratio(fg, bg)
    if ratio >= min_ratio:
        return fg

    bg_lum = relative_luminance(*bg)
    r, g, b = fg

    # Determine direction: darken if bg is light, lighten if bg is dark
    if bg_lum > 0.5:
        # Darken the foreground
        for _ in range(20):
            r = max(0, int(r * 0.9))
            g = max(0, int(g * 0.9))
            b = max(0, int(b * 0.9))
            if contrast_ratio((r, g, b), bg) >= min_ratio:
                return (r, g, b)
    else:
        # Lighten the foreground
        for _ in range(20):
            r = min(255, int(r + (255 - r) * 0.1))
            g = min(255, int(g + (255 - g) * 0.1))
            b = min(255, int(b + (255 - b) * 0.1))
            if contrast_ratio((r, g, b), bg) >= min_ratio:
                return (r, g, b)

    return (r, g, b)


# --- CSS Parsing ---

COLOR_RE = re.compile(
    r"(?:#[0-9a-fA-F]{3,8})"
    r"|(?:rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*(?:,\s*[\d.]+\s*)?\))"
)

FONT_FAMILY_RE = re.compile(
    r"font-family\s*:\s*([^;}{]+)"
)

BG_COLOR_RE = re.compile(
    r"background(?:-color)?\s*:\s*([^;}{]+)"
)

COLOR_PROP_RE = re.compile(
    r"(?<!background-)color\s*:\s*([^;}{]+)"
)


def parse_rgb_string(s: str) -> tuple[int, int, int] | None:
    """Parse rgb(r,g,b) or rgba(r,g,b,a) to tuple."""
    match = re.match(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", s)
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3))
    return None


def normalize_color(color_str: str) -> str | None:
    """Normalize a CSS color value to hex."""
    color_str = color_str.strip()
    if color_str.startswith("#"):
        hex_val = color_str.lstrip("#")
        if len(hex_val) == 3:
            hex_val = "".join(c * 2 for c in hex_val)
        if len(hex_val) == 6:
            return f"#{hex_val.upper()}"
    elif color_str.startswith("rgb"):
        rgb = parse_rgb_string(color_str)
        if rgb:
            return rgb_to_hex(*rgb)
    return None


# --- HTML/CSS Extraction ---

class StyleExtractor(HTMLParser):
    """Extract inline styles and linked stylesheet hints from HTML."""

    def __init__(self):
        super().__init__()
        self.styles: list[str] = []
        self.fonts: dict[str, str] = {}
        self.colors: dict[str, str] = {}
        self._in_style = False
        self._style_buf = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        attr_dict = dict(attrs)
        if tag == "style":
            self._in_style = True
            self._style_buf = ""

        # Extract inline style hints
        style = attr_dict.get("style", "")
        if style:
            self.styles.append(style)

    def handle_data(self, data: str):
        if self._in_style:
            self._style_buf += data

    def handle_endtag(self, tag: str):
        if tag == "style" and self._in_style:
            self._in_style = False
            self.styles.append(self._style_buf)


def extract_tokens_from_css(css_text: str) -> dict[str, str]:
    """Extract semantic tokens from CSS text."""
    tokens: dict[str, str] = {}

    # Look for CSS custom properties on :root
    root_match = re.search(r":root\s*\{([^}]+)\}", css_text)
    if root_match:
        root_block = root_match.group(1)
        for match in re.finditer(r"--([\w-]+)\s*:\s*([^;]+)", root_block):
            tokens[f"--{match.group(1)}"] = match.group(2).strip()

    # Extract background colors
    bg_matches = BG_COLOR_RE.findall(css_text)
    if bg_matches:
        for bg in bg_matches:
            normalized = normalize_color(bg.strip())
            if normalized and "paper" not in tokens:
                tokens["paper_candidate"] = normalized

    # Extract text colors
    color_matches = COLOR_PROP_RE.findall(css_text)
    if color_matches:
        for color in color_matches:
            normalized = normalize_color(color.strip())
            if normalized and "ink_candidate" not in tokens:
                tokens["ink_candidate"] = normalized

    # Extract font families
    font_matches = FONT_FAMILY_RE.findall(css_text)
    if font_matches:
        tokens["font_candidate"] = font_matches[0].strip().strip("\"'")

    return tokens


def fetch_and_extract(url: str) -> dict[str, str]:
    """Fetch URL and extract design tokens."""
    headers = {"User-Agent": "brand-readme-onboard/1.0"}
    req = Request(url, headers=headers)

    try:
        with urlopen(req, timeout=15) as response:
            html = response.read().decode("utf-8", errors="replace")
    except (URLError, HTTPError) as e:
        print(f"✗ Failed to fetch {url}: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse HTML for inline styles
    parser = StyleExtractor()
    parser.feed(html)

    # Combine all style content
    all_css = "\n".join(parser.styles)

    # Also extract from <link> stylesheets referenced in HTML
    # (simplified: just parse what's inline for the MVP)
    tokens = extract_tokens_from_css(all_css)

    # Try to map to semantic roles
    result: dict[str, str] = {}

    # Defaults
    defaults = {
        "--paper": "#FFFFFF",
        "--paper-2": "#F6F8FA",
        "--ink": "#1F2328",
        "--muted": "#656D76",
        "--accent": "#0969DA",
        "--accent-subtle": "#DDF4FF",
        "--font-title": '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif',
        "--font-body": '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif',
        "--font-mono": 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace',
    }

    # Map extracted values to semantic roles
    result.update(defaults)

    if "paper_candidate" in tokens:
        result["--paper"] = tokens["paper_candidate"]
    if "ink_candidate" in tokens:
        result["--ink"] = tokens["ink_candidate"]
    if "font_candidate" in tokens:
        result["--font-body"] = tokens["font_candidate"]
        result["--font-title"] = tokens["font_candidate"]

    # Map any CSS custom properties that match our token names
    for key in ["--paper", "--paper-2", "--ink", "--muted", "--accent"]:
        if key in tokens:
            normalized = normalize_color(tokens[key])
            if normalized:
                result[key] = normalized

    return result


# --- Contrast Verification ---

def verify_contrast(tokens: dict[str, str]) -> list[dict[str, str]]:
    """Verify WCAG AA contrast ratios, return list of adjustments."""
    adjustments: list[dict[str, str]] = []
    paper_rgb = hex_to_rgb(tokens.get("--paper", "#FFFFFF"))

    checks = [
        ("--ink", 4.5),
        ("--muted", 3.0),
        ("--accent", 4.5),
    ]

    for token_name, min_ratio in checks:
        color_hex = tokens.get(token_name)
        if not color_hex or not color_hex.startswith("#"):
            continue

        fg_rgb = hex_to_rgb(color_hex)
        ratio = contrast_ratio(fg_rgb, paper_rgb)

        if ratio < min_ratio:
            adjusted_rgb = adjust_for_contrast(fg_rgb, paper_rgb, min_ratio)
            adjusted_hex = rgb_to_hex(*adjusted_rgb)
            new_ratio = contrast_ratio(adjusted_rgb, paper_rgb)
            adjustments.append({
                "token": token_name,
                "original": color_hex,
                "adjusted": adjusted_hex,
                "original_ratio": f"{ratio:.1f}:1",
                "adjusted_ratio": f"{new_ratio:.1f}:1",
                "min_required": f"{min_ratio}:1",
            })
            tokens[token_name] = adjusted_hex

    return adjustments


# --- Output ---

def generate_style_guide(tokens: dict[str, str], url: str) -> str:
    """Generate the style-guide.md content."""
    today = date.today().isoformat()

    return f"""# Style Guide — Brand Readme Token Store

> Single source of truth for colors, fonts, and spacing.
> Edit this file directly or run `/brand-readme:onboard <URL>` to auto-populate.

---

## Status

- **Configured:** Yes
- **Last Updated:** {today}
- **Source URL:** {url}

---

## Color Tokens — Light Mode

| Token | Semantic Role | Value |
| :--- | :--- | :--- |
| `--paper` | Background canvas | `{tokens['--paper']}` |
| `--paper-2` | Surface / card fill | `{tokens.get('--paper-2', '#F6F8FA')}` |
| `--ink` | Primary text, titles, outlines | `{tokens['--ink']}` |
| `--muted` | Sublabels, dates, hairlines | `{tokens.get('--muted', '#656D76')}` |
| `--accent` | Focal callout, active badge | `{tokens.get('--accent', '#0969DA')}` |
| `--accent-subtle` | Tinted background (10-15% opacity) | `{tokens.get('--accent-subtle', '#DDF4FF')}` |

---

## Color Tokens — Dark Mode

| Token | Semantic Role | Value |
| :--- | :--- | :--- |
| `--paper` | Background canvas | `#0D1117` |
| `--paper-2` | Surface / card fill | `#161B22` |
| `--ink` | Primary text, titles, outlines | `#F0F6FC` |
| `--muted` | Sublabels, dates, hairlines | `#8B949E` |
| `--accent` | Focal callout, active badge | `#58A6FF` |
| `--accent-subtle` | Tinted background (10-15% opacity) | `#0C2D6B` |

---

## Typography Stack

| Role | Token | Font Stack |
| :--- | :--- | :--- |
| Titles & Display | `--font-title` | `{tokens['--font-title']}` |
| Body & Descriptions | `--font-body` | `{tokens['--font-body']}` |
| Code & Metrics | `--font-mono` | `{tokens['--font-mono']}` |

---

## Spacing & Grid

| Property | Value |
| :--- | :--- |
| Base grid unit | `8px` |
| Minimum increment | `4px` |
| Standard canvas width | `800px` |
| Hairline stroke | `1px` or `0.5px` |
| Corner radius (containers) | `0px` or `4px` |
| Corner radius (status dots) | `999px` (only for ≤8px circles) |

---

## Contrast Requirements

All text must satisfy **WCAG AA** minimum contrast ratios:

| Pair | Minimum Ratio |
| :--- | :--- |
| `--ink` over `--paper` | ≥ 4.5:1 |
| `--muted` over `--paper` | ≥ 3:1 (large text only) |
| `--accent` over `--paper` | ≥ 4.5:1 |
| `--ink` over `--paper-2` | ≥ 4.5:1 |
"""


def main():
    parser = argparse.ArgumentParser(
        description="Extract brand tokens from a URL for brand-readme skill."
    )
    parser.add_argument("url", help="URL to extract design tokens from")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write extracted tokens to references/style-guide.md",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output path (default: references/style-guide.md relative to script)",
    )
    args = parser.parse_args()

    print(f"→ Fetching {args.url}...")
    tokens = fetch_and_extract(args.url)

    print("→ Verifying WCAG AA contrast...")
    adjustments = verify_contrast(tokens)

    if adjustments:
        print("\n⚠  Contrast adjustments required:")
        for adj in adjustments:
            print(f"   {adj['token']}: {adj['original']} → {adj['adjusted']}")
            print(f"     Ratio: {adj['original_ratio']} → {adj['adjusted_ratio']} (min: {adj['min_required']})")
        print()

    # Print summary
    print("\n✓ Extracted tokens:")
    for key in ["--paper", "--paper-2", "--ink", "--muted", "--accent"]:
        print(f"  {key:16s} {tokens.get(key, 'N/A')}")
    print(f"  {'--font-title':16s} {tokens.get('--font-title', 'N/A')}")
    print(f"  {'--font-body':16s} {tokens.get('--font-body', 'N/A')}")
    print(f"  {'--font-mono':16s} {tokens.get('--font-mono', 'N/A')}")

    # Verify contrast results
    paper_rgb = hex_to_rgb(tokens["--paper"])
    ink_rgb = hex_to_rgb(tokens["--ink"])
    accent_hex = tokens.get("--accent", "#0969DA")
    accent_rgb = hex_to_rgb(accent_hex)
    print(f"\n  Contrast ink/paper:    {contrast_ratio(ink_rgb, paper_rgb):.1f}:1")
    print(f"  Contrast accent/paper: {contrast_ratio(accent_rgb, paper_rgb):.1f}:1")

    # Generate output
    content = generate_style_guide(tokens, args.url)

    if args.apply:
        output_path = args.output or (
            Path(__file__).parent.parent / "references" / "style-guide.md"
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)
        print(f"\n✓ Written to {output_path}")
    else:
        print("\n--- Proposed style-guide.md (pass --apply to write) ---")
        print(content)


if __name__ == "__main__":
    main()
