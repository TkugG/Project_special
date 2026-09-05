"""
train_model.py - Wrapper สำหรับเรียกใช้งาน src/train.py
(รองรับการรันผ่าน run.bat และสคริปต์รุ่นเดิม)
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.train import train_career_model

def train_and_save_model():
    return train_career_model()

if __name__ == "__main__":
    train_career_model()
