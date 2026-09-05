"""
retrieval.py - Stage 1: Candidate Generation (Hybrid Search: Dense Semantic + BM25 Lexical)
Combines deep semantic vector search with exact keyword matching using Reciprocal Rank Fusion (RRF).
"""

import re
import math
from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd

from src.embeddings import (
    encode_query,
    build_or_load_job_embeddings
)

PROTECTED_TECH_TERMS = {
    "c#", "c++", ".net", "asp.net", "asp.net core", "asp.net mvc",
    "node.js", "react.js", "vue.js", "next.js", "nuxt.js", "ci/cd",
    "ui/ux", "tcp/ip", "pl/sql", "power bi"
}

def tokenize_tech_text(text: str) -> List[str]:
    """Tokenizes text while protecting programming languages and framework terms."""
    if not text or not isinstance(text, str):
        return []
    
    t = text.lower().strip()
    # Replace separators with spaces except protected terms
    tokens = []
    # Match words, symbols like #, +, ., -, /
    raw_tokens = re.findall(r'[a-zA-Z0-9_+#.-]+(?:/[a-zA-Z0-9_+#.-]+)?', t)
    for tok in raw_tokens:
        tok = tok.strip(" ,;:-_./|")
        if tok:
            tokens.append(tok)
    return tokens

class BM25Okapi:
    """
    Production BM25Okapi implementation for exact technical keyword retrieval.
    Follows standard Robertson & Jones BM25 formula.
    """
    def __init__(self, corpus_tokens: List[List[str]], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = len(corpus_tokens)
        self.doc_lens = [len(doc) for doc in corpus_tokens]
        self.avgdl = sum(self.doc_lens) / self.corpus_size if self.corpus_size > 0 else 1.0

        # Term document frequencies
        self.df: Dict[str, int] = {}
        self.doc_term_freqs: List[Dict[str, int]] = []

        for doc in corpus_tokens:
            tf: Dict[str, int] = {}
            for term in doc:
                tf[term] = tf.get(term, 0) + 1
            self.doc_term_freqs.append(tf)

            for term in tf.keys():
                self.df[term] = self.df.get(term, 0) + 1

        # Precompute IDF
        self.idf: Dict[str, float] = {}
        for term, freq in self.df.items():
            # Robertson-Spärck Jones IDF with smoothing
            self.idf[term] = math.log(1.0 + (self.corpus_size - freq + 0.5) / (freq + 0.5))

    def get_scores(self, query_tokens: List[str]) -> np.ndarray:
        """Compute BM25 scores for all documents given tokenized query."""
        scores = np.zeros(self.corpus_size, dtype=np.float32)
        for term in query_tokens:
            if term not in self.idf:
                continue
            idf_val = self.idf[term]
            for idx in range(self.corpus_size):
                tf = self.doc_term_freqs[idx].get(term, 0)
                if tf == 0:
                    continue
                doc_len = self.doc_lens[idx]
                denom = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avgdl))
                scores[idx] += idf_val * ((tf * (self.k1 + 1.0)) / denom)
        return scores

class HybridRetriever:
    """
    Stage 1 Hybrid Retriever:
    Fuses Dense Semantic Similarity (SentenceTransformers) and Lexical Matching (BM25)
    via Reciprocal Rank Fusion (RRF).
    """
    def __init__(self, df_jobs: pd.DataFrame, force_recompute_embeddings: bool = False):
        self.df_jobs = df_jobs.reset_index(drop=True)
        self.job_ids = [str(row.get("JobID", f"JOB-{idx}")) for idx, row in self.df_jobs.iterrows()]
        
        # 1. Initialize Dense Retrieval
        self.embeddings_matrix, _ = build_or_load_job_embeddings(
            self.df_jobs, 
            force_recompute=force_recompute_embeddings
        )

        # 2. Initialize BM25 Lexical Retrieval
        corpus_texts = []
        for _, row in self.df_jobs.iterrows():
            title = str(row.get("Title", ""))
            skills = str(row.get("Skills", ""))
            resps = str(row.get("Responsibilities", ""))
            keywords = str(row.get("Keywords", ""))
            corpus_texts.append(f"{title} {skills} {resps} {keywords}")

        corpus_tokens = [tokenize_tech_text(t) for t in corpus_texts]
        self.bm25 = BM25Okapi(corpus_tokens, k1=1.5, b=0.75)

    def retrieve_candidates(
        self,
        query: str,
        top_k: int = 50,
        rrf_k: int = 60
    ) -> List[Dict[str, Any]]:
        """
        Executes Stage-1 Candidate Retrieval.
        Returns Top-K candidates ranked by Reciprocal Rank Fusion.
        """
        # 1. Dense Semantic Scoring
        query_vec = encode_query(query)
        # Dot product with L2-normalized embeddings is cosine similarity
        dense_sims = np.dot(self.embeddings_matrix, query_vec)
        dense_sims = np.clip(dense_sims, 0.0, 1.0)
        dense_ranking = np.argsort(-dense_sims)  # High to low

        # 2. BM25 Lexical Scoring
        query_tokens = tokenize_tech_text(query)
        bm25_scores = self.bm25.get_scores(query_tokens)
        max_bm25 = np.max(bm25_scores) if np.max(bm25_scores) > 0 else 1.0
        normalized_bm25 = np.clip(bm25_scores / max_bm25, 0.0, 1.0)
        bm25_ranking = np.argsort(-bm25_scores)

        # 3. Reciprocal Rank Fusion (RRF)
        total_docs = len(self.df_jobs)
        dense_rank_dict = {doc_idx: rank + 1 for rank, doc_idx in enumerate(dense_ranking)}
        bm25_rank_dict = {doc_idx: rank + 1 for rank, doc_idx in enumerate(bm25_ranking)}

        rrf_scores = np.zeros(total_docs, dtype=np.float32)
        for idx in range(total_docs):
            r_dense = dense_rank_dict[idx]
            r_bm25 = bm25_rank_dict[idx]
            rrf_scores[idx] = (1.0 / (rrf_k + r_dense)) + (1.0 / (rrf_k + r_bm25))

        top_indices = np.argsort(-rrf_scores)[:top_k]

        candidates = []
        for idx in top_indices:
            candidates.append({
                "doc_idx": int(idx),
                "job_id": self.job_ids[idx],
                "dense_score": float(dense_sims[idx]),
                "bm25_score": float(normalized_bm25[idx]),
                "rrf_score": float(rrf_scores[idx]),
                "dense_rank": dense_rank_dict[idx],
                "bm25_rank": bm25_rank_dict[idx]
            })

        return candidates
