# Delivery — DATABASE.Electronics-Emoji

## Build and test
No build: the pages and modules are served as committed. The PNGs are committed outputs of `renderPNG.py`, re-run by hand. No tests; the only check is `.apk.scripts/smoke.py` (HEAD on origin, `index.html` answers 200) — [SMOKE.md](../%F0%9F%A7%A9Manual%20and%20Artifacts/SMOKE.md). No CI workflow in this repo.

## Where it lands
- **apk.audio** — on every push to the APK.audio root's `main`, `.github/workflows/ci.yml` uploads the Softapps tree over FTPS (`PODS/POD.THIN/WEB.Frontend-Assets/.apk.scripts/deploy.py`, which skips `*.py`). Live: `https://apk.audio/APK:Softapps/DATABASE/DATABASE.Electronics-Emoji/gallery.htm` and `…/index.html` (both 200 on 2026-10-30). This repo reaches that run through a submodule bump in the root (`.apk.scripts/deploy_all.py`).
- **A node** — copied with the Softapps tree into WEB.Frontend-Assets and Storage-Portal (`:8080/Softapps/DATABASE/DATABASE.Electronics-Emoji/gallery.htm`); the OS walker lists it from `display.json` with entry `gallery.htm`. After an edit: `up-stack.sh WEB.Frontend-Assets` and `up-stack.sh DATABASE.server.SQL`.
- **`server.py` and `renderPNG.py`** are never shipped: the root `.dockerignore` drops `Softapps/**/*.py` and the FTPS deploy skips `.py`. They are bench tools.

## Not automated
Re-rendering PNGs after a symbol edit; the submodule bump; node image rebuilds.

Repository: `https://github.com/LikeDotAudio/APK.softapp.DATABASE.Electronics-Emoji.git`
