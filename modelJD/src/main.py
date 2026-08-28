import os
import sys
import re
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from typing import List, Optional
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
    title="IT Job Recommendation & Skill Gap Analysis Engine",
    description="Content-Based Machine Learning Recommendation Engine based purely on Skills and Set Theory",
    version="3.0.0"
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
# 2. CONSTANTS & PROTECTED TECH TERMS
# ---------------------------------------------------------
PROTECTED_TECH_TERMS = {
    "ci/cd": "ci/cd",
    "ui/ux": "ui/ux",
    "tcp/ip": "tcp/ip",
    "c/c++": "c/c++",
    "pl/sql": "pl/sql",
    "asp.net": "asp.net",
    "asp.net core": "asp.net core",
    "asp.net mvc": "asp.net mvc",
    ".net": ".net",
    ".net core": ".net core",
    ".net framework": ".net framework",
    "node.js": "node.js",
    "react.js": "react.js",
    "vue.js": "vue.js",
    "next.js": "next.js",
    "nuxt.js": "nuxt.js"
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
    """ทำความสะอาดข้อความและตัดคำขยะสำหรับสร้างเวกเตอร์ TF-IDF"""
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

def clean_display_title(title: str) -> str:
    """ตัดคำขยายระดับส่วนเกินออกจากชื่อตำแหน่งเพื่อความสวยงามในการแสดงผล"""
    t = str(title).strip()
    if not t:
        return "IT Specialist"
    t_clean = re.sub(r'\s+[-–/]\s*(?:entry[- ]level|fresher|experienced|senior[- ]level|mid[- ]senior(?: level)?|junior|senior|lead|intern|level|\d+[\+\-]?\s*years?).*$', '', t, flags=re.IGNORECASE)
    t_clean = re.sub(r'^(?:entry[- ]level|entry\s+level|fresher|junior|senior|intern)\s+', '', t_clean, flags=re.IGNORECASE)
    t_clean = re.sub(r'\s+', ' ', t_clean).strip()
    return t_clean or t

def extract_career_family(title: str) -> str:
    """สกัดกลุ่มสายงานหลัก (Career Family) สำหรับการคัดกรองความหลากหลาย (Diversity Filter)"""
    t = str(title).lower().strip()
    if not t:
        return ""
    if re.search(r'\b(?:ethical hacker|penetration|pentest|hacker)\b', t):
        return "ethical_hacker"
    if re.search(r'\b(?:cybersecurity|information security|\bsoc\b|cyber defense)\b', t):
        return "cybersecurity"
    if re.search(r'\b(?:network engineer|network analyst|noc engineer|network)\b', t):
        return "network_engineer"
    if re.search(r'\b(?:system engineer|sysadmin|system administrator)\b', t):
        return "system_engineer"
    if re.search(r'\b(?:data science|data scientist)\b', t):
        return "data_scientist"
    if re.search(r'\b(?:data analyst|data analytics)\b', t):
        return "data_analyst"
    if re.search(r'\b(?:data engineer|big data)\b', t):
        return "data_engineer"
    if re.search(r'\b(?:business intelligence|bi analyst|bi developer)\b', t):
        return "bi_analyst"
    if re.search(r'\b(?:machine learning|deep learning|ai engineer|ai prompt|artificial intelligence|nlp|llm)\b', t):
        return "ai_engineer"
    if re.search(r'\b(?:frontend|front end)\b', t):
        return "frontend_developer"
    if re.search(r'\b(?:backend|back end)\b', t):
        return "backend_developer"
    if re.search(r'\b(?:fullstack|full stack)\b', t):
        return "fullstack_developer"
    if re.search(r'\b(?:\.net|dotnet)\b', t):
        return "dotnet_developer"
    if re.search(r'\b(?:python developer|python engineer)\b', t):
        return "python_developer"
    if re.search(r'\b(?:java developer|java engineer)\b', t):
        return "java_developer"
    if re.search(r'\b(?:devops|cloud|aws|azure|gcp|sre|site reliability|infrastructure)\b', t):
        return "devops_cloud"
    if re.search(r'\b(?:qa|quality assurance|tester|testing|test engineer|sdet)\b', t):
        return "qa_tester"
    if re.search(r'\b(?:ux|ui/ux|ui|designer|interaction designer|product designer)\b', t):
        return "ui_ux_designer"
    if re.search(r'\b(?:android|ios|mobile|flutter|react native)\b', t):
        return "mobile_developer"
    if re.search(r'\b(?:blockchain|solidity|ethereum|web3)\b', t):
        return "blockchain"
    if re.search(r'\b(?:software engineer|software developer|programmer)\b', t):
        return "software_engineer"
    
    t_clean = re.sub(r'\s+[-–/]\s*(?:entry[- ]level|fresher|experienced|senior[- ]level|mid[- ]senior(?: level)?|junior|senior|lead|intern|level|\d+[\+\-]?\s*years?).*$', '', t, flags=re.IGNORECASE)
    t_clean = re.sub(r'^(?:entry[- ]level|entry\s+level|fresher|junior|senior|intern)\s+', '', t_clean, flags=re.IGNORECASE)
    return re.sub(r'\s+', '_', t_clean).strip()

STANDARDIZED_ROLES = [
    ".NET Developer", "AI Engineer", "AI Prompt Engineer", "AR/VR Developer", 
    "Backend Developer", "Big Data Engineer", "Blockchain Developer", "Business Intelligence Analyst", 
    "Cloud Architect", "Cloud Cost Optimization Architect", "Cloud Engineer", "Cloud Infrastructure Architect", 
    "Cybersecurity Analyst", "Data Analyst", "Data Engineer", "Data Scientist", 
    "DevOps Engineer", "Ethical Hacker", "FinTech Engineer", "Flutter Developer", 
    "Frontend Developer", "Full Stack Developer", "Game Developer", "Hybrid Cloud Architect", 
    "Incident Response Analyst", "Information Security Analyst", "IoT Engineer", "Java Developer", 
    "Machine Learning Engineer", "Mobile App Developer", "Network Engineer", "Python Developer", 
    "QA Automation Engineer", "QA Tester", "Robotics Software Engineer", "Security Analyst", 
    "Site Reliability Engineer", "Software Developer", "Software Engineer", "Solutions Architect", 
    "System Administrator", "System Engineer", "Test Engineer", "UI/UX Designer", "Web Developer"
]

# ---------------------------------------------------------
# 3. LOAD DATASET & ML MODELS
# ---------------------------------------------------------
CSV_PATH = DATA_DIR / "job_dataset.csv"
if not CSV_PATH.exists():
    CSV_PATH = BASE_DIR / "job_dataset.csv"
if not CSV_PATH.exists():
    raise FileNotFoundError(f"❌ ไม่พบไฟล์ฐานข้อมูล {CSV_PATH}")

print(f"⏳ กำลังโหลดและทำความสะอาดข้อมูลตำแหน่งงานจาก '{CSV_PATH}'...")
df_jobs = pd.read_csv(CSV_PATH).fillna("")
df_jobs = df_jobs[df_jobs["Title"].str.strip() != ""].reset_index(drop=True)

# สกัดทักษะเดี่ยว Atomic Skills สำหรับทุกงาน
UNIQUE_SKILLS_LIST = []
for _, row in df_jobs.iterrows():
    UNIQUE_SKILLS_LIST.extend(extract_atomic_skills(str(row["Skills"])))
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
elif (BASE_DIR / "tfidf_vectorizer.joblib").exists():
    tfidf_vectorizer = joblib.load(BASE_DIR / "tfidf_vectorizer.joblib")
else:
    tfidf_vectorizer = TfidfVectorizer(stop_words="english", token_pattern=r'(?u)\b[\w+#.-]+\b', max_features=5000)
    tfidf_vectorizer.fit(df_jobs["combined_features"])

print("⏳ กำลังสร้าง Job TF-IDF Matrix...")
job_tfidf_matrix = tfidf_vectorizer.transform(df_jobs["combined_features"])

print(f"⏳ กำลังโหลดโมเดล Supervised ML จาก '{MODEL_PATH}'...")
if MODEL_PATH.exists():
    ml_model = joblib.load(MODEL_PATH)
elif (BASE_DIR / "model.joblib").exists():
    ml_model = joblib.load(BASE_DIR / "model.joblib")
else:
    try:
        from src.train_model import train_and_save_model
    except ImportError:
        from train_model import train_and_save_model
    train_and_save_model()
    ml_model = joblib.load(MODEL_PATH)

print("✅ โหลดโมเดล Logistic Regression และ TF-IDF Vectorizer เรียบร้อยแล้ว!")

# ---------------------------------------------------------
# 4. PYDANTIC SCHEMAS
# ---------------------------------------------------------
class RecommendRequest(BaseModel):
    preference: Optional[str] = ""     # สายงานเป้าหมาย (หรือ target_career)
    target_career: Optional[str] = ""  # รองรับ alias target_career
    skills: Optional[List[str]] = []   # ชุดทักษะที่มี (หัวใจหลักในการคำนวณ)

# ---------------------------------------------------------
# 5. API ENDPOINTS
# ---------------------------------------------------------
@app.get("/")
def root_check():
    return {
        "status": "online",
        "message": "Pure Skill-Based Machine Learning Recommendation Engine is running",
        "total_jobs": len(df_jobs),
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
    """ส่งคืนรายการทักษะไอทีเดี่ยว (Atomic Skills) ทั้งหมดในระบบสำหรับ Autocomplete ที่สะอาดและเป็นมาตรฐาน"""
    return {"skills": ALL_TECH_VOCABULARY}

@app.get("/api/roles")
def get_roles():
    """ส่งคืนรายชื่อตำแหน่งงานมาตรฐานสำหรับ Searchable Role Dropdown"""
    return {"roles": STANDARDIZED_ROLES}

@app.post("/recommend")
@app.post("/api/recommend")
def recommend_jobs(data: RecommendRequest):
    """
    ระบบแนะนำงาน Content-Based Machine Learning ด้วย 3 มิติฟีเจอร์ แบบ Dual-Section Recommendation
    1) target_career_analysis: วิเคราะห์ความพร้อมในสายงานเป้าหมาย พร้อม Skill Gap
    2) skill_matched_recommendations: ตำแหน่งงานที่ตรงกับทักษะจริงที่มีมากที่สุด Top 5
    """
    preference = (data.target_career or data.preference or "").strip()
    raw_skills = [clean_atomic_skill(s) for s in (data.skills or []) if clean_atomic_skill(s)]
    
    # ตรวจสอบความถูกต้องให้รับเฉพาะคำศัพท์ทักษะมาตรฐานที่อยู่ในระบบ
    valid_vocab_set = set(ALL_TECH_VOCABULARY)
    skills_list = [s for s in raw_skills if s in valid_vocab_set]
    
    if not preference and not skills_list:
        return {
            "status": "error",
            "message": "กรุณาระบุทักษะที่ถูกต้องจากฐานข้อมูล หรือเลือกสายงานที่สนใจครับ",
            "target_career_analysis": None,
            "skill_matched_recommendations": [],
            "results": []
        }

    pref_family = extract_career_family(preference) if preference else ""
    user_skills_set = set(skills_list)

    # 1. แปลงเวกเตอร์และสกัด 3 ฟีเจอร์หลัก (Orthogonal Feature Extraction)
    user_query = f"{preference} {' '.join(skills_list)}".strip()
    user_vec = tfidf_vectorizer.transform([user_query])
    similarity_scores = cosine_similarity(user_vec, job_tfidf_matrix).flatten()

    X_features = []
    candidate_profiles = []

    for idx in range(len(df_jobs)):
        row = df_jobs.iloc[idx]
        job_id = str(row.get("JobID", f"JOB-{idx+1:03d}")).strip()
        orig_title = str(row["Title"])
        core_title = clean_display_title(orig_title) or orig_title
        exp_level = str(row.get("ExperienceLevel", "")).strip() or "Entry-Level / Fresher"
        years_exp = str(row.get("YearsOfExperience", "")).strip() or "0-1"
        resps_raw = str(row.get("Responsibilities", "")).strip()
        keywords_raw = str(row.get("Keywords", "")).strip()
        skills_raw = str(row.get("Skills", ""))

        # สกัดทักษะของงานแบบ Atomic Item
        job_skills_list = extract_atomic_skills(skills_raw)

        # สกัดรายการความรับผิดชอบและคีย์เวิร์ดเป็น List
        resps_list = [r.strip() for r in re.split(r'[;\n\r|•]+', resps_raw) if r.strip()]
        keywords_list = [k.strip() for k in re.split(r'[;,|]+', keywords_raw) if k.strip()]

        matched_skills = [s for s in job_skills_list if s in user_skills_set]
        missing_skills = [s for s in job_skills_list if s not in user_skills_set]

        raw_sim = float(similarity_scores[idx])
        tfidf_sim = float(np.clip(raw_sim, 0.0, 1.0))
        exact_match_count = float(max(0, len(matched_skills)))
        num_job_skills = len(job_skills_list)
        skill_overlap_ratio = float(np.clip(exact_match_count / num_job_skills, 0.0, 1.0)) if num_job_skills > 0 else 0.0

        # เวกเตอร์คุณลักษณะ 3 มิติ [X1: tfidf_sim, X2: overlap_ratio, X3: exact_count]
        X_features.append([tfidf_sim, skill_overlap_ratio, exact_match_count])
        candidate_profiles.append({
            "idx": idx,
            "job_id": job_id,
            "title": core_title,
            "original_title": orig_title,
            "experience_level": exp_level,
            "years_of_experience": years_exp,
            "responsibilities": resps_raw,
            "responsibilities_list": resps_list,
            "keywords": keywords_raw,
            "keywords_list": keywords_list,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "semantic_score": int(round(tfidf_sim * 100)),
            "exact_score": int(round(skill_overlap_ratio * 100))
        })

    # 2. คำนวณคะแนนด้วยโมเดล Supervised Logistic Regression
    X_matrix = np.array(X_features)
    predicted_probabilities = ml_model.predict_proba(X_matrix)[:, 1]

    for i, profile in enumerate(candidate_profiles):
        ml_prob = float(predicted_probabilities[i])
        overlap = float(profile["exact_score"] / 100.0)
        semantic = float(profile["semantic_score"] / 100.0)
        
        # ปรับคะแนน Match Score ให้สะท้อนความเป็นจริงโดยให้น้ำหนัก Skill Coverage และ Exact Match ร่วมด้วย
        composite_score = (0.50 * ml_prob + 0.35 * overlap + 0.15 * semantic) * 100.0
        profile["score"] = int(np.clip(round(composite_score), 0, 100))
        profile["ml_confidence"] = int(round(ml_prob * 100))

    # 3. ส่วนที่ 1: วิเคราะห์สายงานเป้าหมาย (Target Career Analysis & Skill Gap)
    target_career_analysis = None
    if preference:
        pref_lower = preference.lower().strip()
        
        # 1) ค้นหาตำแหน่งงานที่ชื่อตรงกับ preference
        exact_title_matches = [
            c for c in candidate_profiles
            if pref_lower in c["title"].lower() or pref_lower in c["original_title"].lower()
        ]
        
        if exact_title_matches:
            best_target_job = max(exact_title_matches, key=lambda x: x["score"])
        elif pref_family:
            # 2) ค้นหาตำแหน่งใน Career Family เดียวกัน
            family_matches = [
                c for c in candidate_profiles
                if extract_career_family(c["original_title"]) == pref_family
            ]
            if family_matches:
                best_target_job = max(family_matches, key=lambda x: x["score"])
            else:
                best_target_job = max(candidate_profiles, key=lambda x: x["semantic_score"])
        else:
            best_target_job = max(candidate_profiles, key=lambda x: x["semantic_score"])

        total_req = len(best_target_job["matched_skills"]) + len(best_target_job["missing_skills"])
        readiness = round((len(best_target_job["matched_skills"]) / total_req) * 100.0, 1) if total_req > 0 else 0.0

        target_career_analysis = {
            "target_role": preference,
            "job_id": best_target_job["job_id"],
            "title": best_target_job["title"],
            "original_title": best_target_job["original_title"],
            "experience_level": best_target_job["experience_level"],
            "years_of_experience": best_target_job["years_of_experience"],
            "responsibilities": best_target_job["responsibilities"],
            "responsibilities_list": best_target_job.get("responsibilities_list", []),
            "keywords": best_target_job["keywords"],
            "keywords_list": best_target_job.get("keywords_list", []),
            "score": best_target_job["score"],
            "semantic_score": best_target_job["semantic_score"],
            "exact_score": best_target_job["exact_score"],
            "ml_confidence": best_target_job["ml_confidence"],
            "matched_skills": best_target_job["matched_skills"],
            "missing_skills": best_target_job["missing_skills"],
            "skill_readiness": readiness,
            "total_skills_count": total_req
        }

    # 4. ส่วนที่ 2: จัดอันดับตำแหน่งที่ตรงกับทักษะปัจจุบัน Top 5 (Skill Matched Recommendations)
    sorted_candidates = sorted(candidate_profiles, key=lambda x: x["score"], reverse=True)

    top_results = []
    seen_titles = set()
    family_counts = {}

    for cand in sorted_candidates:
        title_key = cand["title"].lower()
        cand_family = extract_career_family(cand["original_title"])

        # ป้องกันชื่อตำแหน่งงานซ้ำซ้อนใน Top 5
        if title_key in seen_titles:
            continue

        # กระจายความหลากหลายไม่ให้หมวดเดียวกันกินพื้นที่ทั้งหมด
        if cand_family:
            count = family_counts.get(cand_family, 0)
            if pref_family and cand_family == pref_family:
                if count >= 3:
                    continue
            else:
                if count >= 2:
                    continue
            family_counts[cand_family] = count + 1

        seen_titles.add(title_key)
        top_results.append(cand)

        if len(top_results) >= 5:
            break

    # Fallback หากยังไม่ครบ 5 ตำแหน่ง
    if len(top_results) < 5:
        for cand in sorted_candidates:
            if cand not in top_results:
                title_key = cand["title"].lower()
                if title_key not in seen_titles:
                    seen_titles.add(title_key)
                    top_results.append(cand)
                    if len(top_results) >= 5:
                        break

    return {
        "status": "success",
        "target_career_analysis": target_career_analysis,
        "skill_matched_recommendations": top_results,
        "results": top_results,  # รองรับระบบเดิม
        "total_matched": len(top_results)
    }

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 กำลังเริ่มต้นเซิร์ฟเวอร์ Pure Skill-Based Recommendation ที่ http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
