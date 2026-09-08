import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const source = '/Users/t.anh/.gemini/antigravity-ide/scratch/TuanAnh-MKT-Planing/06. Projects/MayMacCTH/BoTuKhoa_MayMacCTH_DaLoc.xlsx';
const output = process.argv[2] || path.join(process.cwd(), 'BoTuKhoa_MayMacCTH_ChuanThuongHieu.xlsx');
const esc = (v) => String(v ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const unesc = (v='') => v.replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#(\d+);/g,(_,n)=>String.fromCodePoint(Number(n)));
const norm = (v) => String(v ?? '').trim().toLocaleLowerCase('vi-VN').normalize('NFC').replace(/\s+/g,' ');
const colName = (n) => { let s=''; while(n){n--;s=String.fromCharCode(65+n%26)+s;n=Math.floor(n/26);} return s; };
function inputRows() {
  const xml = execFileSync('unzip',['-p',source,'xl/worksheets/sheet2.xml'],{encoding:'utf8',maxBuffer:64*1024*1024});
  return [...xml.matchAll(/<row\b[^>]*>([\s\S]*?)<\/row>/g)].map(m => {
    const r={}; for (const c of m[1].matchAll(/<c\b([^>]*)>([\s\S]*?)<\/c>/g)) {
      const key=/r="([A-Z]+)\d+"/.exec(c[1])?.[1]; const raw=/<v>([\s\S]*?)<\/v>/.exec(c[2])?.[1] ?? /<t[^>]*>([\s\S]*?)<\/t>/.exec(c[2])?.[1] ?? '';
      if(key) r[key]=unesc(raw);
    } return r;
  });
}
const remote = ['cần thơ','can tho','bình dương','binh duong','cà mau','ca mau','hồ chí minh','ho chi minh','tphcm','tp hcm','sài gòn','sai gon','đà nẵng','da nang','nha trang','biên hòa','bien hoa','đồng nai','dong nai','vũng tàu','vung tau','long an','huế','hue','quảng nam','quang nam','buôn ma thuột','buon ma thuot'];
const hcmDistricts = ['gò vấp','go vap','tân bình','tan binh','tân phú','tan phu','bình thạnh','binh thanh','phú nhuận','phu nhuan','thủ đức','thu duc','bình chánh','binh chanh','củ chi','cu chi','hóc môn','hoc mon','nhà bè','nha be','cần giờ','can gio'];
const ecommerce = ['shopee','lazada','tiki','tiktok shop','tiktokshop','taobao','1688','hàng quảng châu','hang quang chau','order taobao'];
const lowPrice = ['thanh lý','thanh li','xả kho','xa kho','hàng thùng','hang thung','đồng phục cũ','dong phuc cu'];
const tailoring = ['tiệm may gần đây','tiem may gan day','sửa quần áo','sua quan ao','tiệm may áo dài','tiem may ao dai','may đo quần tây nam','may do quan tay nam','may suit chú rể','may suit chu re'];
const competitors = ['đồng phục gl u','dong phuc glu','đồng phục hải anh','dong phuc hai anh','đồng phục phước thịnh','dong phuc phuoc thinh','đồng phục tân bình','dong phuc tan binh','đồng phục tràng an','dong phuc trang an','đồng phục gia đình','dong phuc gia dinh'];
const b2bSignals = /(đồng phục|dong phuc|áo lớp|ao lop|áo nhóm|ao nhom|team building|áo thun công ty|ao thun cong ty|áo polo|ao polo|áo công nhân|ao cong nhan|bảo hộ|bao ho|phản quang|phan quang|tạp dề|tap de|nhà hàng|nha hang|quán cafe|quan cafe|cà phê|ca phe|spa|khách sạn|khach san|hotel|in logo|in áo|in ao|xưởng may|xuong may|may đồng phục|may dong phuc)/;
function excludedReason(k) {
  const scope = b2bSignals.test(k);
  if (ecommerce.some(x=>k.includes(x))) return 'Sàn TMĐT / mua hộ';
  if (competitors.some(x=>k.includes(x))) return 'Thương hiệu đối thủ';
  if (lowPrice.some(x=>k.includes(x)) || /\b(10|15|20)k\b/.test(k)) return 'Giá quá thấp / xả kho';
  if (tailoring.some(x=>k.includes(x))) return 'May đo cá nhân / tiệm may nhỏ';
  if ((remote.some(x=>k.includes(x)) || hcmDistricts.some(x=>k.includes(x)) || /\bhcm\b|\b(q\.?\s?(?:1[0-2]|[1-9]))\b|\b(quận|quan)\s?(?:1[0-2]|[1-9])\b/.test(k)) && !/(toàn quốc|toan quoc|giao hàng toàn quốc|giao hang toan quoc)/.test(k)) return 'Địa phương ngoài vùng mục tiêu';
  if (/(đồng phục gia đình|dong phuc gia dinh|áo gia đình|ao gia dinh)/.test(k)) return 'Bán lẻ / thời trang cá nhân';
  if (/(áo thun nam|ao thun nam|áo thun nữ|ao thun nu|quần jean|quan jean|áo phông unisex|ao phong unisex|váy nữ công sở|vay nu cong so|đầm nữ|dam nu|áo hoodie nam|ao hoodie nam|áo sweater|ao sweater|quần tây nam đẹp|quan tay nam dep|đồng phục gia đình|dong phuc gia dinh|áo gia đình|ao gia dinh)/.test(k) && !scope) return 'Bán lẻ / thời trang cá nhân';
  if (/(máy in|may in|máy may|may may|tuyển dụng|tuyen dung|việc làm|viec lam|rập may|rap may)/.test(k)) return 'Không thuộc dịch vụ may đồng phục B2B';
  if (!scope) return 'Không đủ tín hiệu B2B / đồng phục';
  return null;
}
function funnel(k) {
  if (/(báo giá|bao gia|giá |gia |xưởng|xuong|đặt |dat |mua |may |in |gia công|gia cong|dịch vụ|dich vu|liên hệ|lien he|số lượng|so luong)/.test(k)) return 'BOFU (Decision & Transaction)';
  if (/(mẫu|mau |so sánh|so sanh|bảng màu|bang mau|thiết kế|thiet ke|kiểu|kieu|form |size|phối màu|phoi mau|đẹp|dep)/.test(k)) return 'MOFU (Consideration)';
  if (/(là gì|la gi|cách |cach |hướng dẫn|huong dan|chất liệu|chat lieu|vải |vai |xu hướng|xu huong|kinh nghiệm|kinh nghiem)/.test(k)) return 'TOFU (Awareness)';
  return 'MOFU (Consideration)';
}
function cluster(k) {
  if (/(hải phòng|hai phong|hà nội|ha noi|quảng ninh|quang ninh|hải dương|hai duong|vsip|tràng duệ|trang due|nomura|đình vũ|dinh vu|kcn)/.test(k)) return 'Local SEO Hải Phòng & Miền Bắc';
  if (/(áo lớp|ao lop|áo nhóm|ao nhom|team building|học sinh|hoc sinh)/.test(k)) return 'B2B/B2C Tập thể: Lớp, Nhóm, Học sinh';
  if (/(bảo hộ|bao ho|công nhân|cong nhan|kỹ sư|ky su|phản quang|phan quang)/.test(k)) return 'B2B Công nghiệp & KCN';
  if (/(nhà hàng|nha hang|cafe|cà phê|ca phe|spa|hotel|khách sạn|khach san|tạp dề|tap de|lễ tân|le tan|f&b)/.test(k)) return 'B2B Ngành dịch vụ';
  if (/(sơ mi|so mi|vest|blazer|công sở|cong so)/.test(k)) return 'B2B Doanh nghiệp: Sơ mi & Vest';
  if (/(polo|áo thun|ao thun|phông|phong|t-shirt|tshirt)/.test(k)) return 'B2B Doanh nghiệp: Polo & Áo thun';
  return 'B2B Doanh nghiệp & Công ty';
}
const rejectionOrder=['Sàn TMĐT / mua hộ','Thương hiệu đối thủ','Giá quá thấp / xả kho','May đo cá nhân / tiệm may nhỏ','Địa phương ngoài vùng mục tiêu','Bán lẻ / thời trang cá nhân','Không thuộc dịch vụ may đồng phục B2B','Không đủ tín hiệu B2B / đồng phục'];
const rows=inputRows(); const sourceHeaders=rows.shift(); if(sourceHeaders.A!=='Từ khóa') throw new Error('Không đọc được cấu trúc Master Từ Khóa nguồn.');
const rejected=new Map(rejectionOrder.map(x=>[x,0])); const clean=[];
for (const r of rows) { const keyword=String(r.A??'').trim(); if(!keyword) continue; const k=norm(keyword); const reason=excludedReason(k); if(reason){rejected.set(reason,(rejected.get(reason)||0)+1);continue;} clean.push({keyword,volume:Number(r.B)||0,kd:r.C===''?null:Number(r.C),cpc:r.D===''?null:Number(r.D),funnel:funnel(k),cluster:cluster(k),intent:r.E||''}); }
clean.sort((a,b)=>b.volume-a.volume||a.keyword.localeCompare(b.keyword,'vi'));
const funnelOrder=['TOFU (Awareness)','MOFU (Consideration)','BOFU (Decision & Transaction)'];
const clusterOrder=['B2B Doanh nghiệp: Polo & Áo thun','B2B Doanh nghiệp: Sơ mi & Vest','B2B Doanh nghiệp & Công ty','B2B Công nghiệp & KCN','B2B Ngành dịch vụ','B2B/B2C Tập thể: Lớp, Nhóm, Học sinh','Local SEO Hải Phòng & Miền Bắc'];
const count=(field,order)=>order.map(n=>[n,clean.filter(x=>x[field]===n).length,clean.length?clean.filter(x=>x[field]===n).length/clean.length:0]);
const stats=[['BỘ TỪ KHÓA MAYMACCTH – CHUẨN THƯƠNG HIỆU','',''],['Chỉ số','Số lượng','Ghi chú'],['Từ khóa đầu vào',rows.length,'Master từ khóa đã gộp'],['Từ khóa bị loại',rows.length-clean.length,'Theo bộ lọc định vị B2B'],['Từ khóa chuẩn thương hiệu',clean.length,'Phù hợp May Mặc CTH'],[],['LOẠI BỎ THEO TIÊU CHÍ','',''],['Tiêu chí','Số lượng',''],...rejectionOrder.map(a=>[a,rejected.get(a),'']),[],['PHÂN BỔ THEO PHỄU MARKETING','',''],['Phễu','Số lượng','Tỷ lệ'],...count('funnel',funnelOrder),[],['PHÂN BỔ THEO CỤM CHỦ ĐỀ','',''],['Cluster','Số lượng','Tỷ lệ'],...count('cluster',clusterOrder)];
const master=[['STT','Từ khóa','Volume','KD','CPC','Phễu','Cluster','Search Intent'],...clean.map((x,i)=>[i+1,x.keyword,x.volume,x.kd,x.cpc,x.funnel,x.cluster,x.intent])];
function articleGroup(k) {
  if (/(hải phòng|hai phong|hà nội|ha noi|quảng ninh|quang ninh|hải dương|hai duong|vsip|tràng duệ|trang due|nomura|đình vũ|dinh vu)/.test(k)) return 'Local SEO: May đồng phục tại Hải Phòng & Miền Bắc';
  if (/(áo lớp|ao lop|học sinh|hoc sinh)/.test(k)) return 'Đồng phục học sinh & áo lớp số lượng lớn';
  if (/(team building|áo nhóm|ao nhom|họp lớp|hop lop)/.test(k)) return 'Áo nhóm & team building';
  if (/(bảo hộ|bao ho|phản quang|phan quang|công nhân|cong nhan|kỹ sư|ky su|kcn)/.test(k)) return 'Quần áo bảo hộ & đồng phục công nghiệp';
  if (/(tạp dề|tap de)/.test(k)) return 'Tạp dề in logo cho doanh nghiệp';
  if (/(nhà hàng|nha hang|cafe|cà phê|ca phe|quán |quan |f&b)/.test(k)) return 'Đồng phục nhà hàng & quán cafe';
  if (/(spa|khách sạn|khach san|hotel|lễ tân|le tan)/.test(k)) return 'Đồng phục spa & khách sạn';
  if (/(sơ mi|so mi)/.test(k)) return 'Áo sơ mi đồng phục công sở';
  if (/(vest|blazer)/.test(k)) return 'Vest đồng phục công sở';
  if (/(polo)/.test(k)) return 'Áo polo đồng phục doanh nghiệp';
  if (/(áo thun|ao thun|phông|phong|t-shirt|tshirt)/.test(k)) return 'Áo thun đồng phục công ty';
  if (/(in áo|in ao|in đồng phục|in dong phuc|in logo)/.test(k)) return 'In áo đồng phục theo yêu cầu';
  if (/(mẫu|mau |thiết kế|thiet ke|bảng màu|bang mau|chất liệu|chat lieu|vải |vai |size|cách |cach |là gì|la gi)/.test(k)) return 'Tư vấn mẫu mã & chất liệu đồng phục';
  if (/(báo giá|bao gia|giá |gia )/.test(k)) return 'Báo giá may đồng phục doanh nghiệp';
  return 'May đồng phục doanh nghiệp theo yêu cầu';
}
const pillarTitles={
  'B2B Doanh nghiệp: Polo & Áo thun':'Pillar 1: Đồng phục doanh nghiệp – áo polo & áo thun',
  'B2B Doanh nghiệp: Sơ mi & Vest':'Pillar 2: Đồng phục công sở – sơ mi & vest',
  'B2B Doanh nghiệp & Công ty':'Pillar 3: May đồng phục doanh nghiệp theo yêu cầu',
  'B2B Công nghiệp & KCN':'Pillar 4: Đồng phục công nghiệp, bảo hộ & KCN',
  'B2B Ngành dịch vụ':'Pillar 5: Đồng phục ngành dịch vụ – F&B, Spa & Hotel',
  'B2B/B2C Tập thể: Lớp, Nhóm, Học sinh':'Pillar 6: Đồng phục tập thể – học sinh, áo lớp & team building',
  'Local SEO Hải Phòng & Miền Bắc':'Pillar 7: May đồng phục tại Hải Phòng & Miền Bắc'
};
const pillarMap=new Map(clusterOrder.map(c=>[c,{title:pillarTitles[c],keywords:[]}]));
for(const x of clean) pillarMap.get(x.cluster).keywords.push(x);
const articles=[['STT','Chủ đề Pillar','Từ khóa chính','Volume chính','Từ khóa liên quan tiêu biểu','Tổng key bao phủ','Cluster nguồn']];
[...pillarMap.entries()].filter(([,p])=>p.keywords.length).sort(([,a],[,b])=>Math.max(...b.keywords.map(x=>x.volume))-Math.max(...a.keywords.map(x=>x.volume))).forEach(([cluster,p],i)=>{p.keywords.sort((x,y)=>y.volume-x.volume||x.keyword.localeCompare(y.keyword,'vi'));const main=p.keywords[0];articles.push([i+1,p.title,main.keyword,main.volume,p.keywords.slice(1,26).map(x=>x.keyword).join(', '),p.keywords.length,cluster]);});
function cell(v,r,c,s=0){const ref=`${colName(c)}${r}`;return typeof v==='number'&&Number.isFinite(v)?`<c r="${ref}" s="${s}"><v>${v}</v></c>`:`<c r="${ref}" s="${s}" t="inlineStr"><is><t xml:space="preserve">${esc(v)}</t></is></c>`;}
function sheet(rows,widths,summary=false){const cols=widths.map((w,i)=>`<col min="${i+1}" max="${i+1}" width="${w}" customWidth="1"/>`).join('');const body=rows.map((row,i)=>`<row r="${i+1}">${row.map((v,j)=>{const header=summary?[1,2,7,8,13,14,18,19].includes(i+1):i===0;const percent=summary&&typeof v==='number'&&j===2&&((i+1)>=15&&(i+1)<=17||(i+1)>=20);return cell(v,i+1,j+1,header?1:percent?3:typeof v==='number'?2:0);}).join('')}</row>`).join('');const last=colName(Math.max(...rows.map(x=>x.length)));return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><dimension ref="A1:${last}${rows.length}"/><sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews><cols>${cols}</cols><sheetData>${body}</sheetData><autoFilter ref="A1:${last}${rows.length}"/></worksheet>`;}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'cth-brand-'));fs.mkdirSync(path.join(tmp,'_rels'));fs.mkdirSync(path.join(tmp,'xl/_rels'),{recursive:true});fs.mkdirSync(path.join(tmp,'xl/worksheets'),{recursive:true});
fs.writeFileSync(path.join(tmp,'[Content_Types].xml'),'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/></Types>');
fs.writeFileSync(path.join(tmp,'_rels/.rels'),'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>');
fs.writeFileSync(path.join(tmp,'xl/workbook.xml'),'<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Báo cáo Thống kê" sheetId="1" r:id="rId1"/><sheet name="Từ khóa chuẩn thương hiệu" sheetId="2" r:id="rId2"/><sheet name="Bộ bài viết Pillar" sheetId="3" r:id="rId3"/></sheets></workbook>');
fs.writeFileSync(path.join(tmp,'xl/_rels/workbook.xml.rels'),'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/><Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>');
fs.writeFileSync(path.join(tmp,'xl/styles.xml'),'<?xml version="1.0" encoding="UTF-8"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="2"><font><sz val="10"/><name val="Aptos"/></font><font><b/><color rgb="FFFFFFFF"/><sz val="10"/><name val="Aptos"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF0F766E"/><bgColor indexed="64"/></patternFill></fill></fills><borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="4"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFill="1" applyFont="1"/><xf numFmtId="3" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/><xf numFmtId="10" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/></cellXfs></styleSheet>');
fs.writeFileSync(path.join(tmp,'xl/worksheets/sheet1.xml'),sheet(stats,[45,18,42],true));fs.writeFileSync(path.join(tmp,'xl/worksheets/sheet2.xml'),sheet(master,[8,42,12,9,14,29,42,20]));fs.writeFileSync(path.join(tmp,'xl/worksheets/sheet3.xml'),sheet(articles,[8,48,36,14,120,16,42]));fs.mkdirSync(path.dirname(output),{recursive:true});execFileSync('zip',['-X','-q','-r',output,'.'],{cwd:tmp});fs.rmSync(tmp,{recursive:true,force:true});
console.log(JSON.stringify({input:rows.length,rejected:Object.fromEntries(rejected),clean:clean.length,pillars:articles.length-1,funnel:count('funnel',funnelOrder),cluster:count('cluster',clusterOrder),output},null,2));
