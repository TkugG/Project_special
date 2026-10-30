import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# Theme: Minimal & Polite (Open Canvas, Natural Flowing Paragraphs, ZERO Overlap)
# Proportions: Chapter 1 (~60%) : Chapter 3 (~30%) : Chapter 2 & Refs (~10%)
# Citations: Exclusively on Slide 13 (References), ZERO citations in headers!
# ==============================================================================
C_BG         = RGBColor(255, 255, 255)  # Pure White Background
C_LINE       = RGBColor(226, 232, 240)  # Slate 200 — Hairline Divider
C_NAVY       = RGBColor(30,  58,  138)  # #1E3A8A — Headings & Brand
C_BLUE       = RGBColor(37,  99,  235)  # #2563EB — Highlights & Categories
C_RED        = RGBColor(225, 29,  72)   # #E11D48 — Problem / Warning Accents
C_TEXT_MAIN  = RGBColor(15,  23,  42)   # #0F172A Slate 900 — High-contrast Body
C_TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B Slate 500 — Subtext

FONT_FAMILY  = "Prompt"

# 16:9 Widescreen Geometry
CONTENT_W = Inches(11.533)
COL2_W    = Inches(5.466);  COL2_X1 = Inches(0.90);  COL2_X2 = Inches(6.966)
COL3_W    = Inches(3.544);  COL3_X1 = Inches(0.90);  COL3_X2 = Inches(4.894);  COL3_X3 = Inches(8.888)

def apply_canvas(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.500))
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_BG
    bg.line.fill.background()
    return bg

def add_hairline(slide, left, top, width, vertical=False, color=C_LINE):
    size = (Inches(0.015), width) if vertical else (width, Inches(0.015))
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, *size)
    div.fill.solid()
    div.fill.fore_color.rgb = color
    div.line.fill.background()
    return div

def add_header(slide, category_text, title_text, subtitle_text=None):
    tb = slide.shapes.add_textbox(Inches(0.90), Inches(0.38), CONTENT_W, Inches(1.20))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.text = category_text.upper()
    p0.font.name = FONT_FAMILY
    p0.font.size = Pt(11.5)
    p0.font.bold = True
    p0.font.color.rgb = C_BLUE
    p0.space_after = Pt(2)
    
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(23)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY
    p1.space_after = Pt(4)
    
    if subtitle_text:
        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.name = FONT_FAMILY
        p2.font.size = Pt(13)
        p2.font.color.rgb = C_TEXT_MUTED
        add_hairline(slide, Inches(0.90), Inches(1.68), CONTENT_W)
    else:
        add_hairline(slide, Inches(0.90), Inches(1.38), CONTENT_W)

def create_flowing_column(slide, left, top, width, height, elements):
    """
    Creates a single unified TextFrame for a column.
    All text flows naturally from top to bottom.
    It is physically impossible for paragraphs to overlap each other!
    """
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    for i, elem in enumerate(elements):
        text = elem.get('text', '')
        size = elem.get('size', Pt(13.5))
        bold = elem.get('bold', False)
        color = elem.get('color', C_TEXT_MAIN)
        space_after = elem.get('space_after', Pt(6))
        space_before = elem.get('space_before', Pt(0))
        align = elem.get('align', PP_ALIGN.LEFT)
        line_spacing = elem.get('line_spacing', 1.18)

        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = text
        p.font.name = FONT_FAMILY
        p.font.size = size
        p.font.bold = bold
        p.font.color.rgb = color
        p.space_after = space_after
        p.space_before = space_before
        p.alignment = align
        p.line_spacing = line_spacing
    return tb

