# Contributing

## Getting started

1. Fork and clone
2. Branch from `main`
3. Make changes
4. Run `python3 skills/brand-readme/scripts/lint-contrast.py --all skills/brand-readme/assets/`
5. Open a PR

---

## Design system constraints

All SVG output must follow the rules in `SKILL.md`:

- Coordinates divisible by 4
- No hardcoded hex in shape nodes — use CSS custom properties
- Hairlines: 1px or 0.5px
- Corner radii: 0 or 4px
- One accent focal element per component
- Density target: 3/10 to 4/10

---

## Adding a component

1. Write `skills/brand-readme/references/component-<name>.md` — parameters, canvas constraints, layout grid, SVG template, design notes
2. Add light + dark SVG templates to `assets/`
3. Wire into the routing table in `SKILL.md` (Section 2)
4. Update `README.md`
5. Linter must pass

---

## Commits

[Conventional Commits](https://www.conventionalcommits.org/). Sign your commits (`-S -s`).

- `feat:` — new component, script, or capability
- `fix:` — bug
- `docs:` — documentation only
- `ci:` — workflow changes
- `refactor:` — no behaviour change

---

## Not accepted

- External logo SVGs (trademark surface — use indicator squares)
- Components exceeding 5 data points
- Interactive or JS-dependent output
- Pill badges or gradient aesthetics

---

## Questions

Open an issue.
