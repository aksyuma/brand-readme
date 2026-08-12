# Component: Stats & Metrics

> Metric callouts, benchmarks, GitHub engagement highlights.

---

## Parameters

| Parameter | Type | Required | Constraints |
| :--- | :--- | :--- | :--- |
| `items` | Array of Objects | Yes | Min 2, Max 4 items |
| `items[].label` | String | Yes | Uppercase, max 18 characters |
| `items[].value` | String | Yes | Numeric with optional unit suffix |
| `items[].diff` | String | No | Change indicator (e.g., `"-40%"`, `"+12"`) |
| `variant` | Enum | No | `grid` (default, columns) or `split` (2×2) |

---

## Canvas Constraints

| Property | Value |
| :--- | :--- |
| Width | `800px` |
| Height | `140px` |
| viewBox | `0 0 800 140` |
| Value font-size | `32px`, `--font-mono`, weight `700` |
| Unit suffix font-size | `18px` (as `<tspan>`) |
| Label font-size | `10px`, `--font-mono`, uppercase, `letter-spacing: 1.5px` |
| Diff font-size | `11px`, `--font-mono` |
| Card fill | `--paper-2` with `--muted` stroke at `0.2` opacity |

---

## Layout: Grid Variant (3–4 columns)

```text
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  P99 LATENCY     │  │  MEMORY          │  │  TEST COVERAGE   │
│                  │  │                  │  │                  │
│  1.2ms           │  │  14MB            │  │  99.8%           │
│       ↑ accent   │  │                  │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

### Column Widths (grid variant)

| Item Count | Card Width | Gap |
| :--- | :--- | :--- |
| 2 | `388px` | `24px` |
| 3 | `250px` | `25px` |
| 4 | `184px` | `21px` |

---

## Layout: Split Variant (2×2)

```text
┌──────────────────┐  ┌──────────────────┐
│  METRIC A        │  │  METRIC B        │
│  1,234           │  │  567ms           │
└──────────────────┘  └──────────────────┘
┌──────────────────┐  ┌──────────────────┐
│  METRIC C        │  │  METRIC D        │
│  99.9%           │  │  42              │
└──────────────────┘  └──────────────────┘
```

- Canvas height for split variant: `296px` (two rows of `140px` + `16px` gap).

---

## SVG Template (Grid, 3 items)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 140" width="800" height="140">
  <style>
    .paper { fill: var(--paper, #ffffff); }
    .card { fill: var(--paper-2, #f6f8fa); stroke: var(--muted, #656d76); stroke-opacity: 0.2; }
    .label { font-family: var(--font-mono, monospace); font-size: 10px; fill: var(--muted, #656d76); letter-spacing: 1.5px; }
    .val { font-family: var(--font-mono, monospace); font-size: 32px; font-weight: 700; fill: var(--ink, #1f2328); }
    .accent-val { fill: var(--accent, #0969da); }
    .diff { font-family: var(--font-mono, monospace); font-size: 11px; fill: var(--muted, #656d76); }
  </style>
  <rect width="100%" height="100%" class="paper" />

  <!-- Stat Item 1 (focal — uses accent) -->
  <rect x="0" y="0" width="250" height="140" rx="4" class="card" />
  <text x="24" y="40" class="label">P99 LATENCY</text>
  <text x="24" y="90" class="val accent-val">1.2<tspan font-size="18">ms</tspan></text>
  <text x="24" y="120" class="diff">↓ -40%</text>

  <!-- Stat Item 2 -->
  <rect x="275" y="0" width="250" height="140" rx="4" class="card" />
  <text x="299" y="40" class="label">MEMORY FOOTPRINT</text>
  <text x="299" y="90" class="val">14<tspan font-size="18">MB</tspan></text>

  <!-- Stat Item 3 -->
  <rect x="550" y="0" width="250" height="140" rx="4" class="card" />
  <text x="574" y="40" class="label">TEST COVERAGE</text>
  <text x="574" y="90" class="val">99.8<tspan font-size="18">%</tspan></text>
</svg>
```

---

## Design Notes

- **Single focal accent:** Only ONE stat item gets `accent-val` class. This is the metric you want readers to notice first. All others use `--ink`.
- **No colorful gauges:** Pure typographic hierarchy. No progress rings, no bar fills, no gradients.
- **Diff indicators:** Optional. Rendered in `--muted` below the value. Use `↓` for decreases, `↑` for increases.
- **Unit suffixes:** Rendered as a `<tspan>` at `18px` within the value `<text>` node. Keep units short: `ms`, `MB`, `%`, `k`, `s`.
- **Card stroke:** `0.5px` stroke, `stroke-opacity="0.2"`. Barely visible — structure through whitespace, not borders.
