const fs = require('fs');
const path = require('path');

// This one-off batch is intentionally local-only: do not write to Google Sheets.
const sheets = require('./src/sheets');
sheets.writeRankingToSheet = async () => false;

const checker = require('./src/checker');

const keywords = [
    'mq international',
    'win flavor',
    'win flavors',
    'mq ingredients',
    'hương anh đào dạng bột',
    'bột bắp cải',
    'hương barbecue dạng bột',
    'hương bí đao dạng bột',
    'bột hương bò mua ở đâu',
    'hương thịt bò dạng bột',
    'hương bơ dạng bột',
    'hương bơ sữa dạng bột',
    'bột cà chua',
    'hương cà chua dạng bột',
    'hương cà phê dạng bột',
    'hương cà phê cappuccino dạng bột',
    'hương cà phê hòa tan dạng bột',
    'bột hương cam',
    'hương cam bột',
    'hương chanh bột',
    'hương chanh dây dạng bột',
    'bột chanh có tác dụng gì',
    'bột chanh dây',
];

function csvCell(value) {
    const text = value == null ? '' : String(value);
    return `"${text.replace(/"/g, '""')}"`;
}

async function main() {
    const outputDir = path.join(__dirname, 'output');
    fs.mkdirSync(outputDir, { recursive: true });

    await checker.startChecker({
        project: 'MQ Flavor',
        domain: 'https://mqflavor.com/',
        keywords,
        options: {
            maxPages: 5,
            chunkSize: 1,
            uuleLocation: 'Tan Phu, Ho Chi Minh City, Vietnam',
        },
    });

    while (true) {
        const status = checker.getStatus();
        console.log(`[MQ Flavor] ${status.done || 0}/${status.total || keywords.length} — ${status.state}`);
        if (status.state === 'done' || status.state === 'error') {
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const jsonPath = path.join(outputDir, `mqflavor-ranking-${timestamp}.json`);
            const csvPath = path.join(outputDir, `mqflavor-ranking-${timestamp}.csv`);
            const payload = {
                project: 'MQ Flavor',
                domain: 'mqflavor.com',
                location: 'Tan Phu, Ho Chi Minh City, Vietnam',
                checkedAt: new Date().toISOString(),
                state: status.state,
                errors: status.errors || [],
                results: status.results || [],
            };
            fs.writeFileSync(jsonPath, JSON.stringify(payload, null, 2));
            const headers = ['STT', 'Keyword', 'Rank', 'Page', 'URL', 'Local', 'Date', 'Time', 'Captcha'];
            const rows = payload.results.map(r => [r.idx, r.keyword, r.rank, r.page, r.url, r.local, r.date, r.time, r.captcha]);
            fs.writeFileSync(csvPath, [headers, ...rows].map(row => row.map(csvCell).join(',')).join('\n'));
            console.log(`JSON: ${jsonPath}`);
            console.log(`CSV: ${csvPath}`);
            process.exit(status.state === 'done' ? 0 : 1);
        }
        await new Promise(resolve => setTimeout(resolve, 3000));
    }
}

main().catch(error => {
    console.error(error);
    process.exit(1);
});
