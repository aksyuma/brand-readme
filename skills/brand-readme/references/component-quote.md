# Component: Editorial Callout / Quote Box

> Testimonials, project philosophies, architectural axioms.

---

## Parameters

| Parameter | Type | Required | Constraints |
| :--- | :--- | :--- | :--- |
| `quote` | String | Yes | Max 140 characters. Rendered in italic serif styling. |
| `author` | String | Yes | Attribution line (e.g., `"@torvalds"`, `"Core Engineering Principles"`) |

---

## Canvas Constraints

| Property | Value |
| :--- | :--- |
| Width | `800px` |
| Height | `130px` |
| viewBox | `0 0 800 130` |
| Left accent border | `3px` wide, `--accent`, full height (`y=0` to `y=130`) |
| Quote font-size | `16px`, italic, `--font-title` (serif if available), `--ink` |
| Author font-size | `12px`, `--font-mono`, `--muted` |
| Internal padding | `40px` left (from accent border), `24px` top |

---

## Layout Grid

```text
┌──┬──────────────────────────────────────────────────────────────────────────┐
│▌ │                                                                           │
│▌ │  "The highest-quality move is usually deletion.                           │
│▌ │   Every node earns its place."                     y=56  (quote)         │
│▌ │                                                                           │
│▌ │  — @torvalds                                       y=96  (author)        │
│▌ │                                                                           │
└──┴──────────────────────────────────────────────────────────────────────────┘
 ↑
 3px accent border
```

---

## SVG Template

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 130" width="800" height="130">
  <style>
    .paper { fill: var(--paper, #ffffff); }
    .ink { fill: var(--ink, #1f2328); }
    .muted { fill: var(--muted, #656d76); }
    .quote-text {
      font-family: var(--font-title, Georgia, "Times New Roman", serif);
      font-size: 16px;
      font-style: italic;
      fill: var(--ink, #1f2328);
    }
    .author-text {
      font-family: var(--font-mono, ui-monospace, SFMono-Regular, "SF Mono", monospace);
      font-size: 12px;
      fill: var(--muted, #656d76);
    }
    .accent-border { fill: var(--accent, #0969da); }
  </style>
  <rect width="100%" height="100%" class="paper" />

  <!-- Left Accent Border -->
  <rect x="0" y="0" width="3" height="130" class="accent-border" />

  <!-- Quote Text -->
  <text x="40" y="56" class="quote-text">
    "The highest-quality move is usually deletion.
    <tspan x="40" dy="24">Every node earns its place."</tspan>
  </text>

  <!-- Author Attribution -->
  <text x="40" y="104" class="author-text">— @torvalds</text>
</svg>
```

---

## Multi-line Handling

For quotes exceeding ~60 characters, wrap to multiple lines using `<tspan>` elements:

```xml
<text x="40" y="48" class="quote-text">
  "First line of the quote that wraps
  <tspan x="40" dy="24">to a second line for readability."</tspan>
</text>
```

- Line height: `24px` (`dy="24"`)
- Max 3 lines of quote text
- If quote requires 3 lines, increase canvas height to `154px`

---

## Design Notes

- **The left accent border is the single focal element.** It draws the eye to the quote block without competing with other accents on the page.
- **Italic serif for quotes.** Use `--font-title` with `font-style: italic`. If the brand's title font is sans-serif, the italic still provides sufficient visual distinction from body text.
- **Em-dash before author.** Always prefix attribution with `— ` (em-dash + space).
- **No quotation mark decorations.** The italic styling and accent border are sufficient. Do not add oversized `"` glyphs or decorative marks.
- **Short quotes (< 60 chars)** render on a single line at `y=56`.
- **Author line** is always 48px below the last line of quote text.
- **No background card.** The accent border + whitespace is enough structure. Do not wrap in a `--paper-2` box.
