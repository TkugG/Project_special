import os
import sys
import re
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from typing import List, Optional, Dict, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.recommend import JobRecommender

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# ---------------------------------------------------------
# 1. INITIALIZATION & APP CONFIG
# ---------------------------------------------------------
app = FastAPI(
    title="SkillMatch IT - Curriculum-Based Career & Job Recommendation Engine",
    description="ระบบจับคู่ทักษะและวิเคราะห์ความพร้อมตาม 8 อาชีพหลักสูตร มคอ.2 สาขา IT ผสานข้อมูลตลาดแรงงานไทย",
    version="4.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
SRC_DIR = BASE_DIR / "src"
JS_DIR = BASE_DIR / "js"
CSS_DIR = BASE_DIR / "css"
INDEX_HTML_PATH = BASE_DIR / "index.html"

if JS_DIR.exists():
    app.mount("/js", StaticFiles(directory=str(JS_DIR)), name="js")
if CSS_DIR.exists():
    app.mount("/css", StaticFiles(directory=str(CSS_DIR)), name="css")

# ---------------------------------------------------------
# 2. DEFINITION OF 8 CURRICULUM ROLES (มคอ.2 สาขา IT)
# ---------------------------------------------------------
CURRICULUM_ROLES = {
    "8.1": {
        "id": "8.1",
        "title": "เจ้าหน้าที่คอมพิวเตอร์",
        "en_title": "Computer Officer / IT Support",
        "full_name": "เจ้าหน้าที่คอมพิวเตอร์ (Computer Officer / IT Support)",
        "desc": "ติดตั้ง บำรุงรักษา แก้ไขปัญหาฮาร์ดแวร์ ซอฟต์แวร์ และให้บริการสนับสนุนงานเทคโนโลยีสารสนเทศแก่ผู้ใช้งานในองค์กร",
        "core_skills": ["windows", "linux", "hardware", "troubleshooting", "basic networking", "helpdesk", "active directory", "backup", "ms office"],
        "patterns": [
            r"\b(it support|helpdesk|technical support|computer officer|desktop support|system operator|it officer|service desk|sales support|it technician)\b",
            r"(เจ้าหน้าที่คอมพิวเตอร์|เจ้าหน้าที่สารสนเทศ|บริการเทคนิค|ช่างคอมพิวเตอร์|ซัพพอร์ต|เจ้าหน้าที่ไอที)"
        ]
    },
    "8.2": {
        "id": "8.2",
        "title": "ผู้ดูแลระบบเครือข่ายคอมพิวเตอร์",
        "en_title": "Network Administrator / Engineer",
        "full_name": "ผู้ดูแลระบบเครือข่ายคอมพิวเตอร์ (Network Administrator / Engineer)",
        "desc": "ออกแบบ ติดตั้ง กำหนดค่า และบริหารจัดการระบบเครือข่ายคอมพิวเตอร์ ความมั่นคงปลอดภัย และเครื่องแม่ข่าย (Server)",
        "core_skills": ["tcp/ip", "cisco", "routing", "switching", "firewall", "vpn", "dns", "dhcp", "linux server", "windows server", "network security"],
        "patterns": [
            r"\b(network engineer|network admin|network analyst|noc engineer|cisco|network security|firewall|system admin|sysadmin|infrastructure engineer|cloud network|devops|sre|cloud engineer)\b",
            r"(ผู้ดูแลระบบเครือข่าย|วิศวกรเครือข่าย|เครือข่ายคอมพิวเตอร์|ดูแลเซิร์ฟเวอร์|วิศวกรระบบ)"
        ]
    },
    "8.3": {
        "id": "8.3",
        "title": "นักพัฒนาและออกแบบสื่อผสม",
        "en_title": "Multimedia Designer & Developer",
        "full_name": "นักพัฒนาและออกแบบสื่อผสม (Multimedia Designer & Developer)",
        "desc": "ออกแบบและพัฒนาสื่อดิจิทัล สื่อมัลติมีเดีย ภาพกราฟิก แอนิเมชัน วิดีโอ ตัวต้นแบบส่วนต่อประสานผู้ใช้ (UI/UX) และสื่อปฏิสัมพันธ์",
        "core_skills": ["ui/ux", "figma", "adobe xd", "photoshop", "illustrator", "premiere pro", "after effects", "3d animation", "game development", "unity", "html/css"],
        "patterns": [
            r"\b(multimedia|ux/ui|ui/ux|ui designer|ux designer|product designer|graphic designer|motion graphic|3d artist|3d animator|game developer|unity|unreal|interactive media|video editor)\b",
            r"(ออกแบบสื่อ|สื่อผสม|แอนิเมชัน|เกม|ออกแบบกราฟิก|ยูเอ็กซ์|ยูไอ|กราฟิกดีไซน์)"
        ]
    },
    "8.4": {
        "id": "8.4",
        "title": "นักจัดการโครงการสารสนเทศ",
        "en_title": "IT Project Manager / Coordinator",
        "full_name": "นักจัดการโครงการสารสนเทศ (IT Project Manager / Coordinator)",
        "desc": "วางแผน ประสานงาน บริหารจัดการทรัพยากร ติดตามความก้าวหน้า และควบคุมคุณภาพการส่งมอบโครงการด้านเทคโนโลยีสารสนเทศ",
        "core_skills": ["agile", "scrum", "jira", "project management", "trello", "communication", "risk management", "sdlc", "budgeting"],
        "patterns": [
            r"\b(it project manager|project manager|scrum master|product owner|project coordinator|it delivery manager|agile coach|it manager|account executive)\b",
            r"(จัดการโครงการ|ผู้จัดการโครงการ|ประสานงานโครงการ)"
        ]
    },
    "8.5": {
        "id": "8.5",
        "title": "นักวิเคราะห์และออกแบบระบบงาน",
        "en_title": "System Analyst / Business Analyst",
        "full_name": "นักวิเคราะห์และออกแบบระบบงาน (System Analyst / Business Analyst)",
        "desc": "รวบรวมและวิเคราะห์ความต้องการทางธุรกิจ ออกแบบผังกระบวนการทำงาน สถาปัตยกรรมระบบ ฐานข้อมูล และจัดทำข้อกำหนดระบบ (SRS)",
        "core_skills": ["system analysis", "business analysis", "uml", "use case", "dfd", "er diagram", "database design", "sql", "requirement gathering", "wireframing"],
        "patterns": [
            r"\b(system analyst|systems analyst|business analyst|\bsa\b|\bba\b|solutions analyst|enterprise architect|functional consultant|data analyst|bi analyst)\b",
            r"(นักวิเคราะห์ระบบ|วิเคราะห์และออกแบบระบบ|นักวิเคราะห์ธุรกิจ|วิเคราะห์ข้อมูล)"
        ]
    },
    "8.6": {
        "id": "8.6",
        "title": "นักพัฒนาซอฟต์แวร์",
        "en_title": "Software Developer / Engineer",
        "full_name": "นักพัฒนาซอฟต์แวร์ (Software Developer / Engineer)",
        "desc": "ออกแบบและเขียนโปรแกรมพัฒนาแอปพลิเคชัน เว็บเซอร์วิส ไมโครเซอร์วิส และระบบประยุกต์บนแพลตฟอร์มต่างๆ ตามมาตรฐานวิศวกรรมซอฟต์แวร์",
        "core_skills": ["python", "java", "c#", ".net", "javascript", "typescript", "react", "node.js", "sql", "rest api", "git", "oop", "docker"],
        "patterns": [
            r"\b(software engineer|software developer|programmer|backend developer|frontend developer|full stack developer|fullstack|mobile developer|ios developer|android developer|flutter developer|python developer|java developer|\.net developer|c# developer|golang developer|react developer|data engineer|qa engineer|automation tester|developer|ai engineer|machine learning)\b",
            r"(นักพัฒนาซอฟต์แวร์|โปรแกรมเมอร์|พัฒนาโปรแกรม|วิศวกรซอฟต์แวร์|เดเวลอปเปอร์)"
        ]
    },
    "8.7": {
        "id": "8.7",
        "title": "นักออกแบบและพัฒนาเว็บไซต์",
        "en_title": "Web Designer & Developer",
        "full_name": "นักออกแบบและพัฒนาเว็บไซต์ (Web Designer & Developer)",
        "desc": "ออกแบบและพัฒนาเว็บไซต์ เว็บแอปพลิเคชัน ส่วนต่อประสานผู้ใช้ที่รองรับทุกอุปกรณ์ (Responsive Web Design) และระบบบริหารจัดการเนื้อหา (CMS)",
        "core_skills": ["html5", "css3", "javascript", "responsive web design", "tailwind", "bootstrap", "wordpress", "php", "mysql", "rest api"],
        "patterns": [
            r"\b(web developer|web designer|wordpress developer|frontend web|webmaster|web application developer|web programmer)\b",
            r"(พัฒนาเว็บไซต์|ออกแบบเว็บไซต์|เว็บมาสเตอร์|นักพัฒนาเว็บ)"
        ]
    },
    "8.8": {
        "id": "8.8",
        "title": "ผู้เชี่ยวชาญด้านเทคโนโลยีสารสนเทศ",
        "en_title": "Specialized IT Professional",
        "full_name": "ผู้เชี่ยวชาญด้านเทคโนโลยีสารสนเทศ (Specialized IT Professional)",
        "desc": "งานเฉพาะทางด้านเทคโนโลยีสารสนเทศ เช่น ปัญญาประดิษฐ์ วิทยาการข้อมูล ความมั่นคงปลอดภัยไซเบอร์ หรือการบริหารจัดการข้อมูลขนาดใหญ่",
        "core_skills": ["machine learning", "deep learning", "nlp", "cybersecurity", "cloud architecture", "big data", "data science", "devsecops"],
        "patterns": [
            r"\b(ai specialist|data scientist|cybersecurity analyst|cloud architect|security specialist|blockchain developer)\b"
        ]
    }
}

STANDARDIZED_ROLES = [info["full_name"] for info in CURRICULUM_ROLES.values()]

# ---------------------------------------------------------
# 3. CONSTANTS & CLEANING UTILITIES
# ---------------------------------------------------------
PROTECTED_TECH_TERMS = {
    "ci/cd": "ci/cd", "ui/ux": "ui/ux", "tcp/ip": "tcp/ip", "c/c++": "c/c++",
    "pl/sql": "pl/sql", "asp.net": "asp.net", "asp.net core": "asp.net core",
    "asp.net mvc": "asp.net mvc", ".net": ".net", ".net core": ".net core",
    ".net framework": ".net framework", "node.js": "node.js", "react.js": "react.js",
    "vue.js": "vue.js", "next.js": "next.js", "nuxt.js": "nuxt.js"
}

def clean_atomic_skill(skill: str) -> str:
    """ทำความสะอาดชื่อทักษะเดี่ยว (Atomic Skill Normalization)"""
    if not skill or not isinstance(skill, str):
        return ""
    s = skill.strip().lower()
    s = re.sub(
        r'\b(basics?|fundamentals?|testing with|knowledge of|experience in|working with|advanced|overview|proficiency in|good to have|familiarity with|strong in|awareness|expert|experienced|exposure|understanding of|ability to|responsible for|practices?)\b',
        '', s, flags=re.IGNORECASE
    )
    s = re.sub(r'[\(\)\[\]\{\}]', ' ', s)
    s = s.strip(" ,;:-_./|&")
    s = re.sub(r'^(?:and|or|with|for|in|to|of|on|a|an|the)\s+', '', s)
    s = re.sub(r'\s+(?:and|or|with|for|in|to|of|on|a|an|the)$', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def extract_atomic_skills(raw_text: str) -> list:
    """แยกและทำความสะอาดชุดข้อความทักษะให้เป็น Atomic Skills"""
    if not raw_text or not isinstance(raw_text, str):
        return []
    t = raw_text.strip()
    t = re.sub(r'[;\n\r|•]+', ';', t)
    t = re.sub(r':\s*', ';', t)
    t = re.sub(r',\s*', ';', t)
    raw_tokens = t.split(';')
    final_skills = []
    for tok in raw_tokens:
        tok = tok.strip()
        if not tok:
            continue
        tok_lower = tok.lower()
        if "/" in tok_lower and tok_lower not in PROTECTED_TECH_TERMS:
            sub_parts = tok.split('/')
            for sp in sub_parts:
                cleaned = clean_atomic_skill(sp)
                if cleaned and (len(cleaned) >= 2 or cleaned in ['c', 'r']) and not cleaned.isdigit():
                    if cleaned not in ["tools", "technologies", "etc", "and", "or", "basics", "skills", "ml/dl", "ml", "dl", "monitoring"]:
                        final_skills.append(cleaned)
        else:
            cleaned = clean_atomic_skill(tok)
            if cleaned and (len(cleaned) >= 2 or cleaned in ['c', 'r']) and not cleaned.isdigit():
                if cleaned not in ["tools", "technologies", "etc", "and", "or", "basics", "skills", "ml/dl", "ml", "dl", "monitoring"]:
                    final_skills.append(cleaned)
    return list(dict.fromkeys(final_skills))

def clean_text_pipeline(text: str) -> str:
    """ทำความสะอาดข้อความสำหรับสร้างเวกเตอร์ TF-IDF"""
    if not text or not isinstance(text, str):
        return ""
    t = text.lower()
    noise_patterns = [
        r'\b(basics?|fundamentals?|testing with|knowledge of|experience in|working with)\b',
        r'\b(assist in|support team in|collaborate with|participate in|learn and apply|responsible for|follow best practices in)\b',
        r'\b(fresher|entry-level|junior|senior|intern)\b'
    ]
    for pattern in noise_patterns:
        t = re.sub(pattern, ' ', t, flags=re.IGNORECASE)
    t = re.sub(r'[;/|\n\r]+', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def match_curriculum_role(preference_str: str) -> Optional[dict]:
    """ค้นหาข้อมูล 8 อาชีพ มคอ.2 จากข้อความ preference ให้แม่นยำสูงสุด"""
    if not preference_str:
        return None
    p_lower = preference_str.lower().strip()
    
    # 1. ตรวจสอบรหัสโดยตรง (เช่น "8.7", "8.1", "8.6")
    for role_id, info in CURRICULUM_ROLES.items():
        if re.search(rf'\b{re.escape(role_id)}\b', p_lower) or p_lower.startswith(role_id):
            return info
            
    # 2. ตรวจสอบชื่อตำแหน่งภาษาไทย
    for role_id, info in CURRICULUM_ROLES.items():
        if info["title"].lower() in p_lower:
            return info
            
    # 3. ตรวจสอบชื่อเฉพาะเจาะจงก่อน (8.7 เว็บไซต์, 8.3 สื่อผสม/UI, 8.5 วิเคราะห์ระบบ)
    priority_order = ["8.7", "8.3", "8.5", "8.4", "8.2", "8.1", "8.6", "8.8"]
    for role_id in priority_order:
        info = CURRICULUM_ROLES[role_id]
        for pat in info["patterns"]:
            if re.search(pat, p_lower):
                return info
    return None

# ---------------------------------------------------------
# 4. LOAD DATASETS & ML MODELS
# ---------------------------------------------------------
CSV_PATH = DATA_DIR / "thai_jobs_dataset.csv"
if not CSV_PATH.exists():
    CSV_PATH = DATA_DIR / "job_dataset.csv"
if not CSV_PATH.exists():
    CSV_PATH = BASE_DIR / "job_dataset.csv"

print(f"⏳ กำลังโหลดและทำความสะอาดข้อมูลตำแหน่งงานจาก '{CSV_PATH}'...")
df_jobs = pd.read_csv(CSV_PATH).fillna("")
df_jobs = df_jobs[df_jobs["Title"].str.strip() != ""].reset_index(drop=True)

# สกัดทักษะเดี่ยว Atomic Skills สำหรับทุกงาน
UNIQUE_SKILLS_LIST = []
for _, row in df_jobs.iterrows():
    UNIQUE_SKILLS_LIST.extend(extract_atomic_skills(str(row["Skills"])))

HISTORICAL_CSV = DATA_DIR / "job_dataset.csv"
if HISTORICAL_CSV.exists() and str(HISTORICAL_CSV) != str(CSV_PATH):
    try:
        df_hist = pd.read_csv(HISTORICAL_CSV).fillna("")
        for _, row in df_hist.iterrows():
            UNIQUE_SKILLS_LIST.extend(extract_atomic_skills(str(row.get("Skills", ""))))
    except Exception as e:
        print(f"⚠️ Warning loading historical skills: {e}")

UNIQUE_SKILLS_LIST = sorted(list(set(UNIQUE_SKILLS_LIST)))

COMMON_IT_TECH = [
    "python", "java", "c#", "c++", "javascript", "typescript", "php", "ruby", "go", "golang", "rust", "scala", "kotlin", "swift", "dart", "r", "sql", "pl/sql", "html", "css", "sass", "less",
    "react", "react.js", "vue", "vue.js", "angular", "next.js", "nuxt.js", "node.js", "express", "express.js", "nestjs", "django", "flask", "fastapi", "spring", "spring boot", "asp.net", "asp.net core", "asp.net mvc", ".net", ".net core", "laravel", "rails",
    "mysql", "postgresql", "oracle", "sql server", "sqlite", "mongodb", "redis", "elasticsearch", "cassandra", "dynamodb", "mariadb",
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "terraform", "ansible", "jenkins", "gitlab ci", "github actions", "ci/cd", "linux", "ubuntu", "centos", "unix", "bash", "shell", "powershell", "git",
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy", "opencv",
    "selenium", "cypress", "playwright", "postman", "jmeter", "junit", "pytest", "jest",
    "ui/ux", "figma", "adobe xd", "wireframing", "prototyping",
    "rest api", "graphql", "grpc", "microservices", "agile", "scrum", "kanban", "jira"
]

ALL_TECH_VOCABULARY = sorted(list(set(UNIQUE_SKILLS_LIST).union(COMMON_IT_TECH)))

clean_titles = df_jobs["Title"].apply(clean_text_pipeline)
clean_skills = df_jobs["Skills"].apply(clean_text_pipeline)
clean_resps = df_jobs["Responsibilities"].apply(clean_text_pipeline) if "Responsibilities" in df_jobs else pd.Series([""] * len(df_jobs))
clean_keywords = df_jobs["Keywords"].apply(clean_text_pipeline) if "Keywords" in df_jobs else pd.Series([""] * len(df_jobs))
df_jobs["combined_features"] = clean_titles + " " + clean_skills + " " + clean_resps + " " + clean_keywords

# =========================================================================
# [จุดสำคัญที่ 10: สถาปัตยกรรม Backend - Singleton Recommender Pattern]
# เราโหลดและเตรียม JobRecommender ไว้ที่ระดับ Global เพียง "ครั้งเดียว" ตอนสตาร์ตแอป
# แทนที่จะสร้างอ็อบเจกต์ใหม่ทุกครั้งที่มีผู้ใช้ยิง HTTP Request เข้ามา
# ทำให้ API ตอบสนองได้ทันทีในเวลาไม่ถึง 10 ms รองรับ Concurrent Requests ได้สบาย
# =========================================================================
print("⏳ กำลังโหลดโมเดลจำแนกกลุ่มอาชีพและระบบแนะนำงาน...")
recommender = JobRecommender()
print("✅ โหลดโมเดลจำแนกกลุ่มอาชีพ (TF-IDF + Logistic Regression) เรียบร้อยแล้ว!")

# ---------------------------------------------------------
# 5. PYDANTIC SCHEMAS (Data Validation สัญญาข้อมูลหน้าบ้าน-หลังบ้าน)
# ---------------------------------------------------------
class RecommendRequest(BaseModel):
    preference: Optional[str] = ""     # รหัสหรือชื่อสายงานเป้าหมายตาม มคอ.2 (เช่น 8.6 หรือ 8.7)
    target_career: Optional[str] = ""  # alias
    skills: Optional[List[str]] = []   # ชุดทักษะที่มี

# ---------------------------------------------------------
# 6. API ENDPOINTS
# ---------------------------------------------------------
@app.get("/")
def root_check():
    return {
        "status": "online",
        "title": "SkillMatch IT - TQF มคอ.2 Curriculum Recommendation Engine",
        "total_jobs": len(df_jobs),
        "total_curriculum_roles": len(CURRICULUM_ROLES),
        "total_skills": len(ALL_TECH_VOCABULARY),
        "ui_url": "/ui"
    }

@app.get("/ui")
def serve_ui():
    """เปิดหน้าเว็บ UI ทันทีจาก FastAPI Server"""
    if INDEX_HTML_PATH.exists():
        return FileResponse(str(INDEX_HTML_PATH))
    return HTMLResponse("<h1>index.html not found</h1>")

@app.get("/api/skills")
def get_skills():
    """ส่งคืนรายการคำศัพท์ทักษะไอทีเดี่ยว (Master Skills Taxonomy) 1,600+ คำ"""
    return {"skills": ALL_TECH_VOCABULARY}

@app.get("/api/roles")
def get_roles():
    """ส่งคืนรายชื่อ 8 อาชีพตามหลักสูตร มคอ.2 สาขา IT พร้อมรายละเอียดสมรรถนะ"""
    roles_list = []
    for info in CURRICULUM_ROLES.values():
        roles_list.append({
            "id": info["id"],
            "title": info["title"],
            "en_title": info["en_title"],
            "full_name": info["full_name"],
            "desc": info["desc"],
            "core_skills": info["core_skills"]
        })
    return {
        "roles": STANDARDIZED_ROLES,
        "curriculum_roles": roles_list
    }

@app.post("/recommend")
@app.post("/api/recommend")
def recommend_jobs(data: RecommendRequest):
    """
    ระบบแนะนำงาน Content-Based Machine Learning (TF-IDF + Multi-Class Logistic Regression)
    1) target_career_analysis: วิเคราะห์ความพร้อมและทำนายสายงานเป้าหมายตามหลักสูตร มคอ.2
    2) skill_matched_recommendations: ตำแหน่งงานจริงในตลาดไอทีไทยที่ตรงกับทักษะมากที่สุด Top 5
    """
    preference = (data.target_career or data.preference or "").strip()
    target_role_info = match_curriculum_role(preference) if preference else None
    target_role_id = target_role_info["id"] if target_role_info else ""

    raw_skills = [clean_atomic_skill(s) for s in (data.skills or []) if clean_atomic_skill(s)]
    valid_vocab_set = set(ALL_TECH_VOCABULARY)
    skills_list = [s for s in raw_skills if s in valid_vocab_set]
    unrecognized_skills = [s for s in raw_skills if s not in valid_vocab_set]

    if not preference and not skills_list:
        return {
            "status": "error",
            "message": "กรุณาระบุทักษะที่ถูกต้อง หรือเลือกสายงานเป้าหมายตามหลักสูตร มคอ.2 ครับ",
            "target_career_analysis": None,
            "skill_matched_recommendations": [],
            "results": [],
            "total_matched": 0,
            "unrecognized_skills": unrecognized_skills
        }

    res = recommender.recommend(
        user_skills=skills_list,
        preference_role_id=target_role_id,
        top_k=5
    )
    res["unrecognized_skills"] = unrecognized_skills
    return res

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 กำลังเริ่มต้นเซิร์ฟเวอร์ SkillMatch IT (TQF มคอ.2) ที่ http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
