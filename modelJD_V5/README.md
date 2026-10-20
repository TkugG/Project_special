# SkillMatch IT: ระบบจำแนกสายงานและแนะนำตำแหน่งงานไอทีด้วย Machine Learning
> โครงงานปริญญานิพนธ์สาขาเทคโนโลยีสารสนเทศ (IT) ตามกรอบมาตรฐานหลักสูตร IT ผสานข้อมูลตลาดแรงงานไอทีไทย

---

## 📌 บทนำและภาพรวมของระบบ (Project Overview)

**SkillMatch IT** คือระบบวิเคราะห์ทักษะและแนะนำตำแหน่งงานสำหรับนักศึกษาและผู้สนใจสายไอที โดยผสานข้อมูลมาตรฐานหลักสูตร (ตามหลักสูตร IT) ร่วมกับประกาศรับสมัครงานจริงในประเทศไทย (253 ตำแหน่งงาน)

ระบบถูกออกแบบภายใต้หลักการ **KISS (Keep It Simple, Stupid)** ที่โปร่งใส เข้าใจง่าย และถูกต้องตามหลักการทางสถิติ แบ่งเป็น 2 ส่วนหลัก:
1. **ส่วนจำแนกสายงาน (Career Classification):** ใช้โมเดล **Multi-Class Logistic Regression** ร่วมกับ **TF-IDF Vectorizer** ทำนายว่าทักษะที่ผู้ใช้มี ตรงกับกลุ่มอาชีพใดใน 8 กลุ่มตามหลักสูตร IT มากที่สุด พร้อมคำนวณระดับความพร้อม (Career Readiness %)
2. **ส่วนแนะนำตำแหน่งงาน (Job Recommendation):** ใช้เทคนิค **Content-Based Filtering** คำนวณเปอร์เซ็นต์ความตรงของทักษะ (Exact Skill Overlap %) ผสานกับความคล้ายคลึงเชิงบริบทคำศัพท์ (TF-IDF Cosine Similarity %) และความน่าจะเป็นของสายงานจากโมเดล ML (Softmax Role Probability 20%) ตามสัดส่วน $50:30:20$ เพื่อแนะนำตำแหน่งงานจริงในไทย Top 5 พร้อมวิเคราะห์ช่องว่างทักษะ (Skill Gap) ด้วยทฤษฎีเซต

---

## 🏛️ สถาปัตยกรรมระบบ (System Architecture)

```
[ผู้ใช้กรอกทักษะ เช่น: golang, js, k8s, reactjs]
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│     เลเยอร์ที่ 1: Canonical Skill Normalization Layer    │
│  แปลงคำพ้อง/ตัวย่อเป็นคำมาตรฐาน (O(1) Taxonomy Mapping):│
│  • golang -> go              • k8s -> kubernetes        │
│  • js -> javascript          • reactjs -> react         │
│  • postgres -> postgresql    • ux/ui -> ui/ux           │
│  (คุ้มครองอักขระพิเศษ: c++, c#, .net, node.js, ci/cd)     │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│     เลเยอร์ที่ 2: TF-IDF Text Feature Extraction        │
│  แปลงรายการคำศัพท์ทักษะมาตรฐานเป็นเวกเตอร์ตัวเลข         │
│  (token_pattern เก็บสัญลักษณ์ภาษา เช่น c#, .net, c++)   │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│  เลเยอร์ที่ 3: Multi-Class Logistic Regression (C=0.3)  │
│  ทำนายความน่าจะเป็นของ 8 กลุ่มอาชีพตามหลักสูตร IT:      │
│  • 8.1 IT Support Specialist  • 8.5 System Analyst      │
│  • 8.2 Network Administrator  • 8.6 Software Developer  │
│  • 8.3 Multimedia Designer    • 8.7 Web Developer       │
│  • 8.4 IT Project Manager     • 8.8 IT Specialist       │
│  (5-Fold CV Accuracy: 98.02%, Macro F1: 97.94%)         │
└───────────────────┬─────────────────────────────────────┘
                    │ (ผลทำนายสายงานและความน่าจะเป็นรายกลุ่ม)
                    ▼
┌─────────────────────────────────────────────────────────┐
│  เลเยอร์ที่ 4: Hybrid Job Matching & Ranking (~6.85ms)  │
│  • Skill Overlap Ratio (50%): Hard Skills ตรงเป๊ะ       │
│  • Cosine Similarity   (30%): ความคล้ายเชิงบริบทคำศัพท์ │
│  • Softmax Role Prob   (20%): ความน่าจะเป็นสายงาน ML     │
│  • Skill Gap Analysis: คำนวณ Matched / Missing ผ่าน Set │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│        Dual-Section Output & Diversity Ranking          │
│  1) Target Career Analysis: เจาะลึกความพร้อมสายงานเป้าหมาย│
│  2) Skill Matched Top-5: แนะนำงานจริงพร้อมชิป Skill Gap │
└─────────────────────────────────────────────────────────┘
```

