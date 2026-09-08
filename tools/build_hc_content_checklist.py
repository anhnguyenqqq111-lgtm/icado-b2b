from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape
import re

OUT = Path("outputs/claude-artifact-checklist/claude-artifact-checklist-7-sheets.xlsx")

COMMON = [
    ["HC-CORE", "Mọi bước", "Luôn áp dụng giọng văn chuẩn Home Credit, chống dịch máy.", "Áp dụng hc-core-voice xuyên suốt mọi bước.", "hc-core-voice", "Giữ giọng tư vấn nhất quán, khách quan và tự nhiên.", "Chưa bắt đầu"],
]

OUTLINE = [
    ["O01", "Discover / Mở rộng", "Check bài cũ", "Canonical trỏ nơi khác + noindex: dừng và báo người dùng. Canonical trỏ nơi khác, không noindex: vẫn báo. Chỉ noindex, tự canonical: báo ngắn, vẫn audit tiếp. Không có bài: chuyển Workflow B. Phát hiện trùng nội dung: không tự quyết, phải hỏi.", "Search site:homecredit.vn/blog [keyword]; nếu có bài thì fetch toàn bộ nội dung, đọc canonical và meta-robots trong head; áp bảng 5 tình huống. Workflow B chỉ search + fetch nội dung. Xe/điện máy kiểm tra đổi tên cùng sản phẩm hoặc bài top tổng hợp cùng dòng. Output đúng 1 dòng kết luận.", "hc-check-existing-article", "Chặn tạo 2 bài trùng cạnh tranh nhau, audit bài đã bị chặn index, và tránh bỏ qua tín hiệu canonical/noindex.", "Chưa bắt đầu"],
    ["O02", "Discover / Mở rộng", "Research đối thủ", "Ưu tiên URL thật người dùng đưa. URL lỗi 404/chặn bot/timeout: không bịa nội dung thay thế. Assessment Note đủ 5 mục: Strengths / Weaknesses / Structure quan sát được / Claims đáng chú ý / Trích dẫn nguyên văn. Mâu thuẫn bản chất từ ≥2 nguồn độc lập: không tự quyết hướng sửa.", "Lấy URL đối thủ, fetch từng URL, đọc toàn bộ nội dung liên quan. Rút Assessment Note ngay sau mỗi lần fetch. URL lỗi: báo rõ, loại khỏi audit, hỏi nguồn thay hay để nguyên. Mâu thuẫn: đánh dấu ưu tiên cao nhất và trích nguyên văn từng nguồn. Lưu song song <slug>_competitor_headings.md cho cả 5 đối thủ.", "hc-research-competitors", "Chặn viết outline dựa trên trí nhớ, bỏ sót mâu thuẫn bản chất, và đánh giá thấp heading cần tách riêng.", "Chưa bắt đầu"],
    ["O03", "Discover / Mở rộng", "Research xe/điện máy", "Chỉ chạy cho xe máy hoặc điện máy. Sản phẩm chưa ra mắt: gắn nhãn tin đồn/chưa xác nhận. Nguồn mâu thuẫn: gắn nhãn cần audit lại trước khi publish, không tự chọn số liệu. Đối chiếu chéo 2–3 nguồn. Xe: thông số, giá niêm yết/lăn bánh, thế hệ, phân phối. Điện thoại/điện máy: giá chính hãng và giá thị trường. Signature mặc định: xe máy = Signature 2; điện thoại/điện máy = Signature 3.", "Tra thông số hiện hành và giá từ nguồn phù hợp; đối chiếu 2–3 nguồn; kiểm tra 2 biến thể keyword cùng sản phẩm và bài tổng hợp cùng dòng model.", "hc-vehicle-specific", "Chặn sai thông số/giá do nhầm đời xe cùng tên model, gây mất uy tín khi khách đối chiếu.", "Chưa bắt đầu"],
    ["O04", "Define / Thu hẹp", "Dựng bảng SWOT", "Đủ 7 cột: # / URL / Strengths / Weaknesses / What We Learn / Opportunity / Example. Strengths/Weaknesses là thực tế của đối thủ. Không thêm hàng tóm tắt ưu tiên, không tự xếp hạng. URL lỗi thì bảng còn 4 hàng và ghi rõ lý do. Assessment Note chuyển thành bảng 5 hàng; What We Learn là insight khái quát; Opportunity là hành động cụ thể; Example là 1 trích dẫn/số liệu trực tiếp.", "Chuyển Assessment Note sau khi fetch thành bảng 5 hàng; nếu có đối thủ lỗi, loại khỏi bảng và ghi lý do; điền đủ 7 cột theo đúng định dạng.", "hc-build-swot", "Chặn định dạng so sánh thay đổi giữa các lần audit, làm khó đối chiếu theo thời gian.", "Chưa bắt đầu"],
    ["O05", "Define / Thu hẹp", "Chốt input", "Đủ 3 mục: từ khóa chính, chủ đề cụ thể, intent người đọc. Intent phải rõ là tìm hiểu thông tin hay đã sẵn sàng vay.", "Xác nhận lần lượt keyword, chủ đề, intent; chỉ hỏi ngắn nếu còn mơ hồ; không hỏi thêm nếu đã đủ.", "Không có skill", "Bước hỏi trực tiếp người dùng; không có logic lặp lại để đóng gói thành quy trình.", "Chưa bắt đầu"],
    ["O06", "Develop / Mở rộng", "Dựng bảng outline", "7 cột: # / Heading / Why / Evidence / Content Direction / Content Format / So với bài hiện tại. H2 số nguyên, H3 thập phân theo H2 cha, không La Mã; mỗi H2 ≥2 H3. Evidence dạng x/5 kèm tên đối thủ. Sau bảng tối đa 2 ghi chú. FAQ tối thiểu 5 H3. TL;DR là tên hàng mở đầu. Heading đầy đủ ngữ nghĩa; phần giữ nguyên ghi Đã có, giữ nguyên. Mâu thuẫn bản chất đưa lên dòng đầu, trích Evidence và ghi cần đội biên tập/pháp lý xác minh. Xuất thêm danh sách heading thuần trong code block.", "Ghép toàn bộ heading đề xuất thành bảng; viết Why cụ thể; gắn Evidence từ bảng đối thủ; bao phủ cả phần giữ nguyên; xử lý mâu thuẫn ở dòng đầu; xuất file heading thuần để copy Google Sheet.", "hc-build-outline / hc-article-structure", "Chặn outline sơ sài, buộc người viết nghiên cứu lại từ đầu, và ngăn tự ý chọn số liệu khi nguồn mâu thuẫn.", "Chưa bắt đầu"],
    ["O07", "Develop / Mở rộng", "Xếp từ khóa phụ", "Mỗi từ khóa đúng 1 nhóm: FAQ / Heading / Loại bỏ. Biến thể/đồng nghĩa của keyword chính luôn vào FAQ. Chỉ chạy khi có bảng keyword phụ/Google Suggest/PAA.", "Phân loại FAQ/Heading/Loại bỏ; nối nhóm Heading vào dòng outline tương ứng; nhóm FAQ vào mục FAQ; nhóm Loại bỏ đưa vào ghi chú kèm lý do. Audit outline cũ thì đối chiếu từng keyword mới, không giả định đã phủ hết.", "hc-classify-keywords", "Chặn nhồi keyword làm vỡ mạch văn và bỏ sót keyword vì tưởng outline cũ đã đủ.", "Chưa bắt đầu"],
    ["O08", "Deliver / Thu hẹp", "Chấm điểm trước khi giao", "5 gate: Voice / Cấu trúc / Nội dung / Coverage / Format bảng. Mỗi gate chỉ 1 điểm khi toàn bộ checklist con pass. Chỉ giao khi đạt 5/5.", "Chạy audit_quality.py --mode table và --mode outline; sửa sạch em-dash/từ dịch máy; chạy check_coverage.py với heading 5 đối thủ; rà thủ công 4 checklist; báo X/5 và gate mất điểm. Dưới 5/5: sửa trực tiếp và chấm lại từ đầu.", "hc-quality-gate", "Lưới an toàn cuối cùng, chặn giao outline còn lỗi rồi phải sửa lại sau khi đã dùng để viết bài.", "Chưa bắt đầu"],
    ["O09", "Deliver / Thu hẹp", "Chốt Disclaimer & Signature", "Đúng 1 trong 8 Signature theo bảng tra. Toàn bộ Signature in nghiêng. Không mix 2 Signature. Signature 4 Credit Card giữ nguyên tuyệt đối. Bài Đầu tư/Tích lũy dùng Signature 5 (VAS), không dùng Signature vay.", "Tra bảng chọn Signature theo chủ đề; copy nguyên văn, giữ URL; xác nhận loại Disclaimer bắt buộc theo bảng phân loại.", "hc-signatures", "Chặn tự diễn giải Signature/CTA và chèo kéo sản phẩm vay sai ngữ cảnh.", "Chưa bắt đầu"],
    ["O10", "Deliver / Thu hẹp", "Xuất file outline", "Bảng meta 4 hàng trước H1. Heading đen, H2 không kẻ ngang, link xanh #0000EE, nền th xám #e6e6e6. Signature/Disclaimer chỉ in nghiêng, không đóng khung. head có title = Meta title. CSS raw chuẩn, không tự đổi. Tự kiểm 7 mục trước khi giao.", "Xuất đúng vị trí và màu/style; copy nguyên khối CSS raw; kiểm CSS, bảng meta, heading/link/th, placeholder ảnh và 3 mục còn lại trong bộ 7 mục.", "hc-html-output-format", "Chặn mỗi lần xuất HTML dùng màu/style khác nhau, làm các bài không đồng nhất.", "Chưa bắt đầu"],
]

