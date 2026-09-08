import zipfile, shutil, os, re
import xml.etree.ElementTree as ET

src = 'BaoGia_ChiTiet_DichVuSEO_SEOGrowth_2026.xlsx'
outdir = 'outputs'
os.makedirs(outdir, exist_ok=True)
dst = os.path.join(outdir, 'BaoGia_ChiTiet_DichVuSEO_SEOGrowth_2026_updated.xlsx')

NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
ET.register_namespace('', NS)
ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
ET.register_namespace('mc', 'http://schemas.openxmlformats.org/markup-compatibility/2006')
ET.register_namespace('x14ac', 'http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac')
ET.register_namespace('xr', 'http://schemas.microsoft.com/office/spreadsheetml/2014/revision')
ET.register_namespace('xr2', 'http://schemas.microsoft.com/office/spreadsheetml/2015/revision2')
ET.register_namespace('xr3', 'http://schemas.microsoft.com/office/spreadsheetml/2016/revision3')

# Existing shared strings are intentionally updated in place so every cell's
# style, merge, formula and shared-string reference remains intact.
updates = {
134: '• Phân tích truy vấn hội thoại và ý định tìm kiếm của người dùng;\n• Tối ưu 6 bài AI-enhanced theo cấu trúc câu hỏi–trả lời, thông tin có nguồn và tín hiệu E-E-A-T;\n• Rà soát crawl/index, tiêu đề, heading, liên kết nội bộ và khả năng đọc trên mobile;\n• Bàn giao brief, bản thảo và báo cáo GSC/GA4 theo tháng. Không cam kết xuất hiện trong câu trả lời AI; kết quả phụ thuộc website và thị trường.',
136: '• Xây dựng Semantic SEO và Topic Cluster theo toàn bộ phễu tìm kiếm;\n• Tối ưu nội dung cho truy vấn hội thoại/voice search, đồng thời kiểm tra sitemap, robots, canonical, redirect và Core Web Vitals;\n• 12 bài AI-enhanced/tháng, 30 liên kết biên tập liên quan và dashboard đo lường;\n• Structured data chỉ triển khai khi phù hợp và có dữ liệu hiển thị thực tế; nghiệm thu bằng log đầu việc, GSC/GA4 và khuyến nghị ưu tiên.',
139: '• Thiết lập/xác minh và tối ưu Google Business Profile cho 1 địa điểm: danh mục, dịch vụ, mô tả, ảnh và thông tin liên hệ;\n• Đồng bộ NAP trên 20 danh bạ phù hợp, xử lý trùng lặp khi có thể và xây dựng 10 liên kết địa phương có liên quan;\n• Viết 4 nội dung địa phương/tháng, đề xuất lịch cập nhật ảnh/bài đăng và theo dõi hiển thị Maps;\n• Khách hàng cung cấp quyền quản trị, thông tin pháp lý, khu vực phục vụ và quy trình duyệt phản hồi.',
141: '• Quản trị tối đa 5 địa điểm: cấu trúc trang chi nhánh, GBP, NAP và dữ liệu LocalBusiness theo từng địa điểm;\n• Đồng bộ 50 citation/tháng, rà soát trùng lặp và cơ hội liên kết địa phương;\n• Nội dung địa phương và bài PR được lập brief, duyệt trước khi xuất bản;\n• Báo cáo theo địa điểm gồm hiển thị, hành động, cuộc gọi và hướng dẫn phối hợp review. Không thay thế quy trình vận hành/giải quyết khiếu nại của doanh nghiệp.',
143: '• Kiểm kê và phân nhóm danh mục/sản phẩm; ưu tiên trang có nhu cầu và khả năng chuyển đổi;\n• Tối ưu tối đa 200 trang sản phẩm/tháng: title, description, dữ liệu thuộc tính, liên kết nội bộ, ảnh và Product structured data khi thông tin hiển thị đầy đủ;\n• Viết 8 bài blog review/tháng, xử lý trang lọc/tham số và đề xuất canonical/indexing;\n• Bàn giao danh sách URL đã xử lý, checklist QA và báo cáo GSC/GA4. Khách hàng cung cấp feed giá, tồn kho, rating và quyền CMS.',
144: '• Xây dựng kiến trúc SEO cho website/sàn trên 1.000 sản phẩm, gồm danh mục, faceted navigation và template theo loại trang;\n• Không giới hạn số trang trong phạm vi đã thống nhất; triển khai hreflang khi có thị trường/ngôn ngữ thực tế;\n• Tập trung crawl budget, sitemap phân đoạn, canonical, redirect, Core Web Vitals và structured data có thể xác minh;\n• 50+ liên kết biên tập liên quan, SEO Manager phụ trách và dashboard theo dõi. Kết quả phụ thuộc chất lượng feed, tồn kho, cạnh tranh và tốc độ phê duyệt.',
156: '• Bài viết mới, có nghiên cứu và đối chiếu nguồn; độ dài 800–1.500 từ theo brief;\n• Cấu trúc Heading rõ, đáp ứng đúng ý định tìm kiếm, title/meta đề xuất, liên kết nội bộ và alt ảnh;\n• Ưu tiên nội dung hữu ích cho người đọc, thể hiện kinh nghiệm/chuyên môn và tránh nhồi từ khóa;\n• Bàn giao file bản thảo, brief, checklist QA và vòng phản hồi theo quy trình duyệt.',
161: '• Bài Pillar Content 2.000–3.000 từ, bao phủ chủ đề theo cụm và liên kết đến các bài hỗ trợ;\n• Nghiên cứu intent, đối thủ và content gap; bổ sung ví dụ, dữ liệu/nguồn tham khảo và CTA phù hợp;\n• Tối ưu khả năng đọc, mobile, heading, ảnh/alt và internal link;\n• Bàn giao outline, bản thảo, nguồn tham khảo và checklist nghiệm thu; khách hàng duyệt thông tin chuyên môn trước xuất bản.',
165: '• Xây dựng nội dung theo hành trình khách hàng và mục tiêu chuyển đổi đã thống nhất;\n• Tối ưu title/meta, H1–H3, thông điệp giá trị, bằng chứng tin cậy, FAQ và CTA;\n• Bố cục ưu tiên mobile, tốc độ đọc và liên kết đến trang dịch vụ liên quan;\n• Bàn giao wireframe nội dung/bản thảo, đề xuất tracking CTA và vòng duyệt. Không bao gồm thiết kế UI hoặc cam kết tỷ lệ chuyển đổi cố định.',
170: '• Viết mô tả 150–300 từ dựa trên thuộc tính và lợi ích đã xác minh;\n• Tối ưu tiêu đề, meta description, điểm khác biệt, thông tin sử dụng và liên kết nội bộ;\n• Tránh nội dung trùng lặp giữa biến thể; kiểm tra khả năng đọc trên mobile;\n• Khách hàng cung cấp thông số, giá, tồn kho, chính sách và duyệt trước khi đăng.',
176: '• Rà soát intent, title/meta, H1–H6, nội dung chính, ảnh/alt và liên kết nội bộ;\n• Kiểm tra canonical, indexability, redirect, khả năng hiển thị mobile và các lỗi template ảnh hưởng crawl;\n• Bàn giao checklist URL, đề xuất ưu tiên và nội dung cần khách hàng/CMS triển khai;\n• Không dùng mật độ từ khóa cứng nhắc; ưu tiên nội dung hữu ích và trải nghiệm người dùng.',
179: '• Xác định loại schema phù hợp với nội dung thực tế của từng URL (Article, Product, FAQ, Breadcrumb, LocalBusiness);\n• Triển khai JSON-LD với dữ liệu hiển thị trên trang, kiểm tra lỗi bằng Rich Results Test và theo dõi báo cáo sau phát hành;\n• Không tạo markup cho thông tin ẩn/không chính xác; bàn giao danh sách URL, cảnh báo và hướng xử lý.',
184: '• Đo PageSpeed/Core Web Vitals trên các mẫu trang đại diện;\n• Nén và định dạng ảnh, lazy-load, cache, giảm CSS/JS không cần thiết theo quyền truy cập;\n• Ưu tiên INP, LCP, CLS và kiểm tra lại trên mobile/desktop sau thay đổi;\n• Bàn giao before/after, danh sách thay đổi và khuyến nghị phối hợp dev. Điểm số phụ thuộc hosting, mã nguồn và bên thứ ba.',
188: '• Tạo/xác minh GA4 và Google Search Console; khai báo sitemap.xml và kiểm tra URL Inspection;\n• Cấu hình đo lường cơ bản cho organic traffic, landing page, sự kiện/CTA đã thống nhất;\n• Kiểm tra quyền truy cập, UTM và tính nhất quán dữ liệu;\n• Bàn giao checklist cấu hình, hướng dẫn đọc báo cáo và danh sách dữ liệu còn phụ thuộc CMS/dev.',
192: '• Ưu tiên liên kết biên tập có liên quan, đa dạng nguồn và anchor tự nhiên;\n• Kiểm tra bối cảnh trang đặt link, khả năng truy cập và rủi ro spam trước khi đề xuất;\n• Bàn giao danh sách URL, loại liên kết, anchor, trạng thái kiểm tra và lịch rà soát;\n• Không mua bán liên kết để thao túng thứ hạng, không cam kết tăng hạng chỉ nhờ số lượng link.',
197: '• Tiếp cận guest post/liên kết biên tập từ website cùng chủ đề, ưu tiên giá trị cho người đọc;\n• Rà soát chất lượng trang, nội dung, thuộc tính liên kết và khả năng duy trì;\n• Bàn giao danh sách placement, bài viết/brief, anchor và trạng thái index;\n• Không sử dụng mạng blog rác, liên kết hàng loạt hoặc kỹ thuật thao túng thứ hạng.',
201: '• Soạn bài PR theo thông tin doanh nghiệp đã xác minh, có giá trị tin tức và link phù hợp ngữ cảnh;\n• Gửi khách hàng duyệt nội dung/đầu báo trước khi đăng;\n• Bàn giao URL bài đăng, ngày đăng, thuộc tính link và bằng chứng nghiệm thu;\n• Không bảo đảm thứ hạng, traffic hay thời gian tồn tại nếu phụ thuộc chính sách biên tập của bên thứ ba.',
206: '• Phân phối nội dung trên các kênh xã hội phù hợp với thương hiệu và cộng đồng mục tiêu;\n• Chuẩn hóa tiêu đề, ảnh đại diện, UTM và lịch đăng; theo dõi referral/engagement trong GA4 khi có dữ liệu;\n• Bàn giao lịch đăng, URL và báo cáo tương tác;\n• Social sharing không được xem là tín hiệu bảo đảm tăng hạng hoặc thay thế liên kết biên tập chất lượng.',
212: '• Thu thập 50–200 từ khóa theo nhóm chủ đề, intent (thông tin/điều tra/giao dịch/địa phương) và giai đoạn phễu;\n• Phân tích volume, cạnh tranh, SERP, biến thể ngữ nghĩa và cơ hội chuyển đổi;\n• Bàn giao file nghiên cứu, keyword map, ưu tiên URL và giả định cần khách hàng xác nhận;\n• Chỉ số công cụ là tham khảo; ưu tiên dữ liệu GSC và mục tiêu kinh doanh thực tế.',
216: '• Phân tích 3 đối thủ về cấu trúc website, trang tạo traffic, intent, content gap và tín hiệu liên kết;\n• So sánh chất lượng nội dung, internal link, SERP feature và trải nghiệm mobile;\n• Bàn giao báo cáo, bảng cơ hội ưu tiên và khuyến nghị thử nghiệm;\n• Không sao chép nội dung/chiến thuật vi phạm chính sách hoặc suy đoán dữ liệu không thể xác minh.',
219: '• Xây dựng Topic Cluster, keyword map và lịch đăng 3 tháng theo nguồn lực/ưu tiên kinh doanh;\n• Viết outline mẫu gồm intent, đối tượng đọc, angle, heading, nguồn, internal link và CTA;\n• Bàn giao content calendar, 10 outline mẫu và tiêu chí nghiệm thu;\n• Doanh nghiệp cung cấp SME, dữ liệu sản phẩm và phê duyệt để bảo đảm tính chính xác.',
223: '• Kiểm tra crawl/index: robots.txt, sitemap, canonical, redirect, status code và URL Inspection;\n• Rà soát meta/heading trùng, liên kết gãy, mobile, Core Web Vitals và các vấn đề nội dung nổi bật;\n• Bàn giao báo cáo PDF, mức độ ưu tiên, tác động và hướng xử lý;\n• Phạm vi cơ bản phù hợp website dưới 100 trang; cần quyền GSC/CMS để xác minh.',
226: '• Audit technical, content, on-page, internal link, structured data, mobile/Core Web Vitals và hồ sơ liên kết;\n• Kiểm tra theo mẫu URL và phân đoạn website; đối chiếu dữ liệu GSC/GA4 khi được cấp quyền;\n• Bàn giao roadmap theo tác động–nỗ lực, danh sách URL và tiêu chí nghiệm thu;\n• Phạm vi/độ sâu được chốt theo quy mô, CMS và quyền truy cập thực tế.',
229: '• Rà soát biến động theo thời gian, GSC, cập nhật thuật toán, manual action và các thay đổi website;\n• Phân loại nguyên nhân có thể xảy ra: technical, content, migration hoặc liên kết không tự nhiên;\n• Bàn giao báo cáo chẩn đoán, kế hoạch khắc phục và tiêu chí theo dõi;\n• Chỉ đề xuất disavow khi có căn cứ và sau khi khách hàng phê duyệt; không bảo đảm phục hồi trong thời hạn cố định.',
233: '• Tạo hoặc tối ưu Google Business Profile: tên, danh mục, dịch vụ, mô tả, ảnh, giờ mở cửa và khu vực phục vụ;\n• Kiểm tra xác minh, thông tin trùng lặp và đề xuất lịch cập nhật;\n• Bàn giao checklist profile, ảnh/metadata đề xuất và hướng dẫn quản trị;\n• Khách hàng chịu trách nhiệm xác minh quyền sở hữu và phản hồi đánh giá.',
237: '• Đăng và đồng bộ tên, địa chỉ, số điện thoại, website trên 30 danh bạ phù hợp;\n• Kiểm tra tính nhất quán NAP, trùng lặp và trạng thái hiển thị;\n• Bàn giao danh sách citation, thông tin đã đăng và các mục cần xác minh;\n• Không tạo danh bạ rác hoặc thông tin không có căn cứ.',
248: '• Tiếp nhận mục tiêu, sản phẩm, thị trường, lịch sử SEO và quyền truy cập;\n• Khảo sát crawl/index, sitemap, robots, canonical, redirect, mobile, Core Web Vitals và 3 đối thủ;\n• Bàn giao bản ghi nhận hiện trạng, rủi ro và câu hỏi cần xác minh trong 2 ngày làm việc;\n• Khách hàng cung cấp website, GSC/GA4 và thông tin ưu tiên kinh doanh.',
250: '• Thống nhất keyword map, URL ưu tiên, phạm vi kỹ thuật/nội dung, KPI đo lường và lịch báo cáo;\n• Chốt ngân sách, đầu ra hàng tháng, người duyệt và mốc nghiệm thu trước khi ký;\n• Bàn giao roadmap, lịch triển khai và danh sách phụ thuộc;\n• Khách hàng xác nhận phạm vi, cung cấp thông tin pháp lý/sản phẩm và thực hiện thanh toán theo thỏa thuận hiện có.',
252: '• Triển khai theo roadmap: technical SEO (crawl/index, sitemap, robots, canonical, redirect, mobile/Core Web Vitals), on-page, content brief, internal link và structured data khi phù hợp;\n• Thực hiện nội dung/link theo phạm vi được duyệt, có checklist QA và lưu vết thay đổi;\n• Bàn giao danh sách URL, file nội dung, ticket kỹ thuật và bằng chứng nghiệm thu;\n• Khách hàng cấp quyền CMS/dev, SME, dữ liệu sản phẩm và phản hồi đúng SLA để không trễ tiến độ.',
254: '• Cuối kỳ gửi báo cáo các đầu việc đã hoàn thành, URL bàn giao, lỗi còn lại, thứ hạng, impressions/clicks, organic traffic và chuyển đổi khi tracking đủ dữ liệu;\n• Họp tổng kết để giải thích biến động, KPI và ưu tiên chu kỳ tiếp theo;\n• Nghiệm thu theo đầu ra/phạm vi đã duyệt, không theo cam kết vị trí cố định;\n• Kết quả phụ thuộc hiện trạng, cạnh tranh, thị trường, tốc độ triển khai và chất lượng phối hợp.',
257: '• Giá trị tính bằng VND, chưa bao gồm 10% VAT; thanh toán chuyển khoản trước ngày mùng 5 theo thỏa thuận;\n• Hóa đơn/chứng từ và thông tin thanh toán thực hiện theo hợp đồng;\n• Mọi thay đổi phạm vi, quyền truy cập hoặc lịch duyệt được ghi nhận bằng email/ticket;\n• Giữ nguyên các mức giá và điều kiện thương mại trong báo giá này.',
259: '• Hợp đồng tối thiểu 3 tháng để đủ thời gian triển khai, thu thập dữ liệu và đánh giá xu hướng;\n• Sau giai đoạn tối thiểu, gia hạn theo tháng theo thỏa thuận hiện có;\n• Không xem thời hạn là cam kết đạt một vị trí cố định; mục tiêu được đánh giá bằng KPI và đầu ra đã thống nhất;\n• Có thể rà soát lại roadmap khi website, thị trường hoặc ưu tiên kinh doanh thay đổi.',
261: '• Combo nhiều dịch vụ lẻ được giảm 5%–15% theo báo giá xác nhận;\n• Phạm vi bàn giao, thời hạn và điều kiện giảm giá ghi rõ trên báo giá/đơn đặt hàng;\n• Dịch vụ chỉ bắt đầu sau khi khách hàng duyệt brief và hoàn tất thanh toán theo thỏa thuận;\n• Không gộp hạng mục ngoài phạm vi nếu chưa có xác nhận bằng văn bản.',
263: '• Giảm 10% cho dịch vụ lẻ lặp lại hàng tháng từ 3 tháng theo chính sách hiện có;\n• Mỗi chu kỳ bàn giao danh sách đầu việc, URL/file và báo cáo ngắn;\n• Khách hàng duyệt kế hoạch và cung cấp dữ liệu/quyền truy cập đúng hạn;\n• Khối lượng có thể cần điều chỉnh nếu website, số lượng URL hoặc yêu cầu thay đổi.',
265: '• Bắt đầu trong 3–5 ngày làm việc sau khi nhận tạm ứng/thanh toán chu kỳ đầu và đủ quyền truy cập;\n• Ngày triển khai thực tế phụ thuộc thời gian nhận dữ liệu, phê duyệt, CMS/dev và bên thứ ba;\n• Agency thông báo blocker và điều chỉnh lịch khi có phụ thuộc từ khách hàng;\n• Mốc giao hàng được theo dõi trong roadmap/ticket, không mặc nhiên thay đổi điều khoản thương mại.',
266: 'Thông tin liên hệ tư vấn trực tiếp: contact@seogrowth.vn | Hotline: 0909 000 000 | Địa chỉ văn phòng: TP. Hồ Chí Minh\nTham chiếu phương pháp: https://developers.google.com/search/docs/fundamentals/seo-starter-guide | https://developers.google.com/search/docs/crawling-indexing/overview | https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data',
}

