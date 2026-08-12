# Brand Readme

**Static SVG components for GitHub READMEs. Brand-aligned, zero-dependency, WCAG AA compliant.**

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="skills/brand-readme/assets/template-hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="skills/brand-readme/assets/template-hero.svg">
  <img alt="Brand Readme Hero" src="skills/brand-readme/assets/template-hero.svg" width="800">
</picture>

Five component types. One agent skill. Reads your site, extracts tokens, maps them to every output. No build step, no runtime, no external dependencies.

---

## Why this exists

I kept getting generic badge output from agents — mismatched colours, default fonts, nothing that matched the rest of the project. The fix is a constrained design system packaged as a skill that agents can load on demand.

> *The highest-grade design move is deletion. Target density: 3/10.*

---

## Components

| Type | Purpose |
| :--- | :--- |
| **Hero** | Repository headers, project banners |
| **Stats** | Metric callouts, benchmarks |
| **Stack** | Tech stack categorization |
| **Timeline** | Changelogs, roadmap milestones |
| **Quote** | Architectural axioms, project principles |

All ship as self-contained SVG with inline `<style>`. Light + dark variants. Embed via `<picture>` tags.

---

## Install

**Pi:**
```
pi install aksyuma/brand-readme
```

**Claude Code:**
```
/plugin install brand-readme@brand-readme
```

**Codex:**
```
npx skills add https://github.com/aksyuma/brand-readme --skill brand-readme
```

### Local install (for customization)

```bash
git clone https://github.com/aksyuma/brand-readme.git ~/code/brand-readme
pi install ~/code/brand-readme
# or
ln -s ~/code/brand-readme/skills/brand-readme ~/.claude/skills/brand-readme
```

---

## Onboarding

Default palette is GitHub editorial (white paper, jet ink, blue accent). Run onboarding to extract your brand:

```
/brand-readme:onboard https://yoursite.com
```

The agent fetches the page, maps computed CSS to semantic roles, verifies WCAG AA contrast, and writes tokens to `references/style-guide.md`.

### Extraction mapping

| Source | Token |
| :--- | :--- |
| `<body>` background | `--paper` |
| Primary text colour | `--ink` |
| Secondary text | `--muted` |
| Container fill | `--paper-2` |
| CTA / link colour | `--accent` |
| Heading font | `--font-title` |
| Body font | `--font-body` |
| Code font | `--font-mono` |

Contrast is checked automatically. If a pair fails (< 4.5:1), luminance is adjusted and you're shown the diff before anything is written.

---

## Quickstart

```bash
# Preview templates
open skills/brand-readme/assets/template-hero.svg

# Ask an agent:
# "Hero banner: title 'Dataflow', tagline 'Real-time stream processing engine'"
# "Stats card: 1.2ms p99, 14MB memory, 99.8% coverage"
# "Tech stack: Core (Go, Kafka), Data (Postgres, Redis), Infra (K8s, Terraform)"
```

---

## Architecture

Progressive disclosure. The agent loads only what is needed for the request.

```
brand-readme/
├── commands/
│   └── onboard.md                    — agent slash command
├── skills/
│   └── brand-readme/
│       ├── SKILL.md                  — routing index, constraints
│       ├── references/
│       │   ├── style-guide.md        — token store
│       │   ├── onboarding.md         — extraction spec
│       │   ├── component-hero.md
│       │   ├── component-stats.md
│       │   ├── component-stack.md
│       │   ├── component-history.md
│       │   └── component-quote.md
│       ├── scripts/
│       │   ├── onboard.py            — token extraction
│       │   └── lint-contrast.py      — WCAG AA linter
│       └── assets/
│           ├── template-hero.svg
│           ├── template-hero-dark.svg
│           └── template-stats.svg
└── .github/
    └── workflows/lint.yml            — CI contrast checks
```

### What loads when

| Request | Loaded |
| :--- | :--- |
| Hero banner | `SKILL.md` + `component-hero.md` |
| Stats card | `SKILL.md` + `component-stats.md` |
| Tech stack | `SKILL.md` + `component-stack.md` |
| Onboarding | `SKILL.md` + `onboarding.md` + `style-guide.md` |

---

## Design constraints

One accent colour per SVG. System font stacks (sans for titles/body, mono for metrics). 1px hairlines, no shadows, `rx` of 0 or 4. Every coordinate divisible by 4. These are the constraints that prevent the output from looking generated.

---

## Linting

```bash
python3 skills/brand-readme/scripts/lint-contrast.py --all skills/brand-readme/assets/
```

Validates WCAG AA ratios (≥ 4.5:1 normal text, ≥ 3:1 large text) on all SVG output.

---

## When not to use this

- **Diagrams or flows** — use [diagram-design](https://github.com/cathrynlavery/diagram-design)
- **Interactive content** — SVGs are static
- **Body text** — use markdown
- **> 5 data points** — use a table

---

## License

MIT — see [LICENSE](LICENSE).
