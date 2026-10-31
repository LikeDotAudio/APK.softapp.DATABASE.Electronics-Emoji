// Part of the APK.audio project — http://APK.audio — made by Anthony Kuzub
// MIT Licence. Free, for everyone, for ever. Full text in LICENSE at the root.
// THE PNG FILENAME RULE — one source for the browser. symbols/<18X18|72X72>/<slug>.png
//   name lower-cased, every run of non [a-z0-9] -> '-', trimmed of '-',
//   + '-color' when the category names a colour variant.
// Its Python twin is slug() in symbols_contract.py (used by renderPNG.py);
// check.py runs both over every symbol and fails if they ever disagree.
export function slug(name, category) {
  let s = name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
  if (/colou?r/i.test(category)) s += '-color';
  return s;
}
