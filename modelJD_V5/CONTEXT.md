# CONTEXT.md — SkillMatch IT: AI Handover & System Status Note
> **เอกสารสรุปบริบทและสถานะปัจจุบันของระบบ สำหรับ AI และนักพัฒนาที่เข้ามารับช่วงต่อ**  
> *(อัปเดตล่าสุด: กันยายน 2026 | เวอร์ชันระบบ: v4.6.0)*

---

## 🧭 1. ภาพรวมโปรเจกต์ (Project Essence)

* **ชื่อระบบ:** SkillMatch IT (ระบบจับคู่ทักษะและแนะนำตำแหน่งงานไอทีตามกรอบหลักสูตร IT)
* **โจทย์ของโครงงาน:** 
  1. วิเคราะห์และทำนายว่าทักษะของผู้ใช้ (Hard Skills) สอดคล้องกับ **8 กลุ่มอาชีพตามหลักสูตร มคอ.2 สาขาเทคโนโลยีสารสนเทศ (IT)** กลุ่มใดมากที่สุด (ใช้ Machine Learning)
  2. แนะนำตำแหน่งงานจริงในประเทศไทยที่มีความต้องการทักษะตรงกับผู้ใช้ (ใช้ Content-Based Filtering & Hybrid Scoring) พร้อมแสดง Skill Gap Analysis เพื่อเป็นแนวทางพัฒนาตนเอง
* **สถาปัตยกรรม:** Client-Server แบบ SPA (Single Page Application)
  * **Frontend:** Vanilla JavaScript (ES6+ Modules), Tailwind CSS (CDN), FontAwesome 6, SweetAlert2 (ไม่มี Node/Vite Build Step ใดๆ ทั้งสิ้น)
  * **Backend:** Python FastAPI, Uvicorn, Scikit-Learn, Pandas, NumPy
  * **ML Model:** TF-IDF Vectorizer + Multi-Class Logistic Regression ($C=0.5$)

---

## 🏛️ 2. มาตรฐาน 8 กลุ่มอาชีพ มคอ.2 (Curriculum 8 Tracks)

ทุกตำแหน่งงานในระบบและ UI ต้องใช้ **ชื่อไทยนำหน้า แล้วตามด้วยชื่อภาษาอังกฤษในวงเล็บ** เสมอ:

1. **8.1 `เจ้าหน้าที่คอมพิวเตอร์ (Computer Officer / IT Support)`**
   * *Core Skills:* `windows`, `linux`, `hardware`, `troubleshooting`, `basic networking`, `helpdesk`, `active directory`, `backup`, `ms office`
2. **8.2 `ผู้ดูแลระบบเครือข่ายคอมพิวเตอร์ (Network Administrator / Engineer)`**
   * *Core Skills:* `tcp/ip`, `cisco`, `routing`, `switching`, `firewall`, `vpn`, `dns`, `dhcp`, `linux server`, `windows server`, `network security`
3. **8.3 `นักพัฒนาและออกแบบสื่อผสม (Multimedia Designer & Developer)`**
   * *ตัวตนหลัก:* งาน Creative Media, Visual, Motion Graphics, 3D, Video Editing, Game, UI/UX Interaction & Prototyping
   * *Core Skills:* `ui/ux`, `figma`, `photoshop`, `illustrator`, `premiere pro`, `after effects`, `blender`, `3d animation`, `unity`, `game development`, `prototyping`
   * ⚠️ **ข้อควรระวัง:** **ห้ามใส่ `html` หรือ `css` ใน 8.3 โดยเด็ดขาด** (เพื่อป้องกันการทับซ้อนกับ 8.7)
4. **8.4 `นักจัดการโครงการสารสนเทศ (IT Project Manager / Coordinator)`**
   * *Core Skills:* `agile`, `scrum`, `jira`, `project management`, `trello`, `communication`, `risk management`, `sdlc`, `budgeting`
5. **8.5 `นักวิเคราะห์และออกแบบระบบงาน (System Analyst / Business Analyst)`**
   * *Core Skills:* `system analysis`, `business analysis`, `uml`, `use case`, `dfd`, `er diagram`, `database design`, `sql`, `requirement gathering`, `wireframing`
6. **8.6 `นักพัฒนาซอฟต์แวร์ (Software Developer / Engineer)`**
   * *Core Skills:* `python`, `java`, `c#`, `.net`, `javascript`, `typescript`, `react`, `node.js`, `sql`, `rest api`, `git`, `docker`
