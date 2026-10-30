import os
import sys
import re
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from pydantic import BaseModel
from src.recommend import JobRecommender
from src.skills_taxonomy import normalize_skill, normalize_skills_list, SKILL_SYNONYMS

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
INSPECT_HTML_PATH = BASE_DIR / "inspect.html"

if JS_DIR.exists():
    app.mount("/js", StaticFiles(directory=str(JS_DIR)), name="js")
if CSS_DIR.exists():
    app.mount("/css", StaticFiles(directory=str(CSS_DIR)), name="css")

# ---------------------------------------------------------
# 2. DEFINITION OF 8 CURRICULUM ROLES (มคอ.2 สาขา IT ตารางที่ 3.1)
# ---------------------------------------------------------
CURRICULUM_ROLES = {
    "G1": {
        "id": "G1",
        "title": "นักพัฒนาซอฟต์แวร์",
        "en_title": "Software Developer",
        "full_name": "G1: นักพัฒนาซอฟต์แวร์ (Software Developer)",
        "desc": "ออกแบบ พัฒนา เขียนชุดคำสั่ง และทดสอบระบบซอฟต์แวร์หรือแอปพลิเคชัน",
        "core_skills": ["sql", ".net", "java", "angular", "javascript", "git", "c#", "python", "rest api", "react"],
        "patterns": [
            r"\b(software engineer|software developer|programmer|backend developer|frontend developer|full stack developer|fullstack|mobile developer|c# developer|python developer|java developer|\.net developer|golang developer|react developer)\b",
            r"(นักพัฒนาซอฟต์แวร์|โปรแกรมเมอร์|พัฒนาโปรแกรม|วิศวกรซอฟต์แวร์|เดเวลอปเปอร์)"
        ]
    },
    "G2": {
        "id": "G2",
        "title": "ผู้ดูแลระบบฐานข้อมูล",
        "en_title": "Database Administrator",
        "full_name": "G2: ผู้ดูแลระบบฐานข้อมูล (Database Administrator)",
        "desc": "ออกแบบ บริหารจัดการ ดูแลความมั่นคงปลอดภัย และสำรองข้อมูลระบบฐานข้อมูล",
        "core_skills": ["sql", "python", "postgresql", "sql server", "mysql", "oracle", "api", "ssis", "oracle rac", "mongodb"],
        "patterns": [
            r"\b(database administrator|dba|database engineer|oracle dba|sql administrator|data engineer|etl developer|data warehouse)\b",
            r"(ผู้ดูแลระบบฐานข้อมูล|ฐานข้อมูล|ดีบีเอ|วิศวกรข้อมูล)"
        ]
    },
    "G3": {
        "id": "G3",
        "title": "นักวิเคราะห์และออกแบบระบบ",
        "en_title": "System Analyst / Designer",
        "full_name": "G3: นักวิเคราะห์และออกแบบระบบ (System Analyst / Designer)",
        "desc": "วิเคราะห์ความต้องการทางธุรกิจ ออกแบบผังกระบวนการทำงาน และข้อกำหนดระบบสารสนเทศ",
        "core_skills": ["api", "sql", "sql server", "java", "postgresql", "react", "uat", "mysql", ".net", "system analysis"],
        "patterns": [
            r"\b(system analyst|systems analyst|business analyst|\bsa\b|\bba\b|solutions analyst|system designer|functional consultant)\b",
            r"(นักวิเคราะห์ระบบ|วิเคราะห์และออกแบบระบบ|นักวิเคราะห์ธุรกิจ|ออกแบบระบบ)"
        ]
    },
    "G4": {
        "id": "G4",
        "title": "เจ้าหน้าที่เทคนิคคอมพิวเตอร์",
        "en_title": "Computer Technical Officer",
        "full_name": "G4: เจ้าหน้าที่เทคนิคคอมพิวเตอร์ (Computer Technical Officer)",
        "desc": "ตรวจสอบ ติดตั้ง ซ่อมบำรุงฮาร์ดแวร์ อุปกรณ์ต่อพ่วง และแก้ไขปัญหาการใช้งานคอมพิวเตอร์",
        "core_skills": ["windows", "vpn", "microsoft 365", "active directory", "printers", "hardware", "troubleshooting", "sql", "helpdesk", "basic networking"],
        "patterns": [
            r"\b(it support|helpdesk|technical support|computer officer|desktop support|system operator|it officer|service desk|it technician|hardware support)\b",
            r"(เจ้าหน้าที่คอมพิวเตอร์|เจ้าหน้าที่เทคนิค|บริการเทคนิค|ช่างคอมพิวเตอร์|ซัพพอร์ต|เจ้าหน้าที่ไอที)"
        ]
    },
    "G5": {
        "id": "G5",
        "title": "ผู้ดูแลระบบ",
        "en_title": "System Administrator",
        "full_name": "G5: ผู้ดูแลระบบ (System Administrator)",
        "desc": "ติดตั้ง กำหนดค่า และบริหารจัดการระบบปฏิบัติการเครื่องแม่ข่ายและระบบเครือข่าย",
        "core_skills": ["linux", "windows server", "active directory", "vmware", "azure", "firewall", "vpn", "microsoft 365", "switches", "network security"],
        "patterns": [
            r"\b(system administrator|sysadmin|network engineer|network administrator|infrastructure engineer|cloud engineer|devops|server engineer)\b",
            r"(ผู้ดูแลระบบ|ดูแลเซิร์ฟเวอร์|วิศวกรระบบ|เครือข่ายคอมพิวเตอร์|วิศวกรเครือข่าย)"
        ]
    },
    "G6": {
        "id": "G6",
        "title": "นักพัฒนาเว็บไซต์",
        "en_title": "Web Developer",
        "full_name": "G6: นักพัฒนาเว็บไซต์ (Web Developer)",
        "desc": "ออกแบบ พัฒนา และบำรุงรักษาเว็บไซต์ เว็บแอปพลิเคชัน และระบบบริการส่วนหน้า",
        "core_skills": ["html5", "css3", "javascript", "react", "next.js", "git", "mysql", "node.js", "php", "tailwind"],
        "patterns": [
            r"\b(web developer|web designer|frontend web|web application developer|wordpress developer|webmaster)\b",
            r"(พัฒนาเว็บไซต์|ออกแบบเว็บไซต์|เว็บมาสเตอร์|นักพัฒนาเว็บ)"
        ]
    },
    "G7": {
        "id": "G7",
        "title": "ผู้ช่วยผู้จัดการโครงการสารสนเทศ",
        "en_title": "IT Project Assistant",
        "full_name": "G7: ผู้ช่วยผู้จัดการโครงการสารสนเทศ (IT Project Assistant)",
        "desc": "ประสานงาน ติดตามแผนงาน จัดทำเอกสารข้อกำหนด และสนับสนุนการบริหารโครงการไอที",
        "core_skills": ["project management", "agile", "scrum", "jira", "ms office", "excel", "powerpoint", "erp", "sap", "communication"],
        "patterns": [
            r"\b(it project manager|project manager|project assistant|project coordinator|it coordinator|scrum master|product owner|agile coach)\b",
            r"(จัดการโครงการ|ผู้จัดการโครงการ|ประสานงานโครงการ|ผู้ช่วยผู้จัดการโครงการ)"
        ]
    },
    "G8": {
        "id": "G8",
        "title": "ผู้สร้างสรรค์เนื้อหาดิจิทัล",
        "en_title": "Content Creator",
        "full_name": "G8: ผู้สร้างสรรค์เนื้อหาดิจิทัล (Content Creator)",
        "desc": "ออกแบบ ผลิต และจัดการสื่อดิจิทัล สื่อประสม กราฟิก และมัลติมีเดียเพื่อการสื่อสาร",
        "core_skills": ["tiktok", "canva", "capcut", "premiere pro", "video editing", "youtube", "photoshop", "instagram", "facebook", "content creator"],
        "patterns": [
            r"\b(content creator|multimedia|ux/ui|ui/ux|ui designer|graphic designer|video editor|motion graphic|media creator|social media specialist)\b",
            r"(สร้างสรรค์เนื้อหา|คอนเทนต์|สื่อดิจิทัล|สื่อผสม|แอนิเมชัน|กราฟิก|วิดีโอ)"
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
    is_dot_prefix = s.startswith(".net")
    strip_chars = " ,;:-_/|&" + ("" if is_dot_prefix else ".")
    s = s.strip(strip_chars)
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
    """ค้นหาข้อมูล 8 อาชีพ จากข้อความ preference ให้แม่นยำสูงสุด รองรับทั้ง G1-G8 และ 8.1-8.8"""
    if not preference_str:
        return None
    p_lower = preference_str.lower().strip()
    
    from src.recommend import ROLE_ALIASES, normalize_role_id
    # 1. ตรวจสอบรหัส G1-G8 หรือ 8.1-8.8 โดยตรง
    p_upper = preference_str.upper().strip()
    if p_upper in CURRICULUM_ROLES:
        return CURRICULUM_ROLES[p_upper]
    if p_lower in ROLE_ALIASES:
        return CURRICULUM_ROLES[ROLE_ALIASES[p_lower]]

    for role_id, info in CURRICULUM_ROLES.items():
        if re.search(rf'\b{re.escape(role_id.lower())}\b', p_lower) or p_lower.startswith(role_id.lower()):
            return info
            
    # 2. ตรวจสอบชื่อตำแหน่งภาษาไทยและอังกฤษ
    for role_id, info in CURRICULUM_ROLES.items():
        if info["title"].lower() in p_lower or info["en_title"].lower() in p_lower:
            return info
            
    # 3. ตรวจสอบตามลำดับความจำเพาะของ Pattern
    for role_id in ["G6", "G8", "G3", "G2", "G5", "G7", "G4", "G1"]:
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

# สกัดทักษะเดี่ยว Atomic Skills สำหรับตลาดงานไทย (253 ตำแหน่งงาน)
THAI_MARKET_SKILLS = sorted(list(set(
    s for _, row in df_jobs.iterrows() for s in extract_atomic_skills(str(row["Skills"]))
)))

# สกัดทักษะประวัติศาสตร์ (สำหรับเป็นพจนานุกรมสำรองในการ Validate คำค้นหา)
HISTORICAL_CSV = DATA_DIR / "job_dataset.csv"
HISTORICAL_SKILLS = []
if HISTORICAL_CSV.exists() and str(HISTORICAL_CSV) != str(CSV_PATH):
    try:
        df_hist = pd.read_csv(HISTORICAL_CSV).fillna("")
        for _, row in df_hist.iterrows():
            HISTORICAL_SKILLS.extend(extract_atomic_skills(str(row.get("Skills", ""))))
    except Exception as e:
        print(f"⚠️ Warning loading historical skills: {e}")

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

ALL_TECH_VOCABULARY = sorted(list(
    set(THAI_MARKET_SKILLS)
    .union(set(HISTORICAL_SKILLS))
    .union(COMMON_IT_TECH)
    .union(set(SKILL_SYNONYMS.keys()))
    .union(set(SKILL_SYNONYMS.values()))
))

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
    preference: Optional[str] = ""     # รหัสหรือชื่อสายงานเป้าหมาย (เช่น 8.6 หรือ 8.7)
    target_career: Optional[str] = ""  # alias
    skills: Optional[List[str]] = []   # ชุดทักษะที่มี

class InspectRequest(BaseModel):
    # 💡 [ทำไมต้องแบบนี้]: กำหนด Schema สำหรับรับข้อมูลทักษะและตำแหน่งงานเป้าหมายในการแกะรอย Pipeline
    skills: Optional[List[str]] = []
    target_job_id: Optional[str] = None

# ---------------------------------------------------------
# 6. API ENDPOINTS
# ---------------------------------------------------------
@app.get("/")
def root_check(request: Request):
    """
    Root endpoint:
    - ถ้าเปิดผ่านเว็บเบราว์เซอร์ (Accept: text/html) จะเปิดหน้า UI index.html ให้ทันที
    - ถ้าเรียกผ่าน API / Fetch / cURL จะส่งคืน JSON Status ของระบบ
    """
    accept = request.headers.get("accept", "")
    if "text/html" in accept and not accept.startswith("*/*"):
        if INDEX_HTML_PATH.exists():
            return FileResponse(str(INDEX_HTML_PATH))
    return {
        "status": "online",
        "title": "SkillMatch IT - TQF มคอ.2 Curriculum Recommendation Engine",
        "total_jobs": len(df_jobs),
        "total_curriculum_roles": len(CURRICULUM_ROLES),
        "total_skills": len(THAI_MARKET_SKILLS),
        "ui_url": "/ui"
    }

@app.get("/health")
@app.get("/api/status")
def health_status():
    """Health check endpoint สำหรับตรวจสอบสถานะ Backend"""
    return {
        "status": "online",
        "title": "SkillMatch IT - TQF มคอ.2 Curriculum Recommendation Engine",
        "total_jobs": len(df_jobs),
        "total_curriculum_roles": len(CURRICULUM_ROLES),
        "total_skills": len(THAI_MARKET_SKILLS),
        "ui_url": "/ui"
    }

@app.get("/ui")
def serve_ui():
    """เปิดหน้าเว็บ UI ทันทีจาก FastAPI Server"""
    if INDEX_HTML_PATH.exists():
        return FileResponse(str(INDEX_HTML_PATH))
    return HTMLResponse("<h1>index.html not found</h1>")

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    """ป้องกัน 404 เมื่อบราวเซอร์ส่งคำขอ favicon.ico"""
    return Response(status_code=204)

@app.get("/api/skills")
def get_skills():
    """ส่งคืนรายการคำศัพท์ทักษะเฉพาะที่มีตำแหน่งงานรองรับจริงในตลาดไอทีไทย (216 ทักษะ)"""
    return {
        "skills": THAI_MARKET_SKILLS,
        "total": len(THAI_MARKET_SKILLS)
    }

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

    # ทำการแปลงคำพ้อง/ตัวย่อเป็นคำมาตรฐาน (Canonical Skills) เช่น golang -> go, k8s -> kubernetes
    raw_skills = [clean_atomic_skill(s) for s in (data.skills or []) if clean_atomic_skill(s)]
    normalized_skills = [normalize_skill(s) for s in raw_skills if normalize_skill(s)]
    valid_vocab_set = set(ALL_TECH_VOCABULARY)
    skills_list = [s for s in normalized_skills if s in valid_vocab_set]
    unrecognized_skills = [raw_skills[i] for i, norm in enumerate(normalized_skills) if norm not in valid_vocab_set]

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

@app.post("/api/inspect")
def inspect_pipeline_endpoint(data: InspectRequest):
    """
    แกะรอย Pipeline และคืนค่าข้อมูลจริงครบ 6 ขั้นตอน
    สำหรับใช้แสดงผลบนหน้าจอ Inspector และแคปเจอร์ภาพประกอบเล่มบทที่ 3-4
    """
    # 💡 [ทำไมต้องแบบนี้]: Lazy-import inspector_engine เพื่อให้เซิร์ฟเวอร์สตาร์ตได้เร็ว และไม่สร้าง overhead กับ request ปกติ
    from src.inspector import inspector_engine
    skills = data.skills or []
    return inspector_engine.inspect(skills, data.target_job_id)

@app.get("/inspect.html")
@app.get("/inspect")
def serve_inspect_page():
    """เปิดหน้าจอ Data & Pipeline Inspector ทันทีจากเซิร์ฟเวอร์"""
    if INSPECT_HTML_PATH.exists():
        return FileResponse(str(INSPECT_HTML_PATH))
    return HTMLResponse("<h1>inspect.html not found</h1>", status_code=404)

if __name__ == "__main__":
    import uvicorn
    import socket
    import threading
    import time
    import webbrowser

    def is_port_in_use(port_to_check: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port_to_check)) == 0

    selected_port = 8000
    candidate_ports = [8000, 8001, 8080, 8888, 5000]
    for p in candidate_ports:
        if not is_port_in_use(p):
            selected_port = p
            break

    def _open_browser_when_ready(port_num: int):
        # รอ 1.2 วินาทีเพื่อให้ Uvicorn ทำการ bind socket และพร้อมรับ request
        time.sleep(1.2)
        try:
            webbrowser.open(f"http://127.0.0.1:{port_num}")
        except Exception:
            pass

    # เปิดเบราว์เซอร์อัตโนมัติ (สามารถปิดได้ด้วย NO_BROWSER=1)
    if os.environ.get("NO_BROWSER", "").lower() not in ("1", "true"):
        threading.Thread(target=_open_browser_when_ready, args=(selected_port,), daemon=True).start()

    print(f"\n========================================================")
    print(f"🚀 SkillMatch IT - เซิร์ฟเวอร์พร้อมใช้งานแล้ว!")
    print(f"🌐 เข้าใช้งานผ่านเว็บเบราว์เซอร์: http://127.0.0.1:{selected_port}")
    print(f"   (กด Ctrl+C ในหน้าต่างนี้เพื่อหยุดการทำงาน)")
    print(f"========================================================\n")

    uvicorn.run(app, host="127.0.0.1", port=selected_port)
