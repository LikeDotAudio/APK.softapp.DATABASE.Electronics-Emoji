#!/usr/bin/env python3
# Part of the APK.audio project — http://APK.audio — made by Anthony Kuzub
# MIT Licence. Free, for everyone, for ever. Full text in LICENSE at the root.
"""Prove the symbol set is consistent. No dependencies (node optional).

    python3 check.py      exit 0 = consistent, 1 = drift (each failure printed)

1. Every symbols/*.js module has a name, a category from the closed set
   (symbols_contract.CATEGORIES) and an inline <svg>.
2. symbols/index.js imports every module once, lists every import in its
   default array, and declares `export const version`.
3. Slugs are unique, and the PNGs in symbols/18X18/ and symbols/72X72/ are
   exactly the slugs — no missing render, no orphan file.
4. The browser's slug (symbols/slug.js) and the Python twin
   (symbols_contract.slug, which renderPNG.py writes with) agree for every
   symbol. Needs `node`; without it this part is skipped and says so.
"""
import json
import re
import shutil
import subprocess
import sys

from symbols_contract import CATEGORIES, SIZES, SYMBOLS_DIRECTORY, module_files, parse, slug

IMPORT_RE = re.compile(r"^import\s+(\w+)\s+from\s+'\./([^']+)';", re.MULTILINE)


def main():
    failures = []
    symbols = []
    for path in module_files():
        svg, name, category = parse(path)
        for part, value in (("name", name), ("category", category), ("svg", svg)):
            if not value:
                failures.append(f"{path.name}: no {part}")
        if category and category not in CATEGORIES:
            failures.append(f"{path.name}: category {category!r} is not in the closed set {CATEGORIES}")
        if name and category:
            symbols.append((path.name, name, category))

    index = (SYMBOLS_DIRECTORY / "index.js").read_text(encoding="utf-8")
    imports = IMPORT_RE.findall(index)
    imported_files = [f for _, f in imports]
    body = index[index.index("export default"):] if "export default" in index else ""
    listed = set(re.findall(r"\b(\w+)\b", re.sub(r"//[^\n]*", "", body)))
    for path in module_files():
        count = imported_files.count(path.name)
        if count != 1:
            failures.append(f"index.js imports {path.name} {count} times (want 1)")
    for identifier, file in imports:
        if identifier not in listed:
            failures.append(f"index.js imports {identifier} ({file}) but does not list it")
    if not re.search(r"^export const version = '\d+\.\d+\.\d+';", index, re.MULTILINE):
        failures.append("index.js has no `export const version = 'X.Y.Z';`")

    slugs = {}
    for file, name, category in symbols:
        s = slug(name, category)
        if s in slugs:
            failures.append(f"slug collision {s!r}: {slugs[s]} and {file}")
        slugs[s] = file
    for folder in SIZES:
        on_disk = {p.stem for p in (SYMBOLS_DIRECTORY / folder).glob("*.png")}
        for missing in sorted(set(slugs) - on_disk):
            failures.append(f"{folder}/{missing}.png missing (run renderPNG.py)")
        for orphan in sorted(on_disk - set(slugs)):
            failures.append(f"{folder}/{orphan}.png has no symbol module")

    node = shutil.which("node")
    if node:
        pairs = [[n, c] for _, n, c in symbols]
        script = ("import { slug } from './symbols/slug.js';"
                  "let d='';process.stdin.on('data',c=>d+=c).on('end',()=>"
                  "console.log(JSON.stringify(JSON.parse(d).map(([n,c])=>slug(n,c)))));")
        run = subprocess.run([node, "--input-type=module", "-e", script], input=json.dumps(pairs),
                             capture_output=True, text=True, cwd=SYMBOLS_DIRECTORY.parent)
        if run.returncode:
            failures.append(f"node could not run symbols/slug.js: {run.stderr.strip()}")
        else:
            for (n, c), js in zip(pairs, json.loads(run.stdout)):
                if js != slug(n, c):
                    failures.append(f"slug drift for {n!r}/{c!r}: slug.js {js!r} vs Python {slug(n, c)!r}")
        twin = "slug.js == Python slug for every symbol"
    else:
        twin = "slug.js twin test skipped (no node)"

    for failure in failures:
        print("FAIL", failure)
    if failures:
        return 1
    print(f"OK {len(symbols)} symbols, {len(set(c for _, _, c in symbols))} categories, "
          f"{len(slugs)} slugs x {len(SIZES)} PNG sizes; {twin}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
