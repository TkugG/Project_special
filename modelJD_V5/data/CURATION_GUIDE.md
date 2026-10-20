# คู่มือการจัดเก็บและสอบทานข้อมูลตำแหน่งงานผ่าน Google Sheets (Curated Dataset Guide)
> **สำหรับ:** ผู้วิจัยโครงงาน SkillMatch IT (ระเบียบวิธีวิจัย Systematic Manual Curation)

---

## 🏛️ 1. หลักการและจริยธรรมการวิจัย (Research Ethics & Data Provenance)

การสร้างชุดข้อมูลตำแหน่งงานในโครงงานนี้ ยึดถือหลักการ **Human-in-the-loop Ground Truth Curation (การรวบรวมและตรวจสอบข้อมูลโดยมนุษย์)**:
1. **ความถูกต้องตามกฎหมายและข้อกำหนด (Terms of Service):** ไม่ใช้วิธีการแฮกเกอร์ แอบยิง API ลับ หรือใช้ Web Scraping บอทที่ละเมิดข้อกำหนดการใช้งาน (ToS) ของเว็บไซต์
2. **การสืบค้นข้อมูลสาธารณะ (Public Data Curation):** ผู้วิจัยเปิดอ่านประกาศรับสมัครงานจริงที่เปิดเป็นสาธารณะ (เช่น Blognone Jobs, JobsDB, JobThai, LinkedIn, เว็บไซต์รับสมัครงานของบริษัทโดยตรง) แล้วคัดลอกเฉพาะข้อมูลทักษะและหน้าที่งานมาบันทึกอย่างเป็นระบบ
3. **การสอบทานและตัดขยะคำศัพท์ (Quality Inspection):** มนุษย์ (ผู้วิจัย) เป็นผู้ตรวจทานความถูกต้องของชุดทักษะ ทำ Normalization คำพ้อง และจัดหมวดหมู่อาชีพตามมาตรฐาน มคอ.2 ด้วยตนเอง ทำให้ชุดข้อมูลมีความน่าเชื่อถือทางวิทยาศาสตร์ 100%

---

## 📋 2. โครงสร้าง 14 คอลัมน์มาตรฐานใน Google Sheets

เมื่อนำไฟล์ `data/GOOGLE_SHEETS_TEMPLATE.csv` ไปเปิดใน Google Sheets จะมีโครงสร้าง 14 คอลัมน์ดังนี้:

| ลำดับ | ชื่อคอลัมน์ (Header) | ตัวอย่างข้อมูล | คำอธิบายและข้อกำหนด |
| :---: | :--- | :--- | :--- |
| 1 | `JobID` | `JOB-8.6-001` | รหัสเฉพาะของงาน (รูปแบบ: `JOB-[รหัสสายงาน]-[ลำดับ 3 หลัก]`) |
| 2 | `Title` | `Backend Developer (Python/Go)` | ชื่อตำแหน่งงานตามประกาศจริง |
| 3 | `CurriculumRoleID` | `8.6` | รหัสสายงาน มคอ.2 (เลือกจาก `8.1` ถึง `8.8`) |
| 4 | `CurriculumRoleTitle` | `นักพัฒนาซอฟต์แวร์` | ชื่อกลุ่มอาชีพภาษาไทย (ดูตารางข้อ 3) |
| 5 | `CurriculumRoleEN` | `Software Developer / Engineer` | ชื่อกลุ่มอาชีพภาษาอังกฤษ (ดูตารางข้อ 3) |
| 6 | `Company` | `LINE MAN Wongnai` | ชื่อบริษัทหรือองค์กรผู้ประกาศรับสมัคร |
| 7 | `Province` | `กรุงเทพมหานคร` | จังหวัดที่ตั้ง หรือ `Remote (ทำงานจากที่บ้านทั่วไทย)` |
| 8 | `Salary` | `ตามโครงสร้างองค์กร / ตามประสบการณ์` | ข้อความระบุเงินเดือน (เลี่ยงตัวเลขเดี่ยวเพื่อไม่ให้เป็นประเด็นสอบ) |
| 9 | `ExperienceLevel` | `Entry-Level / เด็กจบใหม่ (0-2 ปี)` | ระดับประสบการณ์ (`Entry-Level`, `Mid-Level`, `Senior-Level`) |
| 10 | `YearsOfExperience` | `0-2` | ช่วงปีประสบการณ์ (เช่น `0-1`, `0-2`, `1-3`, `3-5+`) |
| 11 | `Skills` | `python; go; docker; sql; rest api; git` | **ทักษะจำเป็น (Hard Skills) คั่นด้วยเครื่องหมายเซมิโคลอน `;` เท่านั้น** |
| 12 | `Responsibilities` | `พัฒนา REST API; ออกแบบฐานข้อมูล; ทำ Unit Test` | หน้าที่ความรับผิดชอบ 2-4 ข้อ คั่นด้วยเซมิโคลอน `;` |
| 13 | `Keywords` | `python; go; docker; sql; rest api; git` | คีย์เวิร์ดสำหรับสืบค้น (ใส่ทักษะซ้ำ 5-8 ตัวแรก) |
| 14 | `ApplyURL` | `https://jobs.blognone.com` | ลิงก์หน้าประกาศงานจริง หรือหน้าเว็บรับสมัครงานของบริษัท |