7. **8.7 `นักออกแบบและพัฒนาเว็บไซต์ (Web Designer & Developer)`**
   * *ตัวตนหลัก:* การพัฒนาเว็บไซต์, Frontend Coding, Web Standards, CMS, Responsive Web, Full Stack Web
   * *Core Skills:* `html5`, `css3`, `javascript`, `responsive web design`, `tailwind`, `bootstrap`, `wordpress`, `php`, `mysql`, `rest api`, `react`
8. **8.8 `ผู้เชี่ยวชาญด้านเทคโนโลยีสารสนเทศ (Specialized IT Professional)`**
   * *Core Skills:* `machine learning`, `deep learning`, `nlp`, `cybersecurity`, `cloud architecture`, `big data`, `data science`, `python`

---

## ⚠️ 3. กฎเหล็กและการตัดสินใจสำคัญ (Architectural Decisions & Invariants)

เมื่อ AI หรือผู้พัฒนาคนใหม่เข้ามาทำงาน **ห้ามละเมิดกฎเหล่านี้โดยเด็ดขาด**:

1. **เรื่องทักษะในระบบ (Taxonomy & Atomic Skills):**
   * ในระบบตลาดงานไทยมี **444 ทักษะมาตรฐาน** (Canonical Skills แปลงคำพ้องแล้วจาก 115 ตำแหน่งงานจริงใน `data/thai_jobs_dataset.csv`)
   * **ห้ามนำข้อความ "1,784 / 1,785 ทักษะ" จากชุดข้อมูล Kaggle เข้ามาแสดงใน UI อีก** ผู้ใช้ได้ตัดออกไปแล้ว และต้องการมุ่งเน้นเฉพาะทักษะที่มีงานรองรับจริงในไทย
   * ทักษะทุกตัวต้องเป็น Atomic Skill ห้ามเขียนคำรวม เช่น **ห้ามใช้ `html/css` เด็ดขาด** ให้แยกเป็น `html` และ `css` สองตัว
2. **เรื่องการแบ่งสาย 8.3 (สื่อผสม) vs 8.7 (เว็บไซต์):**
   * 8.3 เน้น Visual / Media / 3D / Video / Game / Prototyping
   * 8.7 เน้น Web Code / HTML / CSS / JS / WordPress / Frontend Frameworks
   * 8.3 ใน Dataset เปลี่ยนตำแหน่งเดิมจาก `Frontend UI Developer` เป็น **`Interactive Media & Creative Developer`** (Unity, Three.js, Blender, 3D, UI/UX) เพื่อตัดปัญหาแย่งงานกันเอง
3. **เรื่องชื่อสายงาน 8.3:**
   * ต้องขึ้นต้นด้วยภาษาไทยเสมอ: `นักพัฒนาและออกแบบสื่อผสม (Multimedia Designer & Developer)` ไม่ใช่อังกฤษนำ
4. **เรื่อง Frontend Architecture:**
   * เป็น **Vanilla JS เพียวๆ** ไม่มีการ Build (No Webpack, No Vite, No React)
   * หากแก้ไขไฟล์ใน `js/` ต้องปรับ Query String Cache-Buster ใน `index.html` เสมอ (เช่น `?v=5.0.0`) เพื่อป้องกันบราวเซอร์จำแคชเดิม
5. **เรื่องการรันและการทดสอบ:**
   * Backend ทำงานบนพอร์ต `8000` (`http://127.0.0.1:8000`)
   * หลังแก้ไขโค้ด Backend หรือ Dataset ต้องรัน `python src/validate.py` เสมอ (ต้องผ่านครบ 5/5 ข้อ 100%)

---

## 📂 4. แผนผังโครงสร้างโปรเจกต์ (Codebase Map)

