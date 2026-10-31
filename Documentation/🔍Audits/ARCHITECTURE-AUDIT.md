# 🔍 Architecture audit — DATABASE.Electronics-Emoji (2026-10-30)

Audited against the APK.audio multi-repo architecture standard: coupling, boundaries, duplication, contracts.
← [Audits](INDEX.md) · Improvements: [🛣Roadmap/IMPROVEMENTS.md](../%F0%9F%9B%A3Roadmap/IMPROVEMENTS.md)

## Bounded context
Reference data: 81 schematic-symbol ES modules (`symbols/*.js`, aggregated by `symbols/index.js`), their 18 px / 72 px PNG renders, a lookup gallery, a letter-paper Unicode proposal and its frequency proof. Static HTML + vanilla JS, two Python tools (`server.py` 123 lines, `renderPNG.py` 147 lines). 262 tracked files, 162 of them PNGs. Everything tracked was sampled except the individual PNGs.

## Context map
| Talks to | How (topic / endpoint / file / import) | Relationship |
|---|---|---|
| WEB.OsApi project walker (`walk_project()`) | reads [`display.json`](../../display.json) (`entry: gallery.htm`, `app` portal path) | Conformist (manifest schema owned by OsApi) |
| OS snapshot `OS/system/project-apps.json`, `pipeline.json` | generated from `display.json` by `build_os_manifests.py` | Customer (downstream copies) |
| Browser | `import icons from './symbols/index.js'` in `gallery.htm:42`, `index.html:455`, `proof.htm:125` | internal Published Language (`{name, category, svg}`) |
| cairosvg / Pillow | `renderPNG.py` only | third-party, isolated in one tool |
| MQTT bus | none | — |

No other repo imports `symbols/` (grep of `PODS/` for `Electronics-Emoji`: only the two OS snapshots).

## Scorecard
| Category | Score (0–3) | Finding |
|---|---|---|
| Coupling & Cohesion | 3 | Self-contained; no relative path out of the repo, no shared volume, no bus dependency. |
| Boundary Integrity | 3 | Vendor libraries (cairosvg, Pillow) are confined to `renderPNG.py` with a fail-loud import guard; the module shape `{name, category, svg}` is the only interface. |
| Duplication Control | 3 | One slug rule per language (`symbols/slug.js`, `symbols_contract.slug`), proven equal by `check.py` (delivered). |
| Testing & Contracts | 3 | `python3 check.py` asserts the module contract, PNG set and slug twins (delivered); runs by hand, as the house rule is. |
| Change management | 3 | `symbols/index.js` exports `version`; README "Versions" (delivered). |
Score key: 3 meets the standard · 2 minor gaps · 1 significant gaps · 0 absent / violated.

## Findings
1. **Good — one source per symbol.** Each SVG is written once in `symbols/<name>.js`; the gallery, the proposal and the PNGs are all derived from `symbols/index.js`. Nothing is copied into another repo.
2. **Good — `server.py` respects the node.** Binds `127.0.0.1`, defaults to 8093 not Storage-Portal's 8080, honours `APK_EMOJI_PORT`, and defers to an incumbent after an identity probe (`probe_incumbent()`) instead of killing it.
3. **Smoke covers delivery only.** [SMOKE.md](../%F0%9F%A7%A9Manual%20and%20Artifacts/SMOKE.md) checks "HEAD is on origin"; `check.py` now proves the data behind the 81 tiles, but nothing renders the gallery in a browser. Acceptable for a static page.

Delivered items were removed from this page; see [🌍Publishing/DELIVERY.md](../%F0%9F%8C%8DPublishing/DELIVERY.md#delivered-from-the-2026-10-30-audit).
