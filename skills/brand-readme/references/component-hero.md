# Component: Hero Banner

> Repository headers, project intros, personal profile banners.

---

## Parameters

| Parameter | Type | Required | Constraints |
| :--- | :--- | :--- | :--- |
| `title` | String | Yes | Max 28 characters |
| `tagline` | String | Yes | Max 80 characters |
| `version_badge` | String | No | Monospace tag (e.g., `v2.4.0`, `STABLE`) |
| `metadata_items` | Array of Strings | No | Max 3 items (e.g., `["Zero Runtime", "MIT Licensed", "TypeScript"]`) |

---

## Canvas Constraints

| Property | Value |
| :--- | :--- |
| Width | `800px` |
| Height | `220px` |
| viewBox | `0 0 800 220` |
| Title font-size | `32px`, `--font-title`, weight `700` |
| Tagline font-size | `15px`, `--font-body`, weight `400` |
| Metadata font-size | `11px`, `--font-mono`, uppercase |
| Version badge | `11px`, `--font-mono`, `rx="3"` pill on `--paper-2` |
| Bottom hairline | `y=219`, `stroke="var(--muted)"`, `stroke-opacity="0.2"`, `stroke-width="1px"` |

---

## Layout Grid

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│  x=40                                                                        │
│  ┌──────────┐                                                                │
│  │ v1.0.0   │  y=36..56  (version pill, 64×20, rx=3)                        │
│  └──────────┘                                                                │
│                                                                              │
│  Project Title.          y=96   (32px, --font-title, --ink)                  │
│              ↑ accent dot                                                    │
│                                                                              │
│  Tagline text here       y=132  (15px, --font-body, --muted)                │
│                                                                              │
│  META1  •  META2  •  META3   y=176  (11px, --font-mono, --muted)            │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  hairline at y=219                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## SVG Template

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 220" width="800" height="220">
  <style>
    .paper { fill: var(--paper, #ffffff); }
    .ink { fill: var(--ink, #1f2328); font-family: var(--font-title, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif); }
    .muted { fill: var(--muted, #656d76); font-family: var(--font-body, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif); }
    .mono { font-family: var(--font-mono, ui-monospace, SFMono-Regular, "SF Mono", monospace); font-size: 11px; }
    .accent { fill: var(--accent, #0969da); }
    .hairline { stroke: var(--muted, #656d76); stroke-opacity: 0.2; stroke-width: 1px; }
  </style>
  <rect width="100%" height="100%" class="paper" />

  <!-- Version Pill -->
  <rect x="40" y="36" width="64" height="20" rx="3"
        fill="var(--paper-2, #f6f8fa)"
        stroke="var(--muted, #656d76)" stroke-opacity="0.3" stroke-width="0.5"/>
  <text x="72" y="50" text-anchor="middle" class="muted mono">v1.0.0</text>

  <!-- Main Title -->
  <text x="40" y="96" class="ink" font-size="32" font-weight="700">
    Project Title<tspan class="accent">.</tspan>
  </text>

  <!-- Tagline -->
  <text x="40" y="132" class="muted" font-size="15" font-weight="400">
    Editorial-grade typography components for clean project presentation.
  </text>

  <!-- Metadata Row -->
  <text x="40" y="176" class="muted mono">
    LICENSE: MIT   •   RUNTIME: ZERO-DEP   •   STATUS: PRODUCTION
  </text>

  <!-- Bottom Hairline -->
  <line x1="0" y1="219" x2="800" y2="219" class="hairline" />
</svg>
```

---

## Design Notes

- The accent-colored period (`.`) after the title is the single focal accent element.
- Version badge width should adapt to content length (`width = text_width + 24px`).
- Metadata items are separated by ` • ` (thin space + bullet + thin space).
- If `metadata_items` is empty, remove the row and reduce canvas height to `180px`.
- If `version_badge` is empty, remove the pill and shift title up to `y=72`.
