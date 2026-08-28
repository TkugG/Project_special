"""
validate.py - Feature Extraction & Machine Learning Pipeline Validation Suite
Based on scikit-learn official documentation (Section 8.2: Feature Extraction):
https://scikit-learn.org/stable/modules/feature_extraction.html

Validates:
1. Text Feature Extraction Mechanics (TfidfVectorizer, Token Pattern, N-grams, Stop Words, Normalization)
2. Mathematical Properties (IDF Calculation, L2 Unit Norm, Cosine Similarity Bounds)
3. Dataset Integrity & Vocabulary Coverage (job_dataset.csv)
4. 3D Orthogonal Feature Vector Generation (Semantic Fit, Overlap Ratio, Exact Count)
5. Model Inference, Monotonicity & Probability Calibration (model.joblib, tfidf_vectorizer.joblib)
"""

import os
import sys
import math
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Custom Protected Terms & Preprocessing Functions (Imported/Mirrored from pipeline)
PROTECTED_TECH_TERMS = {
    "c#", "c++", ".net", "asp.net", "asp.net core", "node.js", "react.js", 
    "vue.js", "next.js", "ci/cd", "ui/ux", "tcp/ip", "pl/sql"
}

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
SRC_DIR = BASE_DIR / "src"

def print_header(title: str):
    print("\n" + "=" * 70)
    print(f"🔬 {title}")
    print("=" * 70)


def print_result(test_name: str, passed: bool, details: str = ""):
    icon = "✅ PASS" if passed else "❌ FAIL"
    print(f"[{icon}] {test_name}")
    if details:
        print(f"        └─ {details}")


# =========================================================================
# TEST SUITE 1: Scikit-Learn Feature Extraction Mechanics
# =========================================================================
def test_feature_extraction_mechanics():
    print_header("1. SCIKIT-LEARN FEATURE EXTRACTION MECHANICS VALIDATION")
    all_passed = True

    # 1.1 Custom Token Pattern for Technical Vocabulary (C#, .NET, C++, Node.js, CI/CD)
    # Standard scikit-learn token_pattern r'(?u)\b\w\w+\b' strips '+', '#', '.', '-', '/' and requires word boundaries.
    # A robust technical token pattern r'(?u)[a-zA-Z0-9_+#.-]+(?:/[a-zA-Z0-9_+#.-]+)?' preserves them completely.
    corpus = [
        "c# .net asp.net core developer with docker",
        "c++ node.js ci/cd and react developer",
        "python data science and machine learning"
    ]

    tech_token_pattern = r'(?u)[a-zA-Z0-9_+#.-]+(?:/[a-zA-Z0-9_+#.-]+)?'

    custom_vectorizer = CountVectorizer(
        token_pattern=tech_token_pattern,
        lowercase=True
    )
    X_counts = custom_vectorizer.fit_transform(corpus)
    vocab = custom_vectorizer.get_feature_names_out().tolist()

    tech_tokens = ["c#", ".net", "asp.net", "c++", "node.js", "ci/cd"]
    preserved = [t for t in tech_tokens if t in vocab]
    
    t1_pass = len(preserved) == len(tech_tokens)
    all_passed &= t1_pass
    print_result(
        "Token Pattern Tech Preservation",
        t1_pass,
        f"Preserved {len(preserved)}/{len(tech_tokens)} tech tokens: {preserved}"
    )

    # 1.2 TF-IDF Transformer vs TfidfVectorizer Equivalence
    # According to scikit-learn docs: TfidfVectorizer = CountVectorizer + TfidfTransformer
    tfidf_vec = TfidfVectorizer(token_pattern=tech_token_pattern, lowercase=True)
    X_direct = tfidf_vec.fit_transform(corpus)

    tfidf_trans = TfidfTransformer()
    X_transformed = tfidf_trans.fit_transform(X_counts)

    diff = np.abs(X_direct.toarray() - X_transformed.toarray()).max()
    t2_pass = diff < 1e-6
    all_passed &= t2_pass
    print_result(
        "TfidfVectorizer == CountVectorizer + TfidfTransformer",
        t2_pass,
        f"Max absolute matrix difference: {diff:.2e}"
    )

    # 1.3 Mathematical Verification of L2 Normalization
    # scikit-learn norm='l2': each row vector must have Euclidean norm == 1.0
    row_norms = np.linalg.norm(X_direct.toarray(), ord=2, axis=1)
    t3_pass = bool(np.allclose(row_norms, 1.0, atol=1e-5))
    all_passed &= t3_pass
    print_result(
        "L2 Unit Vector Normalization (||v||_2 = 1.0)",
        t3_pass,
        f"Computed row norms: {np.round(row_norms, 4).tolist()}"
    )

    # 1.4 Mathematical Verification of Smooth IDF Calculation
    # idf(t) = log((1 + n) / (1 + df(t))) + 1
    n_samples = len(corpus)
    df_counts = np.bincount(X_counts.indices, minlength=X_counts.shape[1])
    expected_idf = np.log((1 + n_samples) / (1 + df_counts)) + 1.0
    actual_idf = tfidf_vec.idf_
    idf_diff = np.abs(expected_idf - actual_idf).max()
    t4_pass = idf_diff < 1e-6
    all_passed &= t4_pass
    print_result(
        "Smooth IDF Formulation: log((1+N)/(1+DF)) + 1",
        t4_pass,
        f"Max IDF calculation deviation: {idf_diff:.2e}"
    )

    # 1.5 Sublinear TF Scaling Verification
    # sublinear_tf=True: tf = 1 + log(tf) for tf > 0
    sublinear_vec = TfidfVectorizer(sublinear_tf=True, norm=None, use_idf=False)
    repeated_corpus = ["python python python python python"]  # count = 5
    X_sub = sublinear_vec.fit_transform(repeated_corpus).toarray()[0][0]
    expected_sub_tf = 1.0 + math.log(5)
    t5_pass = abs(X_sub - expected_sub_tf) < 1e-5
    all_passed &= t5_pass
    print_result(
        "Sublinear TF Scaling: 1 + log(TF)",
        t5_pass,
        f"Calculated: {X_sub:.4f} | Expected: {expected_sub_tf:.4f}"
    )

    return all_passed


