r"""
========================================================================================
🎓 SCRIPT สื่อการเรียนรู้: การทำงานของระบบ Job Recommendation Engine แบบ Step-by-Step
========================================================================================
โครงสร้างสถาปัตยกรรม 5 ขั้นตอน (End-to-End Pure Skill Machine Learning Pipeline)

  [Step 1] Data Loading & Atomic Vocabulary Building (1,600 คำศัพท์มาตรฐาน)
     ↓
  [Step 2] User Profile Specification (Mock Input)
     ↓
  [Step 3] 3-Dimensional Feature Extraction (X1: Semantic, X2: Coverage, X3: Exact Count)
     ↓
  [Step 4] Supervised ML Prediction & Diversity-Aware Ranking (Logistic Regression Top-5)
     ↓
  [Step 5] Skill Gap Analysis via Set Operations (Intersection ∩ & Difference \)
========================================================================================
"""

import os
import sys
import re
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.train_model import CURRICULUM_ROLES, map_job_to_curriculum_id

# --------------------------------------------------------------------------------------
# คำศัพท์เฉพาะทางไอทีที่ห้ามแยก Slash (Protected IT Terms)
# --------------------------------------------------------------------------------------
PROTECTED_TECH_TERMS = {
    "ci/cd": "ci/cd", "ui/ux": "ui/ux", "tcp/ip": "tcp/ip", "c/c++": "c/c++",
    "pl/sql": "pl/sql", "asp.net": "asp.net", "asp.net core": "asp.net core",
    "asp.net mvc": "asp.net mvc", ".net": ".net", ".net core": ".net core",
    ".net framework": ".net framework", "node.js": "node.js", "react.js": "react.js",
    "next.js": "next.js", "nuxt.js": "nuxt.js"
}

DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
SRC_DIR = BASE_DIR / "src"

DEFAULT_CSV_PATH = DATA_DIR / "job_dataset.csv"
DEFAULT_MODEL_PATH = MODELS_DIR / "model.joblib"
DEFAULT_TFIDF_PATH = MODELS_DIR / "tfidf_vectorizer.joblib"

# ======================================================================================
# ฟังก์ชันทำความสะอาดข้อมูล (Data Cleaning Utilities)
# ======================================================================================

def clean_atomic_skill(skill: str) -> str:
    """
    ทำความสะอาดและปรับมาตรฐานชื่อทักษะ (Skill Normalization)
    - ตัดคำขยายระดับ เช่น basics, fundamentals, knowledge of
    - ลบเครื่องหมายวรรคตอนและคำเชื่อมภาษาอังกฤษ
    """
    if not skill or not isinstance(skill, str):
        return ""
    s = skill.strip().lower()
    s = re.sub(
        r'\b(basics?|fundamentals?|testing with|knowledge of|experience in|working with|advanced|overview|proficiency in|good to have|familiarity with|strong in|awareness|expert|experienced|exposure)\b',
        '', s, flags=re.IGNORECASE
    )
    s = re.sub(r'[\(\)\[\]\{\}]', ' ', s)
    s = s.strip(" ,;:-_./|&")
    s = re.sub(r'^(?:and|or|with|for|in|to|of|on|a|an|the)\s+', '', s)
    s = re.sub(r'\s+(?:and|or|with|for|in|to|of|on|a|an|the)$', '', s)
    return re.sub(r'\s+', ' ', s).strip()

def extract_atomic_skills(raw_text: str) -> list:
    """
    แยกและสกัดข้อความทักษะที่ติดเครื่องหมาย (:, ,, /) ให้เป็นคำเดี่ยวๆ (Atomic Skills)
    ตัวอย่าง:
      'Monitoring: CloudWatch, Prometheus' -> ['cloudwatch', 'prometheus']
      'Docker/Kubernetes'                  -> ['docker', 'kubernetes']
    """
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
            for sp in tok.split('/'):
                cleaned = clean_atomic_skill(sp)
                if cleaned and len(cleaned) >= 2 and not cleaned.isdigit():
                    if cleaned not in ["tools", "technologies", "etc", "basics", "skills", "ml/dl", "ml", "dl", "monitoring"]:
                        final_skills.append(cleaned)
        else:
            cleaned = clean_atomic_skill(tok)
            if cleaned and len(cleaned) >= 2 and not cleaned.isdigit():
                if cleaned not in ["tools", "technologies", "etc", "basics", "skills", "ml/dl", "ml", "dl", "monitoring"]:
                    final_skills.append(cleaned)
    return list(dict.fromkeys(final_skills))

