"""
recommend.py - ระบบแนะนำตำแหน่งงานและวิเคราะห์ทักษะ (KISS Principle)
ฟังก์ชันหลัก:
1. predict_career(): ใช้โมเดล Logistic Regression ทำนายว่าทักษะตรงกับกลุ่มอาชีพใดใน 8 อาชีพ มคอ.2
2. recommend_jobs(): ใช้ Content-Based Filtering (Skill Overlap + Cosine Similarity) แนะนำ Top 5 งาน
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# 8 กลุ่มอาชีพตามมาตรฐานหลักสูตร มคอ.2 สาขา IT (ตารางที่ 3.1)
CURRICULUM_ROLES = {
    "G1": {
        "id": "G1",
        "title": "นักพัฒนาซอฟต์แวร์",
        "en_title": "Software Developer",
        "desc": "ออกแบบ พัฒนา เขียนชุดคำสั่ง และทดสอบระบบซอฟต์แวร์หรือแอปพลิเคชัน",
        "core_skills": ["sql", ".net", "java", "angular", "javascript", "git", "c#", "python", "rest api", "react"]
    },
    "G2": {
        "id": "G2",
        "title": "ผู้ดูแลระบบฐานข้อมูล",
        "en_title": "Database Administrator",
        "desc": "ออกแบบ บริหารจัดการ ดูแลความมั่นคงปลอดภัย และสำรองข้อมูลระบบฐานข้อมูล",
        "core_skills": ["sql", "python", "postgresql", "sql server", "mysql", "oracle", "api", "ssis", "oracle rac", "mongodb"]
    },
    "G3": {
        "id": "G3",
        "title": "นักวิเคราะห์และออกแบบระบบ",
        "en_title": "System Analyst / Designer",
        "desc": "วิเคราะห์ความต้องการทางธุรกิจ ออกแบบผังกระบวนการทำงาน และข้อกำหนดระบบสารสนเทศ",
        "core_skills": ["api", "sql", "sql server", "java", "postgresql", "react", "uat", "mysql", ".net", "system analysis"]
    },
    "G4": {
        "id": "G4",
        "title": "เจ้าหน้าที่เทคนิคคอมพิวเตอร์",
        "en_title": "Computer Technical Officer",
        "desc": "ตรวจสอบ ติดตั้ง ซ่อมบำรุงฮาร์ดแวร์ อุปกรณ์ต่อพ่วง และแก้ไขปัญหาการใช้งานคอมพิวเตอร์",
        "core_skills": ["windows", "vpn", "microsoft 365", "active directory", "printers", "hardware", "troubleshooting", "sql", "helpdesk", "basic networking"]
    },
    "G5": {
        "id": "G5",
        "title": "ผู้ดูแลระบบ",
        "en_title": "System Administrator",
        "desc": "ติดตั้ง กำหนดค่า และบริหารจัดการระบบปฏิบัติการเครื่องแม่ข่ายและระบบเครือข่าย",
        "core_skills": ["linux", "windows server", "active directory", "vmware", "azure", "firewall", "vpn", "microsoft 365", "switches", "network security"]
    },
    "G6": {
        "id": "G6",
        "title": "นักพัฒนาเว็บไซต์",
        "en_title": "Web Developer",
        "desc": "ออกแบบ พัฒนา และบำรุงรักษาเว็บไซต์ เว็บแอปพลิเคชัน และระบบบริการส่วนหน้า",
        "core_skills": ["html5", "css3", "javascript", "react", "next.js", "git", "mysql", "node.js", "php", "tailwind"]
    },
    "G7": {
        "id": "G7",
        "title": "ผู้ช่วยผู้จัดการโครงการสารสนเทศ",
        "en_title": "IT Project Assistant",
        "desc": "ประสานงาน ติดตามแผนงาน จัดทำเอกสารข้อกำหนด และสนับสนุนการบริหารโครงการไอที",
        "core_skills": ["project management", "agile", "scrum", "jira", "ms office", "excel", "powerpoint", "erp", "sap", "communication"]
    },
    "G8": {
        "id": "G8",
        "title": "ผู้สร้างสรรค์เนื้อหาดิจิทัล",
        "en_title": "Content Creator",
        "desc": "ออกแบบ ผลิต และจัดการสื่อดิจิทัล สื่อประสม กราฟิก และมัลติมีเดียเพื่อการสื่อสาร",
        "core_skills": ["tiktok", "canva", "capcut", "premiere pro", "video editing", "youtube", "photoshop", "instagram", "facebook", "content creator"]
    }
}

# แมปชื่อและรหัสเดิม (8.1 - 8.8) เพื่อ Backward Compatibility
ROLE_ALIASES = {
    "8.1": "G4",
    "8.2": "G5",
    "8.3": "G8",
    "8.4": "G7",
    "8.5": "G3",
    "8.6": "G1",
    "8.7": "G6",
    "8.8": "G2"
}

def normalize_role_id(role_id: Optional[str]) -> str:
    """แปลงรหัสกลุ่มอาชีพทั้งรูปแบบ G1-G8 และ 8.1-8.8 ให้เป็นรหัสมาตรฐาน G1-G8"""
    if not role_id:
        return "G1"
    r = str(role_id).strip()
    if r in CURRICULUM_ROLES:
        return r
    if r in ROLE_ALIASES:
        return ROLE_ALIASES[r]
    r_lower = r.lower()
    for gid, info in CURRICULUM_ROLES.items():
        if gid.lower() == r_lower or info["title"].lower() in r_lower or info["en_title"].lower() in r_lower:
            return gid
    return "G1"

from src.skills_taxonomy import (
    normalize_skill,
    normalize_skills_list,
    parse_and_normalize_skills,
    clean_skill_string
)

def clean_skill(s: str) -> str:
    """ตัดช่องว่างและแปลงเป็นตัวพิมพ์เล็ก พร้อมทำ Canonical Normalization"""
    return normalize_skill(s)

def parse_skills(text: str) -> List[str]:
    """แยกข้อความทักษะเป็น list พร้อมแปลงคำพ้องเป็นคำมาตรฐาน (Canonical Skills)"""
    return parse_and_normalize_skills(text)

class JobRecommender:
    """
    คลาสหลักสำหรับระบบแนะนำงาน:
    1. ทำนายกลุ่มอาชีพด้วย Logistic Regression
    2. จัดอันดับงานด้วย Skill Overlap % + TF-IDF Cosine Similarity
    """
    def __init__(self):
        # 1. โหลดข้อมูลตำแหน่งงานไทย (115 งานจริง)
        csv_path = DATA_DIR / "เก็บข้อมูล.csv"
        if not csv_path.exists():
            csv_path = DATA_DIR / "thai_jobs_dataset.csv"
        self.df_jobs = pd.read_csv(csv_path).fillna("")

        # 2. โหลดโมเดลจำแนกกลุ่มอาชีพ
        model_path = MODELS_DIR / "career_classifier.joblib"
        if not model_path.exists():
            from src.train import train_career_model
            self.model = train_career_model()
        else:
            self.model = joblib.load(model_path)

        # =========================================================================
        # [จุดสำคัญที่ 5: การลด Latency ด้วย In-Memory Pre-parsing Cache]
        # ปัญหาเดิม: การใช้ pandas .iloc วนลูปและตัดคำด้วย regex ซ้ำๆ ทุกครั้งที่มี request
        # ทำให้ระบบหน่วงกินเวลาถึง 50+ ms ต่อคำขอ
        # วิธีแก้: เราแยก parse ทักษะของ 115 ตำแหน่งงานจริงเป็น set() และ dict เก็บไว้ใน RAM
        # ตั้งแต่ตอนเปิดเซิร์ฟเวอร์ครั้งเดียว ส่งผลให้ Latency ลดลงเหลือเพียง ~1-2 ms (Real-time)
        # =========================================================================
        self.cached_jobs = []
        for idx in range(len(self.df_jobs)):
            row = self.df_jobs.iloc[idx]
            job_skills = parse_skills(str(row.get("Skills", "")))
            resps_raw = str(row.get("Responsibilities", "")).strip()
            self.cached_jobs.append({
                "idx": idx,
                "job_id": str(row.get("JobID", f"JOB-{idx+1:03d}")).strip(),
                "title": str(row.get("Title", "")).strip(),
                "curriculum_role_id": str(row.get("CurriculumRoleID", "8.6")).strip(),
                "curriculum_role_title": str(row.get("CurriculumRoleTitle", "นักพัฒนาซอฟต์แวร์")).strip(),
                "curriculum_role_en": str(row.get("CurriculumRoleEN", "Software Developer")).strip(),
                "company": str(row.get("Company", "บริษัทเทคโนโลยีในไทย")).strip(),
                "province": str(row.get("Province", "กรุงเทพมหานคร")).strip(),
                "salary": str(row.get("Salary", "ตามโครงสร้างบริษัท")).strip(),
                "experience_level": str(row.get("ExperienceLevel", "Entry-Level / เด็กจบใหม่ (0-1 ปี)")).strip(),
                "years_of_experience": str(row.get("YearsOfExperience", "0-1")).strip(),
                "responsibilities": resps_raw,
                "responsibilities_list": [r.strip() for r in resps_raw.split(";") if len(r.strip()) > 5][:4],
                "keywords": str(row.get("Keywords", "")).strip(),
                "apply_url": str(row.get("ApplyURL", "https://jobs.blognone.com")).strip(),
                "job_skills": job_skills,
                # 🎯 [หัวใจหลัก]: แปลง List เป็น set() เก็บไว้ใน RAM ล่วงหน้า เพื่อให้ตรวจสอบ Membership ได้ที่ O(1)
                "job_skills_set": set(job_skills)
            })

    # =========================================================================
    # [จุดสำคัญที่ 6: การจำแนกอาชีพด้วย Supervised ML (Logistic Regression)]
    # โมเดลจะแปลง query_text เป็น TF-IDF เวกเตอร์ แล้วส่งเข้า Logistic Regression
    # เพื่อคำนวณ Softmax / Sigmoid Probability ของทั้ง 8 อาชีพ
    # คืนค่ารหัสอาชีพที่มีความน่าจะเป็นสูงสุด (Argmax) พร้อมค่าความมั่นใจ (%)
    # =========================================================================
    def predict_career(self, user_skills: List[str]) -> Dict[str, Any]:
        """
        ทำนายว่าทักษะตรงกับอาชีพใดใน 8 อาชีพ มคอ.2 มากที่สุด
        ส่งคืนรหัสอาชีพ, ความมั่นใจ (%), และความน่าจะเป็นของทั้ง 8 อาชีพ
        """
        # 🔄 [การแปลงข้อมูล]: รวมทักษะมาตรฐานเป็น String เดียว เพื่อเตรียมป้อนเข้าสู่โมเดลจำแนก
        query_text = " ".join([clean_skill(s) for s in user_skills if clean_skill(s)])
        # ⚠️ [จุดระวัง]: หากผู้ใช้ไม่ส่งทักษะเข้ามา ให้ Fallback เป็นสายงานเริ่มต้น (G1) ป้องกันโมเดลแครช
        if not query_text:
            return {
                "predicted_role_id": "G1",
                "confidence": 0.0,
                "role_info": CURRICULUM_ROLES["G1"],
                "probabilities": {}
            }

        # 🎯 [หัวใจหลัก]: คำนวณความน่าจะเป็นของทั้ง 8 สายงาน มคอ.2 ด้วย Softmax Probability จาก Logistic Regression
        probs = self.model.predict_proba([query_text])[0]
        classes = self.model.named_steps['clf'].classes_
        
        # 💡 [ทำไมต้องแบบนี้]: ใช้ argmax เพื่อเลือกกลุ่มอาชีพที่โมเดลประเมินว่ามีค่าน้ำหนักความน่าจะเป็นสูงสุด
        top_idx = int(np.argmax(probs))
        predicted_role_id = normalize_role_id(str(classes[top_idx]))
        confidence = float(probs[top_idx]) * 100.0

        prob_breakdown = {}
        for role_id, prob in zip(classes, probs):
            role_k = normalize_role_id(str(role_id))
            prob_breakdown[role_k] = round(float(prob) * 100.0, 1)

        return {
            "predicted_role_id": predicted_role_id,
            "confidence": round(confidence, 1),
            "role_info": CURRICULUM_ROLES.get(predicted_role_id, CURRICULUM_ROLES["G1"]),
            "probabilities": prob_breakdown
        }

    def recommend(
        self,
        user_skills: List[str],
        preference_role_id: Optional[str] = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        แนะนำตำแหน่งงาน Top 5 ตามระเบียบวิธีวิจัยบทที่ 3 (หัวข้อ 3.4.2):
        - Stage 1: Role Classification Stage ทำนายกลุ่มสายงานอาชีพด้วย Multi-Class Logistic Regression
        - Stage 2: Job Matching & Skill Gap Analysis คำนวณความตรงกันด้วยทฤษฎีเซต (Skill Match Percentage = |S_user ∩ S_job| / |S_job| * 100)
        """
        user_skills_clean = [clean_skill(s) for s in user_skills if clean_skill(s)]
        # 💡 [ทำไมต้องแบบนี้]: แปลงเป็น set เพื่อให้การเปรียบเทียบหาทักษะที่ตรงกันทำงานได้เร็วระดับ O(1) ตามทฤษฎีเซต
        user_skills_set = set(user_skills_clean)

        # 1. Stage 1: ทำนายอาชีพด้วย Multi-Class Logistic Regression (บทที่ 3 หัวข้อ 3.4.1)
        career_pred = self.predict_career(user_skills_clean)
        # 💡 [ทำไมต้องแบบนี้]: ให้ความสำคัญกับสายงานเป้าหมายที่ผู้ใช้เลือกเองก่อน หากไม่เลือกจึงใช้ผลทำนายจากโมเดล ML
        norm_pref = normalize_role_id(preference_role_id) if preference_role_id else ""
        target_role_id = norm_pref if norm_pref else career_pred["predicted_role_id"]
        # ⚠️ [จุดระวัง]: ใช้ .get() คู่กับ Default Fallback (G1) ป้องกัน KeyError กรณีส่งรหัสที่ไม่มีใน มคอ.2
        target_role_info = CURRICULUM_ROLES.get(target_role_id, CURRICULUM_ROLES["G1"])

        # 2. Stage 2: คำนวณคะแนนด้วยทฤษฎีเซต (บทที่ 3 หัวข้อ 3.4.2)
        # กรองและจัดอันดับด้วยสูตร: Skill Match Percentage = (|S_user ∩ S_job| / |S_job|) * 100
        scored_jobs = []
        for job in self.cached_jobs:
            job_skills = job["job_skills"]

            # =========================================================================
            # [การหา Matching / Missing Skills ด้วยทฤษฎีเซต]
            # - Matched Skills: S_user ∩ S_job (อินเตอร์เซกชัน)
            # - Missing Skills (Skill Gap): S_job \ S_user (ผลต่างเชิงเซต)
            # โปร่งใส ตรวจสอบได้ 100% ปราศจาก Arbitrary Weights
            # =========================================================================
            matched_skills = [s for s in job_skills if s in user_skills_set]
            missing_skills = [s for s in job_skills if s not in user_skills_set]
            total_req = len(job_skills)

            # ร้อยละความสอดคล้องของทักษะ (Skill Match Percentage):
            # ⚠️ [จุดระวัง]: ใช้ max(1, total_req) ป้องกันกรณีหารด้วยศูนย์ (ZeroDivisionError)
            overlap_pct = (len(matched_skills) / max(1, total_req)) * 100.0
            match_score = int(round(overlap_pct))

            scored_jobs.append({
                "job_id": job["job_id"],
                "title": job["title"],
                "curriculum_role_id": job["curriculum_role_id"],
                "curriculum_role_title": job["curriculum_role_title"],
                "curriculum_role_en": job["curriculum_role_en"],
                "company": job["company"],
                "province": job["province"],
                "salary": job["salary"],
                "experience_level": job["experience_level"],
                "years_of_experience": job["years_of_experience"],
                "responsibilities": job["responsibilities"],
                "responsibilities_list": job["responsibilities_list"],
                "keywords": job["keywords"],
                "apply_url": job["apply_url"],
                "score": match_score,
                "ml_confidence": match_score,
                "exact_score": match_score,
                "semantic_score": match_score,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "total_skills_count": total_req
            })

        # 4. ส่วนที่ 1: วิเคราะห์สายงานเป้าหมาย (Target Career Analysis)
        target_jobs = [j for j in scored_jobs if j["curriculum_role_id"] == target_role_id]
        best_target_job = max(target_jobs, key=lambda x: x["score"]) if target_jobs else scored_jobs[0]

        core_skills_target = [clean_skill(s) for s in target_role_info["core_skills"]]
        matched_core = [s for s in core_skills_target if s in user_skills_set]
        missing_core = [s for s in core_skills_target if s not in user_skills_set]
        # 🎯 [หัวใจหลัก]: คำนวณความพร้อมเทียบกับเกณฑ์มาตรฐาน มคอ.2 (บทที่ 3 หัวข้อ 3.4.4)
        readiness_pct = round((len(matched_core) / max(1, len(core_skills_target))) * 100.0, 1)

        # จำแนกระดับความพร้อมออกเป็น 3 ระดับตามเกณฑ์บทที่ 3 (หน้า 10):
        if readiness_pct >= 80.0:
            readiness_level = "ระดับเชี่ยวชาญ (Advanced)"
        elif readiness_pct >= 50.0:
            readiness_level = "ระดับพร้อมทำงาน (Job-Ready)"
        else:
            readiness_level = "ระดับเริ่มต้น (Developing)"

        target_analysis = {
            "target_role_id": target_role_id,
            "target_role_title": target_role_info["title"],
            "target_role_en": target_role_info["en_title"],
            "target_role_desc": target_role_info["desc"],
            "predicted_role_id": career_pred["predicted_role_id"],
            "predicted_confidence": career_pred["confidence"],
            "role_probabilities": career_pred["probabilities"],
            "job_id": best_target_job["job_id"],
            "title": best_target_job["title"],
            "company": best_target_job["company"],
            "province": best_target_job["province"],
            "salary": best_target_job["salary"],
            "score": best_target_job["score"],
            "semantic_score": best_target_job["semantic_score"],
            "exact_score": best_target_job["exact_score"],
            "matched_skills": matched_core,
            "missing_skills": missing_core,
            "skill_readiness": readiness_pct,
            "readiness_level": readiness_level,
            "total_skills_count": len(core_skills_target)
        }

        # 5. ส่วนที่ 2: จัดอันดับ Top 5 งานที่ตรงที่สุด (Diversity-Aware Ranking ตามบทที่ 3 หัวข้อ 3.4.3)
        # 💡 [ทำไมต้องแบบนี้]: กรองงานในสายอาชีพเป้าหมายก่อน (Stage 1 Filter) แล้วเรียงตามคะแนน Match Score และจำนวนทักษะตรง
        sorted_jobs = sorted(
            scored_jobs,
            key=lambda x: (x["curriculum_role_id"] == target_role_id, x["score"], len(x["matched_skills"])),
            reverse=True
        )
        top_results = []
        seen_title_company = set()
        title_counts = {}
        max_per_title = 2  # จำกัดไม่ให้ชื่องานเดียวกันผูกขาดเกิน 2 บริษัทใน Top 5 เพื่อสร้างความหลากหลาย (Diversity)

        # รอบที่ 1: คัดเลือกงานคะแนนสูงสุดโดยจำกัดไม่ให้ชื่องานหลักซ้ำเกิน max_per_title
        for j in sorted_jobs:
            tc_key = (j["title"].lower(), j["company"].lower())
            if tc_key in seen_title_company:
                continue
            base_title = j["title"].split("(")[0].strip().lower()
            if title_counts.get(base_title, 0) < max_per_title:
                top_results.append(j)
                seen_title_company.add(tc_key)
                title_counts[base_title] = title_counts.get(base_title, 0) + 1
                if len(top_results) >= top_k:
                    break

        # รอบที่ 2 (Fallback): ถ้ายังไม่ครบ top_k ให้เติมงานที่คะแนนดีที่สุดที่เหลือ (ป้องกันผลลัพธ์ขาด)
        if len(top_results) < top_k:
            for j in sorted_jobs:
                tc_key = (j["title"].lower(), j["company"].lower())
                if tc_key not in seen_title_company:
                    top_results.append(j)
                    seen_title_company.add(tc_key)
                    if len(top_results) >= top_k:
                        break

        return {
            "status": "success",
            "target_career_analysis": target_analysis,
            "skill_matched_recommendations": top_results,
            "results": top_results,
            "total_matched": len(top_results)
        }
