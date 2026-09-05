"""
train.py - การฝึกสอนโมเดลจำแนก 8 กลุ่มอาชีพ มคอ.2 (Career Classification)
ใช้เทคนิค: TF-IDF Vectorizer + Multi-Class Logistic Regression
ชุดข้อมูล: ตำแหน่งงานจริงในประเทศไทย 253 งาน (8 กลุ่มอาชีพตามมาตรฐานหลักสูตร มคอ.2 สาขา IT)
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# นิยาม 8 กลุ่มอาชีพตามมาตรฐานหลักสูตร มคอ.2 สาขา IT
ROLE_NAMES = {
    "8.1": "เจ้าหน้าที่คอมพิวเตอร์ (IT Support)",
    "8.2": "ผู้ดูแลระบบเครือข่าย (Network Admin)",
    "8.3": "นักพัฒนาและออกแบบสื่อผสม (Multimedia)",
    "8.4": "นักจัดการโครงการสารสนเทศ (Project Manager)",
    "8.5": "นักวิเคราะห์และออกแบบระบบ (System Analyst)",
    "8.6": "นักพัฒนาซอฟต์แวร์ (Software Developer)",
    "8.7": "นักออกแบบและพัฒนาเว็บไซต์ (Web Developer)",
    "8.8": "ผู้เชี่ยวชาญไอทีเฉพาะด้าน (AI/Data/Cyber)"
}

def clean_text(text: str) -> str:
    """ทำความสะอาดข้อความและตัดสัญลักษณ์พิเศษออก แปลงเป็นตัวพิมพ์เล็ก"""
    if not text or not isinstance(text, str):
        return ""
    return text.lower().replace(";", " ").replace(",", " ").replace("/", " ").strip()

def train_career_model():
    print("=" * 75)
    print("🚀 เริ่มต้นฝึกสอนโมเดลจำแนกกลุ่มอาชีพไอที (TQF 8-Class Career Classifier)")
    print("=" * 75)

    # 1. โหลดข้อมูลตำแหน่งงานไทย
    csv_path = DATA_DIR / "thai_jobs_dataset.csv"
    if not csv_path.exists():
        csv_path = DATA_DIR / "job_dataset.csv"

    print(f"⏳ โหลดชุดข้อมูลจาก: {csv_path.name}")
    df = pd.read_csv(csv_path)

    # =========================================================================
    # [จุดสำคัญที่ 1: การกำจัด Data Leakage]
    # ปัญหาเดิม: ถ้าเราใส่ 'Title' (ชื่อตำแหน่งงาน เช่น Network Engineer) เข้าไปด้วย
    # โมเดลจะแค่อ่านชื่อตำแหน่งแล้วตอบได้ทันที 100% ซึ่งเป็นการ "โกงข้อสอบ"
    # สิ่งที่ถูก: ตัด Title ทิ้ง ให้โมเดลเห็นเฉพาะกลุ่มคำทักษะ (Skills) ล้วนๆ
    # เพื่อจำลองสถานการณ์จริงที่ผู้ใช้กรอกเฉพาะทักษะที่ตัวเองทำเป็นเข้ามา
    # =========================================================================
    skills = df["Skills"].fillna("").apply(clean_text)
    X = skills
    y = df["CurriculumRoleID"].astype(str).str.strip()

    print(f"✅ ข้อมูลทั้งหมด: {len(df)} รายการ แบ่งตาม 8 กลุ่มอาชีพอย่างสมดุล:")
    for role_id, count in y.value_counts().sort_index().items():
        print(f"   • {role_id} - {ROLE_NAMES.get(role_id, 'Other')}: {count} ตำแหน่ง")

    # =========================================================================
    # [จุดสำคัญที่ 2: Pipeline, Regex พิเศษ และ L2 Regularization]
    # 2.1 token_pattern: ปกติ scikit-learn จะตัดเครื่องหมายวรรคตอนทิ้ง
    #     ทำให้คำว่า c++, c#, .net, node.js หายไปหมด เราจึงต้องเขียน regex พิเศษ
    #     r'(?u)[a-zA-Z0-9_+#.-]+' เพื่อรักษาชื่อภาษาและเทคโนโลยีสำคัญไว้
    # 2.2 LogisticRegression C=0.3: ค่า C คือส่วนกลับของ L2 Regularization (1/lambda)
    #     การลด C จาก 1.0 เหลือ 0.3 เป็นการ "ลงโทษค่าน้ำหนักที่สูงเกินไป" ป้องกัน Overfitting
    #     บีบให้โมเดลมองภาพรวมของทักษะ ไม่ยึดติดกับคำคำเดียว
    # =========================================================================
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            token_pattern=r'(?u)[a-zA-Z0-9_+#.-]+',
            ngram_range=(1, 1),   # ใช้คำเดี่ยว (Unigram) เพื่อให้เห็นการทับซ้อนของทักษะจริง เช่น cloud, security, html
            max_features=1000
        )),
        ('clf', LogisticRegression(
            max_iter=1000,
            random_state=42,
            C=0.3  # ปรับ Regularization C=0.3 เพื่อความสมจริงและป้องกันท่องจำ
        ))
    ])

    # =========================================================================
    # [จุดสำคัญที่ 3: การประเมินผลด้วย 5-Fold Stratified Cross-Validation]
    # ทำไมต้อง Stratified? -> เพื่อให้ทั้ง 5 รอบ มีสัดส่วนของทั้ง 8 อาชีพเท่ากันเป๊ะ
    # ทำไมต้องใช้ Pipeline ด้านใน? -> เพื่อป้องกัน Data Leakage ระหว่างเทรนกับเทสต์
    # (คำศัพท์ TF-IDF จะถูก Fit เฉพาะในรอบ Train เท่านั้น Test ไม่มีทางรั่วไหล)
    # =========================================================================
    print("\n⏳ กำลังทดสอบด้วย 5-Fold Stratified Cross-Validation...")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    accuracies = []
    precisions = []
    recalls = []
    f1s = []

    # เมทริกซ์เก็บผลการทำนายรวมเพื่อสร้าง Confusion Matrix
    y_true_all = []
    y_pred_all = []

    for fold, (train_idx, test_idx) in enumerate(skf.split(X, y), 1):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        accuracies.append(accuracy_score(y_test, y_pred))
        precisions.append(precision_score(y_test, y_pred, average='macro', zero_division=0))
        recalls.append(recall_score(y_test, y_pred, average='macro', zero_division=0))
        f1s.append(f1_score(y_test, y_pred, average='macro', zero_division=0))

        y_true_all.extend(y_test)
        y_pred_all.extend(y_pred)

    print("=" * 75)
    print("📊 ผลการทดสอบ 5-Fold Cross-Validation (สำหรับเขียนบทที่ 4):")
    print("=" * 75)
    print(f"  • Accuracy (ความแม่นยำรวม)       : {np.mean(accuracies) * 100:.2f}% (+/- {np.std(accuracies) * 100:.2f}%)")
    print(f"  • Macro Precision (ความเที่ยงตรง): {np.mean(precisions) * 100:.2f}%")
    print(f"  • Macro Recall (ความครอบคลุม)    : {np.mean(recalls) * 100:.2f}%")
    print(f"  • Macro F1-Score (คะแนนเฉลี่ย F1): {np.mean(f1s) * 100:.2f}%")
    print("=" * 75)

    # 4. แสดง Confusion Matrix (ตารางแสดงจุดสับสนของโมเดล)
    roles_order = sorted(list(ROLE_NAMES.keys()))
    cm = confusion_matrix(y_true_all, y_pred_all, labels=roles_order)
    
    print("\n📋 CONFUSION MATRIX (ตารางเปรียบเทียบ ค่าจริง vs ค่าที่โมเดลทำนาย):")
    print("  แนวตั้ง = ค่าจริง (Actual) | แนวนอน = ค่าทำนาย (Predicted)")
    header = "       " + " ".join([f"{r:>5}" for r in roles_order])
    print(header)
    print("  " + "-" * (len(header) + 2))
    for idx, row in enumerate(cm):
        role_label = roles_order[idx]
        row_str = " ".join([f"{val:>5}" for val in row])
        print(f"  {role_label:>4} | {row_str}")
    print()

    # 5. เทรนโมเดลขั้นสุดท้ายบนข้อมูลทั้งหมด 100% แล้วบันทึกไฟล์
    print("⏳ กำลังเทรนโมเดลรอบสุดท้ายบนข้อมูลตำแหน่งงานทั้งหมด...")
    pipeline.fit(X, y)

    # =========================================================================
    # [จุดสำคัญที่ 4: Explainable AI (XAI) และ Feature Importance]
    # Logistic Regression เป็นโมเดลประเภท "White-box" (เปิดดูข้างในได้)
    # เราสามารถดึงค่าสัมประสิทธิ์ (clf.coef_) ของแต่ละอาชีพออกมาดูได้
    # ว่าโมเดลให้น้ำหนักสูงสุดกับคำไหนบ้าง ซึ่งพิสูจน์ให้อาจารย์เห็นว่า
    # โมเดลตัดสินใจจากคำศัพท์ทักษะทางเทคนิคจริง ไม่ได้จำคำขยะหรือ noise
    # =========================================================================
    print("\n🔍 ตัวอย่างคีย์เวิร์ดสำคัญที่โมเดลเรียนรู้ได้ในแต่ละอาชีพ:")
    vectorizer = pipeline.named_steps['tfidf']
    clf = pipeline.named_steps['clf']
    feature_names = np.array(vectorizer.get_feature_names_out())

    for i, role_label in enumerate(clf.classes_):
        top_indices = np.argsort(clf.coef_[i])[-4:][::-1]
        top_words = feature_names[top_indices]
        print(f"  • {role_label} ({ROLE_NAMES.get(role_label, '')[:20]}): {', '.join(top_words)}")

    # 7. บันทึกไฟล์โมเดล
    MODEL_FILE = MODELS_DIR / "career_classifier.joblib"
    joblib.dump(pipeline, MODEL_FILE)
    print(f"\n✅ บันทึกโมเดลเรียบร้อยที่: {MODEL_FILE}")
    print("=" * 75)

    return pipeline

if __name__ == "__main__":
    train_career_model()