def build_presentation(output_path):
    prs = Presentation()
    prs.slide_width  = Inches(13.333)
    prs.slide_height = Inches(7.500)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: COVER
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout); apply_canvas(s1)
    
    # Title Block
    t_box = [
        {'text': 'SENIOR PROJECT PROPOSAL DEFENSE  |  สาขาวิชาเทคโนโลยีสารสนเทศ', 'size': Pt(12), 'bold': True, 'color': C_BLUE, 'space_after': Pt(8)},
        {'text': 'สกิลแมตช์ (SkillMatch)', 'size': Pt(34), 'bold': True, 'color': C_NAVY, 'space_after': Pt(4)},
        {'text': 'ระบบแนะนำงานและวิเคราะห์ช่องว่างทักษะด้านเทคโนโลยีสารสนเทศด้วยการเรียนรู้ของเครื่อง', 'size': Pt(22), 'bold': True, 'color': C_NAVY, 'space_after': Pt(10)},
        {'text': 'SkillMatch: IT Job Recommendation and Skill Gap Analysis System Using Machine Learning', 'size': Pt(13.5), 'color': C_TEXT_MUTED, 'space_after': Pt(0)}
    ]
    create_flowing_column(s1, Inches(0.90), Inches(1.10), CONTENT_W, Inches(2.60), t_box)
    add_hairline(s1, Inches(0.90), Inches(3.85), CONTENT_W)

    # Authors Block
    auth_box = [
        {'text': 'คณะผู้จัดทำโครงงาน', 'size': Pt(15), 'bold': True, 'color': C_NAVY, 'space_after': Pt(8)},
        {'text': 'นายธีรภัทธิ์ แก้วการไร่      รหัสประจำตัว 674230004', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(4)},
        {'text': 'นายปรเมศ ไม้ประเสริฐ     รหัสประจำตัว 674230020', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(6)},
        {'text': 'นักศึกษาชั้นปีที่ 3  หมู่เรียน 67/43', 'size': Pt(13), 'color': C_TEXT_MUTED, 'space_after': Pt(0)}
    ]
    create_flowing_column(s1, COL2_X1, Inches(4.20), COL2_W, Inches(2.50), auth_box)

    # Advisor Block
    adv_box = [
        {'text': 'อาจารย์ที่ปรึกษาและหลักสูตร', 'size': Pt(15), 'bold': True, 'color': C_NAVY, 'space_after': Pt(8)},
        {'text': 'อาจารย์ที่ปรึกษา: อาจารย์แก้วใจ อาภรณ์พิศาล', 'size': Pt(13.5), 'bold': True, 'color': C_BLUE, 'space_after': Pt(4)},
        {'text': 'สาขาวิชาเทคโนโลยีสารสนเทศ คณะวิทยาศาสตร์และเทคโนโลยี', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(6)},
        {'text': 'มหาวิทยาลัยราชภัฏนครปฐม  ภาคเรียนที่ 1 ปีการศึกษา 2569', 'size': Pt(13), 'color': C_TEXT_MUTED, 'space_after': Pt(0)}
    ]
    create_flowing_column(s1, COL2_X2, Inches(4.20), COL2_W, Inches(2.50), adv_box)

    # =========================================================================
    # SLIDE 2: CHAPTER 1 — 1.1 BACKGROUND & PROBLEMS
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout); apply_canvas(s2)
    add_header(s2, "1.1 BACKGROUND & PROBLEM STATEMENT", "ความเป็นมาและความสำคัญของปัญหา",
               "ความท้าทายในตลาดแรงงานไอทีและปัญหาของระบบแนะนำงานแบบดั้งเดิม")
    add_hairline(s2, Inches(6.40), Inches(1.85), Inches(5.10), vertical=True)

    s2_left = [
        {'text': 'ความต้องการทักษะเฉพาะทางในยุคดิจิทัล', 'size': Pt(16), 'bold': True, 'color': C_NAVY, 'space_after': Pt(10)},
        {'text': '• การเติบโตของอุตสาหกรรมดิจิทัล (depa, 2566):', 'size': Pt(14), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'ตลาดต้องการบุคลากรที่มีสมรรถนะตรงสายงาน สถาบันการศึกษาจึงต้องมุ่งเน้นการผลิตบัณฑิตให้สอดคล้องกับกรอบมาตรฐานคุณวุฒิ มคอ.2', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(14)},
        {'text': '• ปัญหาความไม่สอดคล้องของทักษะ (Skill Mismatch):', 'size': Pt(14), 'bold': True, 'color': C_RED, 'space_after': Pt(2)},
        {'text': 'ผู้เรียนไม่สามารถประเมินได้ชัดเจนว่าชุดทักษะที่ตนเองมี สอดคล้องกับกลุ่มอาชีพใดใน 8 ด้านตามมาตรฐานหลักสูตร', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(14)},
        {'text': '• ขาดข้อมูลเชิงลึกในการวางแผนพัฒนาตนเอง:', 'size': Pt(14), 'bold': True, 'color': C_NAVY, 'space_after': Pt(2)},
        {'text': 'นักศึกษาขาดทิศทางในการเตรียมความพร้อมก่อนออกฝึกประสบการณ์วิชาชีพ สหกิจศึกษา และก้าวเข้าสู่ตลาดแรงงานจริง', 'size': Pt(13), 'color': C_TEXT_MUTED, 'space_after': Pt(0)}
    ]
    create_flowing_column(s2, COL2_X1, Inches(1.85), COL2_W, Inches(5.10), s2_left)

    s2_right = [
        {'text': 'ข้อจำกัดของระบบค้นหาตำแหน่งงานแบบดั้งเดิม', 'size': Pt(16), 'bold': True, 'color': C_NAVY, 'space_after': Pt(10)},
        {'text': '• ข้อความกึ่งโครงสร้างและไร้โครงสร้าง (Unstructured):', 'size': Pt(14), 'bold': True, 'color': C_RED, 'space_after': Pt(2)},
        {'text': 'ประกาศงานไอทีมีความหลากหลายทางภาษาศาสตร์ มีคำพ้องความหมาย (Synonyms) และคำย่อ (Abbreviations) เป็นจำนวนมาก', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(14)},
        {'text': '• กับดักการค้นหาคำสำคัญตรงตัว (Lexical Mismatch):', 'size': Pt(14), 'bold': True, 'color': C_RED, 'space_after': Pt(2)},
        {'text': 'ระบบดั้งเดิมพึ่งพาการจับคู่คำสำคัญตรงตัว ขาดความยืดหยุ่นในการเข้าใจบริบททางภาษา จึงคลาดเคลื่อนและตัดโอกาสผู้หางาน', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(14)},
        {'text': '• ขาดกลไกวิเคราะห์ช่องว่างทักษะ (No Gap Analysis):', 'size': Pt(14), 'bold': True, 'color': C_RED, 'space_after': Pt(2)},
        {'text': 'ระบบทั่วไปไม่ชี้เป้าอย่างเป็นรูปธรรมว่าผู้หางาน "ยังขาดทักษะจำเป็นด้านใดบ้าง" ทำให้วางแผนพัฒนาตนเองไม่ได้', 'size': Pt(13), 'color': C_TEXT_MUTED, 'space_after': Pt(0)}
    ]
    create_flowing_column(s2, COL2_X2, Inches(1.85), COL2_W, Inches(5.10), s2_right)

    # =========================================================================
    # SLIDE 3: CHAPTER 1 — 1.2 PROPOSED SOLUTION FRAMEWORK
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout); apply_canvas(s3)
    add_header(s3, "1.2 PROPOSED SOLUTION FRAMEWORK", "แนวคิดในการแก้ไขปัญหา",
               "3 แนวทางดำเนินงานหลักด้วยการประมวลผลภาษาธรรมชาติและการเรียนรู้ของเครื่อง")

    s3_c1 = [
        {'text': 'แนวทางที่ 1', 'size': Pt(12), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'จำแนกสายงาน มคอ.2 ด้วย ML', 'size': Pt(15.5), 'bold': True, 'color': C_NAVY, 'space_after': Pt(10)},
        {'text': 'นำรายการทักษะความเชี่ยวชาญของผู้เรียนมาสกัดคุณลักษณะด้วย TF-IDF และใช้แบบจำลอง Multi-Class Logistic Regression ทำนายกลุ่มสายงานอาชีพที่สอดคล้องตามกรอบหลักสูตร มคอ.2 ทั้ง 8 กลุ่มอาชีพ', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(14)},
        {'text': '• สกัดคุณลักษณะทักษะด้วย TF-IDF', 'size': Pt(12.5), 'color': C_TEXT_MUTED, 'space_after': Pt(4)},
        {'text': '• ทำนายสายงานด้วย Logistic Regression', 'size': Pt(12.5), 'color': C_TEXT_MUTED, 'space_after': Pt(4)},
        {'text': '• ครอบคลุม 8 กลุ่มอาชีพ มคอ.2 ครบถ้วน', 'size': Pt(12.5), 'color': C_TEXT_MUTED, 'space_after': Pt(0)}
    ]
    create_flowing_column(s3, COL3_X1, Inches(1.85), COL3_W - Inches(0.20), Inches(5.10), s3_c1)

    s3_c2 = [
        {'text': 'แนวทางที่ 2', 'size': Pt(12), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'จับคู่ตำแหน่งงานด้วยทฤษฎีเซต', 'size': Pt(15.5), 'bold': True, 'color': C_NAVY, 'space_after': Pt(10)},
        {'text': 'กรองตำแหน่งงานเฉพาะในกลุ่มอาชีพที่ทำนายได้ และเปรียบเทียบความตรงกันของทักษะระหว่างผู้เรียนกับประกาศรับสมัครงานจริงในตลาดแรงงาน เพื่อจัดอันดับ 5 ตำแหน่งงานที่เหมาะสมที่สุด (Top-5)', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(14)},
        {'text': '• กรองเฉพาะสายงานที่ทำนายได้ ป้องกันงานข้ามสาย', 'size': Pt(12.5), 'color': C_TEXT_MUTED, 'space_after': Pt(4)},
        {'text': '• เปรียบเทียบความตรงกันของทักษะด้วย Set', 'size': Pt(12.5), 'color': C_TEXT_MUTED, 'space_after': Pt(4)},
        {'text': '• แนะนำตำแหน่งงานที่เหมาะสมที่สุด Top-5', 'size': Pt(12.5), 'color': C_TEXT_MUTED, 'space_after': Pt(0)}
    ]
    create_flowing_column(s3, COL3_X2, Inches(1.85), COL3_W - Inches(0.20), Inches(5.10), s3_c2)

    s3_c3 = [
        {'text': 'แนวทางที่ 3', 'size': Pt(12), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'วิเคราะห์ช่องว่างทักษะ & Readiness', 'size': Pt(15.5), 'bold': True, 'color': C_NAVY, 'space_after': Pt(10)},
        {'text': 'เปรียบเทียบผลต่างของชุดทักษะ เพื่อชี้เป้าทักษะที่ผู้เรียนยังขาดอยู่ และประเมินระดับความพร้อมในสายอาชีพ (Career Readiness) สำหรับใช้เป็นแนวทางในการวางแผนพัฒนาตนเองอย่างตรงจุด', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(14)},
        {'text': '• คำนวณผลต่างชุดทักษะ (Skill Gap)', 'size': Pt(12.5), 'color': C_TEXT_MUTED, 'space_after': Pt(4)},
        {'text': '• แยกทักษะที่มีออกจากทักษะที่ยังขาด', 'size': Pt(12.5), 'color': C_TEXT_MUTED, 'space_after': Pt(4)},
        {'text': '• ประเมินระดับความพร้อม Career Readiness', 'size': Pt(12.5), 'color': C_TEXT_MUTED, 'space_after': Pt(0)}
    ]
    create_flowing_column(s3, COL3_X3, Inches(1.85), COL3_W - Inches(0.20), Inches(5.10), s3_c3)

    # =========================================================================
    # SLIDE 4: CHAPTER 1 — 1.3 PROJECT OBJECTIVES
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout); apply_canvas(s4)
    add_header(s4, "1.3 PROJECT OBJECTIVES", "วัตถุประสงค์ของโครงงาน",
               "เป้าหมายหลัก 2 ประการในการวิจัยและพัฒนาระบบ (สอดรับตามเกณฑ์บทที่ 1)")
    add_hairline(s4, Inches(6.40), Inches(1.85), Inches(5.10), vertical=True)

    s4_left = [
        {'text': '1. การพัฒนาระบบแนะนำงานและวิเคราะห์ทักษะ', 'size': Pt(16), 'bold': True, 'color': C_BLUE, 'space_after': Pt(6)},
        {'text': 'เพื่อพัฒนาระบบแนะนำงานและวิเคราะห์ช่องว่างทักษะด้านเทคโนโลยีสารสนเทศด้วยการเรียนรู้ของเครื่อง (Machine Learning)', 'size': Pt(14), 'bold': True, 'color': C_NAVY, 'space_after': Pt(12)},
        {'text': '• สกัดคุณลักษณะทักษะผู้เรียนด้วย TF-IDF Feature Extraction', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(8)},
        {'text': '• ทำนายกลุ่มสายงานไอทีตามกรอบ มคอ.2 ทั้ง 8 กลุ่มอาชีพด้วยแบบจำลอง Multi-Class Logistic Regression', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(8)},
        {'text': '• กรองตำแหน่งงานและจัดอันดับด้วยทฤษฎีเซต พร้อมวิเคราะห์ผลต่างของชุดทักษะ (Skill Gap) และประเมิน Career Readiness', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(0)}
    ]
    create_flowing_column(s4, COL2_X1, Inches(1.85), COL2_W, Inches(5.10), s4_left)

    s4_right = [
        {'text': '2. การประเมินประสิทธิภาพแบบจำลองและระบบ', 'size': Pt(16), 'bold': True, 'color': C_NAVY, 'space_after': Pt(6)},
        {'text': 'เพื่อประเมินประสิทธิภาพความแม่นยำของแบบจำลองในการจำแนกกลุ่มอาชีพ และทดสอบประสิทธิภาพเวลาในการประมวลผลของระบบในการให้บริการจริง', 'size': Pt(14), 'bold': True, 'color': C_NAVY, 'space_after': Pt(12)},
        {'text': '• ประเมินความแม่นยำของโมเดล (Model Performance):', 'size': Pt(13.5), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'ทดสอบด้วย 5-Fold Stratified Cross-Validation วัดค่า Accuracy และ Macro F1-Score ครบทั้ง 8 กลุ่มอาชีพ มคอ.2', 'size': Pt(13), 'color': C_TEXT_MAIN, 'space_after': Pt(10)},
        {'text': '• ทดสอบเวลาในการประมวลผล (Processing Time / Latency):', 'size': Pt(13.5), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'วัดเวลาในการตอบสนองคำขอของระบบในการให้บริการจริง (Target Latency ต่ำกว่า 200 ms บนหน่วยความจำหลัก)', 'size': Pt(13), 'color': C_TEXT_MAIN, 'space_after': Pt(0)}
    ]
    create_flowing_column(s4, COL2_X2, Inches(1.85), COL2_W, Inches(5.10), s4_right)

    # =========================================================================
    # SLIDE 5: CHAPTER 1 — 1.4.1 SYSTEM SCOPE (Roles & Functions)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout); apply_canvas(s5)
    add_header(s5, "1.4.1 SYSTEM SCOPE: ROLES & FUNCTIONS", "ขอบเขตด้านหน้าที่การทำงานของระบบ",
               "การแบ่งสิทธิ์และบทบาทการทำงานระหว่างผู้ดูแลระบบและผู้ใช้งานทั่วไป")
    add_hairline(s5, Inches(6.40), Inches(1.85), Inches(5.10), vertical=True)

    s5_left = [
        {'text': '1.4.1.1 บทบาทผู้ดูแลระบบ (Administrator)', 'size': Pt(16), 'bold': True, 'color': C_NAVY, 'space_after': Pt(10)},
        {'text': '1. การจัดการข้อมูลตำแหน่งงาน:', 'size': Pt(14), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'สามารถนำเข้า จัดเตรียม และจัดการข้อมูลประกาศรับสมัครงานเข้าสู่ระบบฐานข้อมูล', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(14)},
        {'text': '2. การฝึกสอนและประเมินโมเดล:', 'size': Pt(14), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'สามารถดำเนินการฝึกสอน (Train) และประเมินประสิทธิภาพของแบบจำลองการเรียนรู้ของเครื่องในระดับระบบ', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(14)},
        {'text': '• การบำรุงรักษาคลังคำศัพท์:', 'size': Pt(14), 'bold': True, 'color': C_NAVY, 'space_after': Pt(2)},
        {'text': 'ตรวจสอบและปรับปรุงพจนานุกรมคำพ้อง (Canonical Map) เพื่อรองรับคำศัพท์เทคนิคใหม่ๆ ในตลาด', 'size': Pt(13), 'color': C_TEXT_MUTED, 'space_after': Pt(0)}
    ]
    create_flowing_column(s5, COL2_X1, Inches(1.85), COL2_W, Inches(5.10), s5_left)

    s5_right = [
        {'text': '1.4.1.2 บทบาทผู้ใช้งานระบบ (User / Student)', 'size': Pt(16), 'bold': True, 'color': C_NAVY, 'space_after': Pt(10)},
        {'text': '1. การเลือกชุดทักษะความเชี่ยวชาญ:', 'size': Pt(14), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'สามารถค้นหาและเลือกทักษะความเชี่ยวชาญทางไอทีของตนเองผ่านระบบ', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(14)},
        {'text': '2. การดูผลการทำนายกลุ่มอาชีพ มคอ.2:', 'size': Pt(14), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'สามารถดูผลการทำนายกลุ่มอาชีพไอทีที่สอดคล้องตามกรอบ มคอ.2 ทั้ง 8 กลุ่มอาชีพ พร้อมระดับความพร้อม', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(14)},
        {'text': '3. การดูผลงานแนะนำและช่องว่างทักษะ:', 'size': Pt(14), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'สามารถดูผลการแนะนำตำแหน่งงานที่เหมาะสมที่สุด 5 อันดับแรก พร้อมรายงานสรุปทักษะที่ตรงกันและทักษะที่ยังขาดอยู่', 'size': Pt(13), 'color': C_TEXT_MUTED, 'space_after': Pt(0)}
    ]
    create_flowing_column(s5, COL2_X2, Inches(1.85), COL2_W, Inches(5.10), s5_right)

    # =========================================================================
    # SLIDE 6: CHAPTER 1 — 1.4.1.3 DATA SCOPE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout); apply_canvas(s6)
    add_header(s6, "1.4.1.3 DATA SCOPE & TAXONOMY", "ขอบเขตด้านข้อมูลและการรวบรวม",
               "กรอบมาตรฐาน 8 กลุ่มอาชีพ มคอ.2 และชุดข้อมูลประกาศงานจริง 160 ตำแหน่ง")
    add_hairline(s6, Inches(6.40), Inches(1.85), Inches(5.10), vertical=True)

    roles_block = [
        {'text': 'กรอบมาตรฐาน 8 กลุ่มอาชีพ มคอ.2 สาขาไอที', 'size': Pt(16), 'bold': True, 'color': C_NAVY, 'space_after': Pt(10)},
        {'text': '1. กลุ่มเจ้าหน้าที่เทคนิคและสนับสนุนคอมพิวเตอร์', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(4)},
        {'text': '2. กลุ่มผู้ดูแลระบบเครือข่ายและเครื่องแม่ข่าย', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(4)},
        {'text': '3. กลุ่มนักพัฒนาและออกแบบสื่อผสม (Multimedia / UI-UX)', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(4)},
        {'text': '4. กลุ่มผู้ประสานงานและจัดการโครงการสารสนเทศ', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(4)},
        {'text': '5. กลุ่มนักวิเคราะห์และออกแบบระบบสารสนเทศ', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(4)},
        {'text': '6. กลุ่มนักพัฒนาซอฟต์แวร์และแอปพลิเคชัน', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(4)},
        {'text': '7. กลุ่มนักพัฒนาและจัดการเว็บไซต์', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(4)},
        {'text': '8. กลุ่มผู้เชี่ยวชาญเฉพาะด้านเทคโนโลยีสารสนเทศ (Data / AI)', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(0)}
    ]
    create_flowing_column(s6, COL2_X1, Inches(1.85), COL2_W, Inches(5.10), roles_block)

    data_block = [
        {'text': 'ข้อมูลประกาศงานและพจนานุกรมคำพ้อง', 'size': Pt(16), 'bold': True, 'color': C_NAVY, 'space_after': Pt(10)},
        {'text': '1. ข้อมูลคำศัพท์ทักษะไอทีและพจนานุกรมคำพ้อง:', 'size': Pt(14), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'สำหรับใช้ในการประมวลผลและจัดการคำศัพท์คุณสมบัติทางไอที พร้อมระบบ Canonical Mapping รองรับคำย่อและคำพ้อง', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(14)},
        {'text': '2. ข้อมูลประกาศรับสมัครงานจริง 160 ตำแหน่งงาน:', 'size': Pt(14), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'รวบรวมจากเว็บไซต์รับสมัครงานชั้นนำในประเทศไทย จำนวน 160 ตำแหน่งงาน (กลุ่มอาชีพละ 20 ตำแหน่งงาน) ครอบคลุมครบ 8 กลุ่มอาชีพตามกรอบหลักสูตร มรภ.นครปฐม', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(14)},
        {'text': '• การควบคุมความสมดุล (Class Balance):', 'size': Pt(14), 'bold': True, 'color': C_NAVY, 'space_after': Pt(2)},
        {'text': 'ควบคุมสัดส่วนให้สมดุลเป๊ะกลุ่มละ 20 งาน ป้องกันปัญหาโมเดลเอนเอียง (Bias) ไปยังกลุ่มอาชีพที่มีประกาศงานมากเกินไป', 'size': Pt(13), 'color': C_TEXT_MUTED, 'space_after': Pt(0)}
    ]
    create_flowing_column(s6, COL2_X2, Inches(1.85), COL2_W, Inches(5.10), data_block)

    # =========================================================================
    # SLIDE 7: CHAPTER 1 — 1.4.2 & 1.4.3 ENVIRONMENT SCOPE
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout); apply_canvas(s7)
    add_header(s7, "1.4.2 & 1.4.3 ENVIRONMENT SCOPE", "ขอบเขตสภาพแวดล้อมฮาร์ดแวร์และซอฟต์แวร์",
               "โครงสร้างพื้นฐานและเครื่องมือที่ใช้ในการวิจัยและพัฒนาระบบ")
    add_hairline(s7, Inches(6.40), Inches(1.85), Inches(5.10), vertical=True)

    hw_block = [
        {'text': '1.4.2 ฮาร์ดแวร์ที่ใช้ในการพัฒนา', 'size': Pt(16), 'bold': True, 'color': C_NAVY, 'space_after': Pt(10)},
        {'text': '1. หน่วยประมวลผลกลาง (CPU):', 'size': Pt(14), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'Intel Core i5-10300H CPU ความเร็ว 2.50 GHz (4 Cores / 8 Threads) สำหรับประมวลผลข้อมูลและฝึกสอนแบบจำลอง', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(14)},
        {'text': '2. หน่วยความจำหลัก (RAM):', 'size': Pt(14), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'ขนาด 16.0 GB สำหรับแคชโมเดลและข้อมูลงานบน Memory เพื่อตอบสนองคำขอแบบ Real-time', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(14)},
        {'text': '3. หน่วยจัดเก็บข้อมูล (Storage):', 'size': Pt(14), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'Solid State Drive (SSD) ขนาดความจุ 512 GB เพื่อความรวดเร็วในการอ่านและเขียนข้อมูล', 'size': Pt(13), 'color': C_TEXT_MUTED, 'space_after': Pt(0)}
    ]
    create_flowing_column(s7, COL2_X1, Inches(1.85), COL2_W, Inches(5.10), hw_block)

    sw_block = [
        {'text': '1.4.3 ซอฟต์แวร์ที่ใช้ในการพัฒนา', 'size': Pt(16), 'bold': True, 'color': C_NAVY, 'space_after': Pt(10)},
        {'text': '1. ระบบปฏิบัติการและสภาพแวดล้อม:', 'size': Pt(14), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'Microsoft Windows 10 ร่วมกับ Visual Studio Code สำหรับพัฒนาโปรแกรมและจัดการเวอร์ชันโค้ด', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(14)},
        {'text': '2. ฝั่งเซิร์ฟเวอร์และแบบจำลอง (Backend & ML Engine):', 'size': Pt(14), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'ภาษา Python ร่วมกับ FastAPI, Scikit-learn, Pandas และ NumPy สำหรับสร้าง REST API และคำนวณโมเดล', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(14)},
        {'text': '3. ส่วนต่อประสานผู้ใช้งาน (Frontend Layer):', 'size': Pt(14), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'ภาษา HTML5, JavaScript (ES6+), Vanilla CSS ร่วมกับ Tailwind CSS (CDN), SweetAlert2 และ Font Awesome 6', 'size': Pt(13), 'color': C_TEXT_MUTED, 'space_after': Pt(0)}
    ]
    create_flowing_column(s7, COL2_X2, Inches(1.85), COL2_W, Inches(5.10), sw_block)

    # =========================================================================
    # SLIDE 8: CHAPTER 1 — 1.5 PROJECT TIMELINE (CRISP-DM)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout); apply_canvas(s8)
    add_header(s8, "1.5 PROJECT TIMELINE (CRISP-DM)", "กรอบระยะเวลาและขั้นตอนการดำเนินงาน (16 สัปดาห์)",
               "การดำเนินงานวิจัยและพัฒนาระบบตามลำดับขั้นตอน CRISP-DM ทั้ง 6 ขั้นตอน ดังตารางที่ 1.1")
    add_hairline(s8, Inches(6.40), Inches(1.85), Inches(5.10), vertical=True)

    t_left = [
        {'text': 'ขั้นตอนที่ 1: การศึกษาบริบทและกำหนดเป้าหมาย (สัปดาห์ 1 - 2)', 'size': Pt(14.5), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'ศึกษาปัญหา Skill Mismatch ทำความเข้าใจกรอบมาตรฐาน มคอ.2 ทั้ง 8 กลุ่มอาชีพ และกำหนดขอบเขตระบบ', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(16)},
        {'text': 'ขั้นตอนที่ 2: การทำความเข้าใจและสำรวจข้อมูล (สัปดาห์ 3 - 5)', 'size': Pt(14.5), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'รวบรวมประกาศงานไอทีจริง 160 งาน (กลุ่มละ 20 งานเป๊ะ) สำรวจรูปแบบข้อความกึ่งโครงสร้างและทักษะจำเป็น', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(16)},
        {'text': 'ขั้นตอนที่ 3: การเตรียมข้อมูลและจัดระเบียบคำศัพท์ (สัปดาห์ 6 - 8)', 'size': Pt(14.5), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'ทำความสะอาดข้อมูล จัดทำพจนานุกรมคำพ้อง (Canonical Map) สกัดทักษะเฉพาะทาง และแปลงเวกเตอร์ TF-IDF', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(0)}
    ]
    create_flowing_column(s8, COL2_X1, Inches(1.85), COL2_W, Inches(5.10), t_left)

    t_right = [
        {'text': 'ขั้นตอนที่ 4: การสร้างและฝึกสอนแบบจำลอง (สัปดาห์ 9 - 11)', 'size': Pt(14.5), 'bold': True, 'color': C_NAVY, 'space_after': Pt(2)},
        {'text': 'ฝึกสอน Multi-Class Logistic Regression จำแนก 8 กลุ่มอาชีพ พัฒนากลไกจัดอันดับ Top-5 และสกัด Skill Gap ด้วยเซต', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(16)},
        {'text': 'ขั้นตอนที่ 5: การประเมินประสิทธิภาพแบบจำลองและระบบ (สัปดาห์ 12 - 14)', 'size': Pt(14.5), 'bold': True, 'color': C_NAVY, 'space_after': Pt(2)},
        {'text': 'ทดสอบความแม่นยำด้วย 5-Fold Stratified Cross-Validation (Accuracy, Macro F1) และทดสอบเวลาตอบสนอง API (Latency)', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(16)},
        {'text': 'ขั้นตอนที่ 6: การพัฒนาและติดตั้งระบบเพื่อใช้งานจริง (สัปดาห์ 15 - 16)', 'size': Pt(14.5), 'bold': True, 'color': C_NAVY, 'space_after': Pt(2)},
        {'text': 'เชื่อมต่อส่วนต่อประสานผู้ใช้งาน SPA เข้ากับ FastAPI Engine ทดสอบระบบแบบบูรณาการ และจัดทำเล่มรายงานสมบูรณ์', 'size': Pt(13.5), 'color': C_TEXT_MAIN, 'space_after': Pt(0)}
    ]
    create_flowing_column(s8, COL2_X2, Inches(1.85), COL2_W, Inches(5.10), t_right)

    # =========================================================================
    # SLIDE 9: CHAPTER 1 — 1.6 EXPECTED BENEFITS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout); apply_canvas(s9)
    add_header(s9, "1.6 EXPECTED BENEFITS", "ประโยชน์ที่คาดว่าจะได้รับจากโครงงาน",
               "คุณค่าและการนำผลลัพธ์ของโครงงานไปประยุกต์ใช้งานจริง สอดรับกับวัตถุประสงค์ 1:1")
    add_hairline(s9, Inches(6.40), Inches(1.85), Inches(5.10), vertical=True)

    s9_left = [
        {'text': '1.6.1 ด้านระบบและแบบจำลองการเรียนรู้ของเครื่อง', 'size': Pt(16), 'bold': True, 'color': C_BLUE, 'space_after': Pt(6)},
        {'text': 'ได้ระบบแนะนำงานและวิเคราะห์ช่องว่างทักษะด้านเทคโนโลยีสารสนเทศด้วยการเรียนรู้ของเครื่อง และสามารถจำแนกกลุ่มอาชีพไอทีตามมาตรฐานหลักสูตรได้อย่างถูกต้องและแม่นยำ', 'size': Pt(14), 'bold': True, 'color': C_NAVY, 'space_after': Pt(14)},
        {'text': '• ระบบสกัดคุณลักษณะทักษะไอที (TF-IDF):', 'size': Pt(13.5), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'แปลงข้อมูลรายการทักษะทางเทคนิคให้อยู่ในรูปเวกเตอร์ตัวเลขได้อย่างมีประสิทธิภาพ พร้อมระบบจัดการคำพ้อง (Canonical Map)', 'size': Pt(13), 'color': C_TEXT_MAIN, 'space_after': Pt(12)},
        {'text': '• ต้นแบบโมเดลจำแนกกลุ่มอาชีพ มคอ.2 ทั้ง 8 ด้าน:', 'size': Pt(13.5), 'bold': True, 'color': C_BLUE, 'space_after': Pt(2)},
        {'text': 'โมเดล Multi-Class Logistic Regression ที่มีความโปร่งใส ตรวจสอบความน่าจะเป็นได้ ป้องกันการจำข้อสอบด้วย Regularization', 'size': Pt(13), 'color': C_TEXT_MAIN, 'space_after': Pt(0)}
    ]
    create_flowing_column(s9, COL2_X1, Inches(1.85), COL2_W, Inches(5.10), s9_left)

    s9_right = [
        {'text': '1.6.2 ด้านระบบช่วยตัดสินใจและการวางแผนพัฒนาตนเอง', 'size': Pt(16), 'bold': True, 'color': C_NAVY, 'space_after': Pt(6)},
        {'text': 'ได้ระบบช่วยตัดสินใจแนะนำตำแหน่งงานและวิเคราะห์ช่องว่างทักษะที่โปร่งใส ตรวจสอบได้ เพื่อช่วยให้นักศึกษาและผู้หางานสามารถวางแผนพัฒนาตนเองได้อย่างมีทิศทางและสอดคล้องกับความต้องการของตลาดแรงงานไอทีอย่างแท้จริง', 'size': Pt(14), 'bold': True, 'color': C_NAVY, 'space_after': Pt(14)},
        {'text': '• การแนะนำงาน Top-5 ที่ตรงบริบทจริง:', 'size': Pt(13.5), 'bold': True, 'color': C_NAVY, 'space_after': Pt(2)},
        {'text': 'คัดกรองตำแหน่งงานเฉพาะในกลุ่มอาชีพที่สอดคล้อง พร้อมคำนวณ Match Rate สะท้อนความตรงกันของทักษะจริง', 'size': Pt(13), 'color': C_TEXT_MAIN, 'space_after': Pt(12)},
        {'text': '• ชี้เป้าช่องว่างทักษะ (Skill Gap) และประเมินความพร้อม:', 'size': Pt(13.5), 'bold': True, 'color': C_NAVY, 'space_after': Pt(2)},
        {'text': 'แยก "ทักษะที่มี" และ "ทักษะที่ยังขาด" อย่างชัดเจน พร้อมระดับ Career Readiness ช่วยให้วางแผน Upskill ได้ตรงจุด', 'size': Pt(13), 'color': C_TEXT_MAIN, 'space_after': Pt(0)}
    ]
    create_flowing_column(s9, COL2_X2, Inches(1.85), COL2_W, Inches(5.10), s9_right)

    # =========================================================================
    # SLIDE 10: CONCLUSION & Q&A
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout); apply_canvas(s10)
    end_box = [
        {'text': 'ขอบคุณครับ', 'size': Pt(44), 'bold': True, 'color': C_NAVY, 'space_after': Pt(12), 'align': PP_ALIGN.CENTER},
        {'text': 'ยินดีรับฟังทุกข้อคิดเห็นและข้อเสนอแนะ เพื่อนำไปพัฒนาโครงงานให้สมบูรณ์ยิ่งขึ้นครับ', 'size': Pt(18), 'bold': True, 'color': C_BLUE, 'space_after': Pt(24), 'align': PP_ALIGN.CENTER},
        {'text': 'อาจารย์ที่ปรึกษาโครงงาน: อาจารย์แก้วใจ อาภรณ์พิศาล', 'size': Pt(15), 'bold': True, 'color': C_NAVY, 'space_after': Pt(8), 'align': PP_ALIGN.CENTER},
        {'text': 'คณะผู้จัดทำ: นายธีรภัทธิ์ แก้วการไร่ (674230004)   |   นายปรเมศ ไม้ประเสริฐ (674230020)   |   หมู่เรียน 67/43', 'size': Pt(13.5), 'bold': True, 'color': C_TEXT_MAIN, 'space_after': Pt(6), 'align': PP_ALIGN.CENTER},
        {'text': 'สาขาวิชาเทคโนโลยีสารสนเทศ คณะวิทยาศาสตร์และเทคโนโลยี มหาวิทยาลัยราชภัฏนครปฐม', 'size': Pt(12.5), 'color': C_TEXT_MUTED, 'space_after': Pt(0), 'align': PP_ALIGN.CENTER}
    ]
    create_flowing_column(s10, Inches(0.90), Inches(1.80), CONTENT_W, Inches(4.50), end_box)

    # Save
    prs.save(output_path)
    print(f"10-Slide Chapter 1 Canva-ready presentation created at: {output_path}")

if __name__ == "__main__":
    out_dir = r"c:\Users\ASUS\Documents\modelJD_V4\slide"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "SkillMatch_IT_Proposal_Defense_CANVA_READY.pptx")
    build_presentation(out_file)

