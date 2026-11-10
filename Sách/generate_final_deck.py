# -*- coding: utf-8 -*-
import os
import re
import base64
import subprocess
from pathlib import Path

# 1. Base64 encode the local fonts
def get_b64(path):
    return base64.b64encode(Path(path).read_bytes()).decode('utf-8')

pf_normal_700 = get_b64("Sách/fonts/PlayfairDisplay-normal-700.ttf")
pf_italic_600 = get_b64("Sách/fonts/PlayfairDisplay-italic-600.ttf")
bv_normal_400 = get_b64("Sách/fonts/BeVietnamPro-normal-400.ttf")
bv_normal_600 = get_b64("Sách/fonts/BeVietnamPro-normal-600.ttf")
bv_normal_700 = get_b64("Sách/fonts/BeVietnamPro-normal-700.ttf")
bv_normal_800 = get_b64("Sách/fonts/BeVietnamPro-normal-800.ttf")

font_face_css = f"""
@font-face {{
  font-family: 'Playfair Display';
  font-style: normal;
  font-weight: 700;
  src: url(data:font/truetype;charset=utf-8;base64,{pf_normal_700}) format('truetype');
}}
@font-face {{
  font-family: 'Playfair Display';
  font-style: italic;
  font-weight: 600;
  src: url(data:font/truetype;charset=utf-8;base64,{pf_italic_600}) format('truetype');
}}
@font-face {{
  font-family: 'Be Vietnam Pro';
  font-style: normal;
  font-weight: 400;
  src: url(data:font/truetype;charset=utf-8;base64,{bv_normal_400}) format('truetype');
}}
@font-face {{
  font-family: 'Be Vietnam Pro';
  font-style: normal;
  font-weight: 600;
  src: url(data:font/truetype;charset=utf-8;base64,{bv_normal_600}) format('truetype');
}}
@font-face {{
  font-family: 'Be Vietnam Pro';
  font-style: normal;
  font-weight: 700;
  src: url(data:font/truetype;charset=utf-8;base64,{bv_normal_700}) format('truetype');
}}
@font-face {{
  font-family: 'Be Vietnam Pro';
  font-style: normal;
  font-weight: 800;
  src: url(data:font/truetype;charset=utf-8;base64,{bv_normal_800}) format('truetype');
}}
"""

# 2. Parse markdown content
content = Path("Sách/noi_dung_duc_ket.md").read_text(encoding="utf-8")
slides_raw = content.split("#### SLIDE ")[1:]

lessons = []
for s in slides_raw:
    lines = s.strip().split("\n")
    header = lines[0].strip()
    m = re.match(r"(\d+)\s*—\s*BÀI HỌC\s*(\d+):\s*(.*)", header)
    if not m:
        continue
    slide_num, lesson_num, title = m.groups()
    body = "\n".join(lines[1:])
    
    def extract_field(field_name):
        pat = rf"\* \*\*\d+\. {field_name}[^*:]*:\*\*\s*\n(.*?)(?=\n\* \*\*\d+\.|\n---|---|\Z)"
        fm = re.search(pat, body, re.DOTALL)
        return fm.group(1).strip() if fm else ""
    
    def clean_text(txt):
        txt = txt.strip()
        txt = txt.replace("$\\rightarrow$", "→").replace("$\\longrightarrow$", "⟶").replace("\\rightarrow", "→").replace("$", "")
        txt = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", txt)
        # remove stray * in reflection or text
        txt = txt.replace("*", "")
        txt = re.sub(r"“|”", '"', txt)
        return txt

    axiom = clean_text(extract_field("Chân lý cốt lõi"))
    mechanism = clean_text(extract_field("Giải phẫu cơ chế"))
    pitfall = clean_text(extract_field("Bẫy sai lầm phổ biến"))
    drill = clean_text(extract_field("Kỹ thuật huấn luyện tuần"))
    dod = clean_text(extract_field("Tiêu chuẩn nghiệm thu"))
    reflection = clean_text(extract_field("Câu hỏi tự vấn"))
    
    ln = int(lesson_num)
    if ln <= 6:
        chang = "CHẶNG I: ĐỊNH THÂN & THỨC TỈNH NỘI TÂM"
    elif ln <= 12:
        chang = "CHẶNG II: KIẾN TẠO BẢN VẼ TÂM TRÍ"
    elif ln <= 18:
        chang = "CHẶNG III: HÒA NHẬP NĂNG LƯỢNG & LUẬT HẤP DẪN"
    else:
        chang = "CHẶNG IV: KHAI MỞ CHÌA KHÓA VÀNG & VẠN VẬT QUY NHẤT"
        
    lessons.append({
        "slide_num": slide_num,
        "lesson_num": lesson_num,
        "title": title.strip(),
        "chang": chang,
        "axiom": axiom,
        "mechanism": mechanism,
        "pitfall": pitfall,
        "drill": drill,
        "dod": dod,
        "reflection": reflection
    })