def set_si_text(si, text):
    # Preserve the shared-string run/font structure if present, replacing only text nodes.
    ts = si.findall('.//{%s}t' % NS)
    if not ts:
        t = ET.SubElement(si, '{%s}t' % NS)
        t.text = text
        return
    ts[0].text = text
    for extra in ts[1:]:
        parent = None
        # ElementTree has no parent pointer; remove extras by rebuilding the first run only.
    # Long strings in this workbook are plain <t>; normalize any accidental extra runs.
    if len(ts) > 1:
        for child in list(si):
            if child.tag != '{%s}t' % NS:
                for t in list(child):
                    if t.tag == '{%s}t' % NS:
                        child.remove(t)
                # keep formatting nodes but ensure first run has the full value
        ts = si.findall('.//{%s}t' % NS)
        if ts:
            ts[0].text = text

with zipfile.ZipFile(src, 'r') as zin:
    files = {name: zin.read(name) for name in zin.namelist()}

root = ET.fromstring(files['xl/sharedStrings.xml'])
sis = root.findall('{%s}si' % NS)
for idx, text in updates.items():
    if idx >= len(sis):
        raise RuntimeError(f'missing shared string {idx}')
    set_si_text(sis[idx], text)
files['xl/sharedStrings.xml'] = ET.tostring(root, encoding='utf-8', xml_declaration=True)

