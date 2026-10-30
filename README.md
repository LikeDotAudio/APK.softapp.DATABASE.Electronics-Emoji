# DATABASE.Electronics-Emoji

> 🗄️ **Electronics Emoji** ⚡ — 81 schematic symbols as small ES modules, their 18 px and 72 px PNG renders, a gallery to look them up, and a letter-paper proposal arguing them into Unicode.

---

## 🧩 Architectural Role
* **Family**: Softapps · `DATABASE` (reference data)
* **Category**: `Pipeline` group, sub-group `01 · Event` (`display.json`); class `artifact`
* **Pipeline Stage**: `01` — Event / Intake, read from the leading digits of `subGroup` (there is no `stage` key)

---

## ⚙️ Repository Overview

| Path | What it is |
|---|---|
| `symbols/<name>.js` | One symbol per file: `export default { name, category, svg: \`<svg …>\` }`. 81 modules. |
| `symbols/index.js` | Imports all 81 and exports them as one ordered array: 40 *Primitive Components*, 7 *Logic Gates*, 27 *Colour Variants*, 7 *Logic Gates (Colour)*. |
| `symbols/18X18/`, `symbols/72X72/` | 81 PNGs each, named by slug (below). |
| `gallery.htm` | The lookup: every symbol, grouped by category, at 60 × 60, 18 × 18 and 72 × 72. Tiles are inline SVG with `role="img"` and an `aria-label`. |
| `index.html` | The proposal for Electronics Schematic Symbol Emoji, laid out for **letter paper** (`@page { size: letter }`): abstract, images and sizes, IP and licence, evidence of frequency, why they are missing, selection factors, factors against, and the search-link proof. |
| `proof.htm` | "Frequency Proof": per symbol, a disambiguated search phrase (e.g. `electrical-switch`, not "switch") with Google Search / Trends / Ngram links, and why the plain word would mislead. |
| `server.py` | Local static server for this folder. |
| `renderPNG.py` | Rasterises every module's SVG to both PNG sizes. |
| `display.json` | Manifest for the OS application walker. |

### PNG names
`slug = name lower-cased, non-alphanumerics → "-", trimmed`, plus `-color` when the category says colour/color — `Switch (closed)` → `switch-closed.png`, `AND` in *Logic Gates (Colour)* → `and-color.png`. The rule is in `renderPNG.py` (`slug()`) and must match `slug()` in `index.html`. Checked 2026-10-30: the 81 slugs `renderPNG.py` derives match the 81 files in `symbols/18X18/` exactly.

---

## 🚀 Usage & Integration
* **View**: `python3 server.py`, which serves this folder on `http://127.0.0.1:8093/` (override with `APK_EMOJI_PORT`) and opens `gallery.htm`, the lookup; the proposal is `/index.html`. **HTTP is required**: both pages `import` `symbols/index.js` as an ES module, and from `file://` they show an empty grid and no error.
* **If the port is taken**: `server.py` fetches `symbols/index.js` from whoever holds the port. If the bytes match, that is this server already running and it opens the URL and exits 0; otherwise it prints that the port belongs to something else and exits 1. It never kills the holder. (The default was `8080` until 2026-10-30, which is Storage-Portal's port on every node, so it always exited 1.)
* **Re-render PNGs** after editing a symbol: `pip install --user cairosvg Pillow` (and the system Cairo library), then `python3 renderPNG.py`. It warns on a slug collision.
* **Tests**: none.
* **Web Portal Entry**: `display.json` → `kind: "web"`, `entry` and `app` both `gallery.htm`, id `ElectronicsEmoji`. The Softapps walker (`PODS/POD.THIN/WEB.OsApi/SRC/server.py`, `walk_project()`) honours a declared `entry` before its `index.html` marker, so a launch opens the gallery. Inside the portal the pages are served over HTTP, so the module import works there.
* **MQTT**: none. `display.json` names `APK.audio/Gui/Display/ElectronicsEmoji` as its display topic; nothing publishes or subscribes.
* **Remote Repository**: `https://github.com/LikeDotAudio/APK.softapp.DATABASE.Electronics-Emoji.git`

---

## 🏛 Philosophy
What the code actually does, in the ecosystem's vocabulary (`Documentation/🏛Philosophy`):

* **One symbol, one file, one source.** Each SVG is written once in its module; the gallery, the proposal and the PNGs are all derived from `symbols/index.js` (`gallery.htm`, `index.html`, `renderPNG.py`).
* **A derived name, computed the same way twice.** PNG paths are a slug of `name` + `category`, so a page can find a PNG from the icon object alone; the two `slug()` implementations are told to stay in sync (`renderPNG.py` header).
* **The second claimant stands down and verifies.** A second `server.py` asks the incumbent on the port whether it is serving the same `symbols/index.js` and defers rather than killing it (`_defer_to_incumbent()`, `probe_incumbent()`); `probe_incumbent` never raises, because it runs on the failure path.
* **Local only.** `server.py` binds `127.0.0.1`.
* **Accessible by construction.** Inline SVG tiles carry `role="img"` and an `aria-label`, and the visible caption is `aria-hidden` so nothing is announced twice (`gallery.htm`).
* **Fail loudly on a missing tool.** `renderPNG.py` exits with an install line when `cairosvg` or `Pillow` is missing.
* **Evidence over assertion.** The proposal's frequency claims link to searches you can run, with the ambiguity of each plain word stated (`proof.htm`).

## 📚 Wiki
Principles with code anchors, architecture and delivery: [Documentation/README.md](Documentation/README.md).

## 🛣 Plans
Plans live only in `Documentation/🛣Roadmap/roadmap.htm` at the APK.audio root.

<!-- wiki:smoke -->
**Smoke test** — ✅ PASS 2/2 since 2026-10-30 12:51 EDT — [results](Documentation/%F0%9F%A7%A9Manual%20and%20Artifacts/SMOKE.md)
<!-- /wiki:smoke -->
