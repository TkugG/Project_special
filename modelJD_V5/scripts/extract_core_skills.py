"""
extract_core_skills.py - สคริปต์สกัด Core Skills แบบ Data-Driven จากประกาศงานจริง
คำนวณ Top 8–10 ทักษะเฉพาะทางที่พบบ่อยที่สุด โดยตัดทักษะสามัญทั่วไป (Generic Noise)
เพื่อนำไปเป็น Core Skills ประจำกลุ่มอาชีพ G1–G8 ในระบบ
"""

import sys
from pathlib import Path
from collections import Counter
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.skills_taxonomy import parse_and_normalize_skills

CSV_PATH = BASE_DIR / "data" / "เก็บข้อมูล.csv"

# ทักษะสามัญทั่วไป (Generic / Soft / Tooling Skills) ที่มักโผล่ปนทุกสายงาน
# ต้องตัดออกเพื่อไม่ให้กลืนเอกลักษณ์เฉพาะด้าน (Role Demarcation)
COMMON_STOPWORDS = {
    "git", "github", "gitlab", "communication", "english", "teamwork", 
    "problem solving", "ms office", "microsoft office", "office 365", 
    "excel", "microsoft excel", "word", "powerpoint", "ai tools", 
    "ai agents", "reporting", "coordination", "interpersonal", "time management"
}

def extract_role_skills(df: pd.DataFrame, top_n: int = 8):
    valid_mask = df["Title"].notna() & (df["Title"].str.strip() != "") & (df["Title"].str.lower() != "title")
    df_valid = df[valid_mask].copy()

    groups = df_valid.groupby("CurriculumRoleID")
    role_skills_dict = {}

    print("=" * 70)
    print("🔬 ผลการสกัด Top Hard Skills แบบ Data-Driven ประจำแต่ละกลุ่มอาชีพ")
    print(f"📁 แหล่งข้อมูล: {CSV_PATH.name} (จากข้อมูลจริงที่ผ่านการคัดกรอง)")
    print("=" * 70)

    for role_id, group in sorted(groups):
        total_jobs_in_group = len(group)
        skill_counter = Counter()

        for _, row in group.iterrows():
            raw_skills = str(row.get("Skills", ""))
            norm_skills = parse_and_normalize_skills(raw_skills)
            # กรอง stopwords และนับ 1 ครั้งต่องาน (Document Frequency)
            unique_job_skills = {s for s in norm_skills if s and s not in COMMON_STOPWORDS}
            skill_counter.update(unique_job_skills)

        top_skills = [skill for skill, count in skill_counter.most_common(top_n)]
        role_skills_dict[role_id] = top_skills

        print(f"\n📌 กลุ่ม: {role_id} (จำนวนตัวอย่าง: {total_jobs_in_group} ตำแหน่งงาน)")
        print(f"   Top {top_n} Core Skills:")
        for idx, (skill, count) in enumerate(skill_counter.most_common(top_n), 1):
            pct = (count / total_jobs_in_group) * 100
            print(f"     {idx}. {skill:<20} ปรากฏ {count:>2}/{total_jobs_in_group} งาน ({pct:5.1f}%)")

    print("\n" + "=" * 70)
    print("💻 โครงสร้างโค้ด Core Skills ที่สกัดได้ (พร้อมนำไปใส่ใน CURRICULUM_ROLES):")
    print("=" * 70)
    print("EXTRACTED_CORE_SKILLS = {")
    for r_id, skills in role_skills_dict.items():
        print(f'    "{r_id}": {skills},')
    print("}\n")

    return role_skills_dict

if __name__ == "__main__":
    if not CSV_PATH.exists():
        print(f"[❌ ERROR] ไม่พบไฟล์ {CSV_PATH}")
        sys.exit(1)

    df_data = pd.read_csv(CSV_PATH)
    extract_role_skills(df_data, top_n=8)
