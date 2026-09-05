"""
ranker.py - Stage 2: Pointwise Scoring & Re-ranking Layer
Extracts heterogeneous features (Dense, BM25, Curriculum Standards, Skill Overlap)
and trains a calibrated, explainable Logistic Regression Ranker using contrastive positive/hard-negative pairs.
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_validate

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"
RANKER_MODEL_PATH = MODELS_DIR / "ranker_pipeline.joblib"

CURRICULUM_ROLES = {
    "8.1": {
        "id": "8.1",
        "title": "เจ้าหน้าที่คอมพิวเตอร์",
        "en_title": "Computer Officer / IT Support",
        "core_skills": ["windows", "linux", "hardware", "troubleshooting", "basic networking", "helpdesk", "active directory", "backup", "ms office"]
    },
    "8.2": {
        "id": "8.2",
        "title": "ผู้ดูแลระบบเครือข่ายคอมพิวเตอร์",
        "en_title": "Network Administrator / Engineer",
        "core_skills": ["tcp/ip", "cisco", "routing", "switching", "firewall", "vpn", "dns", "dhcp", "linux server", "windows server", "network security"]
    },
    "8.3": {
        "id": "8.3",
        "title": "นักพัฒนาและออกแบบสื่อผสม",
        "en_title": "Multimedia Designer & Developer",
        "core_skills": ["ui/ux", "figma", "adobe xd", "photoshop", "illustrator", "premiere pro", "after effects", "3d animation", "game development", "unity", "html/css"]
    },
    "8.4": {
        "id": "8.4",
        "title": "นักจัดการโครงการสารสนเทศ",
        "en_title": "IT Project Manager / Coordinator",
        "core_skills": ["agile", "scrum", "jira", "project management", "trello", "communication", "risk management", "sdlc", "budgeting"]
    },
    "8.5": {
        "id": "8.5",
        "title": "นักวิเคราะห์และออกแบบระบบงาน",
        "en_title": "System Analyst / Business Analyst",
        "core_skills": ["system analysis", "business analysis", "uml", "use case", "dfd", "er diagram", "database design", "sql", "requirement gathering", "wireframing"]
    },
    "8.6": {
        "id": "8.6",
        "title": "นักพัฒนาซอฟต์แวร์",
        "en_title": "Software Developer / Engineer",
        "core_skills": ["python", "java", "c#", ".net", "javascript", "typescript", "react", "node.js", "sql", "rest api", "git", "oop", "docker"]
    },
    "8.7": {
        "id": "8.7",
        "title": "นักออกแบบและพัฒนาเว็บไซต์",
        "en_title": "Web Designer & Developer",
        "core_skills": ["html5", "css3", "javascript", "responsive web design", "tailwind", "bootstrap", "wordpress", "php", "mysql", "rest api"]
    },
    "8.8": {
        "id": "8.8",
        "title": "ผู้เชี่ยวชาญด้านเทคโนโลยีสารสนเทศ",
        "en_title": "Specialized IT Professional",
        "core_skills": ["machine learning", "deep learning", "nlp", "cybersecurity", "cloud architecture", "big data", "data science", "devsecops"]
    }
}

def clean_atomic_skill(skill: str) -> str:
    """Normalize atomic skill name."""
    if not skill or not isinstance(skill, str):
        return ""
    s = skill.strip().lower()
    s = re.sub(r'[\(\)\[\]\{\}]', ' ', s)
    s = s.strip(" ,;:-_./|&")
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def extract_skills_from_str(text: str) -> List[str]:
    """Parse semi-colon or comma delimited skills."""
    if not text or not isinstance(text, str):
        return []
    parts = re.split(r'[;\n\r|•,]+', text)
    cleaned = [clean_atomic_skill(p) for p in parts if clean_atomic_skill(p)]
    return list(dict.fromkeys(cleaned))

def compute_ranking_features(
    dense_score: float,
    bm25_score: float,
    user_skills: List[str],
    job_skills: List[str],
    target_role_id: str,
    job_role_id: str
) -> np.ndarray:
    """
    Extracts 4-dimensional heterogeneous ranking feature vector:
    1. x1: Dense Semantic Similarity (SentenceTransformers)
    2. x2: BM25 Lexical Keyword Fit
    3. x3: Curriculum Standard Alignment (TQF MKO.2)
    4. x4: Exact Job Technical Overlap Ratio
    """
    user_set = set(clean_atomic_skill(s) for s in user_skills if clean_atomic_skill(s))
    job_set = set(clean_atomic_skill(s) for s in job_skills if clean_atomic_skill(s))

    # Feature 3: Curriculum Coverage
    role_info = CURRICULUM_ROLES.get(job_role_id, CURRICULUM_ROLES["8.6"])
    core_skills = [clean_atomic_skill(s) for s in role_info["core_skills"]]
    matched_core = [s for s in core_skills if s in user_set]
    curriculum_cov = float(len(matched_core) / max(1, len(core_skills)))

    # Feature 4: Exact Skill Overlap
    matched_job_skills = [s for s in job_set if s in user_set]
    overlap_ratio = float(len(matched_job_skills) / max(1, len(job_set)))

    # Cross-domain penalty factor
    if target_role_id and target_role_id != job_role_id:
        curriculum_cov *= 0.5

    return np.array([
        float(np.clip(dense_score, 0.0, 1.0)),
        float(np.clip(bm25_score, 0.0, 1.0)),
        float(np.clip(curriculum_cov, 0.0, 1.0)),
        float(np.clip(overlap_ratio, 0.0, 1.0))
    ], dtype=np.float32)

class PointwiseRanker:
    """
    Stage-2 Calibrated Logistic Regression Ranker.
    Combines retrieval signals into a calibrated probability of qualification readiness.
    """
    def __init__(self, model_pipeline: Pipeline = None):
        self.pipeline = model_pipeline
        self.feature_names = [
            "Dense Semantic Similarity (x1)",
            "BM25 Lexical Score (x2)",
            "Curriculum MKO.2 Alignment (x3)",
            "Job Technical Overlap Ratio (x4)"
        ]

    def predict_score(self, features_matrix: np.ndarray) -> np.ndarray:
        """Computes calibrated readiness score (0-100) using Logistic Regression sigmoid probability."""
        if self.pipeline is None:
            # Fallback to balanced weighted sum if model not yet trained
            weights = np.array([0.35, 0.25, 0.20, 0.20])
            scores = np.dot(features_matrix, weights) * 100.0
            return np.clip(scores, 0, 100).astype(int)

        probs = self.pipeline.predict_proba(features_matrix)[:, 1]
        return np.clip(np.round(probs * 100.0), 0, 100).astype(int)

    def explain_weights(self) -> Dict[str, float]:
        """Returns interpretable coefficients of the trained model."""
        if self.pipeline is None:
            return {f: 0.25 for f in self.feature_names}
        clf = self.pipeline.named_steps['clf']
        return dict(zip(self.feature_names, [float(w) for w in clf.coef_[0]]))

def train_pointwise_ranker(df_jobs: pd.DataFrame) -> PointwiseRanker:
    """
    Trains Stage-2 Logistic Regression Ranker using realistic contrastive candidate-job pairs:
    - Positive Pairs (y=1): Candidates seeking the appropriate domain with solid skill foundation
    - Hard Negative Pairs (y=0): Candidates from conflicting domains (Cross-Domain) or lacking core stack
    """
    print("=" * 70)
    print("🚀 TRAINING STAGE-2 LOGISTIC REGRESSION POINTWISE RANKER")
    print("   Contrastive Methodology: Positive Matches vs. Hard Negatives")
    print("=" * 70)

    from src.retrieval import HybridRetriever
    retriever = HybridRetriever(df_jobs)

    X_list = []
    y_list = []
    np.random.seed(42)

    total_jobs = len(df_jobs)
    for idx in range(total_jobs):
        row = df_jobs.iloc[idx]
        job_role_id = str(row.get("CurriculumRoleID", "8.6")).strip()
        job_skills = extract_skills_from_str(str(row.get("Skills", "")))
        if not job_skills:
            continue

        role_info = CURRICULUM_ROLES.get(job_role_id, CURRICULUM_ROLES["8.6"])
        core_skills = role_info["core_skills"]

        # 1. Positive Candidates (y = 1): Prepared candidate for this job
        for _ in range(3):
            k = max(2, int(round(len(job_skills) * np.random.uniform(0.60, 0.90))))
            selected_skills = list(np.random.choice(job_skills, min(k, len(job_skills)), replace=False))
            # Include 1-2 core skills
            selected_skills = list(dict.fromkeys(selected_skills + list(np.random.choice(core_skills, min(2, len(core_skills)), replace=False))))
            
            cand_query = f"{role_info['en_title']} {' '.join(selected_skills)}"
            # Get Stage-1 retrieval signals
            candidates = retriever.retrieve_candidates(cand_query, top_k=5)
            # Find this job's retrieval scores
            match = next((c for c in candidates if c["doc_idx"] == idx), None)
            d_score = match["dense_score"] if match else float(np.random.uniform(0.65, 0.85))
            b_score = match["bm25_score"] if match else float(np.random.uniform(0.50, 0.80))

            feat = compute_ranking_features(
                dense_score=d_score,
                bm25_score=b_score,
                user_skills=selected_skills,
                job_skills=job_skills,
                target_role_id=job_role_id,
                job_role_id=job_role_id
            )
            X_list.append(feat)
            y_list.append(1)

        # 2. Hard Negative Candidate A: Cross-Domain Mismatch (y = 0)
        # Designer applying for Backend, or Network Admin applying for Multimedia
        for _ in range(2):
            other_role_id = np.random.choice([r for r in CURRICULUM_ROLES.keys() if r != job_role_id])
            other_skills = CURRICULUM_ROLES[other_role_id]["core_skills"]
            cand_skills = list(np.random.choice(other_skills, min(3, len(other_skills)), replace=False))
            
            cand_query = f"{CURRICULUM_ROLES[other_role_id]['en_title']} {' '.join(cand_skills)}"
            candidates = retriever.retrieve_candidates(cand_query, top_k=20)
            match = next((c for c in candidates if c["doc_idx"] == idx), None)
            d_score = match["dense_score"] if match else float(np.random.uniform(0.15, 0.35))
            b_score = match["bm25_score"] if match else float(np.random.uniform(0.0, 0.15))

            feat = compute_ranking_features(
                dense_score=d_score,
                bm25_score=b_score,
                user_skills=cand_skills,
                job_skills=job_skills,
                target_role_id=other_role_id,
                job_role_id=job_role_id
            )
            X_list.append(feat)
            y_list.append(0)

        # 3. Hard Negative Candidate B: Severe Skill Gap within Domain (y = 0)
        # Candidate has only 1 minimal generic skill
        for _ in range(2):
            minimal_skill = [np.random.choice(core_skills)]
            cand_query = f"{role_info['en_title']} {minimal_skill[0]}"
            candidates = retriever.retrieve_candidates(cand_query, top_k=20)
            match = next((c for c in candidates if c["doc_idx"] == idx), None)
            d_score = match["dense_score"] if match else float(np.random.uniform(0.30, 0.45))
            b_score = match["bm25_score"] if match else float(np.random.uniform(0.10, 0.25))

            feat = compute_ranking_features(
                dense_score=d_score,
                bm25_score=b_score,
                user_skills=minimal_skill,
                job_skills=job_skills,
                target_role_id=job_role_id,
                job_role_id=job_role_id
            )
            X_list.append(feat)
            y_list.append(0)

    X = np.array(X_list, dtype=np.float32)
    y = np.array(y_list, dtype=np.int32)
    print(f"✅ Constructed training set: {X.shape[0]} samples (Positives: {np.sum(y==1)}, Negatives: {np.sum(y==0)})")

    # Fit Logistic Regression Pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', LogisticRegression(C=1.0, random_state=42, max_iter=500))
    ])

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_validate(pipeline, X, y, cv=cv, scoring=['accuracy', 'roc_auc', 'f1'])
    print(f"📊 5-Fold Validation: ROC-AUC={scores['test_roc_auc'].mean():.4f}, F1={scores['test_f1'].mean():.4f}")

    pipeline.fit(X, y)
    joblib.dump(pipeline, RANKER_MODEL_PATH)
    print(f"✅ Saved Pointwise Ranker to '{RANKER_MODEL_PATH}'")

    ranker = PointwiseRanker(pipeline)
    print("\n🔍 EXPLAINABLE MODEL COEFFICIENTS (w):")
    for feat_name, weight in ranker.explain_weights().items():
        print(f"  • {feat_name:<35}: {weight:+.4f}")
    print(f"  • Intercept (Bias b): {pipeline.named_steps['clf'].intercept_[0]:+.4f}\n")

    return ranker

def load_or_train_ranker(df_jobs: pd.DataFrame) -> PointwiseRanker:
    """Loads existing ranker pipeline or trains a new one."""
    if RANKER_MODEL_PATH.exists():
        try:
            pipeline = joblib.load(RANKER_MODEL_PATH)
            return PointwiseRanker(pipeline)
        except Exception:
            pass
    return train_pointwise_ranker(df_jobs)
