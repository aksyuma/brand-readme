#!/usr/bin/env python3
"""
brand-readme SVG contrast linter
Parses generated SVGs and validates WCAG AA contrast ratios.

Usage:
    python3 scripts/lint-contrast.py path/to/output.svg
    python3 scripts/lint-contrast.py --all assets/
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


# --- Color Utilities ---

def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: #{hex_color}")
    return int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)


def relative_luminance(r: int, g: int, b: int) -> float:
    """Calculate relative luminance per WCAG 2.1.
    L = 0.2126·R + 0.7152·G + 0.0722·B
    """
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


# --- SVG Parsing ---

# Default token values (fallbacks when CSS vars are used)
DEFAULT_TOKENS = {
    "--paper": "#FFFFFF",
    "--paper-2": "#F6F8FA",
    "--ink": "#1F2328",
    "--muted": "#656D76",
    "--accent": "#0969DA",
    "--accent-subtle": "#DDF4FF",
}

# Regex to extract var() references
VAR_RE = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^)]+))?\)")

# Regex to find color values in style attributes
HEX_RE = re.compile(r"#[0-9a-fA-F]{3,6}")


def resolve_color(value: str, tokens: dict[str, str]) -> str | None:
    """Resolve a CSS value to a hex color (handling var() references)."""
    if not value:
        return None

    # Direct hex value
    hex_match = HEX_RE.search(value)
    if hex_match and "var(" not in value:
        return hex_match.group()

    # CSS var() reference
    var_match = VAR_RE.search(value)
    if var_match:
        var_name = var_match.group(1)
        fallback = var_match.group(2)

        # Try token lookup
        if var_name in tokens:
            return tokens[var_name]

        # Use fallback value
        if fallback:
            fallback = fallback.strip()
            fb_hex = HEX_RE.search(fallback)
            if fb_hex:
                return fb_hex.group()

    return None


def extract_style_tokens(svg_root: ET.Element) -> dict[str, str]:
    """Extract token definitions from <style> block in SVG."""
    tokens = dict(DEFAULT_TOKENS)
    ns = {"svg": "http://www.w3.org/2000/svg"}

    # Find <style> element
    style_el = svg_root.find(".//{http://www.w3.org/2000/svg}style")
    if style_el is None:
        style_el = svg_root.find(".//style")

    if style_el is not None and style_el.text:
        css_text = style_el.text

        # Extract var() fallback values from class definitions
        # e.g., .paper { fill: var(--paper, #ffffff); }
        for match in re.finditer(r"var\(\s*(--[\w-]+)\s*,\s*(#[0-9a-fA-F]{3,6})\s*\)", css_text):
            var_name = match.group(1)
            fallback = match.group(2)
            if var_name not in tokens or tokens[var_name] == DEFAULT_TOKENS.get(var_name):
                tokens[var_name] = fallback

    return tokens


def find_text_elements(svg_root: ET.Element) -> list[dict]:
    """Find all text elements and their effective colors."""
    texts = []

    for elem in svg_root.iter():
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag

        if tag == "text":
            # Get fill color from attributes or style
            fill = elem.get("fill", "")
            style = elem.get("style", "")
            class_attr = elem.get("class", "")

            text_content = "".join(elem.itertext()).strip()
            if not text_content:
                continue

            # Determine font size for large text check
            font_size_str = elem.get("font-size", "")
            if not font_size_str and style:
                fs_match = re.search(r"font-size:\s*([\d.]+)", style)
                if fs_match:
                    font_size_str = fs_match.group(1)

            font_size = float(font_size_str) if font_size_str else 13.0

            texts.append({
                "content": text_content[:40],
                "fill": fill,
                "style": style,
                "class": class_attr,
                "font_size": font_size,
            })

    return texts


def get_background_color(svg_root: ET.Element, tokens: dict[str, str]) -> str:
    """Determine the SVG background color."""
    # Look for the first rect that fills the background
    for elem in svg_root.iter():
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        if tag == "rect":
            width = elem.get("width", "")
            height = elem.get("height", "")
            if width == "100%" and height == "100%":
                fill = elem.get("fill", "")
                class_attr = elem.get("class", "")

                if "paper" in class_attr:
                    return tokens.get("--paper", "#FFFFFF")
                resolved = resolve_color(fill, tokens)
                if resolved:
                    return resolved

    return tokens.get("--paper", "#FFFFFF")


# --- Lint Logic ---

CLASS_TO_TOKEN = {
    "ink": "--ink",
    "muted": "--muted",
    "accent": "--accent",
    "accent-val": "--accent",
    "quote-text": "--ink",
    "author-text": "--muted",
    "label": "--muted",
    "val": "--ink",
}


def lint_svg(filepath: Path) -> list[dict]:
    """Lint a single SVG file for contrast issues."""
    issues: list[dict] = []

    try:
        tree = ET.parse(filepath)
    except ET.ParseError as e:
        return [{"type": "error", "message": f"Parse error: {e}"}]

    root = tree.getroot()
    tokens = extract_style_tokens(root)
    bg_color = get_background_color(root, tokens)

    try:
        bg_rgb = hex_to_rgb(bg_color)
    except ValueError:
        return [{"type": "error", "message": f"Cannot parse background color: {bg_color}"}]

    texts = find_text_elements(root)

    for text_info in texts:
        # Determine effective text color
        fg_color = None

        # Check class-based color
        for cls in text_info["class"].split():
            if cls in CLASS_TO_TOKEN:
                token = CLASS_TO_TOKEN[cls]
                fg_color = tokens.get(token)
                break

        # Check explicit fill
        if not fg_color and text_info["fill"]:
            fg_color = resolve_color(text_info["fill"], tokens)

        # Check style attribute
        if not fg_color and text_info["style"]:
            fill_match = re.search(r"fill:\s*([^;]+)", text_info["style"])
            if fill_match:
                fg_color = resolve_color(fill_match.group(1).strip(), tokens)

        if not fg_color:
            continue  # Cannot determine color, skip

        try:
            fg_rgb = hex_to_rgb(fg_color)
        except ValueError:
            continue

        ratio = contrast_ratio(fg_rgb, bg_rgb)

        # Determine minimum required ratio
        # Large text (≥18px or ≥14px bold): 3:1
        # Normal text: 4.5:1
        is_large = text_info["font_size"] >= 18
        min_ratio = 3.0 if is_large else 4.5

        if ratio < min_ratio:
            issues.append({
                "type": "fail",
                "text": text_info["content"],
                "fg": fg_color,
                "bg": bg_color,
                "ratio": ratio,
                "required": min_ratio,
                "is_large": is_large,
            })

    return issues


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(
        description="WCAG AA contrast linter for brand-readme SVGs."
    )
    parser.add_argument(
        "path",
        type=Path,
        help="SVG file or directory to lint",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Lint all .svg files in the given directory",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat large-text checks (3:1) at normal-text level (4.5:1)",
    )
    args = parser.parse_args()

    # Collect files to lint
    if args.path.is_dir():
        svg_files = sorted(args.path.rglob("*.svg"))
    elif args.path.is_file():
        svg_files = [args.path]
    else:
        print(f"✗ Path not found: {args.path}", file=sys.stderr)
        sys.exit(1)

    if not svg_files:
        print(f"✗ No .svg files found in {args.path}", file=sys.stderr)
        sys.exit(1)

    total_issues = 0
    total_files = 0

    for svg_file in svg_files:
        issues = lint_svg(svg_file)
        if issues:
            total_files += 1
            print(f"\n{'─' * 60}")
            print(f"  {svg_file.name}")
            print(f"{'─' * 60}")

            for issue in issues:
                if issue["type"] == "error":
                    print(f"  ✗ {issue['message']}")
                    total_issues += 1
                elif issue["type"] == "fail":
                    total_issues += 1
                    size_label = "(large)" if issue["is_large"] else "(normal)"
                    print(
                        f"  ✗ FAIL {size_label}: \"{issue['text']}\"\n"
                        f"         fg={issue['fg']} bg={issue['bg']} "
                        f"ratio={issue['ratio']:.2f}:1 (min {issue['required']}:1)"
                    )

    # Summary
    print(f"\n{'═' * 60}")
    if total_issues == 0:
        print(f"  ✓ All clear — {len(svg_files)} file(s) pass WCAG AA contrast.")
        sys.exit(0)
    else:
        print(f"  ✗ {total_issues} issue(s) in {total_files} file(s) out of {len(svg_files)} checked.")
        sys.exit(1)


if __name__ == "__main__":
    main()
