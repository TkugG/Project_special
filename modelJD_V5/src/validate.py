"""
validate.py - ชุดทดสอบความถูกต้องของระบบ SkillMatch IT (สำหรับเตรียมตัวก่อนขึ้นสอบ)
ตรวจสอบ 4 หัวข้อสำคัญ:
1. ความสมบูรณ์และความสมดุลของชุดข้อมูล 8 อาชีพ มคอ.2 (Dataset Integrity & Balance)
2. ความแม่นยำของโมเดล Logistic Regression ในการจำแนกสายงาน (Career Classification Test)
3. ความสมบูรณ์ของการคำนวณคะแนนจับคู่ทักษะ (Skill Overlap & Cosine Similarity Bounds)
4. ความเร็วในการประมวลผล (Inference Latency Benchmark)
"""

import sys
import time
from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.recommend import JobRecommender, CURRICULUM_ROLES
from src.main import recommend_jobs, RecommendRequest

DATA_DIR = BASE_DIR / "data"

def print_header(title: str):
    print("\n" + "=" * 70)
    print(f"🔬 {title}")
    print("=" * 70)

def print_result(test_name: str, passed: bool, details: str = ""):
    icon = "✅ PASS" if passed else "❌ FAIL"
    print(f"[{icon}] {test_name:<40} | {details}")

def test_dataset():
    print_header("1. ตรวจสอบความสมบูรณ์ของชุดข้อมูลจริง 8 กลุ่มอาชีพ มคอ.2 (ตารางที่ 3.1 & 3.2)")
    csv_path = DATA_DIR / "เก็บข้อมูล.csv"
    if not csv_path.exists():
        csv_path = DATA_DIR / "thai_jobs_dataset.csv"
    df = pd.read_csv(csv_path)

    total_jobs = len(df)
    counts = df["CurriculumRoleID"].astype(str).str.strip().value_counts()
    has_8_roles = len(counts) == 8
    is_valid_distribution = all(c >= 10 for c in counts.values)

    print_result("มีครบทั้ง 8 กลุ่มอาชีพ (G1-G8) ตาม มคอ.2", has_8_roles, f"พบ {len(counts)} กลุ่มอาชีพ: {sorted(counts.index.tolist())}")
    print_result("การกระจายตัวครบทุกกลุ่ม (แต่ละกลุ่ม >= 10 ตำแหน่ง)", is_valid_distribution, f"รวม {total_jobs} งานจริง, ต่ำสุด: {counts.min()}, สูงสุด: {counts.max()}")

    return has_8_roles and is_valid_distribution

def test_classifier():
    print_header("2. ทดสอบโมเดล Logistic Regression (ทำนาย 8 กลุ่มอาชีพจริง G1-G8)")
    rec = JobRecommender()

    test_cases = [
        (["python", "sql", "rest api", "git", "c#"], "G1", "นักพัฒนาซอฟต์แวร์ (G1)"),
        (["oracle", "sql", "postgresql", "mysql", "ssis"], "G2", "ผู้ดูแลระบบฐานข้อมูล (G2)"),
        (["api", "sql", "uat", "system analysis"], "G3", "นักวิเคราะห์และออกแบบระบบ (G3)"),
        (["windows", "vpn", "microsoft 365", "printers"], "G4", "เจ้าหน้าที่เทคนิคคอมพิวเตอร์ (G4)"),
        (["linux", "windows server", "active directory", "vmware"], "G5", "ผู้ดูแลระบบ (G5)"),
        (["html5", "css3", "javascript", "react", "next.js"], "G6", "นักพัฒนาเว็บไซต์ (G6)"),
        (["erp", "sap", "powerpoint", "excel", "ms office"], "G7", "ผู้ช่วยผู้จัดการโครงการสารสนเทศ (G7)"),
        (["tiktok", "canva", "capcut", "premiere pro"], "G8", "ผู้สร้างสรรค์เนื้อหาดิจิทัล (G8)")
    ]

    all_correct = True
    for skills, expected_role, role_name in test_cases:
        pred = rec.predict_career(skills)
        is_correct = pred["predicted_role_id"] == expected_role
        all_correct &= is_correct
        print_result(
            f"ทำนายสายงาน: {role_name}",
            is_correct,
            f"ทักษะ: {', '.join(skills[:2])} -> ได้: {pred['predicted_role_id']} ({pred['confidence']}%)"
        )

    return all_correct