curated_packs = {
    "01": {
        "principles": [
            ("Năng lượng Động vs. Tĩnh", "Ý niệm là năng lượng tĩnh tiềm tàng; suy nghĩ là năng lượng động sáng tạo. Tâm trí liên tục chuyển hóa ý niệm vô hình thành hiện thực vật chất hữu hình."),
            ("Mối quan hệ Nhân – Quả", "Mọi hoàn cảnh khách quan bên ngoài hoàn toàn phản chiếu tư duy chủ quan bên trong. Trật tự nội tâm sinh ra của cải; hỗn loạn tinh thần sinh ra thiếu thốn."),
            ("Cầu nối Thần kinh kép", "Hệ đại não (ý thức) đưa ra định hướng; Hệ giao cảm tại hạch thái dương (tiềm thức) tiếp nhận mệnh lệnh để phân bổ sinh lực nuôi dưỡng tế bào.")
        ],
        "reflections": [
            "Tôi đang để biến động thị trường bên ngoài chi phối tâm trí, hay dùng thế giới nội tâm để tái lập hoàn cảnh?",
            "Cảm xúc chủ đạo khi tôi đối diện với áp lực công việc là sự chủ động kiểm soát hay phản xạ đổ lỗi cho ngoại cảnh?"
        ],
        "pitfall": ("Cố gồng cứng cơ bắp để ép mình không cử động, khiến hệ thần kinh căng thẳng gấp bội và gây phản lực tâm lý.",
                    "Thả lỏng toàn bộ các bó cơ trước; để cơ thể chìm vào trạng thái an định tự nhiên, dùng ý thức quan sát chứ không cưỡng ép."),
        "drill": [
            ("BƯỚC 1", "<strong>Chuẩn bị &amp; Tách biệt giác quan:</strong> Chọn phòng yên tĩnh, ngồi thẳng lưng trên ghế tựa, chân chạm đất, tay đặt trên đùi. Thả lỏng toàn bộ cơ thể nhưng không buông trôi."),
            ("BƯỚC 2", "<strong>Bất động tuyệt đối (15 phút):</strong> Giữ nguyên vị trí, triệt tiêu 100% các xung động ngọ nguậy, chuyển thế, gãi ngứa. Khống chế hoàn toàn mọi phản xạ vô thức."),
            ("BƯỚC 3", "<strong>Tĩnh lặng ý thức:</strong> Để dòng suy tưởng tự do lướt qua như mây trôi. Không bám chấp, không phán xét cho đến khi tâm trí lắng dịu như mặt hồ phẳng lặng.")
        ],
        "dod": [
            ("CẤP 1", "(THÂN)", "Ngồi trọn vẹn 15 phút không một cử động nhỏ; toàn bộ cơ bắp mềm mại, không có bất kỳ phản xạ co giật cơ hay bồn chồn."),
            ("CẤP 2", "(KHÍ)", "Hơi thở tự động chuyển sang trạng thái êm, chậm, sâu tự nhiên (dưới 10 nhịp/phút) mà không cần dùng ý chí gượng ép."),
            ("CẤP 3", "(TÂM)", "Cảm nhận sự an định và tỉnh thức rõ rệt; nhận diện sâu sắc rằng Cái Tôi là chủ nhân tối cao của thân xác và suy nghĩ.")
        ]
    },
    "07": {
        "principles": [
            ("Kích hoạt Hệ lưới Hoạt hóa (RAS)", "Hình ảnh tinh thần sống động kèm cảm xúc biến tiềm thức thành bộ lọc nhạy bén, tự động nhận diện và thu hút mọi cơ hội ngoài đời thực."),
            ("Trường nhìn Tinh thần Trước thực tại", "Mọi tạo tác vật chất bắt buộc phải tồn tại trong tâm trí trước khi hiển lộ. Bạn không thể chạm tay vào điều mà tâm trí bạn chưa nhìn thấy rõ."),
            ("Sự kết dính của Niềm tin", "Cảm xúc chân thật khi hình dung sẽ kích hoạt các mạng lưới liên kết thần kinh tương đương với trải nghiệm thực tế ngoài đời thực.")
        ],
        "reflections": [
            "Bức tranh về tương lai mà tôi đang mang trong đầu hiện nay sắc nét như một bộ phim hay mờ mịt như sương mù?",
            "Tôi có đang để những nỗi lo sợ về rủi ro làm lu mờ đi hình ảnh mục tiêu vĩ đại mà tôi muốn đạt được?"
        ],
        "pitfall": ("Hình dung chung chung, mờ nhạt ('Tôi muốn thành công') mà không có chi tiết cụ thể, khiến tiềm thức không có dữ liệu để thực thi.",
                    "Xây dựng hình ảnh với độ phân giải cao nhất: đầy đủ đường nét, màu sắc, âm thanh, bối cảnh và cảm xúc sống động."),
        "drill": [
            ("BƯỚC 1", "<strong>Ổn định và nhắm mắt:</strong> Đưa cơ thể vào trạng thái bất động và thả lỏng sâu trong 3 phút, ngắt toàn bộ kích thích giác quan bên ngoài."),
            ("BƯỚC 2", "<strong>Tái hiện hình ảnh người thân:</strong> Quán tưởng chi tiết một người thân yêu: hình dung rõ nét từ ánh mắt, nụ cười, nếp nhăn, giọng nói, dáng đi cho đến cử chỉ quen thuộc nhất."),
            ("BƯỚC 3", "<strong>Duy trì độ nét liên tục:</strong> Giữ vững hình ảnh đó sống động trước mắt tâm thức suốt 10 phút; cảm nhận trọn vẹn sự ấm áp và hiện diện như ngoài đời thực.")
        ],
        "dod": [
            ("CẤP 1", "(ĐỘ NÉT)", "Tái hiện rõ ràng diện mạo người thân trong tâm trí với đầy đủ màu sắc trang phục và biểu cảm khuôn mặt."),
            ("CẤP 2", "(CẢM XÚC)", "Cảm nhận được tình cảm và sự gắn kết chân thực dâng trào trong lồng ngực như đang ngồi đối diện trò chuyện."),
            ("CẤP 3", "(LÀM CHỦ)", "Giữ vững hình ảnh trong tâm trí liên tục trên 3 phút mà không bị bất kỳ hình ảnh tạp niệm nào chen ngang.")
        ]
    }
}

