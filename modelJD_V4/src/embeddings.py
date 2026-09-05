"""
embeddings.py - Dense Semantic Retrieval Layer
Uses SentenceTransformers (paraphrase-multilingual-MiniLM-L12-v2) for bilingual (Thai/English) semantic representations.
Precomputes and caches normalized job embeddings for sub-millisecond dot-product cosine similarity.
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple
import numpy as np
import pandas as pd
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMBEDDINGS_CACHE_PATH = MODELS_DIR / "dense_job_embeddings.npy"
JOB_IDS_CACHE_PATH = MODELS_DIR / "dense_job_ids.joblib"

_model_instance = None

def get_embedding_model():
    """Singleton loader for SentenceTransformer to prevent redundant VRAM/RAM allocation."""
    global _model_instance
    if _model_instance is None:
        from sentence_transformers import SentenceTransformer
        # Load pre-downloaded model from HF cache
        _model_instance = SentenceTransformer(MODEL_NAME)
    return _model_instance

def normalize_embeddings(embeddings: np.ndarray) -> np.ndarray:
    """Normalize vectors to unit length (L2 norm) so dot product equals cosine similarity."""
    norms = np.linalg.norm(embeddings, axis=-1, keepdims=True)
    norms[norms == 0] = 1e-12
    return embeddings / norms

def encode_query(query: str) -> np.ndarray:
    """Encode a single query string into a normalized 1D embedding vector."""
    model = get_embedding_model()
    emb = model.encode(query, show_progress_bar=False, convert_to_numpy=True)
    norm = np.linalg.norm(emb)
    if norm > 0:
        emb = emb / norm
    return emb

def encode_texts(texts: List[str], batch_size: int = 32) -> np.ndarray:
    """Encode a batch of text descriptions into normalized 2D embeddings."""
    model = get_embedding_model()
    embeddings = model.encode(texts, batch_size=batch_size, show_progress_bar=True, convert_to_numpy=True)
    return normalize_embeddings(embeddings)

def build_job_corpus_text(df: pd.DataFrame) -> List[str]:
    """
    Construct rich contextual text representation for each job vacancy.
    Combines Title, Curriculum Role, Core Skills, Responsibilities, and Keywords.
    """
    corpus = []
    for _, row in df.iterrows():
        title = str(row.get("Title", "")).strip()
        role = str(row.get("CurriculumRoleTitle", "")).strip()
        role_en = str(row.get("CurriculumRoleEN", "")).strip()
        skills = str(row.get("Skills", "")).replace(";", ", ").strip()
        resps = str(row.get("Responsibilities", "")).replace(";", ". ").strip()
        keywords = str(row.get("Keywords", "")).replace(";", ", ").strip()

        doc_text = f"ตำแหน่ง: {title} ({role_en} - {role})\nทักษะสำคัญ: {skills}\nหน้าที่: {resps}\nคีย์เวิร์ด: {keywords}"
        corpus.append(doc_text)
    return corpus

def build_or_load_job_embeddings(df: pd.DataFrame, force_recompute: bool = False) -> Tuple[np.ndarray, List[str]]:
    """
    Loads precomputed job embeddings if available; otherwise computes and caches them.
    Returns (normalized_embeddings_matrix, list_of_job_ids).
    """
    job_ids = [str(row.get("JobID", f"JOB-{idx}")) for idx, row in df.iterrows()]

    if not force_recompute and EMBEDDINGS_CACHE_PATH.exists() and JOB_IDS_CACHE_PATH.exists():
        try:
            cached_job_ids = joblib.load(JOB_IDS_CACHE_PATH)
            cached_embeddings = np.load(EMBEDDINGS_CACHE_PATH)
            if len(cached_job_ids) == len(job_ids) and cached_job_ids == job_ids:
                return cached_embeddings, cached_job_ids
        except Exception:
            pass

    print(f"⏳ Computing dense semantic embeddings for {len(df)} jobs using {MODEL_NAME}...")
    corpus = build_job_corpus_text(df)
    embeddings = encode_texts(corpus, batch_size=32)

    np.save(EMBEDDINGS_CACHE_PATH, embeddings)
    joblib.dump(job_ids, JOB_IDS_CACHE_PATH)
    print(f"✅ Cached {len(embeddings)} dense embeddings to '{EMBEDDINGS_CACHE_PATH}'")

    return embeddings, job_ids

if __name__ == "__main__":
    csv_path = DATA_DIR / "thai_jobs_dataset.csv"
    if not csv_path.exists():
        csv_path = DATA_DIR / "job_dataset.csv"
    df_sample = pd.read_csv(csv_path)
    emb_matrix, ids = build_or_load_job_embeddings(df_sample, force_recompute=True)
    print(f"Done! Embedding matrix shape: {emb_matrix.shape}")