WRITE = [
    ["W01", "Discover / Mở rộng", "Research trước khi viết", "Đọc toàn văn bài cũ thật, không suy diễn từ mô tả trong outline. Nguồn/fetch lỗi: không bịa. Mở lại bài Home Credit nếu outline ghi Đã có, giữ nguyên. Tra lại lãi suất, hạn mức, tên thông tư và số liệu cần giữ/bổ sung.", "Đọc bài cũ và kiểm tra số liệu hiện tại; báo rõ và hỏi hướng xử lý nếu nguồn/fetch lỗi.", "Không có skill, tự web_search/fetch", "Tra cứu linh hoạt khác nhau theo từng bài, không có quy trình cố định để đóng gói.", "Chưa bắt đầu"],
    ["W02", "Define / Thu hẹp", "Chọn luồng & chốt H1", "H1 chứa keyword chính, tối đa 55–60 ký tự kể cả dấu cách, sentence case. Đủ keyword chính, toàn bộ keyword phụ trong outline, outline nguồn và intent chính. Chọn đúng 1 luồng: Product-to-Loan hoặc Knowledge-to-Service. Lưu keyword_chinh, tu_khoa_phu, luong, h1 vào article.json.", "Xác nhận đủ 3 input; thiếu thì dừng hỏi; soạn H1 theo luồng; chạy check_h1_keywords.py để kiểm độ dài, keyword và không phải Title Case.", "hc-write-flow-select", "Chặn viết lệch hướng do chọn sai luồng và H1 quá dài bị cắt trên SERP.", "Chưa bắt đầu"],
    ["W03", "Develop / Mở rộng", "Viết Sapo & Meta", "Meta Description 130–160 ký tự, chứa keyword chính, kết CTA thương hiệu. Product-to-Loan: Sapo đúng 3 câu, câu 1 in đậm keyword chính + phụ. Knowledge-to-Service: 70–150 chữ, keyword chính trong 100 chữ đầu. Không block Bài viết liên quan, không placeholder ảnh.", "Product: câu 1 giá & trả góp, câu 2 câu hỏi chuyển ý, câu 3 CTA. Knowledge: Warm Expert, nêu băn khoăn thật rồi dẫn vào bài và CTA thân thiện. Chạy check_write_rules.py sapo.", "hc-write-sapo", "Chặn Meta bị cắt và Sapo Knowledge-to-Service mở đầu lê thê, chung chung.", "Chưa bắt đầu"],
    ["W04", "Develop / Mở rộng", "Viết khối TL;DR", "Heading đúng TL;DR, không đánh số. Đúng 3 bullet ngắn. Có keyword chính; không trùng nguyên văn Sapo/mục 1. Đặt sau Sapo, trước mục 1. Có 1 câu định nghĩa/trả lời tự đủ nghĩa; format - **[Cụm câu hỏi ngắn]**: [câu trả lời]. Không ảnh/link nội bộ.", "Viết answer block tự đủ nghĩa rồi viết đúng 3 bullet theo format; kiểm vị trí và nội dung.", "hc-write-tldr", "Chặn bỏ lỡ người đọc lướt nhanh/AIO và lỗi tên khối không nhất quán.", "Chưa bắt đầu"],
    ["W05", "Develop / Mở rộng", "Viết thân bài", "Đoạn văn tối đa 3 dòng hiển thị; ngắt nhịp bắt buộc ở dòng thứ 6. Bullet đúng 1 dấu :, sau : là câu hoàn chỉnh có chủ-vị. Không ép 25 chữ/câu; cấm robot empathy và giọng bán hàng chèo kéo. Internal link anchor tự nhiên, URL xác minh qua script.", "Triển khai đúng H2 theo outline; bullet chung chung thì web_search số liệu thật; keyword hỏi khó lồng thì đưa FAQ; liệt kê ≥3 hạng mục thì bẻ bullet. Trước khi tách câu chạy 2 test liên kết; 1 test phải gộp thì gộp. Chạy check_write_rules.py body.", "hc-write-body", "Chặn sáo rỗng/thao túng cảm xúc và lỗi tách sai các cặp câu liên kết chặt để né cảnh báo.", "Chưa bắt đầu"],
    ["W06", "Develop / Mở rộng", "Viết sản phẩm & CTA", "Bảng thanh toán đúng 4 cột, không lồng cột hành vi. Lãi suất mô phỏng 1,5%–2,5%/tháng trên dư nợ; xe máy từ 0,59%/tháng. 6 tháng = tất toán sớm; khoảng 12 tháng = phổ thông; 24–36 tháng = dài hạn. Không gán sai phân khúc. 5 bước vay đại lý nếu dùng: giữ nguyên 100% nguyên văn. Đoạn USP 2–3 câu; 4–5 lợi ích.", "Đặt gần cuối thân bài, trước FAQ; tiêu đề đúng khung và hook trước; bài Đầu tư/Tích lũy chuyển sang Gói An tâm Tài chính. Tính lại bằng công cụ thật, phân biệt annuity/gốc chia đều/lãi phẳng. Chạy check_write_rules.py product-cta.", "hc-write-product-cta", "Chặn gợi ý sai sản phẩm/sai đối tượng và lãi suất mô phỏng sai do tính nhẩm.", "Chưa bắt đầu"],
    ["W07", "Deliver / Thu hẹp", "FAQ, kết bài, Signature", "Tối thiểu 5 FAQ, mỗi câu tự đủ nghĩa. Kết bài 2–3 câu dẫn tới anchor Cẩm nang Tài chính số. Disclaimer đúng loại, in nghiêng, trước Signature. Signature đúng 1 mẫu, copy nguyên văn, toàn bộ in nghiêng.", "FAQ heading: Câu hỏi thường gặp về [keyword rút gọn], đặt sau sản phẩm. Kết bài chứa keyword, không CTA liên hệ tư vấn thừa; 2–3 câu cuối nối tự nhiên tới homecredit.vn/blog. Chạy check_write_rules.py faq.", "hc-write-faq-closing", "Chặn FAQ viện dẫn ngược mục khác và đoạn dẫn Cẩm nang Tài chính cụt, rời mạch.", "Chưa bắt đầu"],
]

