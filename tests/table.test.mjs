// Part of the APK.audio project — http://APK.audio — made by Anthony Kuzub
// MIT Licence. Free, for everyone, for ever. Full text in LICENSE at the root.
// THE ONE TABLE (ROAD-3494): the proposal's three tables are APKTables —
// two static markup() hosts (stood in by the vendored apk-table's scan) and the
// proof links via APKTable.create — and the page writes no table markup itself.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { loadApkTable } = require('./apk-table-shim.cjs');
const APP = new URL('..', import.meta.url).pathname;
const html = fs.readFileSync(APP + 'index.html', 'utf8');

test('three tables, each under its own id', () => {
  const hosts = [...html.matchAll(/data-apk-table-host="([^"]+)" data-apk-opts='([^']+)'/g)];
  assert.deepEqual(hosts.map((m) => m[1]), ['emoji-frequency-sources', 'emoji-selection-factors']);
  for (const [, id, opts] of hosts) assert.equal(JSON.parse(opts).id, id);
  assert.match(html, /APKTable\.create\(document\.getElementById\('proof-table'\), \{\s*id: 'emoji-frequency-proof'/);
});

test('the vendored apk-table stands static hosts in, and loads before the module that fills the proof table', () => {
  const { window } = loadApkTable(APP + 'vendor/apk-table/apk-table.js');
  assert.equal(typeof window.APKTable.scan, 'function');
  assert.equal(typeof window.APKTable.create, 'function');
  assert.ok(html.indexOf('vendor/apk-table/apk-table.js') < html.indexOf('<script type="module">'));
  assert.ok(html.indexOf('vendor/apk-table/apk-table.js') > html.indexOf('id="proof-table"'));
});

test('index.html draws no <table> itself, and a symbol is an <img>, not spliced markup', () => {
  assert.doesNotMatch(html, /<table|createElement\(['"]table/);
  assert.doesNotMatch(html, /innerHTML = `<div class="sym">\$\{icon\.svg\}/);
});
