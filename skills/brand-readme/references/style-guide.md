# Style Guide — Brand Readme Token Store

> Single source of truth for colors, fonts, and spacing.
> Edit this file directly or run `/brand-readme:onboard <URL>` to auto-populate.

---

## Status

- **Configured:** No (default GitHub editorial palette)
- **Last Updated:** —
- **Source URL:** —

---

## Color Tokens — Light Mode

| Token | Semantic Role | Value |
| :--- | :--- | :--- |
| `--paper` | Background canvas | `#FFFFFF` |
| `--paper-2` | Surface / card fill | `#F6F8FA` |
| `--ink` | Primary text, titles, outlines | `#1F2328` |
| `--muted` | Sublabels, dates, hairlines | `#656D76` |
| `--accent` | Focal callout, active badge | `#0969DA` |
| `--accent-subtle` | Tinted background (10-15% opacity) | `#DDF4FF` |

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
| Titles & Display | `--font-title` | `-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif` |
| Body & Descriptions | `--font-body` | `-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif` |
| Code & Metrics | `--font-mono` | `ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace` |

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
