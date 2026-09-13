#!/usr/bin/env python3
# Part of the APK.audio project — http://APK.audio — made by Anthony Kuzub
# MIT Licence. Free, for everyone, for ever. Full text in LICENSE at the root.
"""
renderPNG.py — rasterise every schematic symbol to PNG.

Each icon lives in symbols/<file>.js as an ES module exporting
    export default { name, category, svg: `<svg ...>...</svg>` }

This script pulls the inline <svg> out of every module and renders it to a
transparent-background PNG at each target resolution, writing the files into
size-named subfolders of symbols/:

    symbols/18X18/<slug>.png    (18 x 18 px)
    symbols/72X72/<slug>.png    (72 x 72 px)

The output filename is a SLUG derived from the symbol's name + category, NOT
the source module's filename, so index.html can compute the same path purely
from the icon object it imports:

    slug = name.lowercased, non-alphanumerics -> '-', trimmed
           + '-color' if the category is a colour-variant category

    "Resistor"        / Primitive Components   -> resistor
    "Switch (closed)" / Primitive Components   -> switch-closed
    "Op-Amp"          / Primitive Components   -> op-amp
    "Ammeter"         / Colour Variants        -> ammeter-color
    "AND"             / Logic Gates (Colour)   -> and-color

Keep this slug rule in sync with the `slug()` function in index.html.

Dependency: cairosvg  (pip install cairosvg)
Run:        python3 renderPNG.py
"""

import re
import sys
from pathlib import Path

try:
    import cairosvg
except ImportError:
    sys.exit(
        "Missing dependency 'cairosvg'.\n"
        "Install it with:  pip install cairosvg\n"
        "(needs the system Cairo library, e.g. apt install libcairo2)"
    )

try:
    from PIL import Image
except ImportError:
    sys.exit("Missing dependency 'Pillow'. Install with: pip install Pillow")

# ---- Configuration -------------------------------------------------------
SCRIPT_DIR  = Path(__file__).resolve().parent
SYMBOLS_DIRECTORY = SCRIPT_DIR / "symbols"
SIZES       = {"18X18": 18, "72X72": 72}   # folder name -> pixel size
BACKGROUND  = None                          # None = transparent; or e.g. "#000000"

# Tiny sizes look washed-out because thin strokes anti-alias to faint grey.
# For these folders, binarise the alpha channel so strokes are solid/crisp
# (each symbol keeps its colour; only the soft semi-transparent edges go away).
CRISP_SIZES  = {"18X18"}
ALPHA_CUTOFF = 80                           # alpha >= cutoff -> opaque, else transparent

SVG_RE  = re.compile(r"<svg.*?</svg>", re.DOTALL)
NAME_RE = re.compile(r'name:\s*"([^"]*)"')
CAT_RE  = re.compile(r'category:\s*"([^"]*)"')


def slug(name: str, category: str) -> str:
    """Stable filename slug from name + colour category. Mirrors index.html."""
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if "colour" in category.lower() or "color" in category.lower():
        s += "-color"
    return s


def parse(js_path: Path):
    """Return (svg, name, category) from a symbol module, or None if no svg."""
    text = js_path.read_text(encoding="utf-8")
    svg = SVG_RE.search(text)
    if not svg:
        return None
    name = NAME_RE.search(text)
    cat = CAT_RE.search(text)
    return (
        svg.group(0),
        name.group(1) if name else js_path.stem,
        cat.group(1) if cat else "",
    )


def main() -> int:
    if not SYMBOLS_DIRECTORY.is_dir():
        sys.exit(f"symbols directory not found: {SYMBOLS_DIRECTORY}")

    # Create (and clear stale PNGs from) the output subfolders.
    for folder in SIZES:
        out_dir = SYMBOLS_DIRECTORY / folder
        out_dir.mkdir(parents=True, exist_ok=True)
        for old in out_dir.glob("*.png"):
            old.unlink()

    js_files = sorted(p for p in SYMBOLS_DIRECTORY.glob("*.js") if p.name != "index.js")

    rendered, skipped, seen = 0, [], {}
    for js in js_files:
        parsed = parse(js)
        if not parsed:
            skipped.append(js.name)
            continue
        svg, name, category = parsed
        sl = slug(name, category)

        if sl in seen:
            print(f"  ! slug collision: '{sl}' from {js.name} "
                  f"already produced by {seen[sl]} — overwriting")
        seen[sl] = js.name

        svg_bytes = svg.encode("utf-8")
        for folder, px in SIZES.items():
            out = SYMBOLS_DIRECTORY / folder / f"{sl}.png"
            cairosvg.svg2png(
                bytestring=svg_bytes,
                write_to=str(out),
                output_width=px,
                output_height=px,
                background_color=BACKGROUND,
            )
            if folder in CRISP_SIZES:
                im = Image.open(out).convert("RGBA")
                r, g, b, a = im.split()
                a = a.point(lambda v: 255 if v >= ALPHA_CUTOFF else 0)
                Image.merge("RGBA", (r, g, b, a)).save(out)
        rendered += 1
        print(f"  {js.name:<24} -> {sl}.png")

    print(f"\nRendered {rendered} symbol(s) x {len(SIZES)} sizes "
          f"into {', '.join(str(SYMBOLS_DIRECTORY / f) for f in SIZES)}")
    if skipped:
        print(f"Skipped (no <svg> found): {', '.join(skipped)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
