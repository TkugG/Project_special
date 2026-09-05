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
    print_header("1. ตรวจสอบความสมดุลของชุดข้อมูล 8 อาชีพ มคอ.2")
    csv_path = DATA_DIR / "thai_jobs_dataset.csv"
    if not csv_path.exists():
        csv_path = DATA_DIR / "job_dataset.csv"
    df = pd.read_csv(csv_path)

    total_jobs = len(df)
    counts = df["CurriculumRoleID"].astype(str).str.strip().value_counts()
    has_8_roles = len(counts) == 8
    is_balanced = all(c >= 25 for c in counts.values)

    print_result("มีครบทั้ง 8 กลุ่มอาชีพตาม มคอ.2", has_8_roles, f"พบ {len(counts)} กลุ่มอาชีพ")
    print_result("การกระจายตัวสมดุล (แต่ละกลุ่ม >= 25 งาน)", is_balanced, f"รวม {total_jobs} งาน, ต่ำสุด: {counts.min()}, สูงสุด: {counts.max()}")

    return has_8_roles and is_balanced

def test_classifier():
    print_header("2. ทดสอบโมเดล Logistic Regression (ทำนาย 8 กลุ่มอาชีพ)")
    rec = JobRecommender()

    test_cases = [
        (["python", "fastapi", "docker", "sql"], "8.6", "นักพัฒนาซอฟต์แวร์"),
        (["cisco", "routing", "switching", "firewall"], "8.2", "ผู้ดูแลระบบเครือข่าย"),
        (["figma", "ui/ux", "adobe xd", "photoshop"], "8.3", "สื่อผสม / UI-UX"),
        (["jira", "scrum", "agile", "project management"], "8.4", "จัดการโครงการ"),
        (["uml", "use case", "er diagram", "system analysis"], "8.5", "วิเคราะห์ระบบ"),
        (["html5", "css3", "wordpress", "responsive web design"], "8.7", "พัฒนาเว็บไซต์"),
        (["machine learning", "deep learning", "pytorch", "nlp"], "8.8", "ผู้เชี่ยวชาญเฉพาะด้าน (AI)"),
        (["troubleshooting", "hardware", "helpdesk", "windows"], "8.1", "เจ้าหน้าที่คอมพิวเตอร์")
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
    print_header("3. ทดสอบการคำนวณคะแนนและความสมบูรณ์ของผลลัพธ์")
    rec = JobRecommender()
    res = rec.recommend(["python", "fastapi", "docker", "sql"], preference_role_id="8.6")

    top_jobs = res["skill_matched_recommendations"]
    has_5 = len(top_jobs) == 5
    scores_valid = all(0 <= j["score"] <= 100 for j in top_jobs)
    sorted_correctly = all(top_jobs[i]["score"] >= top_jobs[i+1]["score"] for i in range(len(top_jobs)-1))

    print_result("ส่งคืนตำแหน่งงานครบ Top 5", has_5, f"จำนวนงานที่ได้: {len(top_jobs)}")
    print_result("ช่วงคะแนนถูกต้อง (0 - 100 คะแนน)", scores_valid, f"คะแนนอันดับ 1: {top_jobs[0]['score']}")
    print_result("เรียงลำดับคะแนนจากมากไปน้อย", sorted_correctly, f"คะแนน: {[j['score'] for j in top_jobs]}")

    return has_5 and scores_valid and sorted_correctly

def test_latency():
    print_header("4. ทดสอบความเร็วในการตอบสนอง (Latency Benchmark)")
    req = RecommendRequest(
        preference="8.6",
        skills=["python", "fastapi", "docker", "sql", "git"]
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

def main():
    t1 = test_dataset()
    t2 = test_classifier()
    t3 = test_recommendation_logic()
    t4 = test_latency()

    print("\n" + "=" * 70)
    if t1 and t2 and t3 and t4:
        print("🎉 ผ่านการทดสอบครบทุกหัวข้อ (พร้อมสำหรับนำเสนอโครงงาน 100%)")
    else:
        print("⚠️ พบข้อบกพร่องบางจุด กรุณาตรวจสอบผลการทดสอบด้านบน")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
