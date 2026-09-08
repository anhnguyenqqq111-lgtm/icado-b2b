import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const sourceDir = '/Users/t.anh/.gemini/antigravity-ide/scratch/TuanAnh-MKT-Planing/06. Projects/MayMacCTH';
const sources = [
  ['in-đồng-phục_broad-match_vn_2026-08-01.xlsx', 'A', 'B', 'C', null, null],
  ['may-đồng-phục_broad-match_vn_2026-08-01.xlsx', 'A', 'B', 'C', null, null],
  ['gap.keywords_2026-08-01T14_04_42.577Z.xlsx', 'A', 'C', 'D', 'E', 'B'],
  ['ĐỒNG-PHỤC-DOANH-NGHIỆP_pages_2026-08-01.xlsx', 'B', 'H', 'I', null, 'M'],
];
const output = process.argv[2] || path.join(process.cwd(), 'BoTuKhoa_MayMacCTH_DaLoc.xlsx');
const esc = (v) => String(v ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const unesc = (v = '') => v.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n)));
const colNum = (ref) => ref.split('').reduce((n, c) => n * 26 + c.charCodeAt(0) - 64, 0);
const colName = (n) => { let s = ''; while (n) { n--; s = String.fromCharCode(65 + n % 26) + s; n = Math.floor(n / 26); } return s; };
const norm = (s) => String(s ?? '').trim().toLocaleLowerCase('vi-VN').normalize('NFC').replace(/\s+/g, ' ');
const toNum = (v) => { const n = Number(v); return Number.isFinite(n) ? n : null; };

function unzip(file, entry) { return execFileSync('unzip', ['-p', file, entry], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 }); }
function parseSheet(file) {
  const listing = execFileSync('unzip', ['-Z1', file], { encoding: 'utf8' });
  const shared = listing.includes('xl/sharedStrings.xml')
    ? [...unzip(file, 'xl/sharedStrings.xml').matchAll(/<si>([\s\S]*?)<\/si>/g)].map(m => unesc([...m[1].matchAll(/<t[^>]*>([\s\S]*?)<\/t>/g)].map(t => t[1]).join('')))
    : [];
  const xml = unzip(file, 'xl/worksheets/sheet1.xml');
  const rows = [];
  for (const match of xml.matchAll(/<row\b[^>]*>([\s\S]*?)<\/row>/g)) {
    const row = {};
    for (const c of match[1].matchAll(/<c\b([^>]*)>([\s\S]*?)<\/c>/g)) {
      const ref = /r="([A-Z]+)\d+"/.exec(c[1])?.[1]; if (!ref) continue;
      const type = /t="([^"]+)"/.exec(c[1])?.[1];
      const raw = /<v>([\s\S]*?)<\/v>/.exec(c[2])?.[1] ?? /<t[^>]*>([\s\S]*?)<\/t>/.exec(c[2])?.[1] ?? '';
      row[ref] = type === 's' ? shared[Number(raw)] : unesc(raw);
    }
    rows.push(row);
  }
  return rows;
}
const negative = ['shopee','tiki','lazada','tiktok','taobao','thanh lý','thanh li','bán lại','ban lai','cho thuê','cho thue','váy cưới','vay cuoi','đầm dạ hội','dam da hoi','đầm ngủ','dam ngu'];
const competitors = ['đồng phục gl u','dong phuc glu','đồng phục hải anh','dong phuc hai anh','đồng phục phước thịnh','dong phuc phuoc thinh','đồng phục tân bình','dong phuc tan binh','đồng phục tràng an','dong phuc trang an','đồng phục gia đình','dong phuc gia dinh'];
function funnel(k) {
  if (/(báo giá|bao gia|giá |gia |xưởng|xuong|đặt |dat |mua |may |in |gia công|gia cong|dịch vụ|dich vu|liên hệ|lien he|số lượng|so luong)/.test(k)) return 'BOFU (Decision & Transaction)';
  if (/(mẫu|mau |so sánh|so sanh|bảng màu|bang mau|thiết kế|thiet ke|kiểu|kieu|form |size|phối màu|phoi mau|đẹp|dep)/.test(k)) return 'MOFU (Consideration)';
  if (/(là gì|la gi|cách |cach |hướng dẫn|huong dan|chất liệu|chat lieu|vải |vai |xu hướng|xu huong|kinh nghiệm|kinh nghiem)/.test(k)) return 'TOFU (Awareness)';
  return 'MOFU (Consideration)';
}
function cluster(k) {
  if (/(hải phòng|hai phong|miền bắc|mien bac|hà nội|ha noi|quảng ninh|quang ninh|bắc ninh|bac ninh|hưng yên|hung yen|thái bình|thai binh)/.test(k)) return 'Local SEO Hải Phòng & Miền Bắc';
  if (/(polo|áo thun|ao thun|phông|phong|t-shirt|tshirt)/.test(k)) return 'Áo Polo đồng phục';
  if (/(sơ mi|so mi|vest|blazer|công sở|cong so)/.test(k)) return 'Sơ mi & Vest công sở';
  if (/(bảo hộ|bao ho|kcn|khu công nghiệp|khu cong nghiep|công nhân|cong nhan|phản quang|phan quang)/.test(k)) return 'Bảo hộ lao động & KCN';
  if (/(nhà hàng|nha hang|cafe|cà phê|spa|hotel|khách sạn|khach san|f&b|bar |quán |quan |bếp|bep|lễ tân|le tan)/.test(k)) return 'Ngành dịch vụ (F&B / Spa / Hotel)';
  return 'Khác / Đồng phục tổng quát';
}