---

## 🔬 ระเบียบวิธีวิจัยและผลการทดลอง (Methodology & Evaluation)

### 1. ชุดข้อมูลและการกำหนด Ground Truth ($y$)
- **ชุดข้อมูลมาตรฐานและกรณีศึกษาจริง (Curated Curriculum Benchmark):** รวบรวมข้อมูลตำแหน่งงานรวม 253 ตำแหน่ง โดยอิงจากชุดข้อมูลมาตรฐานตามกรอบสมรรถนะหลักสูตร IT (Curriculum Benchmark Dataset 240 ตำแหน่ง) บูรณาการร่วมกับกรณีศึกษาตำแหน่งงานจริงจากตลาดแรงงานไอทีไทย (13 ตำแหน่งงาน) ที่ผ่านการสอบทานคุณภาพข้อมูล (Quality Curation) เพื่อให้สะท้อนทักษะวิชาชีพจริง โดยกระจายตัวครอบคลุม 8 กลุ่มอาชีพอย่างสมดุล (กลุ่มละ 30–37 ตำแหน่งงาน)
- **ค่าเฉลยที่แท้จริง (Ground Truth $y$):** ใช้รหัสกลุ่มอาชีพ (`CurriculumRoleID` 8.1 - 8.8) ของตำแหน่งงานจริง ปราศจากการสร้างฉลากเทียมด้วยเงื่อนไข If-Else
- **การกำจัด Data Leakage:** ตัดฟิลด์ `Title` (ชื่อตำแหน่ง) ออกจากการเทรนทั้งหมด เพื่อป้องกันโมเดลท่องจำชื่อตำแหน่ง คงเหลือเฉพาะฟิลด์ทักษะ (`Skills`) เท่านั้น

### 2. ผลการทดสอบ 5-Fold Stratified Cross-Validation (ไม่มี Data Leakage)
ทดสอบโมเดลบนข้อมูลตำแหน่งงาน 253 ตำแหน่ง ด้วยการแบ่ง 5 ส่วนอย่างยุติธรรม (รักษาสัดส่วนคลาสเท่ากันทุก Fold):
- **Accuracy (ความแม่นยำรวม):** **98.02%** (± 1.77%)
- **Macro Precision (ความเที่ยงตรงเฉลี่ย):** **98.51%**
- **Macro Recall (ความครอบคลุมเฉลี่ย):** **97.92%**
- **Macro F1-Score (คะแนนเฉลี่ย F1):** **97.94%**

### 3. ตาราง Confusion Matrix (จุดสับสนของโมเดลตามความเป็นจริงของตลาดแรงงาน)
```
  แนวตั้ง = ค่าจริง (Actual) | แนวนอน = ค่าทำนาย (Predicted)
         8.1   8.2   8.3   8.4   8.5   8.6   8.7   8.8
  --------------------------------------------------------
   8.1 |    32     0     0     0     0     0     0     0  (100.0%)
   8.2 |     0    26     0     0     0     0     0     4  <-- Network โดนทายสับสนเป็น Cloud/Security
   8.3 |     0     0    30     0     0     0     0     0  (100.0%)
   8.4 |     0     0     0    32     0     0     0     0  (100.0%)
   8.5 |     0     0     0     0    30     0     0     0  (100.0%)
   8.6 |     0     0     0     0     0    37     0     0  (100.0%)
   8.7 |     0     0     0     0     0     0    30     0  (100.0%)
   8.8 |     0     0     0     0     0     1     0    31  <-- Specialist โดนทายสับสนเป็น Dev (Python/Data)
```
> **การอภิปรายผล (Discussion):** 
> 1. ทำนายถูกต้องสมบูรณ์ 100% ใน 6 กลุ่มอาชีพ (8.1, 8.3, 8.4, 8.5, 8.6, 8.7)
> 2. ความคลาดเคลื่อนเพียง 5 รายการจาก 253 ตำแหน่งงาน (1.98%) เกิดขึ้นเฉพาะระหว่างสายงานที่มีชุดทักษะคาบเกี่ยวกันจริงในอุตสาหกรรม (Interdisciplinary Skills):
>    - สาย Network (8.2) ปนกับ Specialist (8.8) จำนวน 4 งาน เนื่องจากมีคำว่า Cloud Infrastructure, Linux Server, Firewall และ Network Security
>    - สาย Specialist (8.8) ปนกับ Software Developer (8.6) จำนวน 1 งาน เนื่องจากงานด้าน Data Science/Data Pipeline มีการใช้ Python และ Docker ร่วมกัน

