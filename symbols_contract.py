# Part of the APK.audio project — http://APK.audio — made by Anthony Kuzub
# MIT Licence. Free, for everyone, for ever. Full text in LICENSE at the root.
"""The symbol-module contract, in Python, with no dependencies.

Shared by renderPNG.py (which writes the PNGs) and check.py (which proves the
set is consistent). The browser's half is symbols/slug.js; check.py runs both
slug implementations over every symbol and fails if they disagree.

A symbol module is symbols/<file>.js:
    export default { name: "...", category: "...", svg: `<svg ...>...</svg>` }
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SYMBOLS_DIRECTORY = HERE / "symbols"
NOT_SYMBOLS = {"index.js", "slug.js"}
SIZES = {"18X18": 18, "72X72": 72}   # PNG folder -> pixel size

# The closed category set. A new category is a deliberate change here.
CATEGORIES = (
    "Primitive Components",
    "Logic Gates",
    "Colour Variants",
    "Logic Gates (Colour)",
)

SVG_RE = re.compile(r"<svg.*?</svg>", re.DOTALL)
NAME_RE = re.compile(r'name:\s*"([^"]*)"')
CAT_RE = re.compile(r'category:\s*"([^"]*)"')


def slug(name: str, category: str) -> str:
    """PNG filename slug from name + colour category. Twin of symbols/slug.js."""
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if re.search(r"colou?r", category, re.IGNORECASE):
        s += "-color"
    return s


def module_files():
    return sorted(p for p in SYMBOLS_DIRECTORY.glob("*.js") if p.name not in NOT_SYMBOLS)


def parse(js_path: Path):
    """Return (svg, name, category); any part missing is None."""
    text = js_path.read_text(encoding="utf-8")
    svg, name, cat = SVG_RE.search(text), NAME_RE.search(text), CAT_RE.search(text)
    return (
        svg.group(0) if svg else None,
        name.group(1) if name else None,
        cat.group(1) if cat else None,
    )