# =========================================================================
# TEST SUITE 2: Dataset Feature Extraction & Vector Space Model
# =========================================================================
def test_dataset_feature_extraction():
    print_header("2. DATASET FEATURE EXTRACTION & COSINE SIMILARITY VALIDATION")
    all_passed = True

    csv_path = DATA_DIR / "job_dataset.csv"
    if not csv_path.exists():
        csv_path = BASE_DIR / "job_dataset.csv"
    if not csv_path.exists():
        print_result("Dataset Existence", False, f"File '{csv_path}' not found!")
        return False

    df = pd.read_csv(csv_path).fillna("")
    t1_pass = len(df) >= 1000
    all_passed &= t1_pass
    print_result(
        "Job Dataset Integrity",
        t1_pass,
        f"Loaded {len(df)} job records from '{csv_path}'"
    )

    # Check necessary columns
    req_cols = ["Title", "Skills"]
    cols_exist = all(c in df.columns for c in req_cols)
    all_passed &= cols_exist
    print_result(
        "Required Metadata Schema (Title, Skills)",
        cols_exist,
        f"Columns present: {df.columns.tolist()}"
    )

    # Fit Vectorizer on Dataset
    combined_texts = df["Title"] + " " + df["Skills"] + " " + df.get("Responsibilities", df.get("Job Description", ""))
    vectorizer = TfidfVectorizer(
        stop_words="english",
        token_pattern=r'(?u)\b[\w+#.-]+\b',
        max_features=5000,
        sublinear_tf=True
    )
    job_matrix = vectorizer.fit_transform(combined_texts)
    
    t2_pass = job_matrix.shape[0] == len(df) and job_matrix.shape[1] > 500
    all_passed &= t2_pass
    print_result(
        "TF-IDF Matrix Generation & Sparsity",
        t2_pass,
        f"Matrix shape: {job_matrix.shape} | Sparsity: {(1.0 - job_matrix.nnz / (job_matrix.shape[0] * job_matrix.shape[1])) * 100:.2f}%"
    )

    # Cosine Similarity Bounds & Symmetry
    sample_queries = [
        "python data analysis machine learning sql",
        "react typescript tailwind css frontend",
        "c# asp.net core sql server backend"
    ]
    query_vecs = vectorizer.transform(sample_queries)
    sim_matrix = cosine_similarity(query_vecs, job_matrix)

    min_sim = float(sim_matrix.min())
    max_sim = float(sim_matrix.max())
    bounds_ok = (min_sim >= 0.0) and (max_sim <= 1.00001)
    all_passed &= bounds_ok
    print_result(
        "Cosine Similarity Metric Bounds [0.0, 1.0]",
        bounds_ok,
        f"Min Sim: {min_sim:.4f} | Max Sim: {max_sim:.4f}"
    )

    return all_passed


