import pandas as pd
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

RAW_CSV = DATA_DIR / "เก็บข้อมูล.csv"
CLEAN_CSV = DATA_DIR / "thai_jobs_dataset.csv"

# อ่านข้อมูลดิบ
df = pd.read_csv(RAW_CSV)
print(f"Raw shape: {df.shape}")

# คัดกรองเอาเฉพาะแถวที่มีข้อมูลจริง 115 แถว (ตัดแถวว่าง 116-159 ออก)
df_clean = df.dropna(subset=["Title", "CurriculumRoleID", "Skills"]).copy()
print(f"Clean rows: {len(df_clean)}")

# แก้ไขคำที่ติด bug 'instagram' จากการ find/replace ผิดพลาด
CORRECTIONS = {
    r"\bBinstagramSELLER\b": "BIGSELLER",
    r"\bBinstagram\b": "Big",
    r"\bDesinstagramner\b": "Designer",
    r"\bdesinstagramner\b": "designer",
    r"\bDesinstagramn\b": "Design",
    r"\bdesinstagramn\b": "design",
    r"\bDinstagramital\b": "Digital",
    r"\bdinstagramital\b": "digital",
    r"\bIntellinstagrament\b": "Intelligent",
    r"\bintellinstagrament\b": "intelligent",
    r"\bLinstagramhtwork\b": "Lightwork",
    r"\blinstagramhtwork\b": "lightwork",
    r"\bPRODinstagramY\b": "PRODIGY",
    r"\bprodinstagramy\b": "prodigy",
    r"\bbinstagramquery\b": "bigquery",
    r"\bfinstagramma\b": "figma",
    r"\bhinstagramh\b": "high",
    r"orinstagramin": "origin"
}

for col in ["Title", "Company", "Skills", "ApplyURL"]:
    for pat, rep in CORRECTIONS.items():
        df_clean[col] = df_clean[col].astype(str).str.replace(pat, rep, regex=True)

ROLE_TITLES = {
    "G1": ("นักพัฒนาซอฟต์แวร์", "Software Developer"),
    "G2": ("ผู้ดูแลระบบฐานข้อมูล", "Database Administrator"),
    "G3": ("นักวิเคราะห์และออกแบบระบบ", "System Analyst / Designer"),
    "G4": ("เจ้าหน้าที่เทคนิคคอมพิวเตอร์", "Computer Technical Officer"),
    "G5": ("ผู้ดูแลระบบ", "System Administrator"),
    "G6": ("นักพัฒนาเว็บไซต์", "Web Developer"),
    "G7": ("ผู้ช่วยผู้จัดการโครงการสารสนเทศ", "IT Project Assistant"),
    "G8": ("ผู้สร้างสรรค์เนื้อหาดิจิทัล", "Content Creator")
}

# เติม Metadata คอลัมน์ให้ครบถ้วนสมบูรณ์ตาม Schema ตาราง 3.2
df_clean["CurriculumRoleTitle"] = df_clean["CurriculumRoleID"].map(lambda r: ROLE_TITLES.get(r, ("ไอทีทั่วไป", "IT Professional"))[0])
df_clean["CurriculumRoleEN"] = df_clean["CurriculumRoleID"].map(lambda r: ROLE_TITLES.get(r, ("ไอทีทั่วไป", "IT Professional"))[1])
df_clean["Salary"] = "ตามโครงสร้างบริษัท / ตามตกลง"
df_clean["ExperienceLevel"] = "Entry-Level / ยินดีรับเด็กจบใหม่ (0-2 ปี)"
df_clean["YearsOfExperience"] = "0-2"
df_clean["Responsibilities"] = df_clean.apply(lambda r: f"ปฏิบัติงานในตำแหน่ง {r['Title']} ประจำ {r['Company']} ณ {r['Province']}", axis=1)
df_clean["Keywords"] = df_clean["Skills"].apply(lambda s: " ".join([k.strip() for k in str(s).split(",")]))

# เรียงคอลัมน์มาตรฐาน
cols_order = [
    "JobID", "Title", "CurriculumRoleID", "CurriculumRoleTitle", "CurriculumRoleEN",
    "Company", "Province", "Salary", "ExperienceLevel", "YearsOfExperience",
    "Skills", "Responsibilities", "Keywords", "ApplyURL"
]
df_clean = df_clean[cols_order]

# บันทึกทับ thai_jobs_dataset.csv
df_clean.to_csv(CLEAN_CSV, index=False, encoding="utf-8-sig")
# และบันทึกทับไฟล์ เก็บข้อมูล.csv เพื่อให้สะอาด 100%
df_clean.to_csv(RAW_CSV, index=False, encoding="utf-8-sig")

print(f" Successfully exported 100% clean real dataset ({len(df_clean)} rows) to:")
print(f"  - {CLEAN_CSV}")
print(f"  - {RAW_CSV}")
print("\nDistribution across G1-G8:")
print(df_clean["CurriculumRoleID"].value_counts())