def parse_tier_tuple(raw_tier):
    m = re.match(r"(CẤP\s*\d+)\s*(\([^)]+\))", raw_tier.strip())
    if m:
        return m.group(1), m.group(2)
    return raw_tier.strip(), ""

def get_pack(p):
    ln = p["lesson_num"]
    if ln in curated_packs:
        return curated_packs[ln]
    
    mech = p["mechanism"]
    points = [s.strip() for s in mech.split(". ") if len(s.strip()) > 10]
    if len(points) < 3:
        points.append("Nhận thức đúng đắn kích hoạt tiềm năng vô biên của tiềm thức; xóa bỏ ma sát nội tâm để tiếp nhận trọn vẹn quy luật vận hành của tự nhiên.")
    
    drill_raw = p["drill"].replace("$\\rightarrow$", "→").replace("$\\longrightarrow$", "⟶").replace("\\rightarrow", "→").replace("$", "")
    d_parts = [s.strip() for s in drill_raw.split(". ") if len(s.strip()) > 8]
    step1 = "<strong>Chuẩn bị &amp; Định vị:</strong> " + (d_parts[0] if len(d_parts) > 0 else "Đưa cơ thể vào trạng thái thả lỏng, giữ cột sống thẳng và bất động tuyệt đối trong phòng yên tĩnh.")
    step2 = "<strong>Thực thi kỷ luật cốt lõi:</strong> " + (d_parts[1] if len(d_parts) > 1 else "Tập trung toàn bộ năng lượng tinh thần vào hành động của bài học, dập tắt mọi tạp niệm xao nhãng.")
    step3 = "<strong>Chuyển hóa &amp; Neo giữ:</strong> " + (d_parts[2] if len(d_parts) > 2 else "Duy trì sự tĩnh lặng, cảm nhận dòng năng lượng thành tựu và biến nhận thức thành phản xạ tự nhiên của tiềm thức.")
    
    dod_raw = p["dod"]
    dod_parts = [s.strip() for s in dod_raw.split("; ") if len(s.strip()) > 5]
    dod1 = dod_parts[0] if len(dod_parts) > 0 else "Hoàn thành trọn vẹn thời lượng bài tập mà không bị phân tâm hoặc cử động thân thể."
    dod2 = dod_parts[1] if len(dod_parts) > 1 else "Cảm nhận được sự chuyển hóa rõ rệt trong nhịp sinh học và cảm xúc nội tâm sau khi tập."
    dod3 = dod_parts[2] if len(dod_parts) > 2 else "Ứng dụng tự nhiên nhận thức này vào các quyết định và hành vi thực tế trong suốt ngày sống."
    
    ref_raw = p["reflection"].replace("*", "")
    refs = [s.strip() for s in ref_raw.split("?") if len(s.strip()) > 5]
    r1 = refs[0] + "?" if len(refs) > 0 else "Tôi đã thực sự thấu hiểu và vận dụng quy luật này vào công việc hàng ngày chưa?"
    r2 = (refs[1] + "?" if len(refs) > 1 and not refs[1].endswith("?") else refs[1] if len(refs) > 1 else "Hành động nào tôi cần thực hiện ngay hôm nay để điều chỉnh hoàn cảnh sống theo đúng chân lý này?")
    
    pf = p["pitfall"]
    if ";" in pf:
        m_con, corr = pf.split(";", 1)
    elif "," in pf and len(pf) > 60:
        parts = pf.split(",", 1)
        m_con, corr = parts[0], parts[1]
    else:
        m_con = pf
        corr = "Thấu suốt quy luật vận hành của tự nhiên, hành động dựa trên sự hiểu biết và kỷ luật thép thay vì cảm xúc bốc đồng."

    return {
        "principles": [
            ("Quy luật Vận hành Cốt lõi", points[0]),
            ("Cơ chế Phản ứng Thần kinh", points[1] if len(points) > 1 else "Tư tưởng kết hợp với cảm xúc mãnh liệt tạo ra tần số rung động tác động trực tiếp vào tiềm thức."),
            ("Ứng dụng Chuyển hóa Thực tiễn", points[2] if len(points) > 2 else "Làm chủ nhận thức giúp người lãnh đạo kiến tạo của cải và trật tự bền vững cho tổ chức.")
        ],
        "reflections": [r1, r2],
        "pitfall": (m_con.strip(), corr.strip()),
        "drill": [
            ("BƯỚC 1", step1),
            ("BƯỚC 2", step2),
            ("BƯỚC 3", step3)
        ],
        "dod": [
            ("CẤP 1", "(KỸ THUẬT)", dod1),
            ("CẤP 2", "(CẢM NHẬN)", dod2),
            ("CẤP 3", "(CHUYỂN HÓA)", dod3)
        ]
    }