def clean_text_pipeline(text: str) -> str:
    """ทำความสะอาดข้อความเนื้อหาตำแหน่งงานและตัดคำขยะสำหรับสร้างเวกเตอร์ TF-IDF"""
    if not text or not isinstance(text, str):
        return ""
    t = text.lower()
    noise_patterns = [
        r'\b(basics?|fundamentals?|testing with|knowledge of|experience in|working with)\b',
        r'\b(assist in|support team in|collaborate with|participate in|learn and apply)\b',
        r'\b(fresher|entry-level|junior|senior|intern)\b'
    ]
    for pattern in noise_patterns:
        t = re.sub(pattern, ' ', t, flags=re.IGNORECASE)
    t = re.sub(r'[;/|\n\r]+', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

def clean_display_title(title: str) -> str:
    """ตัดคำขยายระดับส่วนเกินออกจากชื่อตำแหน่งเพื่อความสวยงามในการแสดงผล"""
    t = str(title).strip()
    if not t:
        return "IT Specialist"
    t_clean = re.sub(r'\s+[-–/]\s*(?:entry[- ]level|fresher|experienced|senior[- ]level|mid[- ]senior(?: level)?|junior|senior|lead|intern|level|\d+[\+\-]?\s*years?).*$', '', t, flags=re.IGNORECASE)
    t_clean = re.sub(r'^(?:entry[- ]level|entry\s+level|fresher|junior|senior|intern)\s+', '', t_clean, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', t_clean).strip() or t

def extract_career_family(title: str) -> str:
    """สกัดกลุ่มสายงานหลัก (Career Family) เพื่อใช้คัดกรองความหลากหลายของผลลัพธ์ (Diversity Filter)"""
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


# ======================================================================================
# STEP 1: DATA LOADING & ATOMIC SKILL VOCABULARY EXTRACTION
# ======================================================================================

def step1_load_and_build_vocabulary(csv_path = None):
    """
    ขั้นตอนที่ 1: โหลด Dataset ตำแหน่งงาน, สกัดคอลัมน์ Skills, และสร้าง Vocabulary List
    """
    if csv_path is None:
        csv_path = DEFAULT_CSV_PATH if DEFAULT_CSV_PATH.exists() else (BASE_DIR / "job_dataset.csv")
    csv_path = Path(csv_path)

    print("\n" + "=" * 80)
    print("📌 STEP 1: DATA LOADING & ATOMIC SKILL VOCABULARY EXTRACTION")
    print("=" * 80)
    print(f"⏳ กำลังโหลดข้อมูลตำแหน่งงานจากไฟล์: '{csv_path}'...")
    
    if not csv_path.exists():
        raise FileNotFoundError(f"❌ ไม่พบไฟล์ {csv_path} กรุณาตรวจสอบว่าอยู่ในโฟลเดอร์ data/")
        
    df_jobs = pd.read_csv(csv_path).fillna("")
    # กรองแถวที่ไม่มีชื่อตำแหน่งงานออก
    df_jobs = df_jobs[df_jobs["Title"].str.strip() != ""].reset_index(drop=True)
    
    # สกัดคลังทักษะแบบ Atomic ทั้งหมด
    unique_skills_set = set()
    job_skills_list = []
    
    for _, row in df_jobs.iterrows():
        skills_raw = str(row.get("Skills", ""))
        extracted = extract_atomic_skills(skills_raw)
        job_skills_list.append(extracted)
        unique_skills_set.update(extracted)
        
    df_jobs["cleaned_skills_list"] = job_skills_list
    vocabulary_list = sorted(list(unique_skills_set))
    
    print(f"✅ โหลดตำแหน่งงานสำเร็จทั้งหมด: {len(df_jobs):,} ตำแหน่งงาน")
    print(f"✅ สกัดคำศัพท์ทักษะเดี่ยว (Atomic Vocabulary) ได้ทั้งหมด: {len(vocabulary_list):,} ทักษะ")
    print(f"🔍 ตัวอย่างคำศัพท์ 10 คำแรก: {vocabulary_list[:10]}")
    
    return df_jobs, vocabulary_list


# ======================================================================================
# STEP 2: USER PROFILE & INPUT SPECIFICATION
# ======================================================================================

def step2_get_user_profile():
    """
    ขั้นตอนที่ 2: กำหนดชุดข้อมูลนำเข้าจำลองของผู้ใช้ (Mock User Skills & Target Role)
    """
    print("\n" + "=" * 80)
    print("📌 STEP 2: USER PROFILE & INPUT SPECIFICATION")
    print("=" * 80)
    
    # กำหนดตัวอย่างทักษะของผู้ใช้
    user_skills = ["python", "aws", "azure", "terraform"]
    target_role = "Cloud Engineer"  # สามารถเว้นว่าง "" หรือระบุชื่อสายงานได้
    
    print("👤 ข้อมูลผู้ใช้จำลอง (User Input Profile):")
    print(f"  • สายงานที่สนใจ (Target Role) : {target_role if target_role else '(ไม่ได้ระบุ - ค้นหาจากทุกสายงาน)'}")
    print(f"  • ทักษะที่มี (User Skills)    : {user_skills}")
    print(f"  • จำนวนทักษะที่เลือก          : {len(user_skills)} ทักษะ")
    
    return user_skills, target_role


# ======================================================================================
# STEP 3: 3-DIMENSIONAL FEATURE EXTRACTION (X1, X2, X3)
# ======================================================================================

def step3_extract_features(df_jobs: pd.DataFrame, user_skills: list, target_role: str = ""):
    """
    ขั้นตอนที่ 3: สกัดเวกเตอร์คุณลักษณะ 3 มิติ [X1, X2, X3]
    
    📐 ที่มาของสูตรคณิตศาสตร์และนิยามเชิงวิชาการ (Academic Formulation):
    ------------------------------------------------------------------------------------
    1. ฟีเจอร์ X1: TF-IDF Cosine Similarity (ความคล้ายคลึงเชิงความหมายในเวกเตอร์สเปซ)
       สูตรคณิตศาสตร์:
          Cosine Similarity(u, d) = (u · d) / (||u||_2 * ||d||_2)
       เนื่องจาก Scikit-Learn TfidfVectorizer ทำ L2 Normalization (||v||_2 = 1) ให้อัตโนมัติ
       ดังนั้น Cosine Similarity จึงเทียบเท่ากับผลคูณดอต (Dot Product: u · d) โดยตรง
       ค่าที่ได้จะอยู่ในช่วง [0.0, 1.0] สะท้อนว่าบริบทข้อความตรงกับรายละเอียดงานมากน้อยเพียงใด
       
    2. ฟีเจอร์ X2: Job Skill Coverage Ratio (สัดส่วนความครอบคลุมของทักษะที่งานต้องการ)
       สูตรคณิตศาสตร์ (Recall-oriented Index):
          Coverage Ratio = |S_user ∩ S_job| / |S_job|
       ค่าที่ได้จะอยู่ในช่วง [0.0, 1.0] แสดงถึงความพร้อมต่อคุณสมบัติที่ตำแหน่งงานนั้นต้องการจริง
       (ต่างจาก Jaccard Similarity |A ∩ B| / |A ∪ B| เพราะเราต้องการวัดความครบถ้วนตามความต้องการของ Job)
       
    3. ฟีเจอร์ X3: Exact Match Count (จำนวนทักษะที่ตรงกันจริง)
       สูตรคณิตศาสตร์:
          Exact Count = |S_user ∩ S_job|
       เป็นจำนวนเต็ม >= 0 สะท้อนปริมาณทักษะที่ตรงกันโดยตรง
    ------------------------------------------------------------------------------------
    """
    print("\n" + "=" * 80)
    print("📌 STEP 3: 3-DIMENSIONAL FEATURE EXTRACTION (X1, X2, X3)")
    print("=" * 80)
    
    # 1. รวมข้อความเพื่อสร้างโมเดล TF-IDF Representation
    clean_titles = df_jobs["Title"].apply(clean_text_pipeline)
    clean_skills = df_jobs["Skills"].apply(clean_text_pipeline)
    clean_resps = df_jobs["Responsibilities"].apply(clean_text_pipeline) if "Responsibilities" in df_jobs else pd.Series([""] * len(df_jobs))
    clean_keywords = df_jobs["Keywords"].apply(clean_text_pipeline) if "Keywords" in df_jobs else pd.Series([""] * len(df_jobs))
    df_jobs["combined_features"] = clean_titles + " " + clean_skills + " " + clean_resps + " " + clean_keywords

    # 2. โหลดหรือสร้าง TF-IDF Vectorizer
    tfidf_file = DEFAULT_TFIDF_PATH if DEFAULT_TFIDF_PATH.exists() else (BASE_DIR / "tfidf_vectorizer.joblib")
    if tfidf_file.exists():
        tfidf_vectorizer = joblib.load(tfidf_file)
    else:
        tfidf_vectorizer = TfidfVectorizer(stop_words="english", token_pattern=r'(?u)\b[\w+#.-]+\b', max_features=5000)
        tfidf_vectorizer.fit(df_jobs["combined_features"])
        
    job_tfidf_matrix = tfidf_vectorizer.transform(df_jobs["combined_features"])

    # 3. แปลงคำค้นหาของผู้ใช้เป็นเวกเตอร์
    user_query = f"{target_role} {' '.join(user_skills)}".strip()
    user_vec = tfidf_vectorizer.transform([user_query])
    
    # คำนวณ Cosine Similarity เทียบกับทุกงานใน Database
    similarity_scores = cosine_similarity(user_vec, job_tfidf_matrix).flatten()

    user_skills_set = set([clean_atomic_skill(s) for s in user_skills])
    X_features = []
    candidate_profiles = []

    for idx in range(len(df_jobs)):
        row = df_jobs.iloc[idx]
        orig_title = str(row["Title"])
        core_title = clean_display_title(orig_title)
        job_skills = row["cleaned_skills_list"]

        # ทฤษฎีเซต: หา Intersection และ Difference
        matched = [s for s in job_skills if s in user_skills_set]
        missing = [s for s in job_skills if s not in user_skills_set]

        # คำนวณค่า 4 ฟีเจอร์ตามมาตรฐาน มคอ.2
        x1_tfidf_sim = float(np.clip(similarity_scores[idx], 0.0, 1.0))
        x4_exact_cnt = float(len(matched))
        x3_coverage_ratio = float(x4_exact_cnt / len(job_skills)) if len(job_skills) > 0 else 0.0

        role_id = map_job_to_curriculum_id(core_title, job_skills)
        core_role_skills = CURRICULUM_ROLES.get(role_id, CURRICULUM_ROLES["8.6"])["core_skills"]
        matched_core = [s for s in core_role_skills if s in user_skills_set]
        x2_core_cov = float(len(matched_core) / max(1, len(core_role_skills)))

        X_features.append([x1_tfidf_sim, x2_core_cov, x3_coverage_ratio, x4_exact_cnt])
        candidate_profiles.append({
            "idx": idx,
            "title": core_title,
            "original_title": orig_title,
            "matched_skills": matched,
            "missing_skills": missing,
            "x1_semantic": x1_tfidf_sim,
            "x2_core": x2_core_cov,
            "x3_coverage": x3_coverage_ratio,
            "x4_exact": x4_exact_cnt
        })

    # แสดงตารางตัวอย่าง 3 แถวแรก
    print("📊 ตารางตัวอย่างค่าฟีเจอร์ [X1, X2, X3, X4] สำหรับ 3 ตำแหน่งงานแรก:")
    print("-" * 80)
    print(f"{'No.':<4} | {'Job Title':<30} | {'X1 (Semantic)':<13} | {'X2 (Core)':<10} | {'X3 (Stack)':<10} | {'X4 (Count)'}")
    print("-" * 80)
    for i in range(3):
        p = candidate_profiles[i]
        print(f"{i+1:<4} | {p['title'][:30]:<30} | {p['x1_semantic']:<13.4f} | {p['x2_core']:<10.4f} | {p['x3_coverage']:<10.4f} | {int(p['x4_exact'])}")
    print("-" * 80)

    return np.array(X_features), candidate_profiles


# ======================================================================================
# STEP 4: MODEL PREDICTION & TOP-5 RANKING
# ======================================================================================

def step4_predict_and_rank(X_matrix: np.ndarray, candidate_profiles: list, user_pref: str = "", model_path = None, top_k: int = 5):
    """
    ขั้นตอนที่ 4: นำค่า X1, X2, X3, X4 เข้าโมเดล Logistic Regression เพื่อคำนวณ Match Score (0-100%)
    
    📐 ที่มาของสมการโมเดลและการสอบเทียบ (Model Rigor & Calibration):
    ------------------------------------------------------------------------------------
    1. โมเดล Logistic Regression Sigmoid Function:
       P(Qualified=1 | X) = σ(z) = 1 / (1 + e^-(beta_0 + beta_1*X1 + beta_2*X2 + beta_3*X3 + beta_4*X4))
       โดยฟีเจอร์ผ่านการทำ Standard Scaling (Mean=0, Std=1) ก่อนเข้าสมการ Sigmoid
       
    2. คะแนนความพร้อม (Readiness Score):
       Readiness Score = P(Qualified=1 | X) * 100%
       สะท้อนความน่าจะเป็นที่ผู้สมัครมีคุณสมบัติผ่านเกณฑ์ มคอ.2 โดยตรงจากโมเดล
       
    3. การคัดกรองความหลากหลายของสายงาน (Career Family Diversity Filter):
       ป้องกันไม่ให้ตำแหน่งงานในหมวดเดียวกันกินพื้นที่ผลลัพธ์ Top 5 ทั้งหมด
    ------------------------------------------------------------------------------------
    """
    print("\n" + "=" * 80)
    print(f"📌 STEP 4: MODEL PREDICTION & TOP-{top_k} RANKING (DIVERSITY-AWARE)")
    print("=" * 80)

    if model_path is None:
        model_path = DEFAULT_MODEL_PATH if DEFAULT_MODEL_PATH.exists() else (BASE_DIR / "model.joblib")
    model_path = Path(model_path)

    if not model_path.exists():
        raise FileNotFoundError(f"❌ ไม่พบไฟล์โมเดล '{model_path}' กรุณารัน train_model.py ก่อน")
        
    ml_model = joblib.load(model_path)
    predicted_probabilities = ml_model.predict_proba(X_matrix)[:, 1]

    for i, profile in enumerate(candidate_profiles):
        ml_prob = float(predicted_probabilities[i])
        profile["score"] = int(np.clip(round(ml_prob * 100), 0, 100))

    # จัดอันดับตามคะแนนจากมากไปน้อย
    sorted_candidates = sorted(candidate_profiles, key=lambda x: x["score"], reverse=True)

    # กรองความหลากหลายของสายงานและชื่อตำแหน่ง (Diversity Filtering)
    pref_family = extract_career_family(user_pref) if user_pref else ""
    top_results = []
    seen_titles = set()
    family_counts = {}

    for cand in sorted_candidates:
        title_key = cand["title"].lower()
        cand_family = extract_career_family(cand["original_title"])

        if title_key in seen_titles:
            continue

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

        if len(top_results) >= top_k:
            break

    print(f"🏆 ผลการจัดอันดับ Top {len(top_results)} ตำแหน่งงานที่เหมาะสมที่สุด:")
    print("-" * 80)
    for rank, job in enumerate(top_results, 1):
        # สร้างแท่ง Progress Bar แสดงคะแนนใน Terminal
        bar_len = 20
        filled = int(round(bar_len * (job['score'] / 100.0)))
        bar = "█" * filled + "░" * (bar_len - filled)
        
        print(f"อันดับที่ {rank}: {job['title']}")
        print(f"  คะแนนความเหมาะสม : [{bar}] {job['score']:>3}%")
        print(f"  มิติการคำนวณ     : Semantic={int(job['x1_semantic']*100)}% | Core={int(job['x2_core']*100)}% | Stack={int(job['x3_coverage']*100)}% | Exact={int(job['x4_exact'])} ทักษะ")
        print(f"  ทักษะที่ตรงกัน   : {job['matched_skills']}")
        print("-" * 80)

    return top_results


# ======================================================================================
# STEP 5: SKILL GAP ANALYSIS VIA SET OPERATIONS
# ======================================================================================

def step5_skill_gap_analysis(top_job: dict, user_skills: list):
    r"""
    ขั้นตอนที่ 5: วิเคราะห์ช่องว่างทางทักษะ (Skill Gap Analysis) ด้วยทฤษฎีเซต (Set Theory)
    
    📐 ที่มาของสูตรเซต:
    ------------------------------------------------------------------------------------
    1. ทักษะที่มีตรงกัน (Matched Skills) -> Intersection (S_user ∩ S_job)
    2. ทักษะที่ยังขาดอยู่ (Missing Skills) -> Difference (S_job \ S_user)
    ------------------------------------------------------------------------------------
    """
    print("\n" + "=" * 80)
    print("📌 STEP 5: SKILL GAP ANALYSIS (SET OPERATIONS)")
    print("=" * 80)
    
    user_set = set([clean_atomic_skill(s) for s in user_skills])
    job_skills_all = top_job["matched_skills"] + top_job["missing_skills"]
    job_set = set(job_skills_all)

    # คำนวณด้วย Set Operations
    matched_skills = sorted(list(user_set.intersection(job_set)))
    missing_skills = sorted(list(job_set.difference(user_set)))

    print(f"🎯 วิเคราะห์ตำแหน่งอันดับที่ 1: '{top_job['title']}' (คะแนนรวม: {top_job['score']}%)")
    print(f"  • ทักษะทั้งหมดที่ตำแหน่งนี้ต้องการ ({len(job_skills_all)} ทักษะ): {job_skills_all}")
    print("\n" + "─" * 60)
    print(f"  ✅ 1. ทักษะที่คุณมีตรงกับงานนี้ [Intersection ∩] ({len(matched_skills)} ทักษะ):")
    for s in matched_skills:
        print(f"     [✔] {s}")
        
    print("\n" + "─" * 60)
    print(f"  ⚠️  2. ทักษะที่ควรศึกษาเพิ่มเติม [Difference \\] ({len(missing_skills)} ทักษะ):")
    for s in missing_skills:
        print(f"     [➕] {s} (แนะนำให้ศึกษาเพิ่มเติมเพื่อเพิ่มโอกาสการได้งาน)")
    print("=" * 80 + "\n")


# ======================================================================================
# MAIN EXECUTION PIPELINE
# ======================================================================================

def main_pipeline_walkthrough():
    """ฟังก์ชันหลักสำหรับรันการทำงานทั้ง 5 ขั้นตอนแบบต่อเนื่อง"""
    print("\n" + "🚀" * 40)
    print("🌟 ยินดีต้อนรับสู่สคริปต์สอนระบบ Job Recommendation Engine (ML Walkthrough) 🌟")
    print("🚀" * 40)

    # 1. Load Data & Build Vocabulary
    df_jobs, vocabulary_list = step1_load_and_build_vocabulary(DEFAULT_CSV_PATH)

    # 2. Get User Profile
    user_skills, target_role = step2_get_user_profile()

    # 3. Extract 3-D Features
    X_matrix, candidate_profiles = step3_extract_features(df_jobs, user_skills, target_role)

    # 4. Predict & Rank Top-5 with Diversity Filter
    top_results = step4_predict_and_rank(X_matrix, candidate_profiles, user_pref=target_role, model_path=DEFAULT_MODEL_PATH, top_k=5)

    # 5. Skill Gap Analysis on Top-1
    if top_results:
        step5_skill_gap_analysis(top_results[0], user_skills)

    print("🎉 การประมวลผลและการอธิบายครบทั้ง 5 ขั้นตอนเสร็จสิ้นสมบูรณ์แบบ! 🎉\n")

if __name__ == "__main__":
    main_pipeline_walkthrough()
