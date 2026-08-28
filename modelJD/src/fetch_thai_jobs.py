"""
fetch_thai_jobs.py - โมดูลดึงข้อมูลตำแหน่งงานไอทีจริงในประเทศไทย (Blognone REST API)
และจำแนกหมวดหมู่เข้าสู่ 8 อาชีพตามกรอบหลักสูตร มคอ.2 สาขา IT
"""

import os
import sys
import re
import html
import time
from pathlib import Path
import requests
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# ---------------------------------------------------------
# 1. นิยาม 8 อาชีพตามกรอบหลักสูตร มคอ.2 สาขา IT
# ---------------------------------------------------------
CURRICULUM_ROLES = {
    "8.1": {
        "id": "8.1",
        "title": "เจ้าหน้าที่คอมพิวเตอร์",
        "en_title": "Computer Officer / IT Support",
        "patterns": [
            r"\b(it support|helpdesk|technical support|computer officer|desktop support|system operator|it officer|service desk|sales support)\b",
            r"(เจ้าหน้าที่คอมพิวเตอร์|เจ้าหน้าที่สารสนเทศ|บริการเทคนิค|ช่างคอมพิวเตอร์|ซัพพอร์ต)"
        ]
    },
    "8.2": {
        "id": "8.2",
        "title": "ผู้ดูแลระบบเครือข่ายคอมพิวเตอร์",
        "en_title": "Network Administrator / Engineer",
        "patterns": [
            r"\b(network engineer|network admin|network analyst|noc engineer|cisco|network security|firewall|system admin|sysadmin|infrastructure engineer|cloud network|devops|sre|cloud engineer)\b",
            r"(ผู้ดูแลระบบเครือข่าย|วิศวกรเครือข่าย|เครือข่ายคอมพิวเตอร์|ดูแลเซิร์ฟเวอร์|วิศวกรระบบ)"
        ]
    },
    "8.3": {
        "id": "8.3",
        "title": "นักพัฒนาและออกแบบสื่อผสม",
        "en_title": "Multimedia Designer & Developer",
        "patterns": [
            r"\b(multimedia|ux/ui|ui/ux|ui designer|ux designer|product designer|graphic designer|motion graphic|3d artist|3d animator|game developer|unity|unreal|interactive media|video editor)\b",
            r"(ออกแบบสื่อ|สื่อผสม|แอนิเมชัน|เกม|ออกแบบกราฟิก|ยูเอ็กซ์|ยูไอ)"
        ]
    },
    "8.4": {
        "id": "8.4",
        "title": "นักจัดการโครงการสารสนเทศ",
        "en_title": "IT Project Manager / Coordinator",
        "patterns": [
            r"\b(it project manager|project manager|scrum master|product owner|project coordinator|it delivery manager|agile coach|it manager|account executive)\b",
            r"(จัดการโครงการ|ผู้จัดการโครงการ|ประสานงานโครงการ)"
        ]
    },
    "8.5": {
        "id": "8.5",
        "title": "นักวิเคราะห์และออกแบบระบบงาน",
        "en_title": "System Analyst / Business Analyst",
        "patterns": [
            r"\b(system analyst|systems analyst|business analyst|\bsa\b|\bba\b|solutions analyst|enterprise architect|functional consultant|data analyst|bi analyst)\b",
            r"(นักวิเคราะห์ระบบ|วิเคราะห์และออกแบบระบบ|นักวิเคราะห์ธุรกิจ|วิเคราะห์ข้อมูล)"
        ]
    },
    "8.6": {
        "id": "8.6",
        "title": "นักพัฒนาซอฟต์แวร์",
        "en_title": "Software Developer / Engineer",
        "patterns": [
            r"\b(software engineer|software developer|programmer|backend developer|frontend developer|full stack developer|fullstack|mobile developer|ios developer|android developer|flutter developer|python developer|java developer|\.net developer|c# developer|golang developer|react developer|data engineer|qa engineer|automation tester|developer|ai engineer|machine learning)\b",
            r"(นักพัฒนาซอฟต์แวร์|โปรแกรมเมอร์|พัฒนาโปรแกรม|วิศวกรซอฟต์แวร์|เดเวลอปเปอร์)"
        ]
    },
    "8.7": {
        "id": "8.7",
        "title": "นักออกแบบและพัฒนาเว็บไซต์",
        "en_title": "Web Designer & Developer",
        "patterns": [
            r"\b(web developer|web designer|wordpress developer|frontend web|webmaster|web application developer|web programmer)\b",
            r"(พัฒนาเว็บไซต์|ออกแบบเว็บไซต์|เว็บมาสเตอร์|นักพัฒนาเว็บ)"
        ]
    }
}

