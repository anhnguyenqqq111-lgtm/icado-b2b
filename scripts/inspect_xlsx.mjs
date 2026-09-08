import { execFileSync } from 'node:child_process';
import path from 'node:path';

const files = process.argv.slice(2);
const decode = (s = '') => s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n)));
const cells = (xml, shared) => {
  const rows = [];
  for (const row of xml.matchAll(/<row\b[^>]*>([\s\S]*?)<\/row>/g)) {
    const out = {};
    for (const cell of row[1].matchAll(/<c\b([^>]*)>([\s\S]*?)<\/c>/g)) {
      const ref = /r="([A-Z]+)\d+"/.exec(cell[1])?.[1];
      const type = /t="([^"]+)"/.exec(cell[1])?.[1];
      const raw = /<v>([\s\S]*?)<\/v>/.exec(cell[2])?.[1] ?? /<t[^>]*>([\s\S]*?)<\/t>/.exec(cell[2])?.[1] ?? '';
      out[ref] = decode(type === 's' ? shared[Number(raw)] : raw);
    }
    rows.push(out);
  }
  return rows;
};
for (const file of files) {
  const list = execFileSync('unzip', ['-Z1', file], { encoding: 'utf8' });
  const shared = list.includes('xl/sharedStrings.xml') ? [...execFileSync('unzip', ['-p', file, 'xl/sharedStrings.xml'], {encoding:'utf8'}).matchAll(/<si>([\s\S]*?)<\/si>/g)].map(x => decode([...x[1].matchAll(/<t[^>]*>([\s\S]*?)<\/t>/g)].map(y=>y[1]).join(''))) : [];
  const sheets = list.split('\n').filter(x => /^xl\/worksheets\/sheet\d+\.xml$/.test(x));
  console.log(`FILE: ${path.basename(file)}`);
  for (const sheet of sheets) {
    const rows = cells(execFileSync('unzip', ['-p', file, sheet], {encoding:'utf8'}), shared);
    console.log(`${sheet}:`, JSON.stringify(rows.slice(0, 3)));
  }
}