AUDIT = [
    ["A01", "Discover / Mở rộng", "Rà văn phong", "0 em-dash/en-dash toàn bài; 0 từ dịch máy trong danh sách cấm. Chỉ báo cáo, không tự sửa file. Rà 5 nhóm: Khen sáo rỗng / Robot-jargon / Giả tài chính / Filler / Marketing mơ hồ; báo câu chứa và đề xuất thay thế. Self-check tính từ cường điệu, dấu chấm bullet, bullet thiếu câu dẫn, chữ sau : không viết hoa.", "Chạy audit_quality.py --mode article; lập báo cáo lỗi và đề xuất thay thế. Word salad là câu kêu nhưng không có thông tin cụ thể.", "hc-audit-zero-flair", "Tạo vòng kiểm độc lập để bắt lỗi văn phong người viết khó tự nhận ra.", "Chưa bắt đầu"],
    ["A02", "Define / Thu hẹp", "Kiểm tra logic tài chính", "Dư nợ = Giá − Trả trước; lãi suất 1,5%–2,5%/tháng, xe máy từ 0,59%. Mọi ví dụ tính lại bằng công cụ thật. Kiểm phân khúc, thời hạn, bảng 4 cột và dấu ~. Nếu số chính thức mâu thuẫn công thức: báo cả 2, không tự chọn.", "Tính lại thủ công dư nợ/lãi suất; đối chiếu vùng hợp lý; kiểm 12–24 tháng không gọi là tất toán sớm.", "hc-audit-financial-logic", "Chặn sai số liệu tài chính, rủi ro uy tín/pháp lý và lãi suất mô phỏng vô lý.", "Chưa bắt đầu"],
    ["A03", "Develop / Mở rộng", "Kiểm tra cấu trúc & định dạng", "H1 ≤55–60 ký tự; Meta 130–160 ký tự; đoạn ≤3 dòng; không 3 đoạn xuôi liên tiếp thiếu bullet/bảng/ảnh; câu đủ chủ-vị. Heading tối thiểu 2–3 H2, đánh số đúng, sentence case. Bullet/bảng đúng format; không placeholder ảnh; FAQ/kết/disclaimer đúng vị trí và loại.", "Đối chiếu Title/Meta/Sapo với luồng; đọc lướt câu/đoạn; kiểm bullet, bảng, ảnh và các khối bắt buộc.", "hc-audit-structure-format", "Chặn thiếu thành phần bắt buộc trước khi bài được xem là hoàn chỉnh.", "Chưa bắt đầu"],
    ["A04", "Develop / Mở rộng", "Đếm độ dài & mật độ từ khóa", "Knowledge-to-Service: 1.500–5.000 từ. Keyword chính tối đa 1%/bài. Mỗi keyword phụ xuất hiện ≥1 lần.", "Tạo bản copy tạm bỏ Signature/Disclaimer, không sửa file gốc; chạy count_keywords.py đúng luồng; đối chiếu 4 chỉ số.", "hc-audit-seo-metrics", "Chặn bài quá dài loãng trọng tâm, quá ngắn thiếu chiều sâu hoặc keyword nhồi/thiếu.", "Chưa bắt đầu"],
    ["A05", "Deliver / Thu hẹp", "Đếm & xác minh internal link", "Tối thiểu 5 internal link. Mỗi URL đúng 1 lần. Anchor tự nhiên, không tại đây. Không dồn cụm 2–4 link liền nhau. URL menu_only_not_in_sitemap: báo xác minh thủ công. homecredit.vn/blog là ngoại lệ, không tính lỗi.", "Chạy search_internal_links.py --count-in-file; kiểm thủ công external, anchor và cụm link.", "hc-audit-internal-links", "Chặn dẫn tới URL không tồn tại/đã đổi, gây trải nghiệm xấu và mất uy tín.", "Chưa bắt đầu"],
    ["A06", "Deliver / Thu hẹp", "Gate cuối: Disclaimer & Signature", "Signature in nghiêng, URL giữ nguyên 100%. Hotline đúng: 1900 633 633 hoặc 1900 633 999. Cả 5 audit trước phải pass. Disclaimer có mặt, đúng loại, đúng vị trí trước Signature. Signature đúng 1/8, khớp chủ đề; bài Đầu tư/Tích lũy dùng Signature 5; Signature 4 Credit Card giữ nguyên tuyệt đối.", "Kiểm lại Disclaimer/Signature; xác nhận pass của 5 skill audit trước, không suy luận đã sửa xong; nếu chưa xác nhận thì chạy lại.", "hc-audit-signature-disclaimer", "Gate pháp lý cuối cùng, chặn bài thiếu Disclaimer hoặc dùng sai nguyên văn Signature đã duyệt.", "Chưa bắt đầu"],
    ["A07", "Deliver / Thu hẹp", "Xuất file bài viết", "Đúng thứ tự H1 → Sapo → TL;DR → thân bài → sản phẩm/CTA → FAQ → Kết bài → Disclaimer → Signature. Bảng meta 4 hàng trước H1. Xuất .html sau khi cả 6 gate audit đạt. Dùng CSS raw cố định và tự kiểm 7 mục.", "Xuất sau khi 6 gate sạch; kiểm thứ tự, CSS raw, meta và 7 mục trước bàn giao.", "hc-html-output-format", "Chặn mỗi bài ra một màu/style khác nhau do chọn ngẫu hứng.", "Chưa bắt đầu"],
]