# ---------------------------------------------------------
# 2. โหลดคลังคำศัพท์ทักษะมาตรฐาน 1,600+ คำเดิม (Master Taxonomy)
# ---------------------------------------------------------
def load_master_skills_vocabulary():
    """โหลดคลังทักษะไอทีมาตรฐานจากฐานข้อมูลเดิมเพื่อใช้เป็นพจนานุกรมตรวจจับ"""
    skills_set = set()
    csv_path = DATA_DIR / "job_dataset.csv"
    if csv_path.exists():
        df = pd.read_csv(csv_path).fillna("")
        for _, row in df.iterrows():
            raw = str(row.get("Skills", ""))
            tokens = re.split(r'[;,\n\r|•]+', raw)
            for t in tokens:
                s = t.strip().lower()
                s = re.sub(r'[\(\)\[\]\{\}]', '', s).strip(" ,;:-_./|&")
                if len(s) >= 2 or s in ['c', 'r']:
                    if not s.isdigit() and s not in ["basics", "tools", "technologies", "etc"]:
                        skills_set.add(s)
    
    thai_market_tech = [
        "react", "react.js", "next.js", "vue", "vue.js", "nuxt.js", "angular", "node.js", "express.js", "nestjs",
        "golang", "go", "python", "fastapi", "django", "flask", "java", "spring boot", "c#", ".net", ".net core",
        "php", "laravel", "flutter", "dart", "swift", "kotlin", "react native", "sql", "mysql", "postgresql",
        "mongodb", "redis", "docker", "kubernetes", "k8s", "aws", "azure", "gcp", "ci/cd", "git", "gitlab", "github",
        "figma", "adobe xd", "photoshop", "illustrator", "jira", "scrum", "agile", "rest api", "graphql", "microservices",
        "tailwind", "css", "html", "javascript", "typescript", "linux", "selenium", "cypress", "postman", "power bi", "tableau",
        "blockchain", "solidity", "socket.io", "socketio", "webpack", "vite", "prisma", "typeorm", "kafka", "rabbitmq"
    ]
    skills_set.update(thai_market_tech)
    return sorted(list(skills_set))

MASTER_VOCABULARY = load_master_skills_vocabulary()

# ---------------------------------------------------------
# 3. ฟังก์ชันทำความสะอาดและจำแนกหมวดหมู่
# ---------------------------------------------------------
def clean_html(raw_html: str) -> str:
    """ลบ HTML Tags และถอดรหัส HTML Entities"""
    if not raw_html:
        return ""
    text = re.sub(r'<[^>]+>', ' ', raw_html)
    text = html.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()

