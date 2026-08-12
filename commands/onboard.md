---
name: brand-readme:onboard
description: Extract brand tokens from a URL and write them to the style guide
arguments:
  - name: url
    description: Website URL to extract design tokens from
    required: true
---

# /brand-readme:onboard

Extract your brand's colors and fonts from a live URL, verify WCAG AA contrast, and write the tokens to `references/style-guide.md`.

## Usage

```
/brand-readme:onboard https://yoursite.com
```

## Procedure

1. Read `skills/brand-readme/references/onboarding.md` for the full extraction spec.
2. Read `skills/brand-readme/references/style-guide.md` to check current state.
3. Run `python3 skills/brand-readme/scripts/onboard.py <url>` to extract tokens.
4. Review the proposed diff with the user.
5. If approved, run `python3 skills/brand-readme/scripts/onboard.py <url> --apply` to write.
6. Confirm the update and show the final token summary.

## What gets extracted

| Source | Token |
| :--- | :--- |
| `<body>` background | `--paper` |
| Primary text color | `--ink` |
| Secondary text | `--muted` |
| Card / container fill | `--paper-2` |
| CTA / link color | `--accent` |
| `<h1>` font | `--font-title` |
| `<body>` font | `--font-body` |
| `<code>` font | `--font-mono` |

## Contrast verification

Before writing, the script checks:
- `--ink` over `--paper` ≥ 4.5:1
- `--muted` over `--paper` ≥ 3.0:1
- `--accent` over `--paper` ≥ 4.5:1

If any pair fails, it auto-adjusts luminance and asks for confirmation.

## Example output

```
✓ Brand tokens extracted from https://yoursite.com
  --paper:      #FAFAFA
  --ink:        #1A1A2E
  --muted:      #6B7280
  --accent:     #3B82F6
  --font-title: "Inter", sans-serif
  --font-body:  "Inter", sans-serif
  --font-mono:  "JetBrains Mono", monospace

  Contrast ink/paper: 14.2:1 ✓
  Contrast accent/paper: 5.8:1 ✓
```
