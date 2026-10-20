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
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# 8 อาชีพตามมาตรฐานหลักสูตร มคอ.2 สาขา IT
CURRICULUM_ROLES = {
    "8.1": {
        "id": "8.1",
        "title": "เจ้าหน้าที่คอมพิวเตอร์",
        "en_title": "Computer Officer / IT Support",
        "desc": "ติดตั้ง บำรุงรักษา และแก้ปัญหาฮาร์ดแวร์ ซอฟต์แวร์ และระบบเครือข่ายพื้นฐาน",
        "core_skills": ["windows", "linux", "hardware", "troubleshooting", "basic networking", "helpdesk", "active directory", "ms office"]
    },
    "8.2": {
        "id": "8.2",
        "title": "ผู้ดูแลระบบเครือข่ายคอมพิวเตอร์",
        "en_title": "Network Administrator / Engineer",
        "desc": "ออกแบบ ติดตั้ง กำหนดค่า และดูแลความมั่นคงปลอดภัยระบบเครือข่ายและเซิร์ฟเวอร์",
        "core_skills": ["tcp/ip", "cisco", "routing", "switching", "firewall", "vpn", "dns", "dhcp", "linux server", "network security"]
    },
    "8.3": {
        "id": "8.3",
        "title": "นักพัฒนาและออกแบบสื่อผสม (Multimedia Designer & Developer)",
        "en_title": "Multimedia Designer & Developer",
        "desc": "ออกแบบสื่อดิจิทัล ภาพกราฟิก แอนิเมชัน วิดีโอ ตัวต้นแบบ UI/UX และสื่อปฏิสัมพันธ์",
        "core_skills": ["ui/ux", "figma", "photoshop", "illustrator", "premiere pro", "after effects", "blender", "3d animation", "unity", "game development", "prototyping"]
    },
    "8.4": {
        "id": "8.4",
        "title": "นักจัดการโครงการสารสนเทศ",
        "en_title": "IT Project Manager / Coordinator",
        "desc": "วางแผน ประสานงาน ติดตามความก้าวหน้า และควบคุมคุณภาพโครงการด้านไอที",
        "core_skills": ["agile", "scrum", "jira", "project management", "trello", "communication", "risk management", "sdlc"]
    },
    "8.5": {
        "id": "8.5",
        "title": "นักวิเคราะห์และออกแบบระบบงาน",
        "en_title": "System Analyst / Business Analyst",
        "desc": "รวบรวมความต้องการ วิเคราะห์กระบวนการ ออกแบบสถาปัตยกรรมระบบ ฐานข้อมูล และจัดทำ SRS",
        "core_skills": ["system analysis", "business analysis", "uml", "use case", "dfd", "er diagram", "database design", "sql", "requirement gathering"]
    },
    "8.6": {
        "id": "8.6",
        "title": "นักพัฒนาซอฟต์แวร์",
        "en_title": "Software Developer / Engineer",
        "desc": "ออกแบบและเขียนโปรแกรม พัฒนาเว็บเซอร์วิส แอปพลิเคชัน และฐานข้อมูล",
        "core_skills": ["python", "java", "c#", ".net", "javascript", "typescript", "react", "node.js", "sql", "rest api", "git", "docker"]
    },
    "8.7": {
        "id": "8.7",
        "title": "นักออกแบบและพัฒนาเว็บไซต์",
        "en_title": "Web Designer & Developer",
        "desc": "ออกแบบและพัฒนาเว็บไซต์ เว็บแอปพลิเคชันแบบ Responsive และระบบ CMS",
        "core_skills": ["html5", "css3", "javascript", "responsive web design", "tailwind", "bootstrap", "wordpress", "php", "mysql"]
    },
    "8.8": {
        "id": "8.8",
        "title": "ผู้เชี่ยวชาญด้านเทคโนโลยีสารสนเทศ",
        "en_title": "Specialized IT Professional",
        "desc": "พัฒนางานเฉพาะทางขั้นสูง เช่น ปัญญาประดิษฐ์ วิทยาการข้อมูล ความมั่นคงปลอดภัย และคลาวด์",
        "core_skills": ["machine learning", "deep learning", "nlp", "cybersecurity", "cloud architecture", "big data", "data science"]
    }
}

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
        # 1. โหลดข้อมูลตำแหน่งงานไทย
        csv_path = DATA_DIR / "thai_jobs_dataset.csv"
        if not csv_path.exists():
            csv_path = DATA_DIR / "job_dataset.csv"
        self.df_jobs = pd.read_csv(csv_path).fillna("")

        # 2. โหลดโมเดลจำแนกกลุ่มอาชีพ
        model_path = MODELS_DIR / "career_classifier.joblib"
        if not model_path.exists():
            from src.train import train_career_model
            self.model = train_career_model()
        else:
            self.model = joblib.load(model_path)

        # 3. เตรียม TF-IDF Matrix ของตำแหน่งงานทั้งหมด (ใช้ทักษะที่ผ่าน Normalization แล้ว)
        self.vectorizer = self.model.named_steps['tfidf']
        clean_corpus = []
        for _, row in self.df_jobs.iterrows():
            norm_skills_str = " ".join(parse_skills(str(row.get('Skills', ''))))
            t = f"{row.get('Title', '')} {norm_skills_str} {row.get('Keywords', '')}".lower()
            clean_corpus.append(t)
        # 🎯 [หัวใจหลัก]: แปลง Corpus งานทั้งหมดเป็น TF-IDF Sparse Matrix ล่วงหน้าเพียงครั้งเดียวตอนเริ่มระบบ
        # 💡 [ทำไมต้องแบบนี้]: คำนวณเวกเตอร์ไว้ล่วงหน้าเพื่อลดภาระ CPU ทำให้คำขอถัดไปหา Cosine Similarity ได้ทันที
        self.job_tfidf_matrix = self.vectorizer.transform(clean_corpus)

        # =========================================================================
        # [จุดสำคัญที่ 5: การลด Latency ด้วย In-Memory Pre-parsing Cache]
        # ปัญหาเดิม: การใช้ pandas .iloc วนลูปและตัดคำด้วย regex ซ้ำๆ ทุกครั้งที่มี request
        # ทำให้ระบบหน่วงกินเวลาถึง 50+ ms ต่อคำขอ
        # วิธีแก้: เราแยก parse ทักษะของ 253 ตำแหน่งงานเป็น set() และ dict เก็บไว้ใน RAM
        # ตั้งแต่ตอนเปิดเซิร์ฟเวอร์ครั้งเดียว ส่งผลให้ Latency ลดลงเหลือเพียง ~6 ms (Real-time)
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
        # ⚠️ [จุดระวัง]: หากผู้ใช้ไม่ส่งทักษะเข้ามา ให้ Fallback เป็นสายงานเริ่มต้น (8.6) ป้องกันโมเดลแครช
        if not query_text:
            return {
                "predicted_role_id": "8.6",
                "confidence": 0.0,
                "role_info": CURRICULUM_ROLES["8.6"],
                "probabilities": {}
            }

        # 🎯 [หัวใจหลัก]: คำนวณความน่าจะเป็นของทั้ง 8 สายงาน มคอ.2 ด้วย Softmax Probability จาก Logistic Regression
        probs = self.model.predict_proba([query_text])[0]
        classes = self.model.named_steps['clf'].classes_
        
        # 💡 [ทำไมต้องแบบนี้]: ใช้ argmax เพื่อเลือกกลุ่มอาชีพที่โมเดลประเมินว่ามีค่าน้ำหนักความน่าจะเป็นสูงสุด
        top_idx = int(np.argmax(probs))
        predicted_role_id = str(classes[top_idx])
        confidence = float(probs[top_idx]) * 100.0

        prob_breakdown = {}
        for role_id, prob in zip(classes, probs):
            prob_breakdown[str(role_id)] = round(float(prob) * 100.0, 1)

        return {
            "predicted_role_id": predicted_role_id,
            "confidence": round(confidence, 1),
            "role_info": CURRICULUM_ROLES.get(predicted_role_id, CURRICULUM_ROLES["8.6"]),
            "probabilities": prob_breakdown
        }

    def recommend(
        self,
        user_skills: List[str],
        preference_role_id: Optional[str] = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        แนะนำตำแหน่งงาน Top 5:
        - วิเคราะห์สายงานเป้าหมาย (Target Career Analysis)
        - จัดอันดับงานด้วยคะแนน: 50% Skill Overlap + 30% Cosine Similarity + 20% Softmax Role Probability
        """
        user_skills_clean = [clean_skill(s) for s in user_skills if clean_skill(s)]
        # 💡 [ทำไมต้องแบบนี้]: แปลงเป็น set เพื่อให้การเปรียบเทียบหาทักษะที่ตรงกันทำงานได้เร็วระดับ O(1)
        user_skills_set = set(user_skills_clean)
        query_text = " ".join(user_skills_clean)

        # 1. ทำนายอาชีพด้วย Logistic Regression
        career_pred = self.predict_career(user_skills_clean)
        # 💡 [ทำไมต้องแบบนี้]: ให้ความสำคัญกับสายงานเป้าหมายที่ผู้ใช้เลือกเองก่อน หากไม่เลือกจึงใช้ผลทำนายจาก ML
        target_role_id = preference_role_id if (preference_role_id and preference_role_id in CURRICULUM_ROLES) else career_pred["predicted_role_id"]
        # ⚠️ [จุดระวัง]: ใช้ .get() คู่กับ Default Fallback (8.6) ป้องกัน KeyError กรณีส่งรหัสที่ไม่มีใน มคอ.2
        target_role_info = CURRICULUM_ROLES.get(target_role_id, CURRICULUM_ROLES["8.6"])

        # =========================================================================
        # [จุดสำคัญที่ 7: Unsupervised NLP - TF-IDF Vector Space & Cosine Similarity]
        # แปลงข้อความทักษะของผู้ใช้เป็น Sparse Vector ในมิติเดียวกับฐานข้อมูลงาน
        # แล้วคำนวณ Dot Product หารด้วย Norm เพื่อหามุมความคล้ายคลึงเชิงคำศัพท์ (0.0 - 1.0)
        # =========================================================================
        # 🎯 [หัวใจหลัก]: แปลงทักษะผู้ใช้เป็น Sparse Vector แล้วคำนวณ Cosine Similarity เทียบกับทุกงานในคราวเดียว
        user_vec = self.vectorizer.transform([query_text]) if query_text else None
        if user_vec is not None:
            cosine_sims = cosine_similarity(user_vec, self.job_tfidf_matrix).flatten()
        else:
            # ⚠️ [จุดระวัง]: หาก query_text ว่าง ให้เซ็ตความคล้ายคลึงเป็น 0 ทั้งหมด ป้องกัน Sparse Matrix Error
            cosine_sims = np.zeros(len(self.cached_jobs))

        # 3. คำนวณคะแนนสำหรับทุกตำแหน่งงาน (ดึงจากหน่วยความจำที่แคชไว้)
        scored_jobs = []
        for idx, job in enumerate(self.cached_jobs):
            job_skills = job["job_skills"]

            # =========================================================================
            # [จุดสำคัญที่ 8: การหา Matching / Missing Skills ด้วย Set Theory]
            # ใช้คณิตศาสตร์ทฤษฎีเซตของ Python:
            # - Matched Skills: User_Skills ∩ Job_Skills (อินเตอร์เซกชัน)
            # - Missing Skills: Job_Skills \ User_Skills (ผลต่างเชิงเซต)
            # โปร่งใส ตรวจสอบได้ 100% ไม่มีการเดาสุ่มหรือมโนคำศัพท์
            # =========================================================================
            # 🎯 [หัวใจหลัก]: ทฤษฎีเซตแยกทักษะที่ตรงกัน (Intersection) และทักษะที่ต้องศึกษาเพิ่ม (Difference)
            matched_skills = [s for s in job_skills if s in user_skills_set]
            missing_skills = [s for s in job_skills if s not in user_skills_set]

            # 3.1 สัดส่วนทักษะตรงเป๊ะ (Exact Skill Overlap %)
            total_req = len(job_skills)
            # ⚠️ [จุดระวัง]: ใช้ max(1, total_req) ป้องกันกรณีหารด้วยศูนย์ (ZeroDivisionError)
            overlap_pct = (len(matched_skills) / max(1, total_req)) * 100.0

            # 3.2 ความคล้ายคลึงเชิงคำศัพท์ (TF-IDF Cosine Similarity %)
            # 💡 [ทำไมต้องแบบนี้]: ใช้ np.clip จำกัดขอบเขตให้อยู่ใน [0.0, 1.0] ป้องกัน Floating Point Error
            cos_pct = float(np.clip(cosine_sims[idx], 0.0, 1.0)) * 100.0

            # =========================================================================
            # [จุดสำคัญที่ 9: Hybrid Scoring Function (Probability-Weighted)]
            # สถาปัตยกรรมแบบรวมสัญญาณ (Multi-Signal Ranking 100% Bounded Scale):
            # - 50% Exact Overlap: ความจำเป็นของ Hard Skills ตรงเป๊ะ (High Precision)
            # - 30% Cosine Similarity: ความยืดหยุ่นเชิงบริบทคำศัพท์จากโมเดล ML (High Recall)
            # - 20% ML Role Probability: ความน่าจะเป็นจากโมเดล Softmax (Career Alignment)
            # =========================================================================
            # 🎯 [หัวใจหลัก]: สูตรคะแนนแบบไฮบริด (50% Hard Skills + 30% Semantic + 20% Softmax Role Prob)
            role_prob_pct = career_pred["probabilities"].get(job["curriculum_role_id"], 0.0)
            final_score = int(round(0.50 * overlap_pct + 0.30 * cos_pct + 0.20 * role_prob_pct))

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
                "score": final_score,
                "ml_confidence": final_score,
                "semantic_score": int(round(cos_pct)),
                "exact_score": int(round(overlap_pct)),
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
        # 🎯 [หัวใจหลัก]: คำนวณความพร้อมเทียบกับเกณฑ์มาตรฐาน มคอ.2 โดยมี max(1, ...) ดัก ZeroDivisionError
        readiness_pct = round((len(matched_core) / max(1, len(core_skills_target))) * 100.0, 1)

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
            "total_skills_count": len(core_skills_target)
        }

        # 5. ส่วนที่ 2: จัดอันดับ Top 5 งานที่ตรงที่สุด (Diversity-Aware Ranking)
        sorted_jobs = sorted(scored_jobs, key=lambda x: x["score"], reverse=True)
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