def classify_to_curriculum_role(job_title: str, job_desc: str) -> dict:
    """จำแนกประกาศงานเข้าสู่ 8 อาชีพตามหลักสูตร มคอ.2"""
    full_text = f"{job_title} {job_desc}".lower()
    
    # ตรวจสอบชื่อตำแหน่งก่อน
    for role_id, info in CURRICULUM_ROLES.items():
        for pattern in info["patterns"]:
            if re.search(pattern, job_title, flags=re.IGNORECASE):
                return info
    
    # ตรวจสอบเนื้อหาโดยรวม
    for role_id, info in CURRICULUM_ROLES.items():
        for pattern in info["patterns"]:
            if re.search(pattern, full_text, flags=re.IGNORECASE):
                return info

    if re.search(r'\b(engineer|developer|coding|programmer)\b', full_text, flags=re.IGNORECASE):
        return CURRICULUM_ROLES["8.6"]
    
    return {
        "id": "8.8",
        "title": "ผู้เชี่ยวชาญ/อาชีพอื่นด้านเทคโนโลยีสารสนเทศ",
        "en_title": "Specialized / Other IT Professional"
    }

def extract_skills_from_text(text: str, explicit_skills: list, master_vocab: list) -> list:
    """รวมทักษะที่บริษัทระบุตรงๆ และสแกนเพิ่มเติมจากเนื้อหาด้วย Master Taxonomy"""
    found_skills = set()
    
    # 1. ทักษะที่บริษัทกรอกมาในระบบ
    for s in explicit_skills:
        clean_s = str(s).strip().lower()
        if clean_s:
            found_skills.add(clean_s)
            
    # 2. สแกนจากเนื้อหาข้อความ
    text_lower = f" {text.lower()} "
    for skill in master_vocab:
        escaped_skill = re.escape(skill)
        if skill in ["c", "r", "go"]:
            pattern = rf'(?:\b|\s){escaped_skill}(?:\b|\s|,|\.)'
        elif "." in skill or "#" in skill or "+" in skill or "/" in skill:
            pattern = rf'(?:^|[\s,;:(]){escaped_skill}(?:$|[\s,;:).])'
        else:
            pattern = rf'\b{escaped_skill}\b'
            
        if re.search(pattern, text_lower):
            found_skills.add(skill)
            
    return sorted(list(found_skills))

def format_experience(level_str: str, text: str) -> tuple:
    """แปลงระดับประสบการณ์เป็นรูปแบบที่เข้าใจง่าย"""
    lvl = (level_str or "").upper()
    if lvl == "ENTRY":
        return "Entry-Level / เด็กจบใหม่ (0-1 ปี)", "0-1"
    elif lvl == "MIDDLE":
        return "Mid-Level / มีประสบการณ์ (1-3 ปี)", "1-3"
    elif lvl == "SENIOR":
        return "Senior-Level / มีประสบการณ์สูง (3-5+ ปี)", "3-5+"
        
    t = text.lower()
    if re.search(r'\b(senior|lead|principal|5\+|5\s*years?)\b', t):
        return "Senior-Level / มีประสบการณ์สูง (3-5+ ปี)", "3-5+"
    elif re.search(r'\b(junior|entry|fresher|intern|0-1|0-2\s*years?)\b', t):
        return "Entry-Level / เด็กจบใหม่ (0-1 ปี)", "0-1"
    return "Mid-Level / ไม่ระบุ (1-3 ปี)", "1-3"

def format_salary(salary_min: str, salary_max: str, display_fmt: str) -> str:
    """แปลงข้อมูลเงินเดือนให้อ่านง่าย"""
    try:
        s_min = int(float(salary_min)) if salary_min else 0
        s_max = int(float(salary_max)) if salary_max else 0
        if s_min > 0 and s_max > 0:
            return f"฿{s_min:,} - ฿{s_max:,} บาท"
        elif s_min > 0:
            return f"฿{s_min:,}+ บาท"
        elif s_max > 0:
            return f"สูงสุด ฿{s_max:,} บาท"
    except (ValueError, TypeError):
        pass
    return "ตามตกลง / โครงสร้างบริษัท"

