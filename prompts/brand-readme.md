---
name: brand-readme
description: Generate an editorial SVG component for a GitHub README
arguments:
  - name: type
    description: "Component type: hero, stats, stack, timeline, or quote"
    required: true
  - name: content
    description: "Content parameters (title, tagline, items, etc.)"
    required: true
---

# /brand-readme

Generate a brand-aligned SVG component for GitHub README embedding.

## Procedure

1. Read `skills/brand-readme/SKILL.md` for routing and constraints.
2. Check `skills/brand-readme/references/style-guide.md` for brand tokens.
   - If unconfigured, ask whether to run onboarding, paste tokens, or use defaults.
3. Based on `{type}`, load the corresponding component spec from `references/`.
4. Generate the SVG following all design system constraints.
5. Output both light and dark variants.
6. Provide the `<picture>` embed snippet for GitHub Markdown.

## Example usage

```
/brand-readme type=hero content="title: Dataflow, tagline: Real-time stream processing engine, version: v2.1.0"
/brand-readme type=stats content="items: [{label: P99, value: 1.2ms}, {label: Memory, value: 14MB}, {label: Coverage, value: 99.8%}]"
/brand-readme type=stack content="categories: [{category: CORE, skills: [Go, Kafka]}, {category: DATA, skills: [Postgres, Redis]}]"
```
