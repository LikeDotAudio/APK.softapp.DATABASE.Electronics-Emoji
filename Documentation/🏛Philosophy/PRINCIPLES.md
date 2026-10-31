# Principles — DATABASE.Electronics-Emoji

Each principle with the code that keeps it. Ecosystem rules: the APK.audio root's `Documentation/🏛Philosophy/` (cited by path).

| Principle | Kept by |
|---|---|
| **One symbol, one file, one source.** Each SVG is written once in `symbols/<name>.js`; the gallery, the proposal and the PNGs are all derived from `symbols/index.js`. | `gallery.htm:42`, `index.html:455` (`import icons from './symbols/index.js'`); `renderPNG.py:79` `parse()` |
| **A derived name, computed the same way twice.** A PNG path is a slug of `name` + `category`; the Python and JS `slug()` must agree. | `symbols_contract.py` `slug()` (renderPNG.py) and `symbols/slug.js` (index.html); `check.py` fails if they disagree |
| **The second claimant stands down and verifies.** A second `server.py` asks the port's holder for `symbols/index.js` and defers if the bytes match; it never kills it. Root: `Doctrine/readme.The second claimant stands down and verifies.md`. | `server.py:48` `probe_incumbent()`, `server.py:74` `_defer_to_incumbent()` |
| **Never raise on the failure path.** `probe_incumbent()` swallows every error and answers False. | `server.py:48–65` |
| **Do not squat on a shared port.** Default `8093`, not Storage-Portal's `8080`; `APK_EMOJI_PORT` overrides. | `server.py:31` |
| **Local only.** Binds `127.0.0.1`. | `server.py:32` |
| **The right door first.** The launcher and `server.py` both open `gallery.htm` (the lookup), not the letter-paper proposal. | `display.json` `entry`; `server.py` `ENTRY` |
| **Accessible by construction.** Tiles are inline SVG with `role="img"` + `aria-label`; the caption is `aria-hidden` so nothing is announced twice. | `gallery.htm:101–104` |
| **Fail loudly on a missing tool.** `renderPNG.py` exits with an install line when `cairosvg` or `Pillow` is missing. | `renderPNG.py` imports |
| **A contract, checked.** Module shape, closed category set, index completeness, `version`, slug uniqueness and the PNG set are asserted by one command. | `check.py` |
| **Evidence over assertion.** Frequency claims link to searches a reader can run, each with the ambiguity of the plain word stated. | `proof.htm` |

## Where it falls short
- `check.py` runs by hand (the root CI verifies nothing on purpose); there is no render test that the gallery draws 81 tiles in a browser.
