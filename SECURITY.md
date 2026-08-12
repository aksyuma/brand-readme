# Security

## Supported versions

| Version | Supported |
| :--- | :--- |
| 1.x | Yes |

## Reporting

Do not open a public issue for security vulnerabilities.

Email: **security@aksyuma.dev**

Acknowledgment within 48 hours. Fix timeline: 7 days critical, 30 days moderate. Public disclosure after fix ships.

## Attack surface

This project generates static SVGs. The relevant surface:

- **`scripts/onboard.py`** fetches external URLs. Validate it does not execute arbitrary content from fetched pages.
- **SVG output** must not contain `<script>`, `<foreignObject>`, or event handler attributes. GitHub's sanitiser strips these, but downstream consumers may not.