# ---------------------------------------------------------
# 4. ฟังก์ชันหลักสำหรับดึงงานจาก Blognone REST API
# ---------------------------------------------------------
def fetch_and_map_thai_jobs(max_pages: int = 5):
    print("=" * 80)
    print(f"🚀 เริ่มต้นดึงข้อมูลตำแหน่งงานไอทีไทยจาก Blognone REST API (จำนวน {max_pages} หน้า)...")
    print("=" * 80)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Origin': 'https://jobs.blognone.com',
        'Referer': 'https://jobs.blognone.com/'
    }
    
    all_raw_jobs = []
    seen_slugs = set()
    
    for page in range(1, max_pages + 1):
        url = f"https://jobs-api.blognone.com/search?page={page}"
        try:
            r = requests.get(url, headers=headers, timeout=8)
            if r.status_code != 200:
                print(f"⚠️ หน้า {page}: HTTP {r.status_code}")
                break
            data = r.json()
            jobs = data.get("jobs", [])
            if not jobs:
                break
            
            new_cnt = 0
            for j in jobs:
                slug = j.get("slug")
                if slug and slug not in seen_slugs:
                    seen_slugs.add(slug)
                    all_raw_jobs.append(j)
                    new_cnt += 1
            print(f"  • หน้า {page:>2}: ดึงได้ {len(jobs):>2} ตำแหน่ง (ใหม่ {new_cnt:>2}) | สะสม: {len(all_raw_jobs):>2} ตำแหน่ง")
            if new_cnt == 0:
                break
            time.sleep(0.2)
        except Exception as e:
            print(f"❌ หน้า {page}: เกิดข้อผิดพลาด {e}")
            break
            
    print(f"\n✅ ดึงข้อมูลตำแหน่งงานไอทีในไทยสำเร็จทั้งหมด: {len(all_raw_jobs)} ตำแหน่ง")
    
    # 5. ประมวลผลรายละเอียดและจำแนกเข้าสู่ 8 อาชีพ มคอ.2
    print("⏳ กำลังจำแนกหมวดหมู่เข้าสู่ 8 อาชีพตามหลักสูตร มคอ.2 และสกัดทักษะ...")
    
    parsed_jobs = []
    role_stats = {k: 0 for k in CURRICULUM_ROLES.keys()}
    role_stats["8.8"] = 0
    
    for idx, raw in enumerate(all_raw_jobs, 1):
        job_id = f"BN-TH-{idx:03d}"
        title = raw.get("title", "IT Specialist")
        comp = raw.get("company", {})
        comp_name = comp.get("name_th") or comp.get("name_en") or "Tech Company in Thailand"
        comp_slug = comp.get("slug", "")
        job_slug = raw.get("slug", "")
        province = raw.get("province", "กรุงเทพมหานคร")
        raw_skills = raw.get("skills", [])
        raw_level = raw.get("level", "")
        salary_str = format_salary(raw.get("salary_min"), raw.get("salary_max"), raw.get("salary_display_format"))
        
        # ดึงรายละเอียดแบบเจาะลึก
        detail_desc = ""
        detail_qual = ""
        if comp_slug and job_slug:
            try:
                detail_url = f"https://jobs-api.blognone.com/company/{comp_slug}/jobs/{job_slug}"
                r_det = requests.get(detail_url, headers=headers, timeout=4)
                if r_det.status_code == 200:
                    det_json = r_det.json().get("job", {})
                    detail_desc = clean_html(det_json.get("description", ""))
                    detail_qual = clean_html(det_json.get("qualification", ""))
                    if det_json.get("skills"):
                        raw_skills.extend(det_json.get("skills"))
            except Exception:
                pass
                
        full_text = f"{title} {detail_desc} {detail_qual}"
        
        # 1. จำแนกเข้า 8 อาชีพ มคอ.2
        matched_role = classify_to_curriculum_role(title, full_text)
        role_stats[matched_role["id"]] = role_stats.get(matched_role["id"], 0) + 1
        
        # 2. สกัดทักษะด้วย Master Skills Taxonomy
        extracted_skills = extract_skills_from_text(full_text, raw_skills, MASTER_VOCABULARY)
        
        # 3. ตรวจจับระดับประสบการณ์
        exp_level, years_exp = format_experience(raw_level, full_text)
        
        # สร้าง Responsibilities List
        resps_list = [r.strip() for r in re.split(r'[;\n\r|•]+', detail_desc) if len(r.strip()) > 10]
        if not resps_list:
            resps_list = ["ปฏิบัติงานและพัฒนาโซลูชันตามที่ได้รับมอบหมายในทีม"]
            
        parsed_jobs.append({
            "JobID": job_id,
            "Title": title,
            "CurriculumRoleID": matched_role["id"],
            "CurriculumRoleTitle": matched_role["title"],
            "CurriculumRoleEN": matched_role.get("en_title", ""),
            "Company": comp_name,
            "Province": province,
            "Salary": salary_str,
            "ExperienceLevel": exp_level,
            "YearsOfExperience": years_exp,
            "Skills": "; ".join(extracted_skills),
            "SkillsList": extracted_skills,
            "Responsibilities": "; ".join(resps_list[:4]),
            "ResponsibilitiesList": resps_list[:4],
            "Keywords": "; ".join(extracted_skills[:6]),
            "ApplyURL": f"https://jobs.blognone.com/company/{comp_slug}/job/{job_slug}" if comp_slug and job_slug else "https://jobs.blognone.com"
        })
        
    # แสดงสถิติตารางสรุป 8 อาชีพ มคอ.2
    print("\n" + "=" * 80)
    print("📊 สถิติตำแหน่งงานไอทีไทยที่ถูกจำแนกเข้าสู่ 8 อาชีพตามหลักสูตร มคอ.2:")
    print("=" * 80)
    print(f"{'รหัส':<6} | {'ชื่ออาชีพตามหลักสูตร มคอ.2':<35} | {'จำนวน':<8} | {'สัดส่วน':<8} | กราฟ")
    print("-" * 80)
    for r_id, info in CURRICULUM_ROLES.items():
        cnt = role_stats.get(r_id, 0)
        pct = (cnt / len(parsed_jobs)) * 100 if parsed_jobs else 0
        bar = "█" * int(cnt)
        print(f"{info['id']:<6} | {info['title']:<35} | {cnt:>2} งาน   | {pct:>5.1f}%  | {bar}")
    if role_stats.get("8.8", 0) > 0:
        cnt8 = role_stats.get("8.8", 0)
        pct8 = (cnt8 / len(parsed_jobs)) * 100 if parsed_jobs else 0
        print(f"{'8.8':<6} | {'ผู้เชี่ยวชาญ/อาชีพอื่นด้านเทคโนโลยี':<35} | {cnt8:>2} งาน   | {pct8:>5.1f}%  | {'█' * cnt8}")
    print("-" * 80)
    
    # แสดงตัวอย่าง 5 ตำแหน่งงานแรก
    print("\n🔍 ตัวอย่างผลลัพธ์ตำแหน่งงานจริง 5 รายการแรกที่พร้อมส่งเข้า ML Recommendation:")
    print("=" * 80)
    for i, j in enumerate(parsed_jobs[:5], 1):
        print(f"[{i}] {j['Title']}")
        print(f"    🏢 บริษัท     : {j['Company']} ({j['Province']})")
        print(f"    🎯 อาชีพ มคอ.2 : [{j['CurriculumRoleID']}] {j['CurriculumRoleTitle']}")
        print(f"    💰 เงินเดือน   : {j['Salary']}")
        print(f"    🎓 ประสบการณ์ : {j['ExperienceLevel']}")
        print(f"    💻 ทักษะที่สกัด ({len(j['SkillsList'])} ทักษะ): {', '.join(j['SkillsList'][:8])}")
        print(f"    🔗 ลิงก์สมัคร  : {j['ApplyURL']}")
        print("-" * 80)
        
    return parsed_jobs

if __name__ == "__main__":
    fetch_and_map_thai_jobs(max_pages=5)
