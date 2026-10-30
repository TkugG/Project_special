"""
src/inspector.py - ระบบแกะรอยและเปิดเผยข้อมูลจริงทุกขั้นตอน (Data & Pipeline Inspector)
ทำหน้าที่:
1. แกะรอยการทำงานตั้งแต่ Input -> Normalization -> TF-IDF -> Logistic Regression -> Softmax -> Argmax -> Set Theory
2. สกัดตัวเลขจริง (Logits, Weights, Probabilities, Sparsity, Set Math) สำหรับการทำวิจัยและภาพประกอบบทที่ 3-4
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.skills_taxonomy import clean_skill_string, normalize_skill, SKILL_SYNONYMS
from src.recommend import JobRecommender, CURRICULUM_ROLES, normalize_role_id

class PipelineInspector:
    def __init__(self, recommender: Optional[JobRecommender] = None):
        # 💡 [ทำไมต้องแบบนี้]: ใช้ Singleton Pattern ร่วมกับ Recommender หลักเพื่อไม่ต้องโหลดโมเดลใหม่ซ้ำซ้อน
        self.recommender = recommender if recommender is not None else JobRecommender()
        self.model = self.recommender.model
        self.tfidf = self.model.named_steps['tfidf']
        self.clf = self.model.named_steps['clf']
        self.feature_names = self.tfidf.get_feature_names_out()
        self.total_features = len(self.feature_names)
        self.cached_jobs = self.recommender.cached_jobs

    def inspect(self, raw_skills: List[str], target_job_id: Optional[str] = None) -> Dict[str, Any]:
        """
        วิเคราะห์และคืนค่าข้อมูลจริงครบทั้ง 6 สเต็ป
        """
        # =========================================================================
        # ด่านที่ 1: การทำความสะอาดและจับคู่คำพ้อง (Input & Canonical Normalization)
        # =========================================================================
        normalization_trace = []
        cleaned_raw_list = []
        normalized_skills_list = []

        for s in raw_skills:
            clean_s = clean_skill_string(str(s))
            if not clean_s:
                continue
            cleaned_raw_list.append(clean_s)
            norm_s = normalize_skill(clean_s)
            normalized_skills_list.append(norm_s)
            
            is_mapped = (clean_s != norm_s) or (clean_s in SKILL_SYNONYMS)
            normalization_trace.append({
                "raw_input": clean_s,
                "canonical_token": norm_s,
                "is_mapped": is_mapped,
                "note": f"แปลงคำพ้อง/ตัวย่อ '{clean_s}' -> '{norm_s}'" if is_mapped else "คำมาตรฐานอยู่แล้ว"
            })

        query_text = " ".join(normalized_skills_list)

        # =========================================================================
        # ด่านที่ 2: การแปลงเวกเตอร์ตัวเลข TF-IDF (1,000 มิติ)
        # =========================================================================
        # 💡 [ทำไมต้องแบบนี้]: Scikit-learn คืนค่าเป็น Scipy CSR Matrix เราแปลงเป็น Index และ Weight จริงเพื่อให้เห็นตัวเลขในหน่วยความจำ
        if query_text.strip():
            sparse_vector = self.tfidf.transform([query_text])
            non_zero_indices = sparse_vector.indices
            non_zero_weights = sparse_vector.data
            
            active_features = []
            for idx, w in zip(non_zero_indices, non_zero_weights):
                token = self.feature_names[idx]
                active_features.append({
                    "feature_index": int(idx),
                    "token": str(token),
                    "weight": round(float(w), 4),
                    "formula_note": f"TF-IDF(t={token}, d) = {float(w):.4f}"
                })
            # เรียงจากค่าน้ำหนักมากไปน้อย
            active_features.sort(key=lambda x: x["weight"], reverse=True)
            non_zero_count = len(active_features)
            sparsity_pct = round((1.0 - (non_zero_count / max(1, self.total_features))) * 100.0, 2)
        else:
            sparse_vector = self.tfidf.transform([""])
            active_features = []
            non_zero_count = 0
            sparsity_pct = 100.0

        tfidf_stage = {
            "query_string": query_text,
            "total_vocabulary_dimensions": self.total_features,
            "non_zero_count": non_zero_count,
            "sparsity_percentage": sparsity_pct,
            "active_features": active_features,
            "raw_vector_preview": [round(float(sparse_vector[0, i]), 4) for i in range(min(15, self.total_features))]
        }

        # =========================================================================
        # ด่านที่ 3: แบบจำลอง Multi-Class Logistic Regression & Softmax Probability
        # =========================================================================
        classes = self.clf.classes_
        if query_text.strip():
            # 💡 [ทำไมต้องแบบนี้]: decision_function คืนค่า Logit (คะแนนดิบทางเส้นตรง w*x + b) ก่อนเข้า Softmax
            raw_logits = self.clf.decision_function(sparse_vector)[0]
            probs = self.clf.predict_proba(sparse_vector)[0]
        else:
            raw_logits = np.zeros(len(classes))
            probs = np.ones(len(classes)) / len(classes)

        distribution = []
        for role_id, logit, p in zip(classes, raw_logits, probs):
            r_id = normalize_role_id(str(role_id))
            r_meta = CURRICULUM_ROLES.get(r_id, {
                "title": f"กลุ่ม {r_id}",
                "en_title": f"Role {r_id}",
                "desc": ""
            })
            distribution.append({
                "role_id": r_id,
                "title": r_meta["title"],
                "en_title": r_meta["en_title"],
                "raw_logit": round(float(logit), 4),
                "probability_pct": round(float(p) * 100.0, 2),
                "probability_raw": round(float(p), 4),
                "is_positive_logit": bool(logit > 0)
            })

        # เรียงตามความน่าจะเป็นสูงสุดลงมา
        distribution.sort(key=lambda x: x["probability_pct"], reverse=True)

        # =========================================================================
        # ด่านที่ 4: การตัดสินใจเลือกสายอาชีพด้วย Argmax
        # =========================================================================
        top_idx = int(np.argmax(probs))
        predicted_role_id = normalize_role_id(str(classes[top_idx]))
        top_role_meta = CURRICULUM_ROLES.get(predicted_role_id, CURRICULUM_ROLES["G1"])

        argmax_stage = {
            "decision_rule": "k* = argmax_k P(y=k | x)",
            "selected_role_id": predicted_role_id,
            "selected_role_title": top_role_meta["title"],
            "selected_role_en": top_role_meta["en_title"],
            "confidence_percentage": round(float(probs[top_idx]) * 100.0, 2),
            "margin_over_second": round(float(distribution[0]["probability_pct"] - distribution[1]["probability_pct"]), 2) if len(distribution) > 1 else 0.0
        }

        # =========================================================================
        # ด่านที่ 5 & 6: การคำนวณทฤษฎีเซตและการจับคู่งานจริง (เหมือน recommend.py 100%)
        # =========================================================================
        # 1. ค้นหาตำแหน่งงานในสายงานนี้ทั้งหมดตาม Stage 1 Filter
        track_jobs = [j for j in self.cached_jobs if normalize_role_id(j["curriculum_role_id"]) == predicted_role_id]
        if not track_jobs:
            track_jobs = self.cached_jobs

        user_set = set(normalized_skills_list)

        # 2. คำนวณคะแนนด้วยทฤษฎีเซตสำหรับทุกงานในสายอาชีพนี้เหมือน recommend.py
        scored_track_jobs = []
        for j in track_jobs:
            j_skills = j["job_skills"]
            j_set = set(j_skills)
            m_set = user_set.intersection(j_set)
            miss_set = j_set.difference(user_set)
            denom = max(1, len(j_set))
            pct = round((len(m_set) / denom) * 100.0, 2)
            scored_track_jobs.append({
                "job": j,
                "job_id": j["job_id"],
                "title": j["title"],
                "company": j["company"],
                "salary": j.get("salary", "ตามโครงสร้างบริษัท"),
                "province": j.get("province", "กรุงเทพมหานคร"),
                "curriculum_role_id": j["curriculum_role_id"],
                "curriculum_role_title": j["curriculum_role_title"],
                "skills_count": len(j_skills),
                "job_set": j_set,
                "matched_set": m_set,
                "missing_set": miss_set,
                "surplus_set": user_set.difference(j_set),
                "match_score_pct": pct
            })

        # 3. เรียงลำดับจากงานที่ได้คะแนน Match Score สูงสุดลงมา (Diversity/Match Ranking เหมือน recommend.py)
        scored_track_jobs.sort(key=lambda x: (x["match_score_pct"], len(x["matched_set"])), reverse=True)

        # 4. เลือกตำแหน่งงานเป้าหมายที่จะแสดง:
        # - ถ้าผู้ใช้ระบุ target_job_id เจาะจง ให้ใช้ใบนั้น
        # - ถ้าไม่ได้ระบุ ให้เลือก "งานที่ได้คะแนน Match Score สูงสุดในสายงานนั้น (best_target_job)" เหมือน recommend.py
        selected_scored = None
        if target_job_id:
            for sj in scored_track_jobs:
                if str(sj["job_id"]).strip().lower() == str(target_job_id).strip().lower():
                    selected_scored = sj
                    break

        if selected_scored is None and len(scored_track_jobs) > 0:
            selected_scored = scored_track_jobs[0]

        selected_job = selected_scored["job"] if selected_scored else None
        job_set = selected_scored["job_set"] if selected_scored else set()
        matched_set = selected_scored["matched_set"] if selected_scored else set()
        missing_set = selected_scored["missing_set"] if selected_scored else set()
        surplus_set = selected_scored["surplus_set"] if selected_scored else set()
        match_score_pct = selected_scored["match_score_pct"] if selected_scored else 0.0

        set_theory_stage = {
            "target_job": {
                "job_id": selected_job["job_id"] if selected_job else "N/A",
                "title": selected_job["title"] if selected_job else "N/A",
                "company": selected_job["company"] if selected_job else "N/A",
                "curriculum_role_id": selected_job["curriculum_role_id"] if selected_job else "N/A",
                "curriculum_role_title": selected_job["curriculum_role_title"] if selected_job else "N/A",
                "salary": selected_job.get("salary", "ตามโครงสร้างบริษัท") if selected_job else "N/A",
                "province": selected_job.get("province", "กรุงเทพมหานคร") if selected_job else "N/A",
                "total_skills_required": len(job_set)
            },
            "math_formula": {
                "intersection_formula": "S_matched = S_user ∩ S_job",
                "skill_gap_formula": "S_gap = S_job \\ S_user",
                "match_score_formula": "Match Score (%) = (|S_user ∩ S_job| / |S_job|) × 100"
            },
            "user_skill_set": sorted(list(user_set)),
            "job_skill_set": sorted(list(job_set)),
            "matched_skills": sorted(list(matched_set)),
            "missing_skills": sorted(list(missing_set)),
            "surplus_skills": sorted(list(surplus_set)),
            "match_score_percentage": match_score_pct,
            "total_job_skills_count": len(job_set),
            "matched_count": len(matched_set),
            "missing_count": len(missing_set)
        }

        # รายการตำแหน่งงานในกลุ่มนี้ทั้งหมดเพื่อนำไปทำตัวเลือก Dropdown (เรียงตามคะแนนที่ตรงที่สุดก่อน)
        available_jobs_in_track = []
        for sj in scored_track_jobs[:10]:
            available_jobs_in_track.append({
                "job_id": sj["job_id"],
                "title": sj["title"],
                "company": sj["company"],
                "skills_count": sj["skills_count"],
                "match_score_pct": sj["match_score_pct"]
            })

        return {
            "status": "success",
            "stage_1_normalization": {
                "raw_skills": cleaned_raw_list,
                "normalized_skills": normalized_skills_list,
                "mappings": normalization_trace
            },
            "stage_2_tfidf_vector": tfidf_stage,
            "stage_3_model_distribution": {
                "classifier_type": "Multi-Class Logistic Regression (L2 Regularization C=0.5)",
                "classes_count": len(classes),
                "distribution": distribution
            },
            "stage_4_argmax_decision": argmax_stage,
            "stage_5_6_set_theory": set_theory_stage,
            "available_jobs_in_track": available_jobs_in_track
        }

# สร้างอินสแตนซ์พร้อมใช้งาน
inspector_engine = PipelineInspector()
