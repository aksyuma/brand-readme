---
name: brand-readme
description: "Generates editorial, brand-aligned SVG primitives for GitHub READMEs and profiles. Zero build steps, zero third-party badge clunk, self-contained SVG."
version: 1.0.0
---

# Brand Readme — Skill Specification

Editorial GitHub README and profile components your designer won't hate.

## 1. Core Philosophy

1. **Ink-to-Paper Restraint:** The highest-grade design move is deletion. Target visual density: **3/10 to 4/10**.
2. **Single Focal Accent:** Only one or two elements per SVG earn the `--accent` token. Everything else stays in `--ink` or `--muted`.
3. **No Shields.io Slop:** No generic pill badges, neon progress bars, or plastic drop-shadows. Clean typographic scale, hairline dividers, and deliberate whitespace.
4. **Zero Build Dependency:** Outputs standalone SVGs with inline `<style>` and web font `@import` tags. Every output renders standalone inside GitHub Markdown `<picture>` tags.
5. **Progressive Disclosure:** Load ONLY what is strictly required for the target component. Do not pollute working context with unused specs.

---

## 2. Progressive Disclosure & Loading Architecture

When a request is received, follow this deterministic lookup pattern:

```text
[User Prompt]
      │
      ▼
1. Check `references/style-guide.md`
   ├── Unset/Default? ──► Prompt Onboarding (`references/onboarding.md`)
   └── Customized?    ──► Continue to Routing
      │
      ▼
2. Route to Component Spec
   ├── "hero", "banner", "header"          ──► Load `references/component-hero.md`
   ├── "stats", "metrics", "analytics"     ──► Load `references/component-stats.md`
   ├── "stack", "tech", "tools", "skills"  ──► Load `references/component-stack.md`
   ├── "timeline", "history", "changelog"  ──► Load `references/component-history.md`
   └── "quote", "callout", "testimonial"   ──► Load `references/component-quote.md`
      │
      ▼
3. Validate Output against Design System Constraints (Section 3)
      │
      ▼
4. Emit Standalone SVG File pair (light & dark variants)
```

---

## 3. Design System & SVG Technical Constraints

All generated SVGs must adhere strictly to these constraints:

### Canvas & Spacing Grid

- **Base Grid Unit:** 8px. All x, y, padding, margin, dx, dy must be multiples of 4 or 8.
- **Standard Widths:**
  - Hero / Timeline / Quote: `width="800"` (fixed or `viewBox="0 0 800 H"`).
  - Stats / Stack: `width="800"` or dual-column `width="392"`.
- **Hairlines:** Stroke widths must be exactly `1px` or `0.5px`. Do not use 2px+ borders for standard boxes.
- **Corner Radii:** Use strict square (`rx="0"`) for pure editorial, or micro-radius (`rx="4"`) for containers. Never use pill shapes (`rx="999"`) except for small status dots.

### Typography Stack

```css
/* Titles & Display */
--font-title: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
/* Node names, body, descriptions */
--font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
/* Code, metrics, versions, commit SHAs */
--font-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
```

### Semantic Color Roles

Never hardcode hex values inside the SVG shape nodes. Assign classes or inline CSS referencing these exact token roles:

| Role | Semantic Purpose | Light Default | Dark Default |
| :--- | :--- | :--- | :--- |
| `--paper` | Background Canvas | `#FFFFFF` | `#0D1117` |
| `--paper-2` | Surface Containers / Card fills | `#F6F8FA` | `#161B22` |
| `--ink` | Primary text, titles, major outlines | `#1F2328` | `#F0F6FC` |
| `--muted` | Sublabels, dates, hairlines, secondary text | `#656D76` | `#8B949E` |
| `--accent` | Primary callout, single focal stat, active badge | `#0969DA` | `#58A6FF` |
| `--accent-subtle` | Accent tinted background (10-15% opacity) | `#DDF4FF` | `#0C2D6B` |

---

## 4. When NOT to Use This Skill

Do not use brand-readme for:

- **Interactive web applications or live JavaScript charts:** SVGs are static visual primitives for GitHub Markdown.
- **Standard documentation bodies:** Use regular GitHub Markdown for paragraphs, tables, and lists.
- **Diagrams and flows:** If the user asks for a flowchart, architecture diagram, sequence map, or data flow, route to `diagram-design`.
- **More than 5 distinct data points per card:** SVGs must remain scannable in under 3 seconds. If content exceeds density rules, push for a markdown table instead.

---

## 5. First-Run Gate & Execution Rules

1. Before generating any SVG, read `references/style-guide.md`.
2. If `references/style-guide.md` contains unpopulated placeholders, ask the user:
   > "I noticed brand-readme hasn't been configured for your brand yet. Would you like to run `/brand-readme:onboard <URL>` to extract your palette, paste tokens manually, or proceed with the default GitHub editorial palette?"
3. Always generate both a `light.svg` and `dark.svg` (or a single SVG leveraging CSS `@media (prefers-color-scheme: dark)` where compatible).
4. Provide the exact Markdown snippet to embed the result with GitHub light/dark switching:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="banner-light.svg">
  <img alt="Project Banner" src="banner-light.svg" width="800">
</picture>
```

---

## 6. Output Validation Checklist

Before delivering any SVG, verify:

- [ ] All coordinates divisible by 4
- [ ] No hardcoded hex in shape nodes (use CSS custom properties or classes)
- [ ] `viewBox` matches declared `width` and `height`
- [ ] Font stacks reference `--font-title`, `--font-body`, or `--font-mono`
- [ ] Maximum one accent-colored focal element per component
- [ ] Hairlines are 1px or 0.5px, never thicker
- [ ] Corner radii are 0 or 4px, never pill-shaped
- [ ] WCAG AA contrast (≥4.5:1) for ink over paper
