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
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

TFIDF_PATH = MODELS_DIR / "tfidf_vectorizer.joblib"
MODEL_PATH = MODELS_DIR / "model.joblib"

print(f"⏳ กำลังโหลด TF-IDF Vectorizer จาก '{TFIDF_PATH}'...")
if TFIDF_PATH.exists():
    tfidf_vectorizer = joblib.load(TFIDF_PATH)
else:
    tfidf_vectorizer = TfidfVectorizer(stop_words="english", token_pattern=r'(?u)\b[\w+#.-]+\b', max_features=5000)
    tfidf_vectorizer.fit(df_jobs["combined_features"])

print("⏳ กำลังสร้าง Job TF-IDF Matrix...")
job_tfidf_matrix = tfidf_vectorizer.transform(df_jobs["combined_features"])

print(f"⏳ กำลังโหลดโมเดล Supervised ML จาก '{MODEL_PATH}'...")
if MODEL_PATH.exists():
    ml_model = joblib.load(MODEL_PATH)
else:
    from src.train_model import train_and_save_model
    train_and_save_model()
    ml_model = joblib.load(MODEL_PATH)

print("✅ โหลดโมเดลและฐานข้อมูล 8 อาชีพ มคอ.2 เรียบร้อยแล้ว!")

# ---------------------------------------------------------
# 5. PYDANTIC SCHEMAS
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
    ระบบแนะนำงาน Content-Based Machine Learning ด้วย 3 มิติฟีเจอร์ แบบ Dual-Section
    1) target_career_analysis: วิเคราะห์ความพร้อมในสายงานเป้าหมายตามหลักสูตร มคอ.2 พร้อม Skill Gap Roadmap
    2) skill_matched_recommendations: ตำแหน่งงานจริงในตลาดไอทีไทยที่ตรงกับทักษะมากที่สุด Top 5
    """
    preference = (data.target_career or data.preference or "").strip()
    raw_skills = [clean_atomic_skill(s) for s in (data.skills or []) if clean_atomic_skill(s)]
    
    valid_vocab_set = set(ALL_TECH_VOCABULARY)
    skills_list = [s for s in raw_skills if s in valid_vocab_set]
    # #7: เก็บ skills ที่ไม่อยู่ใน vocabulary เพื่อส่งกลับใน response
    unrecognized_skills = [s for s in raw_skills if s not in valid_vocab_set]

    if not preference and not skills_list:
        return {
            "status": "error",
            "message": "กรุณาระบุทักษะที่ถูกต้อง หรือเลือกสายงานเป้าหมายตามหลักสูตร มคอ.2 ครับ",
            "target_career_analysis": None,
            "skill_matched_recommendations": [],
            "results": []
        }

    user_skills_set = set(skills_list)

    # 1. สกัด 3 มิติฟีเจอร์ [X1: TF-IDF Cosine, X2: Overlap Ratio, X3: Exact Count]
    user_query = f"{preference} {' '.join(skills_list)}".strip()
    user_vec = tfidf_vectorizer.transform([user_query])
    similarity_scores = cosine_similarity(user_vec, job_tfidf_matrix).flatten()

    X_features = []
    candidate_profiles = []

    for idx in range(len(df_jobs)):
        row = df_jobs.iloc[idx]
        job_id = str(row.get("JobID", f"JOB-{idx+1:03d}")).strip()
        orig_title = str(row["Title"])
        curr_id = str(row.get("CurriculumRoleID", "8.6")).strip()
        curr_title = str(row.get("CurriculumRoleTitle", "นักพัฒนาซอฟต์แวร์")).strip()
        curr_en = str(row.get("CurriculumRoleEN", "Software Developer")).strip()
        company = str(row.get("Company", "บริษัทเทคโนโลยีในไทย")).strip()
        province = str(row.get("Province", "กรุงเทพมหานคร")).strip()
        salary = str(row.get("Salary", "ตามตกลง / โครงสร้างบริษัท")).strip()
        exp_level = str(row.get("ExperienceLevel", "Entry-Level / เด็กจบใหม่ (0-1 ปี)")).strip()
        years_exp = str(row.get("YearsOfExperience", "0-1")).strip()
        resps_raw = str(row.get("Responsibilities", "")).strip()
        keywords_raw = str(row.get("Keywords", "")).strip()
        skills_raw = str(row.get("Skills", ""))
        apply_url = str(row.get("ApplyURL", "https://jobs.blognone.com")).strip()

        job_skills_list = extract_atomic_skills(skills_raw)
        resps_list = [r.strip() for r in re.split(r'[;\n\r|•]+', resps_raw) if len(r.strip()) > 5]
        keywords_list = [k.strip() for k in re.split(r'[;,|]+', keywords_raw) if k.strip()]

        matched_skills = [s for s in job_skills_list if s in user_skills_set]
        missing_skills = [s for s in job_skills_list if s not in user_skills_set]

        raw_sim = float(similarity_scores[idx])
        tfidf_sim = float(np.clip(raw_sim, 0.0, 1.0))
        exact_match_count = float(max(0, len(matched_skills)))
        num_job_skills = len(job_skills_list)
        skill_overlap_ratio = float(np.clip(exact_match_count / num_job_skills, 0.0, 1.0)) if num_job_skills > 0 else 0.0

        X_features.append([tfidf_sim, skill_overlap_ratio, exact_match_count])
        candidate_profiles.append({
            "idx": idx,
            "job_id": job_id,
            "title": orig_title,
            "curriculum_role_id": curr_id,
            "curriculum_role_title": curr_title,
            "curriculum_role_en": curr_en,
            "company": company,
            "province": province,
            "salary": salary,
            "experience_level": exp_level,
            "years_of_experience": years_exp,
            "responsibilities": resps_raw,
            "responsibilities_list": resps_list[:4],
            "keywords": keywords_raw,
            "keywords_list": keywords_list[:6],
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "apply_url": apply_url,
            "semantic_score": int(round(tfidf_sim * 100)),
            "exact_score": int(round(skill_overlap_ratio * 100))
        })

    if not candidate_profiles:
        return {
            "status": "error",
            "message": "ไม่พบข้อมูลตำแหน่งงานในฐานข้อมูลสำหรับทำการประมวลผล",
            "target_career_analysis": None,
            "skill_matched_recommendations": [],
            "results": [],
            "total_matched": 0,
            "unrecognized_skills": unrecognized_skills
        }

    # 2. คำนวณ Match Score ด้วยโมเดล Calibrated Logistic Regression
    X_matrix = np.array(X_features)
    predicted_probabilities = ml_model.predict_proba(X_matrix)[:, 1]

    for i, profile in enumerate(candidate_profiles):
        ml_prob = float(predicted_probabilities[i])
        overlap = float(profile["exact_score"] / 100.0)
        semantic = float(profile["semantic_score"] / 100.0)
        
        composite_score = (0.50 * ml_prob + 0.35 * overlap + 0.15 * semantic) * 100.0
        profile["score"] = int(np.clip(round(composite_score), 0, 100))
        profile["ml_confidence"] = int(round(ml_prob * 100))

    # 3. ส่วนที่ 1: วิเคราะห์ความพร้อมใน 8 อาชีพ มคอ.2 (Target Curriculum Career Analysis & Skill Gap)
    target_career_analysis = None
    target_role_info = match_curriculum_role(preference) if preference else None

    if target_role_info:
        role_id = target_role_info["id"]
        role_title = target_role_info["title"]
        core_skills = [clean_atomic_skill(s) for s in target_role_info["core_skills"]]
        
        matched_core = [s for s in core_skills if s in user_skills_set]
        missing_core = [s for s in core_skills if s not in user_skills_set]
        
        total_core = len(core_skills)
        readiness = round((len(matched_core) / total_core) * 100.0, 1) if total_core > 0 else 0.0

        # ค้นหาตำแหน่งงานจริงในไทยที่อยู่ในหมวดอาชีพนี้ที่มีคะแนนสูงสุด
        role_jobs = [c for c in candidate_profiles if c["curriculum_role_id"] == role_id]
        if not role_jobs:
            role_jobs = candidate_profiles
            
        best_target_job = max(role_jobs, key=lambda x: x["score"])

        target_career_analysis = {
            "target_role_id": role_id,
            "target_role_title": role_title,
            "target_role_en": target_role_info["en_title"],
            "target_role_desc": target_role_info["desc"],
            "job_id": best_target_job["job_id"],
            "title": best_target_job["title"],
            "company": best_target_job["company"],
            "province": best_target_job["province"],
            "salary": best_target_job["salary"],
            "experience_level": best_target_job["experience_level"],
            "years_of_experience": best_target_job["years_of_experience"],
            "responsibilities": best_target_job["responsibilities"],
            "responsibilities_list": best_target_job["responsibilities_list"],
            "apply_url": best_target_job["apply_url"],
            "score": best_target_job["score"],
            "semantic_score": best_target_job["semantic_score"],
            "exact_score": best_target_job["exact_score"],
            "ml_confidence": best_target_job["ml_confidence"],
            "matched_skills": matched_core,
            "missing_skills": missing_core,
            "skill_readiness": readiness,
            "total_skills_count": total_core
        }

    # 4. ส่วนที่ 2: จัดอันดับตำแหน่งงานจริงในไทยที่ตรงกับทักษะ Top 5 (Skill Matched Recommendations)
    sorted_candidates = sorted(candidate_profiles, key=lambda x: x["score"], reverse=True)

    top_results = []
    seen_titles = set()
    role_counts = {}

    target_id = target_role_info["id"] if target_role_info else ""

    for cand in sorted_candidates:
        title_key = cand["title"].lower()
        cand_role_id = cand["curriculum_role_id"]

        if title_key in seen_titles:
            continue

        # กระจายความหลากหลายไม่ให้สายงานเดียวยึด Top 5 ทั้งหมด
        count = role_counts.get(cand_role_id, 0)
        if target_id and cand_role_id == target_id:
            if count >= 3:
                continue
        else:
            if count >= 2:
                continue
        role_counts[cand_role_id] = count + 1

        seen_titles.add(title_key)
        top_results.append(cand)

        if len(top_results) >= 5:
            break

    # Fallback หากยังไม่ครบ 5 ตำแหน่ง
    if len(top_results) < 5:
        for cand in sorted_candidates:
            title_key = cand["title"].lower()
            if title_key not in seen_titles:
                top_results.append(cand)
                seen_titles.add(title_key)
                if len(top_results) >= 5:
                    break

    return {
        "status": "success",
        "target_career_analysis": target_career_analysis,
        "skill_matched_recommendations": top_results,
        "results": top_results,
        "total_matched": len(top_results),
        "unrecognized_skills": unrecognized_skills  # #7: ทักษะที่ไม่อยู่ใน vocabulary
    }

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 กำลังเริ่มต้นเซิร์ฟเวอร์ SkillMatch IT (TQF มคอ.2) ที่ http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
