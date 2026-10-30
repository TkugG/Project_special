"""
scripts/see_with_your_own_eyes.py
รันไฟล์นี้ด้วยคำสั่ง: py scripts/see_with_your_own_eyes.py
เพื่อดูหลักฐานด้วยตาตัวเองว่า Model ให้ค่าอะไร และ Set Theory ให้ค่าอะไร
"""

import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 1. โหลดโมเดลจริงที่เทรนไว้
model_path = BASE_DIR / "models" / "career_classifier.joblib"
model = joblib.load(model_path)

# 2. โหลดประกาศงานจริงใบแรกจาก data/เก็บข้อมูล.csv
df = pd.read_csv(BASE_DIR / "data" / "เก็บข้อมูล.csv")
real_job = df.iloc[0]

# 3. กำหนดทักษะจำลองของผู้ใช้
user_skills = ["python", "sql", "git", "docker"]
user_skills_str = " ".join(user_skills)

print("=" * 75)
print("👁️ ดูด้วยตาตัวเอง: หลักฐานเชิงประจักษ์ (Empirical Proof)")
print("=" * 75)
print(f"📌 ทักษะที่ผู้ใช้กรอกเข้ามา : {user_skills}")
print(f"📌 ตำแหน่งงานจริงในฐานข้อมูล : {real_job['Title']} ({real_job['Company']})")
print(f"📌 ทักษะที่งานนี้ต้องการจริง  : {real_job['Skills']}")
print("=" * 75)

# =========================================================================
# ด่านที่ 1: ดูผลลัพธ์จริงที่หลุดออกมาจาก Machine Learning Model
# =========================================================================
print("\n[ด่านที่ 1] สิ่งที่ Model (Logistic Regression + Softmax) ส่งออกมาจริง:")
raw_probabilities = model.predict_proba([user_skills_str])[0]
classes = model.named_steps['clf'].classes_

print(f" • ชนิดข้อมูล (Data Type) : {type(raw_probabilities)}")
print(f" • ขนาดข้อมูล (Shape)     : {raw_probabilities.shape} (มีแค่ตัวเลข 8 ตัว!)")
print(" • ค่าตัวเลขจริงที่ Model คำนวณได้:")
for role, prob in zip(classes, raw_probabilities):
    bar = "█" * int(prob * 40)
    print(f"    - {role}: {prob*100:5.2f}% | {bar}")

print("\n❓ ในตัวเลขพวกนี้ มีคำว่า 'html' หรือ 'css' โผล่มาสักคำไหม?")
print("   👉 คำตอบ: ไม่มีเลยแม้แต่คำเดียว! เพราะ Model ส่งคืนแค่ 'เปอร์เซ็นต์ของ 8 อาชีพ'")

# =========================================================================
# ด่านที่ 2: ดูผลลัพธ์จริงที่ได้จากทฤษฎีเซต (Set Theory)
# =========================================================================
print("\n" + "=" * 75)
print("[ด่านที่ 2] สิ่งที่ทฤษฎีเซต (Set Theory) คำนวณออกมา:")
set_user = set(user_skills)
set_job = set([s.strip().lower() for s in str(real_job['Skills']).split(',') if s.strip()])

intersection = set_user.intersection(set_job)  # A ∩ B
difference = set_job.difference(set_user)       # B \\ A (Skill Gap)
match_score = (len(intersection) / len(set_job)) * 100

print(f" • เซตทักษะผู้ใช้ (Set A)        : {set_user}")
print(f" • เซตทักษะของงาน (Set B)        : {set_job}")
print(" -------------------------------------------------------------------------")
print(f" • ทักษะที่มีตรงกัน (A ∩ B)      : {intersection}  --> คิดเป็น Match Score: {match_score:.2f}%")
print(f" • ทักษะที่ยังขาดอยู่ (B \\ A)    : {difference}  --> นี่คือ Skill Gap!")
print("=" * 75)