# Expand only rows whose descriptions were materially lengthened. Existing styles,
# merges, column widths and wrap settings remain untouched.
row_heights = {
    'xl/worksheets/sheet3.xml': {6: 105, 7: 120, 9: 105, 10: 120, 12: 120, 13: 135},
    'xl/worksheets/sheet4.xml': {6: 90, 7: 90, 8: 90, 9: 90, 10: 90, 11: 90, 12: 105, 13: 90, 14: 90, 15: 90, 16: 105, 17: 90, 18: 105, 19: 105, 20: 105, 21: 105, 22: 105, 23: 105, 24: 105, 25: 105},
    'xl/worksheets/sheet5.xml': {5: 105, 6: 120, 7: 120, 8: 105, 10: 120, 11: 120, 12: 120, 13: 120, 14: 120, 16: 135},
}
for fn, heights in row_heights.items():
    root = ET.fromstring(files[fn])
    for row in root.findall('.//{%s}row' % NS):
        r = int(row.attrib.get('r', '0'))
        if r in heights:
            row.set('ht', str(heights[r]))
            row.set('customHeight', '1')
    serialized = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    # ElementTree drops unused namespace declarations. Excel's worksheet root
    # retains mc:Ignorable references to these prefixes, so restore them.
    if b'mc:Ignorable' in serialized:
        marker = b' xmlns="' + NS.encode() + b'"'
        decls = (
            b' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
            b' xmlns:xr2="http://schemas.microsoft.com/office/spreadsheetml/2015/revision2"'
            b' xmlns:xr3="http://schemas.microsoft.com/office/spreadsheetml/2016/revision3"'
        )
        if b'xmlns:r=' not in serialized:
            serialized = serialized.replace(marker, marker + decls.split(b' xmlns:xr2=')[0], 1)
        if b'xmlns:xr2=' not in serialized:
            serialized = serialized.replace(b' xmlns:x14ac=', b' xmlns:xr2="http://schemas.microsoft.com/office/spreadsheetml/2015/revision2" xmlns:xr3="http://schemas.microsoft.com/office/spreadsheetml/2016/revision3" xmlns:x14ac=', 1)
    files[fn] = serialized

with zipfile.ZipFile(dst, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
    for name, data in files.items():
        zout.writestr(name, data)
print(dst)