# 3. CSS Scaled up by +2 sizes across all elements
css = f"""
{font_face_css}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}
@page {{ size: 1920px 1080px; margin: 0; }}
html, body {{
  margin: 0;
  padding: 0;
  width: 1920px;
  line-height: 0;
  font-size: 0;
  background-color: #F7F4EE;
  -webkit-font-smoothing: antialiased;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}}

.slide {{
  width: 1920px;
  height: 1080px;
  max-height: 1080px;
  overflow: hidden;
  background-color: #F7F4EE;
  background-image: radial-gradient(#E5DFD3 0.75px, transparent 0.75px);
  background-size: 24px 24px;
  position: relative;
  page-break-inside: avoid;
  break-inside: avoid;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 16.5px;
  line-height: 1.55;
  color: #1F2124;
}}
.slide:not(:last-child) {{
  page-break-after: always;
  break-after: page;
}}
.slide:last-child {{
  page-break-after: avoid !important;
  break-after: avoid !important;
}}

.outer-frame {{
  width: 1840px;
  height: 1000px;
  border: 1px solid rgba(140, 125, 105, 0.32);
  position: relative;
  padding: 38px 56px 30px 56px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: rgba(247, 244, 238, 0.94);
}}
.inner-border {{
  position: absolute;
  inset: 8px;
  border: 1px solid rgba(140, 125, 105, 0.12);
  pointer-events: none;
}}

/* Header & Footer */
.header-bar {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(140, 125, 105, 0.22);
  padding-bottom: 12px;
  flex-shrink: 0;
}}
.brand-tag {{
  font-size: 13.5px;
  font-weight: 700;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: #7A6F62;
}}
.lesson-index {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 24px;
  font-style: italic;
  font-weight: 600;
  color: #8C7355;
  font-variant-numeric: lining-nums;
  font-feature-settings: "lnum" 1;
}}

.footer-bar {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13.5px;
  letter-spacing: 0.12em;
  color: #8A7E70;
  border-top: 1px solid rgba(140, 125, 105, 0.22);
  padding-top: 12px;
  flex-shrink: 0;
}}
.style-badge {{
  font-weight: 700;
  text-transform: uppercase;
  background: #E8E1D5;
  padding: 5px 16px;
  border-radius: 20px;
  font-size: 12.5px;
  letter-spacing: 0.15em;
  color: #554C41;
}}

/* Main Grid */
.content-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 44px;
  align-items: stretch;
  height: 865px;
  padding: 8px 0;
}}

/* LEFT COLUMN */
.left-col {{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding-right: 6px;
}}

.chapter-meta {{
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 4px;
}}
.chapter-meta .line {{
  width: 38px;
  height: 2px;
  background: #8C7355;
}}
/* TĂNG SIZE CHỮ TIÊU ĐỀ PHỤ */
.chapter-meta .label {{
  font-size: 17.5px;
  font-weight: 800;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #8C7355;
}}

/* TÊN ĐẦU ĐỀ: BẮT BUỘC DÙNG PLAYFAIR DISPLAY BOLD NORMAL (KHÔNG ITALIC, LINING NUMS BẰNG CHỮ BÀI) */
.lesson-title {{
  font-family: 'Playfair Display', Georgia, serif !important;
  font-style: normal !important;
  font-size: 42px !important;
  font-weight: 700 !important;
  color: #1A1B1E !important;
  line-height: 1.2 !important;
  letter-spacing: -0.01em !important;
  margin-bottom: 12px !important;
  font-variant-numeric: lining-nums !important;
  font-feature-settings: "lnum" 1 !important;
}}

.axiom-box {{
  background: #EFEBE1;
  border-left: 4px solid #8C7355;
  padding: 20px 26px;
  border-radius: 0 8px 8px 0;
  margin-bottom: 14px;
}}
.axiom-text {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 26.5px;
  line-height: 1.38;
  font-weight: 600;
  font-style: italic;
  color: #24221E;
}}

/* 3 Core Principles */
.principles-section {{
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 14px;
}}
.section-tag-small {{
  font-size: 17px;
  font-weight: 800;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #7A6F62;
  margin-bottom: 2px;
}}
.principle-row {{
  display: flex;
  gap: 18px;
  align-items: center; /* CĂN GIỮA DỌC */
  background: rgba(255, 255, 255, 0.55);
  border: 1px solid rgba(140, 125, 105, 0.20);
  border-radius: 6px;
  padding: 12px 18px;
}}
.principle-num {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 26px;
  font-weight: 700;
  color: #8C7355;
  line-height: 1;
  width: 30px;
  flex-shrink: 0;
  text-align: center;
  font-variant-numeric: lining-nums;
  font-feature-settings: "lnum" 1;
}}
.principle-content h4 {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 18px;
  font-weight: 700;
  color: #22252A;
  margin-bottom: 2px;
  font-variant-numeric: lining-nums;
}}
.principle-content p {{
  font-size: 15.5px;
  line-height: 1.55;
  color: #4E473F;
}}

/* Reflection Box */
.reflection-box {{
  background: #FAF7F2;
  border: 1px solid rgba(140, 125, 105, 0.25);
  border-radius: 8px;
  padding: 14px 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}}
.reflection-header {{
  font-size: 13.5px;
  font-weight: 800;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: #8C7355;
  display: flex;
  align-items: center;
  gap: 8px;
}}
.reflection-header::before {{
  content: "✦";
  font-size: 13px;
  color: #8C7355;
}}
.reflection-item {{
  font-size: 15.5px;
  line-height: 1.55;
  color: #38322B;
}}

/* RIGHT COLUMN (ZEN EDITORIAL CARD) */
.right-col {{
  display: flex;
  flex-direction: column;
}}

.zen-card {{
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(140, 125, 105, 0.28);
  border-radius: 12px;
  padding: 26px 28px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.02);
}}

.card-block {{
  display: flex;
  flex-direction: column;
  gap: 8px;
}}

.card-block-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(140, 125, 105, 0.16);
  padding-bottom: 6px;
}}
.card-block-tag {{
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #7A6F62;
  display: flex;
  align-items: center;
  gap: 8px;
}}
.card-block-badge {{
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 3px 10px;
  border-radius: 4px;
}}

/* Block 1: Pitfall & Correction */
.badge-pitfall {{
  background: #EFEBE5;
  color: #6E533F;
  border: 1px solid #D6CBC1;
}}
.pitfall-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}}
.pitfall-item {{
  background: #F9F6F0;
  border: 1px solid rgba(140, 125, 105, 0.2);
  border-radius: 6px;
  padding: 12px 16px;
}}
.pitfall-item .title {{
  font-size: 13.5px;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #8C5A40;
  margin-bottom: 4px;
}}
.pitfall-item .desc {{
  font-size: 15px;
  line-height: 1.55;
  color: #554A41;
}}

/* Block 2: 3-Stage Drill */
.badge-drill {{
  background: #EFE7DC;
  color: #735C3E;
  border: 1px solid #D9CEBF;
}}
.drill-steps-wrap {{
  display: flex;
  flex-direction: column;
  gap: 8px;
}}
.step-row {{
  display: flex;
  gap: 18px;
  align-items: center; /* CĂN GIỮA DỌC */
  background: #FAF7F2;
  border-left: 3.5px solid #8C7355;
  border-radius: 0 6px 6px 0;
  padding: 11px 18px;
}}
.step-order {{
  font-size: 14.5px;
  font-weight: 800;
  color: #8C7355;
  width: 78px;
  flex-shrink: 0;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  text-align: center;
  background: rgba(140, 125, 105, 0.12);
  padding: 7px 0;
  border-radius: 4px;
}}
.step-text {{
  font-size: 15.5px;
  line-height: 1.55;
  color: #38332E;
}}
.step-text strong {{
  color: #1F2124;
}}

/* Block 3: Mastery Checklist */
.badge-dod {{
  background: #E6ECE8;
  color: #3D5443;
  border: 1px solid #C4D3C7;
}}
.dod-list {{
  display: flex;
  flex-direction: column;
  gap: 7px;
}}
.dod-row {{
  display: flex;
  gap: 18px;
  align-items: center; /* CĂN GIỮA DỌC */
  background: #F4F7F4;
  border-left: 3.5px solid #4D6E55;
  border-radius: 0 6px 6px 0;
  padding: 10px 18px;
}}
/* THẺ CẤP 1 (..) CHỮ TRONG NGOẶC XUỐNG DÒNG */
.dod-tier {{
  font-size: 13px;
  font-weight: 800;
  color: #3D5443;
  width: 110px;
  flex-shrink: 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-align: center;
  background: rgba(61, 84, 67, 0.12);
  padding: 6px 4px;
  border-radius: 5px;
  line-height: 1.35;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}}
.tier-name {{
  font-size: 13.5px;
  font-weight: 800;
}}
.tier-sub {{
  font-size: 11.5px;
  font-weight: 700;
  opacity: 0.9;
}}
.dod-desc {{
  font-size: 15px;
  line-height: 1.55;
  color: #2F4234;
}}

/* Cover & Overview Styles */
.cover-center {{
  height: 840px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}}
.cover-title {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 84px;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: #1F2124;
  line-height: 1.15;
  margin-bottom: 20px;
  font-variant-numeric: lining-nums;
  font-feature-settings: "lnum" 1;
}}
.cover-subtitle {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 42px;
  font-style: italic;
  font-weight: 400;
  color: #755B3E;
  margin-bottom: 36px;
}}
.cover-divider {{
  width: 140px;
  height: 2px;
  background: #8C7355;
  margin: 0 auto 36px auto;
}}
.cover-desc {{
  font-size: 19.5px;
  line-height: 1.85;
  color: #5D564C;
  max-width: 950px;
  margin: 0 auto;
}}

.framework-center {{
  height: 840px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 36px;
}}
.flow-boxes {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}}
.flow-card {{
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(140, 125, 105, 0.28);
  border-radius: 12px;
  padding: 30px 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 330px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.02);
}}
.flow-num {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 40px;
  font-weight: 700;
  color: #8C7355;
  margin-bottom: 10px;
  font-variant-numeric: lining-nums;
  font-feature-settings: "lnum" 1;
}}
.flow-title {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 22px;
  font-weight: 700;
  color: #1F2124;
  margin-bottom: 10px;
  font-variant-numeric: lining-nums;
}}
.flow-desc {{
  font-size: 15.5px;
  line-height: 1.6;
  color: #5D564C;
}}

.core-axioms-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
}}
.axiom-item {{
  background: #FAF7F2;
  border-left: 3.5px solid #8C7355;
  padding: 22px 26px;
  border-radius: 0 10px 10px 0;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.015);
}}
.axiom-item h4 {{
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 20px;
  font-weight: 700;
  color: #24262A;
  margin-bottom: 6px;
  font-variant-numeric: lining-nums;
}}
.axiom-item p {{
  font-size: 15.5px;
  line-height: 1.6;
  color: #5D564C;
}}
"""

