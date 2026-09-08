import re
import sys

def check_article(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    text = "".join(lines)
    words = text.split()
    word_count = len(words)
    
    print(f"=== Checking {filepath} ===")
    print(f"Total Word Count: {word_count}")
    if word_count >= 2000:
        print(f"❌ FAIL: Word count is {word_count}, must be UNDER 2000 words!")
    else:
        print(f"✅ PASS: Word count {word_count} is under 2000.")

    forbidden_words = [
        "tuyệt tác", "bom tấn", "đỉnh cao", "hoàn hảo", "siêu phẩm",
        "tĩnh lặng", "cỗ máy", "chứng thực xếp hạng",
        "điều phối lương bổng", "dư địa đầu tư", "tiết kiệm sinh sản",
        "điểm nổi trội đáng báo giá", "vòng gửi xe", "hộ chiếu uy tín", "chinh phục"
    ]
    
    found_forbidden = []
    for word in forbidden_words:
        if re.search(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE):
            found_forbidden.append(word)
            
    if found_forbidden:
        print(f"❌ FAIL: Found forbidden/metaphorical words: {found_forbidden}")
    else:
        print("✅ PASS: No forbidden vocabulary found.")

    bullet_ends_with_period = []
    heading_then_bullet = []
    colon_bullet_bad = []
    
    in_bullet_list = False
    last_line_was_heading = False
    
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        
        if stripped.startswith("#"):
            last_line_was_heading = True
            in_bullet_list = False
            continue
            
        if stripped.startswith("- ") or stripped.startswith("* "):
            if last_line_was_heading:
                heading_then_bullet.append(idx)
            
            if stripped.endswith("."):
                bullet_ends_with_period.append((idx, stripped))
                
            colon_match = re.match(r'^[-*]\s+\*\*([^*]+)\*\*:\s*(.)', stripped)
            if colon_match:
                suffix_char = colon_match.group(2)
                if suffix_char.islower():
                    colon_bullet_bad.append((idx, stripped))
                    
            in_bullet_list = True
        else:
            if stripped != "":
                last_line_was_heading = False
                in_bullet_list = False

    if heading_then_bullet:
        print(f"❌ FAIL: Direct bullet list after heading on lines: {heading_then_bullet}")
    else:
        print("✅ PASS: No direct bullet lists after headings.")
        
    if colon_bullet_bad:
        print(f"❌ FAIL: Bullet list colon suffix lowercase on lines: {colon_bullet_bad}")
    else:
        print("✅ PASS: All bold colon bullets have capitalized suffix.")
        
    if bullet_ends_with_period:
        print(f"⚠️ WARNING: {len(bullet_ends_with_period)} bullet points end with a period:")
        for l_num, l_txt in bullet_ends_with_period[:5]:
            print(f"  Line {l_num}: {l_txt}")
    else:
        print("✅ PASS: No bullet points end with a period.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for p in sys.argv[1:]:
            check_article(p)
