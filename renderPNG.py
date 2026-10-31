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

The slug rule and the module parser live in symbols_contract.py (its browser
twin is symbols/slug.js); check.py proves the two agree.

Dependency: cairosvg  (pip install cairosvg)
Run:        python3 renderPNG.py
"""

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
from symbols_contract import SIZES, SYMBOLS_DIRECTORY, module_files, parse, slug

BACKGROUND  = None                          # None = transparent; or e.g. "#000000"

# Tiny sizes look washed-out because thin strokes anti-alias to faint grey.
# For these folders, binarise the alpha channel so strokes are solid/crisp
# (each symbol keeps its colour; only the soft semi-transparent edges go away).
CRISP_SIZES  = {"18X18"}
ALPHA_CUTOFF = 80                           # alpha >= cutoff -> opaque, else transparent


def main() -> int:
    if not SYMBOLS_DIRECTORY.is_dir():
        sys.exit(f"symbols directory not found: {SYMBOLS_DIRECTORY}")

    # Create (and clear stale PNGs from) the output subfolders.
    for folder in SIZES:
        out_dir = SYMBOLS_DIRECTORY / folder
        out_dir.mkdir(parents=True, exist_ok=True)
        for old in out_dir.glob("*.png"):
            old.unlink()

    js_files = module_files()

    rendered, skipped, seen = 0, [], {}
    for js in js_files:
        svg, name, category = parse(js)
        if not svg:
            skipped.append(js.name)
            continue
        name, category = name or js.stem, category or ""
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