slides_html = []

# Slide 1: Cover
slides_html.append("""
<div class="slide">
  <div class="outer-frame">
    <div class="inner-border"></div>
    <div class="header-bar">
      <div class="brand-tag">THE MASTER KEY SYSTEM &nbsp;·&nbsp; CHARLES F. HAANEL (1912)</div>
      <div></div>
    </div>
    <div class="cover-center">
      <h1 class="cover-title">THE MASTER KEY SYSTEM</h1>
      <div class="cover-subtitle">24 Bài Học Thần Kỳ Nhất Thế Giới</div>
      <div class="cover-divider"></div>
      <p class="cover-desc">
        Hệ thống triết học Tân Tư Tưởng kinh điển từng bị phong tỏa suốt 70 năm. Bộ tài liệu chuyển hóa trọn vẹn 24 tuần rèn luyện: từ làm chủ cơ thể, định hướng tiềm thức, kích hoạt Luật Hấp Dẫn đến hòa nhập vào Trí Tuệ Toàn Năng của Vũ Trụ.
      </p>
    </div>
    <div class="footer-bar">
      <div>THE MASTER KEY SYSTEM</div>
      <div></div>
    </div>
  </div>
</div>
""")

# Slide 2: Framework
slides_html.append("""
<div class="slide">
  <div class="outer-frame">
    <div class="inner-border"></div>
    <div class="header-bar">
      <div class="brand-tag">MÔ HÌNH TỔNG QUAN &nbsp;·&nbsp; THE MASTER KEY FRAMEWORK</div>
      <div class="lesson-index">Cơ Chế Chuyển Hóa Năng Lượng</div>
    </div>
    <div class="framework-center">
      <div>
        <div class="chapter-meta">
          <span class="line"></span>
          <span class="label">BỐN TẦNG CHUYỂN HÓA VẬT CHẤT CỦA TƯ TƯỞNG</span>
        </div>
        <div class="flow-boxes">
          <div class="flow-card">
            <div>
              <div class="flow-num">01</div>
              <div class="flow-title">Vũ Trụ &amp; Tự Nhiên</div>
            </div>
            <div class="flow-desc">Nguồn năng lượng sáng tạo vô biên chứa đựng mọi quy luật và tiềm năng vật chất chưa khai phá.</div>
          </div>
          <div class="flow-card">
            <div>
              <div class="flow-num">02</div>
              <div class="flow-title">Ý Thức (Lý Tính)</div>
            </div>
            <div class="flow-desc">Hệ thần kinh đại não: phán đoán logic, chọn lọc mục tiêu và đóng vai trò 'Người gác cổng' tâm trí.</div>
          </div>
          <div class="flow-card">
            <div>
              <div class="flow-num">03</div>
              <div class="flow-title">Tiềm Thức (Hệ Giao Cảm)</div>
            </div>
            <div class="flow-desc">Tiếp nhận vô điều kiện mọi mệnh lệnh kèm cảm xúc mạnh từ ý thức để tự động vận hành và khuếch đại.</div>
          </div>
          <div class="flow-card">
            <div>
              <div class="flow-num">04</div>
              <div class="flow-title">Hiện Thực Khách Quan</div>
            </div>
            <div class="flow-desc">Sức khỏe, của cải, con người và hoàn cảnh bên ngoài phản chiếu trọn vẹn trạng thái nội tâm bên trong.</div>
          </div>
        </div>
      </div>
      <div>
        <div class="chapter-meta">
          <span class="line"></span>
          <span class="label">HAI NGUYÊN TẮC BẤT DI BẤT DỊCH CỦA BẬC THẦY</span>
        </div>
        <div class="core-axioms-grid">
          <div class="axiom-item">
            <h4>1. Thế giới bên trong sáng tạo ra thế giới bên ngoài</h4>
            <p>Trật tự nội tâm sinh ra thịnh vượng; hỗn loạn nội tâm sinh ra túng thiếu. Không thể thay đổi quả ngọt nếu không thay đổi hạt giống tư tưởng.</p>
          </div>
          <div class="axiom-item">
            <h4>2. Kỷ luật sinh lý là nền tảng của tự do tâm thức</h4>
            <p>Người không thể điều khiển cơ thể mình ngồi yên lặng 15 phút sẽ không bao giờ làm chủ được số phận và hoàn cảnh sống.</p>
          </div>
        </div>
      </div>
    </div>
    <div class="footer-bar">
      <div>THE MASTER KEY SYSTEM</div>
      <div class="style-badge">LỘ TRÌNH 4 CHẶNG RÈN LUYỆN</div>
    </div>
  </div>
</div>
""")

