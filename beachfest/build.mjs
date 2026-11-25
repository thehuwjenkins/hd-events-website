// Bundles public/ into src/files.gen.js so the worker serves the page itself (no asset upload needed).
import {readFileSync, readdirSync, statSync, writeFileSync} from 'node:fs';
import {join, relative} from 'node:path';
const TYPES = {html: 'text/html; charset=utf-8', png: 'image/png', jpg: 'image/jpeg', css: 'text/css', js: 'text/javascript', svg: 'image/svg+xml', ico: 'image/x-icon', txt: 'text/plain'};
const files = {};
const walk = (d) => readdirSync(d).forEach((f) => { const p = join(d, f); if (statSync(p).isDirectory()) return walk(p); const ext = f.split('.').pop(); if (TYPES[ext]) files['/' + relative('public', p)] = {type: TYPES[ext], b64: readFileSync(p).toString('base64')}; });
walk('public');
writeFileSync('src/files.gen.js', 'export const FILES = ' + JSON.stringify(files) + ';\n');
console.log(Object.keys(files));