const merged = new Map(); let rawCount = 0; let excludedCount = 0;
for (const [fileName, keyCol, volumeCol, kdCol, cpcCol, intentCol] of sources) {
  const rows = parseSheet(path.join(sourceDir, fileName));
  for (const row of rows.slice(1)) {
    const keyword = String(row[keyCol] ?? '').trim(); if (!keyword) continue; rawCount++;
    const key = norm(keyword); if (negative.some(x => key.includes(x)) || competitors.some(x => key.includes(x))) { excludedCount++; continue; }
    const volume = toNum(row[volumeCol]); const kd = toNum(row[kdCol]); const cpc = cpcCol ? toNum(row[cpcCol]) : null;
    const item = merged.get(key) || { keyword, volume: null, kd: null, cpc: null, intent: '', sources: new Set() };
    if ((volume ?? -1) > (item.volume ?? -1)) { item.keyword = keyword; item.volume = volume; item.kd = kd; item.cpc = cpc; item.intent = intentCol ? String(row[intentCol] ?? '') : item.intent; }
    else { item.kd ??= kd; item.cpc ??= cpc; item.intent ||= intentCol ? String(row[intentCol] ?? '') : ''; }
    item.sources.add(fileName); merged.set(key, item);
  }
}
const master = [...merged.values()].map(x => ({
  'Từ khóa': x.keyword, 'Volume': x.volume, 'KD': x.kd, 'CPC (VND)': x.cpc,
  'Intent nguồn': x.intent, 'Phễu Marketing': funnel(norm(x.keyword)), 'Cụm chủ đề': cluster(norm(x.keyword)),
  'Nguồn': [...x.sources].join(' | ')
})).sort((a, b) => (b.Volume ?? -1) - (a.Volume ?? -1) || a['Từ khóa'].localeCompare(b['Từ khóa'], 'vi'));
const counts = (field, order) => order.map(name => ({ 'Nhóm': name, 'Số lượng từ khóa': master.filter(x => x[field] === name).length, 'Tỷ lệ': master.length ? master.filter(x => x[field] === name).length / master.length : 0 }));
const funnelOrder = ['TOFU (Awareness)','MOFU (Consideration)','BOFU (Decision & Transaction)'];
const clusterOrder = ['Áo Polo đồng phục','Sơ mi & Vest công sở','Bảo hộ lao động & KCN','Ngành dịch vụ (F&B / Spa / Hotel)','Local SEO Hải Phòng & Miền Bắc','Khác / Đồng phục tổng quát'];
const summary = [
  ['BỘ TỪ KHÓA SEO MAYMACCTH – ĐÃ LỌC', '', ''], ['Chỉ số', 'Giá trị', 'Ghi chú'],
  ['Tổng từ khóa gốc', rawCount, 'Gộp từ 4 tệp đầu vào'], ['Loại do từ khóa phủ định/đối thủ', excludedCount, 'Bao gồm sàn TMĐT, B2C không phù hợp và thương hiệu đối thủ'],
  ['Từ khóa sạch sau lọc & deduplicate', master.length, 'Dùng làm master keyword list'], [], ['PHÂN BỔ THEO PHỄU MARKETING', '', ''], ['Phễu Marketing', 'Số lượng từ khóa', 'Tỷ lệ'],
  ...counts('Phễu Marketing', funnelOrder).map(x => [x['Nhóm'], x['Số lượng từ khóa'], x['Tỷ lệ']]), [], ['PHÂN BỔ THEO CỤM CHỦ ĐỀ', '', ''], ['Cụm chủ đề', 'Số lượng từ khóa', 'Tỷ lệ'],
  ...counts('Cụm chủ đề', clusterOrder).map(x => [x['Nhóm'], x['Số lượng từ khóa'], x['Tỷ lệ']]), [], ['Nguồn dữ liệu', 'Trạng thái', ''], ...sources.map(x => [x[0], 'Đã xử lý', ''])
];
const masterRows = [['Từ khóa','Volume','KD','CPC (VND)','Intent nguồn','Phễu Marketing','Cụm chủ đề','Nguồn'], ...master.map(x => Object.values(x))];
function cell(v, r, c, style = 0) { const ref = `${colName(c)}${r}`; if (typeof v === 'number' && Number.isFinite(v)) return `<c r="${ref}" s="${style}"><v>${v}</v></c>`; return `<c r="${ref}" s="${style}" t="inlineStr"><is><t xml:space="preserve">${esc(v)}</t></is></c>`; }
function sheetXml(rows, widths, freeze = true, summaryMode = false) {
  const lastRow = rows.length, lastCol = Math.max(...rows.map(r => r.length));
  const cols = widths.map((w, i) => `<col min="${i + 1}" max="${i + 1}" width="${w}" customWidth="1"/>`).join('');
  const body = rows.map((row, ri) => { const r = ri + 1; const cells = row.map((v, ci) => { const isHeader = summaryMode ? [1,2,7,8,13,14,21].includes(r) : r === 1; const style = isHeader ? 1 : (typeof v === 'number' ? (summaryMode && (r >= 9 && r <= 11 || r >= 15 && r <= 20) && ci === 2 ? 3 : 2) : 0); return cell(v, r, ci + 1, style); }).join(''); return `<row r="${r}">${cells}</row>`; }).join('');
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><dimension ref="A1:${colName(lastCol)}${lastRow}"/><sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews><cols>${cols}</cols><sheetData>${body}</sheetData><autoFilter ref="A1:${colName(lastCol)}${lastRow}"/></worksheet>`;
}
const styles = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="2"><font><sz val="10"/><name val="Aptos"/></font><font><b/><color rgb="FFFFFFFF"/><sz val="10"/><name val="Aptos"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF0F766E"/><bgColor indexed="64"/></patternFill></fill></fills><borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="4"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFill="1" applyFont="1"/><xf numFmtId="3" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/><xf numFmtId="10" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/></cellXfs></styleSheet>`;
const workdir = fs.mkdtempSync(path.join(os.tmpdir(), 'maymaccth-xlsx-')); fs.mkdirSync(path.join(workdir, '_rels')); fs.mkdirSync(path.join(workdir, 'xl/_rels'), {recursive:true}); fs.mkdirSync(path.join(workdir, 'xl/worksheets'), {recursive:true});
fs.writeFileSync(path.join(workdir, '[Content_Types].xml'), `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/></Types>`);
fs.writeFileSync(path.join(workdir, '_rels/.rels'), `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>`);
fs.writeFileSync(path.join(workdir, 'xl/workbook.xml'), `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Thống Kê" sheetId="1" r:id="rId1"/><sheet name="Master Từ Khóa" sheetId="2" r:id="rId2"/></sheets></workbook>`);
fs.writeFileSync(path.join(workdir, 'xl/_rels/workbook.xml.rels'), `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>`);
fs.writeFileSync(path.join(workdir, 'xl/styles.xml'), styles);
fs.writeFileSync(path.join(workdir, 'xl/worksheets/sheet1.xml'), sheetXml(summary, [42,20,55], true, true));
fs.writeFileSync(path.join(workdir, 'xl/worksheets/sheet2.xml'), sheetXml(masterRows, [42,13,10,15,22,32,38,55]));
fs.mkdirSync(path.dirname(output), {recursive:true}); execFileSync('zip', ['-X', '-q', '-r', output, '.'], {cwd: workdir}); fs.rmSync(workdir, {recursive:true, force:true});
console.log(JSON.stringify({rawCount, excludedCount, cleanCount: master.length, output, funnel: counts('Phễu Marketing', funnelOrder), cluster: counts('Cụm chủ đề', clusterOrder)}, null, 2));