HANDOVER = [
    ["Ngày", "Mã bước", "Đầu việc / bằng chứng", "Link hoặc file bằng chứng", "Người thực hiện", "Người kiểm tra", "Kết quả", "Ghi chú"],
    ["", "", "", "", "", "", "Chưa kiểm", ""],
    ["", "", "", "", "", "", "Chưa kiểm", ""],
    ["", "", "", "", "", "", "Chưa kiểm", ""],
    ["", "", "", "", "", "", "Chưa kiểm", ""],
    ["", "", "", "", "", "", "Chưa kiểm", ""],
]

def col_letter(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s

def cell_ref(row, col):
    return f"{col_letter(col)}{row}"

def x(s):
    return escape(str(s)).replace("\n", "&#10;")

def split_items(text):
    parts = re.split(r"(?<=[.!?])\s+|;\s+", text.strip())
    return [p.strip(" -") for p in parts if p.strip(" -")]

def expand_checklist(rows):
    expanded = []
    step_no = 1
    for item in rows:
        task_id, phase, task, requirements, how_to, skill, purpose, _status = item
        for req in split_items(requirements):
            expanded.append(["☐", step_no, phase, task, skill, req, how_to, "", "Chưa bắt đầu", "", purpose])
            step_no += 1
        for action in split_items(how_to):
            expanded.append(["☐", step_no, phase, task, skill, "Thực hiện thao tác này", action, "", "Chưa bắt đầu", "", purpose])
            step_no += 1
    return expanded

def sheet_xml(title, rows, widths, tab_color, headers=None):
    headers = headers or ["ID", "Giai đoạn", "Đầu việc lớn", "Yêu cầu cần đạt", "Cách làm", "Skill áp dụng", "Skill dùng để làm gì", "Trạng thái"]
    all_rows = [headers] + rows
    xml = [f'<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetPr><tabColor rgb="{tab_color}"/></sheetPr>']
    xml.append('<sheetViews><sheetView workbookViewId="0" showGridLines="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>')
    xml.append(f'<cols>{"".join(f"<col min=\"{i+1}\" max=\"{i+1}\" width=\"{w}\" customWidth=\"1\"/>" for i,w in enumerate(widths))}</cols>')
    xml.append('<sheetData>')
    for r, row in enumerate(all_rows, 1):
        ht = 28 if r == 1 else (72 if len(headers) > 8 else 108)
        xml.append(f'<row r="{r}" ht="{ht}" customHeight="1">')
        for c, val in enumerate(row, 1):
            style = 1 if r == 1 else (2 if c in (1,2,9) and len(headers) > 8 else (2 if c in (1,8) else 3))
            ref = cell_ref(r,c)
            xml.append(f'<c r="{ref}" s="{style}" t="inlineStr"><is><t xml:space="preserve">{x(val)}</t></is></c>')
        xml.append('</row>')
    xml.append('</sheetData>')
    xml.append(f'<autoFilter ref="A1:{col_letter(len(headers))}{len(all_rows)}"/>')
    xml.append('</worksheet>')
    return ''.join(xml)

def simple_sheet(name, rows, widths, tab_color):
    return sheet_xml(name, rows, widths, tab_color)

def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sheets = [
        ("00_Tong_quan", [["Home Credit Vietnam — checklist quy trình nội dung"], ["Nguồn", "Nội dung do người dùng cung cấp, trích từ skill thật", "Ngày", "2026-08-21"]], [22, 30, 28, 28, 22, 28, 34, 18], "1F4E78"),
        ("01_Quy_tac_chung", COMMON, [16,20,38,55,25,45,18], "7F6000"),
        ("02_Checklist_Outline", expand_checklist(OUTLINE), [7,8,22,28,28,58,62,28,18,30,52], "4472C4"),
        ("03_Checklist_Viet_bai", expand_checklist(WRITE), [7,8,22,30,28,58,62,28,18,30,52], "70AD47"),
        ("04_Checklist_Audit", expand_checklist(AUDIT), [7,8,22,30,28,58,62,28,18,30,52], "C55A11"),
        ("05_Danh_muc_trang_thai", [["Trạng thái", "Ý nghĩa"], ["Chưa bắt đầu", "Chưa thực hiện"], ["Đang làm", "Đang triển khai"], ["Chờ xác nhận", "Cần người dùng/biên tập/pháp lý quyết định"], ["Đạt", "Đã pass tiêu chuẩn"], ["Không đạt", "Cần quay lại skill tương ứng để sửa và kiểm lại"]], [25,70,25,25,25,25,25,18], "A5A5A5"),
        ("06_Nhat_ky_ban_giao", HANDOVER, [14,14,34,42,22,22,18,34], "8064A2"),
    ]
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>''' + ''.join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1,len(sheets)+1)) + '</Types>'
    rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>'
    wb = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>' + ''.join(f'<sheet name="{x(n)}" sheetId="{i}" r:id="rId{i}"/>' for i,(n,*_) in enumerate(sheets,1)) + '</sheets></workbook>'
    wb_rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + ''.join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1,len(sheets)+1)) + '<Relationship Id="rId99" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'
    styles = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="2"><font><sz val="10"/><name val="Aptos"/></font><font><b/><sz val="10"/><name val="Aptos"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="solid"><fgColor rgb="1F4E78"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="D9EAF7"/></patternFill></fill></fills><borders count="2"><border/><border><bottom style="thin"><color rgb="B7C9D6"/></bottom></border></borders><cellXfs count="4"><xf fontId="0" fillId="0" borderId="0"/><xf fontId="1" fillId="1" borderId="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf><xf fontId="1" fillId="2" borderId="1" applyAlignment="1"><alignment horizontal="center" vertical="top" wrapText="1"/></xf><xf fontId="0" fillId="0" borderId="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf></cellXfs></styleSheet>'''
    with ZipFile(OUT, 'w', ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types)
        z.writestr('_rels/.rels', rels)
        z.writestr('xl/workbook.xml', wb)
        z.writestr('xl/_rels/workbook.xml.rels', wb_rels)
        z.writestr('xl/styles.xml', styles)
        step_headers = ["☐", "Step", "Giai đoạn", "Đầu việc lớn", "Skill áp dụng", "Yêu cầu cần hoàn thành", "Cách thực hiện", "Kết quả / Evidence", "Trạng thái", "Ghi chú", "Skill dùng để làm gì"]
        for i,(name, rows, widths, color) in enumerate(sheets,1):
            z.writestr(f'xl/worksheets/sheet{i}.xml', sheet_xml(name, rows, widths, color, step_headers if i in (3,4,5) else None))
    print(OUT)

if __name__ == '__main__':
    build()