# Slides 3 to 26: 24 Lessons
for p in lessons:
    pack = get_pack(p)
    p1, p2, p3 = pack["principles"][0], pack["principles"][1], pack["principles"][2]
    d1, d2, d3 = pack["drill"][0], pack["drill"][1], pack["drill"][2]
    
    def format_dod_item(item):
        if len(item) == 3:
            name, sub, desc = item
            return f'<div class="dod-tier"><span class="tier-name">{name}</span><span class="tier-sub">{sub}</span></div>', desc
        raw_tier, desc = item
        name, sub = parse_tier_tuple(raw_tier)
        return f'<div class="dod-tier"><span class="tier-name">{name}</span><span class="tier-sub">{sub}</span></div>', desc

    m1_tag, m1_desc = format_dod_item(pack["dod"][0])
    m2_tag, m2_desc = format_dod_item(pack["dod"][1])
    m3_tag, m3_desc = format_dod_item(pack["dod"][2])

    r1, r2 = pack["reflections"][0], pack["reflections"][1]
    miscon, correct = pack["pitfall"]

    slide_html = f"""
<div class="slide">
  <div class="outer-frame">
    <div class="inner-border"></div>
    <div class="header-bar">
      <div class="brand-tag">THE MASTER KEY SYSTEM &nbsp;·&nbsp; {p['chang']}</div>
      <div class="lesson-index">Bài học số {p['lesson_num']} / 24</div>
    </div>

    <div class="content-grid">
      <!-- CỘT TRÁI -->
      <div class="left-col">
        <div>
          <div class="chapter-meta">
            <span class="line"></span>
            <span class="label">TRIẾT LÝ &amp; GIẢI PHẪU KHOA HỌC TÂM TRÍ</span>
          </div>
          <h1 class="lesson-title">BÀI {p['lesson_num']}: {p['title']}</h1>

          <div class="axiom-box">
            <div class="axiom-text">“{p['axiom'].replace('"', '')}”</div>
          </div>

          <div class="principles-section">
            <div class="section-tag-small">3 NGUYÊN LÝ CỐT LÕI VỀ TÂM THỨC</div>
            
            <div class="principle-row">
              <div class="principle-num">I</div>
              <div class="principle-content">
                <h4>{p1[0]}</h4>
                <p>{p1[1]}</p>
              </div>
            </div>

            <div class="principle-row">
              <div class="principle-num">II</div>
              <div class="principle-content">
                <h4>{p2[0]}</h4>
                <p>{p2[1]}</p>
              </div>
            </div>

            <div class="principle-row">
              <div class="principle-num">III</div>
              <div class="principle-content">
                <h4>{p3[0]}</h4>
                <p>{p3[1]}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="reflection-box">
          <div class="reflection-header">TỰ VẤN NỘI TÂM DÀNH CHO NGƯỜI LÃNH ĐẠO</div>
          <div class="reflection-item">1. {r1}</div>
          <div class="reflection-item">2. {r2}</div>
        </div>
      </div>

      <!-- CỘT PHẢI (ZEN CARD) -->
      <div class="right-col">
        <div class="zen-card">
          <!-- 1. Bẫy sai lầm -->
          <div class="card-block">
            <div class="card-block-header">
              <span class="card-block-tag">1. BẪY TÂM LÝ &amp; ĐIỂM NGHẼN THỰC HÀNH</span>
              <span class="card-block-badge badge-pitfall">LƯU Ý QUAN TRỌNG</span>
            </div>
            <div class="pitfall-grid">
              <div class="pitfall-item">
                <div class="title">NGỘ NHẬN PHỔ BIẾN</div>
                <div class="desc">{miscon}</div>
              </div>
              <div class="pitfall-item">
                <div class="title">CHỈ DẪN CHUẨN XÁC</div>
                <div class="desc">{correct}</div>
              </div>
            </div>
          </div>

          <!-- 2. Kỹ thuật huấn luyện tuần -->
          <div class="card-block">
            <div class="card-block-header">
              <span class="card-block-tag">2. QUY TRÌNH HUẤN LUYỆN THỰC CHIẾN (15–30 PHÚT/NGÀY)</span>
              <span class="card-block-badge badge-drill">KỶ LUẬT TUẦN {p['lesson_num']}</span>
            </div>
            <div class="drill-steps-wrap">
              <div class="step-row">
                <div class="step-order">{d1[0]}</div>
                <div class="step-text">{d1[1]}</div>
              </div>
              <div class="step-row">
                <div class="step-order">{d2[0]}</div>
                <div class="step-text">{d2[1]}</div>
              </div>
              <div class="step-row">
                <div class="step-order">{d3[0]}</div>
                <div class="step-text">{d3[1]}</div>
              </div>
            </div>
          </div>

          <!-- 3. Tiêu chuẩn nghiệm thu -->
          <div class="card-block">
            <div class="card-block-header">
              <span class="card-block-tag">3. TIÊU CHUẨN NGHIỆM THU NĂNG LỰC (DEFINITION OF DONE)</span>
              <span class="card-block-badge badge-dod">THƯỚC ĐO ĐẠT CHUẨN</span>
            </div>
            <div class="dod-list">
              <div class="dod-row">
                {m1_tag}
                <div class="dod-desc">{m1_desc}</div>
              </div>
              <div class="dod-row">
                {m2_tag}
                <div class="dod-desc">{m2_desc}</div>
              </div>
              <div class="dod-row">
                {m3_tag}
                <div class="dod-desc">{m3_desc}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="footer-bar">
      <div>THE MASTER KEY SYSTEM</div>
      <div class="style-badge">TUẦN {p['lesson_num']} / 24 &nbsp;·&nbsp; {p['chang'].split(':')[0]}</div>
    </div>
  </div>
</div>
"""
    slides_html.append(slide_html)

