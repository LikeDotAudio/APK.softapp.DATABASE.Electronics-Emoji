# Architecture — DATABASE.Electronics-Emoji

## Use it
```bash
python3 server.py                     # http://127.0.0.1:8093/gallery.htm  (APK_EMOJI_PORT to change)
pip install --user cairosvg Pillow    # plus the system Cairo library
python3 renderPNG.py                  # re-render symbols/18X18 and symbols/72X72 after editing a symbol
```
HTTP is required: both pages import `symbols/index.js` as an ES module, and under `file://` they show an empty grid with no error.

## How it fits together
```
symbols/<name>.js  ──►  symbols/index.js (ordered array of 81)
                              │
          ┌───────────────────┼────────────────────┐
          ▼                   ▼                    ▼
    gallery.htm          index.html           renderPNG.py
  (lookup, 3 sizes)  (letter-paper proposal)  (parse svg → PNG 18 px / 72 px)
```
- A module is `export default { name, category, svg }`. Categories: *Primitive Components* (40), *Logic Gates* (7), *Colour Variants* (27), *Logic Gates (Colour)* (7).
- `renderPNG.py` reads each module's text (it does not run JS) through `symbols_contract.parse()`, rasterises with `cairosvg`, and names the file by `symbols_contract.slug(name, category)`; it warns on a slug collision. `index.html` computes the same path with `symbols/slug.js`.
- `check.py` proves the set consistent (module shape, closed categories, index completeness, `version`, unique slugs, PNG set, JS == Python slug via `node`).
- `server.py` is a `ThreadingHTTPServer` over this folder bound to `127.0.0.1`. On `EADDRINUSE` it probes the holder for `symbols/index.js`: same bytes → open the URL and exit 0; different → print and exit 1.

## Files
| File | Role |
|---|---|
| `symbols/*.js`, `symbols/index.js` | the symbol modules and their ordered index (`export const version`) |
| `symbols/slug.js`, `symbols_contract.py` | the slug rule (browser / Python twins) and the module contract |
| `check.py` | the contract check, `python3 check.py` |
| `symbols/18X18/`, `symbols/72X72/` | rendered PNGs (81 each) |
| `gallery.htm` | the lookup (launcher entry) |
| `index.html` | the Unicode proposal, `@page { size: letter }` |
| `proof.htm` | per-symbol disambiguated search phrases and links |
| `server.py` | local static server |
| `renderPNG.py` | SVG → PNG renderer |
| `display.json` | launcher manifest, `entry: gallery.htm` |
