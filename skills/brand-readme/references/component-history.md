# Component: Milestone Timeline Stream

> Linear changelogs, architecture version transitions, roadmap progress.

---

## Parameters

| Parameter | Type | Required | Constraints |
| :--- | :--- | :--- | :--- |
| `events` | Array of Objects | Yes | Max 4 items |
| `events[].date` | String | Yes | Short date label (e.g., `"2026 Q1"`, `"Mar 2025"`) |
| `events[].title` | String | Yes | Max 24 characters |
| `events[].status` | Enum | Yes | `completed` \| `active` \| `upcoming` |

---

## Canvas Constraints

| Property | Value |
| :--- | :--- |
| Width | `800px` |
| Height | `140px` |
| viewBox | `0 0 800 140` |
| Timeline axis | Horizontal line at `y=70`, full width |
| Axis stroke | `1px`, `--muted`, `stroke-opacity: 0.3` |
| Node diameter | `8px` (circle `r="4"`) |
| Date font-size | `10px`, `--font-mono`, uppercase, `--muted` |
| Title font-size | `13px`, `--font-body`, `--ink` |

---

## Layout Grid

```text
     ●──────────────────●──────────────────●──────────────────○
   2025 Q1           2025 Q3            2026 Q1            2026 Q3
   Engine v1         Migration          Engine v2          Platform
   (completed)       (completed)        (active)           (upcoming)
```

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  Date labels        y=44   (10px, --font-mono, --muted)                     │
│                                                                              │
│  ●────────────●────────────●────────────○    y=70  (axis + nodes)           │
│                                                                              │
│  Event titles       y=100  (13px, --font-body, --ink)                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Node Positions (evenly distributed)

| Event Count | X Positions |
| :--- | :--- |
| 2 | `200`, `600` |
| 3 | `133`, `400`, `667` |
| 4 | `100`, `300`, `500`, `700` |

---

## Status Styling

| Status | Node Fill | Node Stroke | Text Color |
| :--- | :--- | :--- | :--- |
| `completed` | `--accent` | none | `--ink` |
| `active` | `--accent` | `--accent` (2px ring) | `--ink` (bold) |
| `upcoming` | `--paper` | `--muted` (1px) | `--muted` |

---

## SVG Template (4 events)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 140" width="800" height="140">
  <style>
    .paper { fill: var(--paper, #ffffff); }
    .ink { fill: var(--ink, #1f2328); font-family: var(--font-body, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif); font-size: 13px; }
    .muted { fill: var(--muted, #656d76); font-family: var(--font-mono, monospace); font-size: 10px; letter-spacing: 1.5px; }
    .axis { stroke: var(--muted, #656d76); stroke-opacity: 0.3; stroke-width: 1px; }
    .node-done { fill: var(--accent, #0969da); }
    .node-active { fill: var(--accent, #0969da); stroke: var(--accent, #0969da); stroke-width: 2px; stroke-opacity: 0.4; }
    .node-upcoming { fill: var(--paper, #ffffff); stroke: var(--muted, #656d76); stroke-width: 1px; }
  </style>
  <rect width="100%" height="100%" class="paper" />

  <!-- Timeline Axis -->
  <line x1="60" y1="70" x2="740" y2="70" class="axis" />

  <!-- Event 1: completed -->
  <text x="100" y="44" text-anchor="middle" class="muted">2025 Q1</text>
  <circle cx="100" cy="70" r="4" class="node-done" />
  <text x="100" y="100" text-anchor="middle" class="ink">Engine v1</text>

  <!-- Event 2: completed -->
  <text x="300" y="44" text-anchor="middle" class="muted">2025 Q3</text>
  <circle cx="300" cy="70" r="4" class="node-done" />
  <text x="300" y="100" text-anchor="middle" class="ink">Migration</text>

  <!-- Event 3: active -->
  <text x="500" y="44" text-anchor="middle" class="muted">2026 Q1</text>
  <circle cx="500" cy="70" r="5" class="node-active" />
  <text x="500" y="100" text-anchor="middle" class="ink" font-weight="600">Engine v2</text>

  <!-- Event 4: upcoming -->
  <text x="700" y="44" text-anchor="middle" class="muted">2026 Q3</text>
  <circle cx="700" cy="70" r="4" class="node-upcoming" />
  <text x="700" y="100" text-anchor="middle" style="fill: var(--muted, #656d76); font-family: var(--font-body, sans-serif); font-size: 13px;">Platform</text>
</svg>
```

---

## Design Notes

- **Timeline reads left-to-right**, earliest to latest. No vertical timelines.
- **Active milestone** gets a slightly larger node (`r=5`) with a 2px stroke ring as a subtle pulse effect.
- **Upcoming milestones** are hollow (paper fill, muted stroke) to visually recede.
- **Axis extends 60px beyond first and last nodes** for visual breathing room.
- **Maximum 4 events.** If more milestones are needed, use a markdown table instead.
- **Text anchors are centered** on the node x-position. Keep titles short to avoid overlap.
- **No connector arrows.** The axis line itself implies sequence.
