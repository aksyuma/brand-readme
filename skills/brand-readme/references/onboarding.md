# Onboarding — URL-to-Tokens Extraction Flow

> This document specifies how `/brand-readme:onboard <URL>` extracts design tokens from a target website and writes them to `references/style-guide.md`.

---

## Trigger

```text
User:  "onboard brand-readme to https://yoursite.com"
       — or —
       /brand-readme:onboard https://yoursite.com
```

---

## Execution Flow

```text
1. Fetch URL
   └── GET <URL>, follow redirects, parse full HTML + linked CSS

2. Extract Tokens (see Extraction Matrix below)
   └── Map computed CSS properties → semantic roles

3. Contrast Verification
   ├── ink over paper   ≥ 4.5:1  (WCAG AA normal text)
   ├── muted over paper ≥ 3.0:1  (WCAG AA large text)
   └── accent over paper ≥ 4.5:1 (focal elements are small)
   └── FAIL? → auto-adjust luminance, show diff, ask confirmation

4. Present Diff
   └── Show proposed token changes as a before/after table

5. Write to style-guide.md
   └── Only after user confirms "yes, apply it"
```

---

## CSS Property Extraction Matrix

| Detected from Source Site | Extraction Selector | Maps to Token | Contrast Requirement |
| :--- | :--- | :--- | :--- |
| `<body>` background color | `getComputedStyle(document.body).backgroundColor` | `--paper` | Base canvas |
| Primary text color | `getComputedStyle(querySelector('p, body')).color` | `--ink` | ≥ 4.5:1 over `--paper` |
| Secondary / subtitle text | `getComputedStyle(querySelector('small, footer, .muted, time')).color` | `--muted` | ≥ 3:1 over `--paper` |
| Card / container fill | `getComputedStyle(querySelector('.card, article, section')).backgroundColor` | `--paper-2` | Must contrast against `--paper` |
| Primary CTA / link color | `getComputedStyle(querySelector('a, button.primary, .btn-primary')).backgroundColor \|\| color` | `--accent` | ≥ 4.5:1 over `--paper` |
| Display heading font | `getComputedStyle(querySelector('h1')).fontFamily` | `--font-title` | Fallback: system sans |
| Body text font | `getComputedStyle(document.body).fontFamily` | `--font-body` | Fallback: system sans |
| Code / monospace font | `getComputedStyle(querySelector('pre, code')).fontFamily` | `--font-mono` | Fallback: system mono |

---

## Contrast Verification Algorithm

```python
def relative_luminance(r, g, b):
    """sRGB → relative luminance (WCAG 2.1 formula)"""
    def linearize(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)

def contrast_ratio(fg, bg):
    l1 = relative_luminance(*fg)
    l2 = relative_luminance(*bg)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)
```

If a token pair fails, adjust the foreground luminance by darkening (light mode) or lightening (dark mode) in 5% steps until the ratio passes. Present the original and adjusted values to the user.

---

## Output Behavior

On successful onboarding:

1. Update `references/style-guide.md` with extracted values.
2. Set `Status > Configured: Yes`.
3. Set `Status > Source URL: <URL>`.
4. Set `Status > Last Updated: <ISO date>`.
5. Print confirmation:

```text
✓ Brand tokens extracted from https://yoursite.com
  --paper:      #FAFAFA
  --ink:        #1A1A2E
  --muted:      #6B7280
  --accent:     #3B82F6
  --font-title: "Inter", sans-serif
  --font-body:  "Inter", sans-serif
  --font-mono:  "JetBrains Mono", monospace

  All contrast checks passed (ink/paper: 14.2:1, accent/paper: 5.8:1).
```

---

## Fallback Behavior

- If the URL is unreachable: report error, offer to retry or paste tokens manually.
- If no `<h1>` or `<code>` element exists: use system default font stacks.
- If no `.card` / `article` / `section` has a distinct background: set `--paper-2` to a 3% darker/lighter variant of `--paper`.
- If the site uses CSS variables (custom properties): attempt to resolve them from `:root`.

---

## Implementation

See `scripts/onboard.py` for the Python extraction script that drives this flow.
