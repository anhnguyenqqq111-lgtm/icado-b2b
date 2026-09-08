import fs from "node:fs";

const initialPath = "heritage-internal-link-research.md";
const expandedPath = "heritage-internal-links-574.md";
const outputPath = "heritage-internal-links-combined.md";

const initial = fs.readFileSync(initialPath, "utf8");
const expanded = fs.readFileSync(expandedPath, "utf8");

const initialBody = initial.slice(initial.indexOf("## 1. Nơi đại ngàn khoáng đạt"));
const expandedBody = expanded.slice(expanded.indexOf("## 7 trải nghiệm Hanoi-core"));

const header = `# Nghiên cứu internal link – Heritage Vietnam Airlines

- Website: https://heritagevietnamairlines.com/
- Ngày nghiên cứu: 06/08/2026
- Phần ban đầu: 16 bài nguồn, 48 đề xuất.
- Phần mở rộng từ Excel: đọc thành công 563/574 bài, 1.319 đề xuất; 216 bài chưa đủ 3 anchor mạnh.
- Tiêu chí: anchor có nguyên văn trong thân bài; URL đích cùng domain; không self-link hoặc trùng cặp nguồn–đích.

`;

const merged = `${header}${initialBody.trim()}\n\n---\n\n## Phần nghiên cứu mở rộng\n\n${expandedBody.trim()}\n`;
fs.writeFileSync(outputPath, merged, "utf8");