### 4. ตัวอย่างคีย์เวิร์ดสำคัญที่โมเดลเรียนรู้ได้ (Explainable AI - XAI)
ตรวจสอบค่าน้ำหนักสัมประสิทธิ์ของ Logistic Regression ($w$) เพื่อยืนยันความโปร่งใสของโมเดล:
- **8.1 (IT Support):** troubleshooting, hardware, helpdesk, active directory, windows
- **8.2 (Network Admin):** network, cisco, routing, bash, firewall, switching
- **8.3 (Multimedia):** design, ui, ux, figma, effects, photoshop, illustrator
- **8.4 (Project Manager):** management, jira, scrum, communication, sdlc, agile
- **8.5 (System Analyst):** analysis, system design, business, uml, requirements
- **8.6 (Software Developer):** rest api, java, c#, .net, python, git, docker
- **8.7 (Web Developer):** web, css3, html5, php, javascript, responsive
- **8.8 (IT Specialist):** machine learning, cloud, security, deep learning, data

---

## 🔌 RESTful API Endpoints (FastAPI Backend)

| Endpoint | HTTP Method | รายละเอียดการทำงาน |
| :--- | :---: | :--- |
| `/` | `GET` | ตรวจสอบสถานะการทำงานของระบบ (Health Check) |
| `/ui` | `GET` | หน้าเว็บแอปพลิเคชันหลักของระบบ (`index.html`) |
| `/api/skills` | `GET` | คืนค่ารายการคำศัพท์ทักษะเฉพาะที่มีตำแหน่งงานรองรับจริงในตลาดไอทีไทย (216 ทักษะ) |
| `/api/roles` | `GET` | คืนค่าข้อมูล 8 กลุ่มอาชีพตามหลักสูตร IT พร้อมสมรรถนะและ Core Skills |
| `/api/recommend` | `POST` | ทำนายสายงาน, คำนวณความพร้อม, แนะนำงาน Top 5 และวิเคราะห์ Skill Gap ในคำขอเดียว |

---

## 🚀 คู่มือการรันและทดสอบระบบ (Execution Guide)

### 0. วิธีรันระบบในคลิกเดียว (One-Click Launch สำหรับ Windows)
ดับเบิ้ลคลิกไฟล์ `run.bat` หรือรันผ่าน Terminal:
```cmd
run.bat
```
*ระบบจะตรวจสอบ Python, Dependencies, Model, เคลียร์พอร์ตที่ค้าง และเปิดเว็บเบราว์เซอร์ให้อัตโนมัติทันที*
- **บังคับเทรนโมเดลใหม่:** `run.bat train`
- **รันชุดทดสอบความถูกต้อง:** `run.bat test`

### 1. ติดตั้ง Dependencies (กรณีรัน Manual)
```bash
pip install -r requirements.txt
```

### 2. รันการเทรนโมเดลจำแนกกลุ่มอาชีพ
```bash
python src/train.py
```

### 3. รันชุดทดสอบความถูกต้องของระบบ (Validation Suite)
```bash
python src/validate.py
```

### 4. รัน Web Application Server (FastAPI)
```bash
python src/main.py
```
เปิดบราวเซอร์ไปที่: `http://127.0.0.1:8000/ui`

---

## 🎯 แนวทางการตอบคำถามกรรมการสอบโครงงาน (Defense Cheatsheet)

สำหรับคู่มือเตรียมตัวสอบข้อเสนอโครงงาน (Proposal Defense), โครงสร้างสไลด์นำเสนอ 11 สไลด์, เจาะลึก 10 คำถามไม้ตายของกรรมการพร้อมสคริปต์ตอบจริง, โพยตัวเลขสถิติ, และสคริปต์ Live Demo 2 นาที ได้ถูกรวบรวมและจัดระเบียบไว้อย่างสมบูรณ์ใน:

👉 **[DEFENSE_CHEAT_SHEET.md](DEFENSE_CHEAT_SHEET.md)**