---

## 🏛️ 3. ตารางมาตรฐาน 8 กลุ่มอาชีพ มคอ.2 (ต้องสะกดให้ตรง 100%)

| รหัส | ชื่อไทย (`CurriculumRoleTitle`) | ชื่ออังกฤษ (`CurriculumRoleEN`) | แกนทักษะหลัก |
| :---: | :--- | :--- | :--- |
| **8.1** | `เจ้าหน้าที่คอมพิวเตอร์` | `Computer Officer / IT Support` | windows, hardware, troubleshooting, active directory, helpdesk |
| **8.2** | `ผู้ดูแลระบบเครือข่ายคอมพิวเตอร์` | `Network Administrator / Engineer` | cisco, tcp/ip, routing, switching, firewall, vpn, linux server |
| **8.3** | `นักพัฒนาและออกแบบสื่อผสม` | `Multimedia Designer & Developer` | ui/ux, figma, photoshop, illustrator, blender, 3d, unity *(ห้ามใส่ html/css)* |
| **8.4** | `นักจัดการโครงการสารสนเทศ` | `IT Project Manager / Coordinator` | agile, scrum, jira, project management, trello, sdlc, risk management |
| **8.5** | `นักวิเคราะห์และออกแบบระบบงาน` | `System Analyst / Business Analyst` | system analysis, business analysis, uml, use case, dfd, database design, sql |
| **8.6** | `นักพัฒนาซอฟต์แวร์` | `Software Developer / Engineer` | python, java, c#, .net, javascript, typescript, react, go, sql, docker |
| **8.7** | `นักออกแบบและพัฒนาเว็บไซต์` | `Web Designer & Developer` | html5, css3, javascript, responsive web design, tailwind, wordpress, php |
| **8.8** | `ผู้เชี่ยวชาญด้านเทคโนโลยีสารสนเทศ` | `Specialized IT Professional` | machine learning, deep learning, nlp, cybersecurity, cloud architecture |

---

## 🔄 4. ขั้นตอนการนำข้อมูลจาก Google Sheets เข้าสู่ระบบ

1. **เปิด Google Sheets:** ไปที่ Google Sheets แล้วเลือก `File (ไฟล์)` -> `Import (นำเข้า)` -> อัปโหลดไฟล์ `data/GOOGLE_SHEETS_TEMPLATE.csv`
2. **กรอกหรือแก้ไขข้อมูล:** เพิ่มตำแหน่งงานจริงที่คุณสำรวจมาทีละแถว คั่นทักษะด้วยเครื่องหมาย `;` เสมอ
3. **ดาวน์โหลดเป็น CSV:** ใน Google Sheets กด `File (ไฟล์)` -> `Download (ดาวน์โหลด)` -> `Comma Separated Values (.csv)`
4. **นำมาแทนที่ไฟล์ระบบ:** บันทึกทับไฟล์ `data/thai_jobs_dataset.csv` ในโฟลเดอร์โปรเจกต์
5. **ทดสอบความถูกต้อง:** เปิด Terminal แล้วรันคำสั่ง:
   ```powershell
   python src/validate.py
   ```
   *ระบบจะทดสอบความสมบูรณ์ 5 มิติให้ทันที หากผ่านครบ 5/5 ข้อ แปลว่าข้อมูลของคุณพร้อมใช้งาน 100%!*
