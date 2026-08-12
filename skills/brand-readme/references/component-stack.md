# Component: Tech Stack & Ecosystem

> Clean tech stack categorization without mismatched badge icons.

---

## Parameters

| Parameter | Type | Required | Constraints |
| :--- | :--- | :--- | :--- |
| `categories` | Array of Objects | Yes | Max 3 categories |
| `categories[].category` | String | Yes | Uppercase label, max 12 characters |
| `categories[].skills` | Array of Strings | Yes | Max 6 items per category |

---

## Canvas Constraints

| Property | Value |
| :--- | :--- |
| Width | `800px` |
| Height | `180px` (adaptive: `+40px` per extra skill row) |
| viewBox | `0 0 800 180` |
| Category label | `10px`, `--font-mono`, uppercase, `letter-spacing: 1.5px`, `--muted` |
| Skill item | `13px`, `--font-body`, `--ink` |
| Indicator square | `3px × 3px`, `rx="0"`, filled `--accent` (first category) or `--muted` |
| Vertical hairlines | Between categories, `stroke-width: 1px`, `stroke-opacity: 0.12` |

---

## Layout Grid

```text
┌─────────────────────────┼─────────────────────────┼─────────────────────────┐
│  CORE                   │  DATA                   │  INFRA                  │
│                         │                         │                         │
│  ■ Rust                 │  ■ PostgreSQL           │  ■ Docker               │
│  ■ Tokio                │  ■ Redis                │  ■ Kubernetes           │
│  ■ WebAssembly          │  ■ ClickHouse           │  ■ Terraform            │
│                         │                         │                         │
└─────────────────────────┼─────────────────────────┼─────────────────────────┘
          hairline dividers between columns
```

### Column Widths

| Category Count | Column Width | Separator |
| :--- | :--- | :--- |
| 1 | `800px` (full width) | None |
| 2 | `392px` | 1 vertical hairline at `x=400` |
| 3 | `258px` | 2 vertical hairlines at `x=266`, `x=533` |

---

## SVG Template (3 categories)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 180" width="800" height="180">
  <style>
    .paper { fill: var(--paper, #ffffff); }
    .ink { fill: var(--ink, #1f2328); font-family: var(--font-body, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif); font-size: 13px; }
    .label { font-family: var(--font-mono, monospace); font-size: 10px; fill: var(--muted, #656d76); letter-spacing: 1.5px; }
    .dot-accent { fill: var(--accent, #0969da); }
    .dot-muted { fill: var(--muted, #656d76); }
    .divider { stroke: var(--muted, #656d76); stroke-opacity: 0.12; stroke-width: 1px; }
  </style>
  <rect width="100%" height="100%" class="paper" />

  <!-- Column 1: CORE -->
  <text x="24" y="28" class="label">CORE</text>
  <rect x="24" y="52" width="3" height="3" class="dot-accent" />
  <text x="36" y="56" class="ink">Rust</text>
  <rect x="24" y="76" width="3" height="3" class="dot-accent" />
  <text x="36" y="80" class="ink">Tokio</text>
  <rect x="24" y="100" width="3" height="3" class="dot-accent" />
  <text x="36" y="104" class="ink">WebAssembly</text>

  <!-- Divider 1 -->
  <line x1="266" y1="12" x2="266" y2="168" class="divider" />

  <!-- Column 2: DATA -->
  <text x="290" y="28" class="label">DATA</text>
  <rect x="290" y="52" width="3" height="3" class="dot-muted" />
  <text x="302" y="56" class="ink">PostgreSQL</text>
  <rect x="290" y="76" width="3" height="3" class="dot-muted" />
  <text x="302" y="80" class="ink">Redis</text>
  <rect x="290" y="100" width="3" height="3" class="dot-muted" />
  <text x="302" y="104" class="ink">ClickHouse</text>

  <!-- Divider 2 -->
  <line x1="533" y1="12" x2="533" y2="168" class="divider" />

  <!-- Column 3: INFRA -->
  <text x="557" y="28" class="label">INFRA</text>
  <rect x="557" y="52" width="3" height="3" class="dot-muted" />
  <text x="569" y="56" class="ink">Docker</text>
  <rect x="557" y="76" width="3" height="3" class="dot-muted" />
  <text x="569" y="80" class="ink">Kubernetes</text>
  <rect x="557" y="100" width="3" height="3" class="dot-muted" />
  <text x="569" y="104" class="ink">Terraform</text>
</svg>
```

---

## Design Notes

- **No external logos.** Use 3px indicator squares instead of SVG brand icons. This avoids trademark issues and keeps the component visually consistent.
- **First category gets accent dots.** The primary/focal category uses `--accent` for its indicator squares. All other categories use `--muted`.
- **Vertical hairlines, not box borders.** Categories are separated by subtle vertical rules, not enclosed in cards.
- **Skill items stack vertically** at `24px` line-height intervals (`dy=24` per item).
- **Adaptive height:** Base height `180px` assumes ≤5 items per column. Add `24px` for each additional item beyond 5.
- **No hover states or interactivity.** These are static SVG primitives.