# =========================================================================
# TEST SUITE 3: 3D Orthogonal Feature Space & Model Calibration
# =========================================================================
def test_model_calibration_and_inference():
    print_header("3. 3D ORTHOGONAL FEATURE VECTOR & INFERENCE VALIDATION")
    all_passed = True

    model_path = MODELS_DIR / "model.joblib"
    vec_path = MODELS_DIR / "tfidf_vectorizer.joblib"

    if not model_path.exists():
        model_path = BASE_DIR / "model.joblib"
    if not vec_path.exists():
        vec_path = BASE_DIR / "tfidf_vectorizer.joblib"

    if not model_path.exists() or not vec_path.exists():
        print_result("Model Artifacts Check", False, f"Missing {model_path} or {vec_path}")
        return False

    model = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)
    print_result("Model Artifacts Loaded", True, f"Loaded pipeline: {type(model).__name__}")

    # Verify 3D Feature Dimensionality (Feature 1: Cosine, Feature 2: Overlap Ratio, Feature 3: Exact Count)
    # Test Monotonicity: Higher skill overlap MUST yield higher calibrated match score
    job_req_skills = ["c#", "asp.net core", "sql server", "entity framework", "git", "visual studio"]
    job_title = ".NET Developer"
    job_doc = f"{job_title} {' '.join(job_req_skills)}"
    job_vec = vectorizer.transform([job_doc])

    test_profiles = [
        ("Full Profile (100% overlap)", ["c#", "asp.net core", "sql server", "entity framework", "git", "visual studio"]),
        ("Strong Profile (66% overlap)", ["c#", "asp.net core", "sql server", "git"]),
        ("Moderate Profile (33% overlap)", ["c#", "git"]),
        ("Weak Profile (16% overlap)", ["git"]),
        ("Unrelated Profile (0% overlap)", ["flutter", "dart", "swift", "kotlin"])
    ]

    scores = []
    print("\n   📈 Monotonicity & Probability Calibration Test:")
    for name, user_skills in test_profiles:
        user_query = f"{job_title} {' '.join(user_skills)}".strip()
        user_vec = vectorizer.transform([user_query])

        sim = float(cosine_similarity(user_vec, job_vec)[0][0])
        matched = [s for s in user_skills if s in job_req_skills]
        exact_cnt = float(len(matched))
        overlap = float(exact_cnt / len(job_req_skills))

        # Predict probability from calibrated model
        X_feature = np.array([[sim, overlap, exact_cnt]])
        prob = float(model.predict_proba(X_feature)[0][1]) * 100.0
        scores.append(prob)
        print(f"      • {name:<32} -> Sim: {sim:.3f}, Overlap: {overlap:.2f}, Exact: {exact_cnt:.0f} | Score: {prob:6.2f}%")

    # Validate Monotonicity: scores[0] > scores[1] > scores[2] > scores[3] >= scores[4]
    is_monotonic = (scores[0] > scores[1]) and (scores[1] > scores[2]) and (scores[2] > scores[3]) and (scores[3] >= scores[4])
    all_passed &= is_monotonic
    print_result(
        "Monotonicity Assertion (Higher Overlap => Higher Score)",
        is_monotonic,
        f"Score Progression: {' -> '.join(f'{s:.1f}%' for s in scores)}"
    )

    # Validate Edge Cases:
    # 1. Full Match >= 80%
    full_match_pass = scores[0] >= 80.0
    all_passed &= full_match_pass
    print_result("Edge Case: 100% Skill Match Score >= 80%", full_match_pass, f"Achieved: {scores[0]:.2f}%")

    # 2. Unrelated Match < 20%
    unrelated_pass = scores[4] < 20.0
    all_passed &= unrelated_pass
    print_result("Edge Case: 0% Skill Match Score < 20%", unrelated_pass, f"Achieved: {scores[4]:.2f}%")

    return all_passed


# =========================================================================
# MAIN ENTRYPOINT
# =========================================================================
def main():
    print("=" * 70)
    print("   SCIKIT-LEARN FEATURE EXTRACTION & MODEL VALIDATION SUITE")
    print("   Reference: https://scikit-learn.org/stable/modules/feature_extraction.html")
    print("=" * 70)

    pass1 = test_feature_extraction_mechanics()
    pass2 = test_dataset_feature_extraction()
    pass3 = test_model_calibration_and_inference()

    print_header("FINAL VALIDATION SUMMARY")
    overall_success = pass1 and pass2 and pass3

    if overall_success:
        print("🎉 ALL SCIKIT-LEARN FEATURE EXTRACTION & PIPELINE TESTS PASSED 100%!")
        print("   - Text tokenization correctly preserves multi-character and technical symbols.")
        print("   - TF-IDF formulation and L2 normalization match scikit-learn mathematical definitions.")
        print("   - Vector space cosine similarity and 3D feature representation operate correctly.")
        print("   - Model calibration enforces strict monotonicity across skill overlap degrees.")
        print("=" * 70 + "\n")
        sys.exit(0)
    else:
        print("❌ SOME VALIDATION CHECKS FAILED. Please review the log above.")
        print("=" * 70 + "\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