```
modelJD_V4/
├── CONTEXT.md                    # [คุณกำลังอ่านไฟล์นี้] สรุปสถานะและข้อตกลงของระบบสำหรับ AI
├── PROJECT_CHEATSHEET.md         # 💡 โพยสรุปความเข้าใจ & ข้อควรรู้ฉบับไม่แตะโค้ด (สำหรับตอบคำถาม/พรีเซนต์)
├── README.md                     # รายงานโครงงานฉบับเต็ม พร้อมผลการทดลองทางสถิติและแนวทางการตอบกรรมการ
├── index.html                    # หน้าหลัก SPA (Single Page Application)
├── run.bat                       # สคริปต์คลิกเดียวรันทั้งระบบบน Windows
├── requirements.txt              # รายการ Python dependencies (FastAPI, scikit-learn, etc.)
│
├── data/                         # ชุดข้อมูลหลัก
│   ├── thai_jobs_dataset.csv     # ⭐️ ชุดข้อมูลงานไทย 115 งานจริง (ครบ 8 สายงาน มคอ.2) มี 444 ทักษะมาตรฐาน
│   ├── job_dataset.csv           # ข้อมูลดิบ/สำรอง
│   └── taxonomy_synonyms.json    # พจนานุกรมแปลงคำพ้อง (Synonyms: golang->go, k8s->kubernetes, ฯลฯ)
│
├── models/                       # โมเดล ML ที่ใช้งานจริง
│   └── career_classifier.joblib  # ⭐️ โมเดล Logistic Regression + TF-IDF (8 อาชีพ มคอ.2)
│
├── src/                          # โค้ดฝั่ง Backend & Machine Learning (Active Production Only)
│   ├── main.py                   # FastAPI Server, REST Endpoints (/api/skills, /api/roles, /recommend)
│   ├── recommend.py              # โมดูลคำนวณการแนะนำ (JobRecommender, Hybrid Scoring, ML Predictor)
│   ├── skills_taxonomy.py        # ระบบจัดระเบียบคำศัพท์ทักษะ (Skill Normalization Layer)
│   ├── fetch_thai_jobs.py        # ตัวสร้างและอัปเดต thai_jobs_dataset.csv ตาม 8 อาชีพ มคอ.2
│   ├── train.py                  # สคริปต์เทรนโมเดล Logistic Regression
│   └── validate.py               # ⭐️ ชุดทดสอบความถูกต้อง 5 มิติ (รันเช็คระบบทุกครั้งหลังแก้โค้ด)
│
├── js/                           # โค้ดฝั่ง Frontend SPA (Vanilla JS)
│   ├── app.js                    # จุดเริ่มต้นของแอปพลิเคชัน (Init App)
│   ├── router.js                 # ตัวจัดการ Client-side Hash Router (#/matcher, #/careers, #/skills)
│   ├── state.js                  # Global Reactive State Manager (AppState)
│   ├── api.js                    # ตัวเรียก REST API คุยกับ FastAPI Backend
│   ├── components/
│   │   └── jobCard.js            # คอมโพเนนต์การ์ดแสดงตำแหน่งงาน, Match Score และชิป Skill Gap
│   └── views/
│       ├── matcherView.js        # หน้าหลัก: ตัวเลือกสายงาน, ตะกร้าทักษะ, ปุ่ม Preset, และผลลัพธ์การจับคู่
│       ├── careersView.js        # หน้าสำรวจ 8 กลุ่มอาชีพ มคอ.2 พร้อม Roadmap ลิงก์
│       └── skillsView.js         # หน้าคลังทักษะไอทียอดนิยม (ค้นหา/กรองตามหมวดหมู่)
│
└── archive/                      # 📦 กรุเก็บไฟล์เก่า/โค้ดทดลอง (ไม่ได้รันบน Production, ห้ามแก้ไข)
    ├── legacy_src/               # โค้ดเก่าที่เลิกใช้แล้ว (train_model.py, study_pipeline.py)
    ├── experiments_benchmark/    # ชุดทดลองวิจัย IR (embeddings.py, retrieval.py, ranker.py, evaluate.py)
    ├── unused_views/             # Views หน้าเก่าที่ไม่ได้เชื่อมในเมนู (roadmapView.js, aboutView.js)
    ├── old_models/               # โมเดลเก่าที่ปลดระวางแล้ว (model.joblib, tfidf_vectorizer.joblib)
    └── backups/                  # ไฟล์สำรองและบันทึกเก่า (thai_jobs_dataset_backup.csv, walkthrough, etc.)
```

---

## ⚡️ 5. วิธีรันและทดสอบระบบด่วน (Quick Commands)

* **รันชุดทดสอบ (Validation Suite):**
  ```powershell
  python src/validate.py
  ```
* **สตาร์ตเซิร์ฟเวอร์ (Development Server):**
  ```powershell
  python src/main.py
  ```
  *(เข้าใช้งานผ่าน `http://127.0.0.1:8000` หรือ `http://127.0.0.1:8000/ui`)*
* **รีสตาร์ตเซิร์ฟเวอร์เมื่อพอร์ต 8000 ชน (PowerShell):**
  ```powershell
  Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
  python src/main.py
  ```
* **สร้าง Dataset งานไทยใหม่จากเทมเพลตมาตรฐาน 8 อาชีพ:**
  ```powershell
  python src/fetch_thai_jobs.py
  ```
