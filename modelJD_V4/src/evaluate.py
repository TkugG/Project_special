"""
evaluate.py - Industry-Standard Information Retrieval Evaluation Suite
Calculates NDCG@5, MRR, and HitRate@5 on the Golden Benchmark Set.
Compares:
1. Pure Lexical Baseline (BM25)
2. Pure Dense Semantic Baseline (SentenceTransformers)
3. Stage-1 Hybrid Fusion (Reciprocal Rank Fusion - RRF)
4. Proposed Two-Stage System (Hybrid Retrieval + Stage-2 Pointwise Ranker)
"""

import json
import math
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

DATA_DIR = BASE_DIR / "data"

from src.retrieval import HybridRetriever, tokenize_tech_text
from src.embeddings import encode_query
from src.ranker import (
    load_or_train_ranker,
    compute_ranking_features,
    extract_skills_from_str
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def dcg_at_k(relevance_scores: List[int], k: int = 5) -> float:
    """Calculates Discounted Cumulative Gain at rank K using exponential gain formula."""
    dcg = 0.0
    for idx, rel in enumerate(relevance_scores[:k]):
        gain = (2 ** rel) - 1.0
        discount = math.log2(idx + 2.0)  # idx is 0-based, so rank is idx + 1, denom is log2(rank + 1)
        dcg += gain / discount
    return dcg

def ndcg_at_k(predicted_job_ids: List[str], ground_truth: Dict[str, int], k: int = 5) -> float:
    """Calculates Normalized Discounted Cumulative Gain at rank K."""
    pred_scores = [ground_truth.get(jid, 0) for jid in predicted_job_ids[:k]]
    actual_dcg = dcg_at_k(pred_scores, k=k)

    # Ideal ranking (sort ground truth descending)
    ideal_scores = sorted(ground_truth.values(), reverse=True)
    ideal_dcg = dcg_at_k(ideal_scores, k=k)

    if ideal_dcg == 0.0:
        return 1.0 if actual_dcg == 0.0 else 0.0
    return actual_dcg / ideal_dcg

def reciprocal_rank(predicted_job_ids: List[str], ground_truth: Dict[str, int], relevance_threshold: int = 2) -> float:
    """Calculates Reciprocal Rank (1/rank) for the first relevant document."""
    for idx, jid in enumerate(predicted_job_ids):
        if ground_truth.get(jid, 0) >= relevance_threshold:
            return 1.0 / (idx + 1.0)
    return 0.0

def hit_at_k(predicted_job_ids: List[str], ground_truth: Dict[str, int], k: int = 5, relevance_threshold: int = 2) -> float:
    """Returns 1.0 if at least one relevant document is found in Top-K, else 0.0."""
    for jid in predicted_job_ids[:k]:
        if ground_truth.get(jid, 0) >= relevance_threshold:
            return 1.0
    return 0.0

def run_evaluation_benchmark():
    print("=" * 80)
    print("🔬 RUNNING IR EVALUATION BENCHMARK (NDCG@5, MRR, HitRate@5)")
    print("=" * 80)

    # 1. Load Data & Benchmark
    csv_path = DATA_DIR / "thai_jobs_dataset.csv"
    if not csv_path.exists():
        csv_path = DATA_DIR / "job_dataset.csv"
    df_jobs = pd.read_csv(csv_path)

    bench_path = DATA_DIR / "eval_benchmark.json"
    if not bench_path.exists():
        from data.create_benchmark import generate_benchmark_json
        generate_benchmark_json()

    with open(bench_path, "r", encoding="utf-8") as f:
        benchmark_queries = json.load(f)

    # 2. Initialize Models
    print("⏳ Initializing Hybrid Retriever & Pointwise Ranker...")
    retriever = HybridRetriever(df_jobs)
    ranker = load_or_train_ranker(df_jobs)

    job_ids = retriever.job_ids
    total_docs = len(job_ids)

    # Performance containers
    metrics = {
        "BM25 Only (Lexical)": {"ndcg": [], "mrr": [], "hit": []},
        "Dense Semantic (SentenceTransformers)": {"ndcg": [], "mrr": [], "hit": []},
        "Hybrid Search (RRF Stage 1)": {"ndcg": [], "mrr": [], "hit": []},
        "Proposed: Two-Stage (Hybrid + LR Ranker)": {"ndcg": [], "mrr": [], "hit": []},
    }

    for item in benchmark_queries:
        query_text = item["query_text"]
        target_role_id = item["target_role_id"]
        user_skills = item["skills"]
        ground_truth = item["relevance_grades"]

        # --- System 1: BM25 Only ---
        q_tokens = tokenize_tech_text(query_text)
        bm25_scores = retriever.bm25.get_scores(q_tokens)
        bm25_top_idx = np.argsort(-bm25_scores)[:5]
        bm25_jids = [job_ids[i] for i in bm25_top_idx]

        metrics["BM25 Only (Lexical)"]["ndcg"].append(ndcg_at_k(bm25_jids, ground_truth, k=5))
        metrics["BM25 Only (Lexical)"]["mrr"].append(reciprocal_rank(bm25_jids, ground_truth))
        metrics["BM25 Only (Lexical)"]["hit"].append(hit_at_k(bm25_jids, ground_truth, k=5))

        # --- System 2: Dense Semantic Only ---
        q_vec = encode_query(query_text)
        dense_sims = np.dot(retriever.embeddings_matrix, q_vec)
        dense_top_idx = np.argsort(-dense_sims)[:5]
        dense_jids = [job_ids[i] for i in dense_top_idx]

        metrics["Dense Semantic (SentenceTransformers)"]["ndcg"].append(ndcg_at_k(dense_jids, ground_truth, k=5))
        metrics["Dense Semantic (SentenceTransformers)"]["mrr"].append(reciprocal_rank(dense_jids, ground_truth))
        metrics["Dense Semantic (SentenceTransformers)"]["hit"].append(hit_at_k(dense_jids, ground_truth, k=5))

        # --- System 3: Hybrid Search (RRF) ---
        candidates = retriever.retrieve_candidates(query_text, top_k=50)
        hybrid_jids = [c["job_id"] for c in candidates[:5]]

        metrics["Hybrid Search (RRF Stage 1)"]["ndcg"].append(ndcg_at_k(hybrid_jids, ground_truth, k=5))
        metrics["Hybrid Search (RRF Stage 1)"]["mrr"].append(reciprocal_rank(hybrid_jids, ground_truth))
        metrics["Hybrid Search (RRF Stage 1)"]["hit"].append(hit_at_k(hybrid_jids, ground_truth, k=5))

        # --- System 4: Proposed Two-Stage (Hybrid Retrieval + LR Ranker) ---
        # Stage 2 re-ranking on the top 30 candidates
        stage2_features = []
        for cand in candidates[:30]:
            c_idx = cand["doc_idx"]
            row = df_jobs.iloc[c_idx]
            job_role = str(row.get("CurriculumRoleID", "8.6")).strip()
            job_skills = extract_skills_from_str(str(row.get("Skills", "")))

            feat = compute_ranking_features(
                dense_score=cand["dense_score"],
                bm25_score=cand["bm25_score"],
                user_skills=user_skills,
                job_skills=job_skills,
                target_role_id=target_role_id,
                job_role_id=job_role
            )
            stage2_features.append(feat)

        feats_matrix = np.array(stage2_features)
        ranker_scores = ranker.predict_score(feats_matrix)

        # Sort candidates by calibrated ranker score
        sorted_pairs = sorted(
            zip(candidates[:30], ranker_scores),
            key=lambda p: p[1],
            reverse=True
        )
        two_stage_jids = [pair[0]["job_id"] for pair in sorted_pairs[:5]]

        metrics["Proposed: Two-Stage (Hybrid + LR Ranker)"]["ndcg"].append(ndcg_at_k(two_stage_jids, ground_truth, k=5))
        metrics["Proposed: Two-Stage (Hybrid + LR Ranker)"]["mrr"].append(reciprocal_rank(two_stage_jids, ground_truth))
        metrics["Proposed: Two-Stage (Hybrid + LR Ranker)"]["hit"].append(hit_at_k(two_stage_jids, ground_truth, k=5))

    # Print Formatted Results Table
    print("\n" + "=" * 80)
    print(f"{'Ablation System Architecture':<44} | {'NDCG@5':<10} | {'MRR':<10} | {'Hit Rate@5':<10}")
    print("-" * 80)
    for sys_name, vals in metrics.items():
        mean_ndcg = np.mean(vals["ndcg"])
        mean_mrr = np.mean(vals["mrr"])
        mean_hit = np.mean(vals["hit"])
        print(f"{sys_name:<44} | {mean_ndcg:<10.4f} | {mean_mrr:<10.4f} | {mean_hit:<10.4f}")
    print("=" * 80 + "\n")

    return metrics

if __name__ == "__main__":
    run_evaluation_benchmark()