# Slide 27: Summary & Roadmap
slides_html.append("""
<div class="slide">
  <div class="outer-frame">
    <div class="inner-border"></div>
    <div class="header-bar">
      <div class="brand-tag">TỔNG KẾT HÀNH ĐỘNG &nbsp;·&nbsp; THE MASTER KEY ROADMAP</div>
      <div class="lesson-index">Lộ Trình 24 Tuần Chuyển Hóa</div>
    </div>
    <div class="framework-center">
      <div>
        <div class="chapter-meta">
          <span class="line"></span>
          <span class="label">BỐN CHẶNG RÈN LUYỆN ĐẠT TỚI BẬC THẦY</span>
        </div>
        <div class="flow-boxes">
          <div class="flow-card">
            <div>
              <div class="flow-num">I</div>
              <div class="flow-title">Định Thân &amp; Thức Tỉnh</div>
            </div>
            <div class="flow-desc"><strong>Bài 01 – 06:</strong> Bất động thân xác, giải tỏa căng cơ, chặn đứng tư tưởng tiêu cực, nhận diện Cái Tôi chủ nhân.</div>
          </div>
          <div class="flow-card">
            <div>
              <div class="flow-num">II</div>
              <div class="flow-title">Bản Vẽ Tâm Trí</div>
            </div>
            <div class="flow-desc"><strong>Bài 07 – 12:</strong> Làm chủ nghệ thuật Quán tưởng (Visualization), xây dựng bản thiết kế tinh thần sắc nét và vững tin tuyệt đối.</div>
          </div>
          <div class="flow-card">
            <div>
              <div class="flow-num">III</div>
              <div class="flow-title">Hòa Nhập Tần Số</div>
            </div>
            <div class="flow-desc"><strong>Bài 13 – 18:</strong> Xóa bỏ hận thù rò rỉ năng lượng, phụng sự giá trị, kích hoạt Luật Hấp Dẫn bằng lòng biết ơn trù phú.</div>
          </div>
          <div class="flow-card">
            <div>
              <div class="flow-num">IV</div>
              <div class="flow-title">Vạn Vật Quy Nhất</div>
            </div>
            <div class="flow-desc"><strong>Bài 19 – 24:</strong> Đón nhận trực giác, sống trong chân lý, mở rộng tư duy 10X, làm chủ chiếc Chìa Khóa Vạn Năng.</div>
          </div>
        </div>
      </div>
      <div>
        <div class="chapter-meta">
          <span class="line"></span>
          <span class="label">CHECKLIST HÀNH ĐỘNG CHUYỂN HÓA 7 – 30 – 90 NGÀY</span>
        </div>
        <div class="core-axioms-grid">
          <div class="axiom-item">
            <h4>7 – 30 Ngày: Làm sạch bộ lọc tiềm thức</h4>
            <p>15 phút ngồi yên mỗi ngày; cắt bỏ 100% tin tức tiêu cực; đóng vai 'Người gác cổng' chặn đứng mọi suy nghĩ tự ti, than thở.</p>
          </div>
          <div class="axiom-item">
            <h4>90 Ngày: Kiến tạo hiện thực &amp; Quyết liệt hành động</h4>
            <p>Phác thảo Bản vẽ tinh thần chi tiết; sống trong cảm xúc của người đã thành công; đón bắt mọi cơ hội mà trực giác mách bảo.</p>
          </div>
        </div>
      </div>
    </div>
    <div class="footer-bar">
      <div>THE MASTER KEY SYSTEM</div>
      <div class="style-badge">HOÀN TẤT GIÁO TRÌNH 24 TUẦN</div>
    </div>
  </div>
</div>
""")

full_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>The Master Key System - 24 Bài Học Thần Kỳ Nhất Thế Giới</title>
<style>
{css}
</style>
</head>
<body>
{"".join(slides_html)}
</body>
</html>"""

Path("Sách/24_bai_hoc_than_ky_slides.html").write_text(full_html, encoding="utf-8")
print("Generated Sách/24_bai_hoc_than_ky_slides.html with embedded Base64 fonts successfully!")
