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
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)

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
    """ทำความสะอาดข้อความและตัดคำขยะ (Text Preprocessing Pipeline)"""
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

def train_and_save_model():
    print("=" * 60)
    print("🚀 Starting Calibrated Machine Learning Model Training (TQF มคอ.2 IT Architecture)")
    print("=" * 60)

    # 1. Load Dataset
    DATA_DIR = BASE_DIR / "data"
    MODELS_DIR = BASE_DIR / "models"
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # Load Thai jobs dataset if exists, otherwise base dataset
    CSV_PATH = DATA_DIR / "thai_jobs_dataset.csv"
    if not CSV_PATH.exists():
        CSV_PATH = DATA_DIR / "job_dataset.csv"
    if not CSV_PATH.exists():
        CSV_PATH = BASE_DIR / "job_dataset.csv"

    print(f"⏳ Loading and cleaning data from '{CSV_PATH}'...")
    df_jobs = pd.read_csv(CSV_PATH).fillna("")
    df_jobs = df_jobs[df_jobs["Title"].str.strip() != ""].reset_index(drop=True)

    # If dataset has both Thai jobs and historical jobs, we can enrich training samples
    HISTORICAL_PATH = DATA_DIR / "job_dataset.csv"
    if HISTORICAL_PATH.exists() and str(HISTORICAL_PATH) != str(CSV_PATH):
        df_hist = pd.read_csv(HISTORICAL_PATH).fillna("")
        df_train_corpus = pd.concat([df_jobs, df_hist], ignore_index=True)
    else:
        df_train_corpus = df_jobs.copy()

    job_skills_map = []
    for _, row in df_train_corpus.iterrows():
        job_skills_map.append(extract_atomic_skills(str(row["Skills"])))

    # Clean text columns before feature representation
    clean_titles = df_train_corpus["Title"].apply(clean_text_pipeline)
    clean_skills = df_train_corpus["Skills"].apply(clean_text_pipeline)
    clean_resps = df_train_corpus.get("Responsibilities", df_train_corpus.get("Job Description", "")).apply(clean_text_pipeline)
    clean_keywords = df_train_corpus.get("Keywords", "").apply(clean_text_pipeline)

    df_train_corpus["combined_features"] = (
        clean_titles + " " +
        clean_skills + " " +
        clean_resps + " " +
        clean_keywords
    )

    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(
        stop_words="english",
        token_pattern=r'(?u)[a-zA-Z0-9_+#.-]+(?:/[a-zA-Z0-9_+#.-]+)?',
        max_features=5000,
        sublinear_tf=True
    )
    job_tfidf_matrix = vectorizer.fit_transform(df_train_corpus["combined_features"])

    TFIDF_PATH = MODELS_DIR / "tfidf_vectorizer.joblib"
    joblib.dump(vectorizer, TFIDF_PATH)
    print(f"✅ Fitted Cleaned TF-IDF Vectorizer and saved to '{TFIDF_PATH}'")

    # 2. Generate Balanced & Calibrated Training Pairs
    print("⏳ Generating calibrated training dataset (Features X and Target y)...")
    np.random.seed(42)

    X_list = []
    y_list = []
    num_jobs = len(df_train_corpus)

    for i in range(num_jobs):
        job_row = df_train_corpus.iloc[i]
        job_title = str(job_row["Title"])
        req_skills = job_skills_map[i]
        job_tfidf = job_tfidf_matrix[i]
        num_req = len(req_skills)

        if num_req == 0:
            continue

        # 1. High/Strong Coverage (60% to 100% of required skills) -> Positive match (y = 1)
        for _ in range(4):
            n_select = max(2, int(round(num_req * np.random.uniform(0.60, 1.0))))
            n_select = min(num_req, n_select)
            cand_skills = list(np.random.choice(req_skills, n_select, replace=False))
            cand_pref = job_title if np.random.rand() > 0.3 else ""
            cand_query = f"{cand_pref} {' '.join(cand_skills)}".strip()
            cand_vec = vectorizer.transform([cand_query])

            sim = float(np.clip(cosine_similarity(cand_vec, job_tfidf)[0][0], 0.0, 1.0))
            exact_cnt = float(len(cand_skills))
            overlap = float(exact_cnt / num_req)

            X_list.append([sim, overlap, exact_cnt])
            y_list.append(1)

        # 2. Moderate Coverage (35% to 55% of required skills) -> Proportional Label
        for _ in range(3):
            n_select = max(1, int(round(num_req * np.random.uniform(0.35, 0.55))))
            n_select = min(num_req, n_select)
            cand_skills = list(np.random.choice(req_skills, n_select, replace=False))
            cand_pref = job_title if np.random.rand() > 0.4 else ""
            cand_query = f"{cand_pref} {' '.join(cand_skills)}".strip()
            cand_vec = vectorizer.transform([cand_query])

            sim = float(np.clip(cosine_similarity(cand_vec, job_tfidf)[0][0], 0.0, 1.0))
            exact_cnt = float(len(cand_skills))
            overlap = float(exact_cnt / num_req)

            X_list.append([sim, overlap, exact_cnt])
            y_list.append(1 if (overlap >= 0.45 and exact_cnt >= 2) else 0)

        # 3. Weak Coverage (Only 1 skill or < 25% overlap) -> Negative match (y = 0)
        for _ in range(4):
            cand_skills = [np.random.choice(req_skills)]
            cand_pref = job_title if np.random.rand() > 0.3 else ""
            cand_query = f"{cand_pref} {' '.join(cand_skills)}".strip()
            cand_vec = vectorizer.transform([cand_query])

            sim = float(np.clip(cosine_similarity(cand_vec, job_tfidf)[0][0], 0.0, 1.0))
            exact_cnt = 1.0
            overlap = float(1.0 / num_req)

            X_list.append([sim, overlap, exact_cnt])
            y_list.append(0)

        # 4. Unrelated / Mismatched Random Profiles -> Negative match (y = 0)
        for _ in range(3):
            j = np.random.choice([idx for idx in range(num_jobs) if idx != i])
            other_skills = job_skills_map[j]
            other_title = str(df_train_corpus.iloc[j]["Title"])
            if other_skills:
                n_sel = max(1, min(len(other_skills), np.random.randint(1, 4)))
                cand_skills = list(np.random.choice(other_skills, n_sel, replace=False))
            else:
                cand_skills = []

            cand_pref = other_title if np.random.rand() > 0.3 else ""
            cand_query = f"{cand_pref} {' '.join(cand_skills)}".strip()
            cand_vec = vectorizer.transform([cand_query])

            sim = float(np.clip(cosine_similarity(cand_vec, job_tfidf)[0][0], 0.0, 1.0))
            matched = [s for s in cand_skills if s in req_skills]
            exact_cnt = float(len(matched))
            overlap = float(exact_cnt / num_req)

            X_list.append([sim, overlap, exact_cnt])
            y_list.append(0)

    X = np.array(X_list)
    y = np.array(y_list)

    print(f"✅ Generated calibrated dataset: X shape = {X.shape}, y distribution = {np.bincount(y)}")

    # 3. Train/Test Split (80:20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 4. Train Scaled Logistic Regression Pipeline
    print("⏳ Fitting StandardScaler + LogisticRegression pipeline...")
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression(C=0.1, random_state=42, max_iter=1000))
    ])
    pipeline.fit(X_train, y_train)

    # 5. Evaluate Model
    y_pred = pipeline.predict(X_test)
    y_pred_proba = pipeline.predict_proba(X_test)[:, 1]

    cm = confusion_matrix(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred_proba)

    print("\n" + "=" * 60)
    print("📊 MODEL EVALUATION RESULTS (TEST SET):")
    print("=" * 60)
    print(f"Accuracy:  {acc:.4f} ({acc*100:.2f}%)")
    print(f"Precision: {prec:.4f} ({prec*100:.2f}%)")
    print(f"Recall:    {rec:.4f} ({rec*100:.2f}%)")
    print(f"F1-Score:  {f1:.4f}")
    print(f"ROC-AUC:   {auc:.4f}")
    print("=" * 60 + "\n")

    # 6. Save Pipeline Model to models/model.joblib
    MODEL_PATH = MODELS_DIR / "model.joblib"
    joblib.dump(pipeline, MODEL_PATH)
    print(f"✅ Calibrated ML Pipeline saved successfully to '{MODEL_PATH}'!")

    return {
        "accuracy": acc,
        "f1": f1,
        "auc": auc
    }

if __name__ == "__main__":
    train_and_save_model()
