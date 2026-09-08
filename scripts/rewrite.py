import re

file_path = r'C:\Users\MSI\Documents\Antigravity-SEO\Keywords\Trung Nguyên TNT\sua-may-tron-nhua\article.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract sections
# We will split by '## ' and recreate
parts = re.split(r'\n## ', '\n' + content)

header_and_intro = parts[0].strip()
sections = {}
for p in parts[1:]:
    title_line = p.split('\n')[0]
    num_match = re.match(r'^(\d+)\.', title_line)
    if num_match:
        num = num_match.group(1)
        sections[num] = p

# Sections map:
# 1: Tại sao sửa chữa
# 2: Các sự cố
# 3: Phân tích kỹ thuật
# 4: Quy trình
# 5: Các nguyên tắc an toàn
# 6: Tại sao chọn
# 7: Bảng báo giá
# 8: Câu hỏi thường gặp
# 9: Tổng kết

# Modify sections to be service-oriented

s2 = sections['2'].replace('2. Các sự cố thường gặp ở máy khuấy, máy trộn nhựa', '1. Dịch vụ chuyên trị các sự cố máy khuấy, máy trộn nhựa')
s3 = sections['3'].replace('3. Phân tích kỹ thuật (TDS) và xử lý cốt lõi từng dòng máy trộn', '2. Các hạng mục sửa chữa cốt lõi theo từng dòng máy trộn')
s6 = sections['6'].replace('6. Tại sao chọn dịch vụ sửa chữa tại công ty TNHH Trung Nguyên TNT?', '3. Tại sao chọn dịch vụ sửa chữa tại Trung Nguyên TNT?')
s7 = sections['7'].replace('7. Bảng báo giá sửa chữa và bảo hành máy trộn nhựa', '4. Bảng báo giá dịch vụ sửa chữa và bảo hành máy trộn nhựa')

# Section 4 (Quy trình) needs specific H3s added/modified
s4 = sections['4'].replace('4. Quy trình sửa chữa minh bạch của công ty Trung Nguyên TNT', '5. Quy trình dịch vụ sửa chữa minh bạch của Trung Nguyên TNT')
s4 = s4.replace('### 4.1 Tiếp nhận yêu cầu, chẩn đoán sơ bộ', '### 5.1 Điều kiện tiếp nhận dịch vụ (Conditions)\n\nChúng tôi tiếp nhận mọi yêu cầu sửa máy trộn nhựa công nghiệp (từ 50kg trở lên). Khách hàng chỉ cần cung cấp video lỗi hiện trạng, báo mã lỗi tủ điện qua Zalo. Chẩn đoán sơ bộ sẽ diễn ra trong vòng 30 phút mà không ràng buộc chi phí.\n\n### 5.2 Các bước sửa chữa thực tế (Procedures)')
s4 = s4.replace('### 4.2 Khảo sát trực tiếp, lập Technical Data Sheet phương án', '**Bước 1: Khảo sát tận nơi và lập Technical Data Sheet:**')
s4 = s4.replace('### 4.3 Quá trình sửa chữa, thay thế vật tư (bạc đạn, cánh khuấy Inox 304)', '**Bước 2: Thay thế vật tư chính hãng:**')
s4 = s4.replace('### 4.4 Nghiệm thu, thử mẻ trộn và bàn giao công nghệ', '**Bước 3: Nghiệm thu và thử mẻ tải:**\n\n### 5.3 Quyền lợi và lợi ích khách hàng (Benefits)\n\nSau khi bàn giao, nhà máy được cấp sổ bảo hành vật tư lên đến 12 tháng. Sự phối hợp của TNT đảm bảo giảm 85% rủi ro tái hỏng hóc cùng vị trí, giúp doanh nghiệp an tâm sản xuất dài hạn.')

s1 = sections['1'].replace('1. Tại sao sửa chữa và bảo dưỡng máy trộn nhựa lại sống còn đối với nhà máy?', '6. Rủi ro Downtime và lý do cần bảo dưỡng định kỳ')
s5 = sections['5'].replace('5. Các nguyên tắc an toàn và cách vệ sinh máy trộn nhựa đúng chuẩn', '7. Gói dịch vụ bảo trì định kỳ và vệ sinh máy trộn nhựa đúng chuẩn')
s8 = sections['8'].replace('8. Câu hỏi thường gặp (FAQs) về bảo trì máy trộn nhựa', '8. Câu hỏi thường gặp (FAQs) về dịch vụ')
s9 = sections['9'].replace('9. Tổng kết & thông tin khảo sát tận nơi cùng TNT', '9. Liên hệ khảo sát tận nơi ngay hôm nay')

# Re-number H3s to match new H2 numbers
import re
s2 = re.sub(r'### 2\.', '### 1.', s2)
s3 = re.sub(r'### 3\.', '### 2.', s3)
s6 = re.sub(r'### 6\.', '### 3.', s6)
s1 = re.sub(r'### 1\.', '### 6.', s1)
s5 = re.sub(r'### 5\.', '### 7.', s5)

new_content = [
    header_and_intro.replace('# Sửa máy trộn nhựa từ kỹ sư TNT: Giảm downtime, tối ưu năng suất', '# Dịch vụ sửa máy trộn nhựa từ chuyên gia TNT: Uy tín, trọn gói, xử lý 24/7'),
    '## ' + s2,
    '## ' + s3,
    '## ' + s6,
    '## ' + s7,
    '## ' + s4,
    '## ' + s1,
    '## ' + s5,
    '## ' + s8,
    '## ' + s9
]

final_text = '\n\n'.join(new_content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(final_text.strip() + '\n')

print('Done')