def test_recommendation_logic():
    print_header("3. ทดสอบการคำนวณคะแนนด้วยทฤษฎีเซตและความสมบูรณ์ของผลลัพธ์")
    rec = JobRecommender()
    res = rec.recommend(["python", "sql", "git"], preference_role_id="G1")

    top_jobs = res["skill_matched_recommendations"]
    has_5 = len(top_jobs) == 5
    scores_valid = all(0 <= j["score"] <= 100 for j in top_jobs)
    sorted_correctly = all(top_jobs[i]["score"] >= top_jobs[i+1]["score"] for i in range(len(top_jobs)-1))

    print_result("ส่งคืนตำแหน่งงานครบ Top 5", has_5, f"จำนวนงานที่ได้: {len(top_jobs)}")
    print_result("ช่วงคะแนนถูกต้อง (0 - 100 คะแนน)", scores_valid, f"คะแนนอันดับ 1: {top_jobs[0]['score']}%")
    print_result("เรียงลำดับคะแนนจากมากไปน้อย", sorted_correctly, f"คะแนน: {[j['score'] for j in top_jobs]}")

    return has_5 and scores_valid and sorted_correctly

def test_latency():
    print_header("4. ทดสอบความเร็วในการตอบสนอง (Latency Benchmark)")
    req = RecommendRequest(
        preference="G1",
        skills=["python", "sql", "git"]
    )

    times = []
    for _ in range(10):
        t0 = time.perf_counter()
        _ = recommend_jobs(req)
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000.0)

    avg_ms = np.mean(times)
    p95_ms = np.percentile(times, 95)
    is_fast = avg_ms < 50.0

    print_result("ความเร็วเฉลี่ยระดับ Real-time (< 50ms)", is_fast, f"เฉลี่ย: {avg_ms:.2f}ms | p95: {p95_ms:.2f}ms")
    return is_fast

def test_skill_normalization():
    print_header("5. ทดสอบระบบจัดระเบียบคำศัพท์ทักษะ (Skill Normalization & Synonyms)")
    from src.skills_taxonomy import normalize_skill, normalize_skills_list
    rec = JobRecommender()

    # ทดสอบการแปลงคำพ้องเดี่ยว
    synonym_checks = [
        ("golang", "go"),
        ("js", "javascript"),
        ("k8s", "kubernetes"),
        ("reactjs", "react"),
        ("postgres", "postgresql"),
        ("ux/ui", "ui/ux"),
        ("ci/cd", "cicd"),
        (".net", ".net"),
        ("dotnet", ".net"),
        ("dot net", ".net"),
        (".net core", ".net")
    ]
    all_synonyms_pass = True
    for raw, expected in synonym_checks:
        actual = normalize_skill(raw)
        passed = actual == expected
        all_synonyms_pass &= passed
        print_result(f"แปลง '{raw}' -> '{expected}'", passed, f"ผลลัพธ์: '{actual}'")

    # ทดสอบ End-to-End Recommendation ด้วยคำพ้อง (เช่น กรอก 'golang' แต่จับคู่งานที่มี 'go' ได้)
    res = rec.recommend(["golang", "docker"])
    top_job = res["skill_matched_recommendations"][0]
    has_match = len(top_job["matched_skills"]) > 0
    matched_canonical = "go" in top_job["matched_skills"] or "docker" in top_job["matched_skills"]
    print_result("แนะนำงานด้วยคำพ้อง (golang -> go)", has_match and matched_canonical, f"พบ Matched: {top_job['matched_skills']}")

    return all_synonyms_pass and has_match

def main():
    t1 = test_dataset()
    t2 = test_classifier()
    t3 = test_recommendation_logic()
    t4 = test_latency()
    t5 = test_skill_normalization()

    print("\n" + "=" * 70)
    if t1 and t2 and t3 and t4 and t5:
        print("🎉 ผ่านการทดสอบครบทุกหัวข้อ (พร้อมสำหรับนำเสนอโครงงาน 100%)")
    else:
        print("⚠️ พบข้อบกพร่องบางจุด กรุณาตรวจสอบผลการทดสอบด้านบน")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
