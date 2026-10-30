"""
check_progress.py - สคริปต์ตรวจความคืบหน้าและควบคุมคุณภาพข้อมูล (QC Progress Tracker)
สำหรับชุดข้อมูลจริง 160 ตำแหน่งงาน (data/เก็บข้อมูล.csv)
"""

import sys
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "เก็บข้อมูล.csv"

# เป้าหมาย 8 กลุ่มอาชีพ มรภ.นครปฐม (กลุ่มละ 20 งาน = 160 งาน)
TARGET_ROLES = [f"G{i}" for i in range(1, 9)]
TARGET_PER_ROLE = 20
TOTAL_TARGET = len(TARGET_ROLES) * TARGET_PER_ROLE

def main():
    print("=" * 65)
    print("📊 รายงานความคืบหน้าและการตรวจสอบคุณภาพข้อมูล (160 ตำแหน่งงาน)")
    print(f"📁 ไฟล์ข้อมูล: {CSV_PATH.relative_to(BASE_DIR)}")
    print("=" * 65)

    if not CSV_PATH.exists():
        print(f"[❌ ERROR] ไม่พบไฟล์ {CSV_PATH}")
        sys.exit(1)

    df = pd.read_csv(CSV_PATH)
    
    # 1. กรองแถวที่มีข้อมูลจริง (ไม่ใช่แถวว่าง template)
    valid_mask = df["Title"].notna() & (df["Title"].str.strip() != "") & (df["Title"].str.lower() != "title")
    df_valid = df[valid_mask].copy()
    
    total_valid = len(df_valid)
    progress_pct = (total_valid / TOTAL_TARGET) * 100
    
    # Visual Progress Bar
    bar_len = 30
    filled_len = int(round(bar_len * total_valid / TOTAL_TARGET))
    bar = "█" * filled_len + "░" * (bar_len - filled_len)
    
    print(f"\nความคืบหน้ารวม: [{bar}] {total_valid}/{TOTAL_TARGET} งาน ({progress_pct:.1f}%)\n")
    print(f"{'กลุ่มอาชีพ':<12} | {'จำนวนที่เก็บได้':<15} | {'เป้าหมาย':<10} | {'ขาดอีก':<10} | {'สถานะ'}")
    print("-" * 65)
    
    role_counts = df_valid["CurriculumRoleID"].value_counts().to_dict()
    
    issues = []
    seen_urls = set()
    
    for role in TARGET_ROLES:
        count = role_counts.get(role, 0)
        remaining = max(0, TARGET_PER_ROLE - count)
        if count >= TARGET_PER_ROLE:
            status = "✅ ครบแล้ว"
        elif count > 0:
            status = f"⏳ กำลังเก็บ ({count}/{TARGET_PER_ROLE})"
        else:
            status = "❌ ยังไม่ได้เริ่ม"
        print(f"{role:<12} | {count:<15} | {TARGET_PER_ROLE:<10} | {remaining:<10} | {status}")
    
    print("-" * 65)
    
    # 2. ตรวจสอบ Data Quality Issues
    print("\n🔍 การตรวจสอบคุณภาพของข้อมูล (Quality Control):")
    for idx, row in df_valid.iterrows():
        row_num = idx + 2  # CSV line number
        job_id = str(row.get("JobID", f"Row-{row_num}"))
        role_id = str(row.get("CurriculumRoleID", "")).strip()
        skills = str(row.get("Skills", "")).strip()
        url = str(row.get("ApplyURL", "")).strip()
        
        # ตรวจสอบ Role ID
        if role_id not in TARGET_ROLES:
            issues.append(f"แถวที่ {row_num} ({job_id}): รหัสอาชีพ '{role_id}' ไม่อยู่ในกลุ่ม G1–G8")
        
        # ตรวจสอบ Skills ว่าง หรือสั้นผิดปกติ
        if not skills or skills.lower() == "nan" or len(skills.split(",")) < 2:
            issues.append(f"แถวที่ {row_num} ({job_id}): ช่อง Skills ว่าง หรือมีทักษะน้อยกว่า 2 ทักษะ")
        
        # ตรวจสอบ URL ซ้ำ
        if url and url.lower() != "nan":
            clean_url = url.split("?")[0].strip()
            if clean_url in seen_urls:
                issues.append(f"แถวที่ {row_num} ({job_id}): พบ URL ประกาศงานซ้ำกับแถวก่อนหน้า")
            else:
                seen_urls.add(clean_url)

            # ตรวจสอบการเผลอใส่เซมิโคลอนแทนคอมม่า
            if ";" in skills:
                issues.append(f"แถวที่ {row_num} ({job_id}): พบเครื่องหมาย ';' ในช่อง Skills ควรเปลี่ยนเป็นคอมม่า ','")

            # ตรวจสอบการเผลอใส่วงเล็บติดมา เช่น swift (ios)
            if "(" in skills or ")" in skills:
                issues.append(f"แถวที่ {row_num} ({job_id}): มีวงเล็บ () ในช่อง Skills ควรแยกเป็นคำเดี่ยว")

    if not issues:
        print("  ✅ ไม่พบข้อผิดพลาดด้านฟอร์แมตในแถวที่มีข้อมูล (ข้อมูลเรียบร้อยดี)")
    else:
        print(f"  ⚠️ พบจุดที่ต้องแก้ไข {len(issues)} จุด:")
        for iss in issues[:10]:
            print(f"     - {iss}")
        if len(issues) > 10:
            print(f"     ...และอีก {len(issues) - 10} รายการ")

    print("\n" + "=" * 65)
    if total_valid >= TOTAL_TARGET and not issues:
        print("🎉 ข้อมูลครบ 160 งานและสมบูรณ์แล้ว! สามารถรันสคริปต์สกัดสกิลและเทรนโมเดลได้ทันที")
    else:
        print(f"👉 สรุปงานต่อไป: ให้เพื่อนช่วยกันเก็บงานอีก {TOTAL_TARGET - total_valid} งาน ให้ครบ G1-G8")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    main()
