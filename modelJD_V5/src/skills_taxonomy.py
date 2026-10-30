"""
skills_taxonomy.py - ระบบจัดระเบียบคำศัพท์ทักษะไอทีและพจนานุกรมคำพ้อง (Canonical Skill Taxonomy)
แก้ปัญหา Synonymy Problem ในระบบ Information Retrieval & Recommendation
ตัวอย่าง:
  - golang -> go
  - js / javascript -> javascript
  - k8s -> kubernetes
  - reactjs / react.js -> react
  - postgres / postgresql -> postgresql
  - ux/ui / user experience -> ui/ux
"""

import re
from typing import List, Dict, Set

# =========================================================================
# 1. พจนานุกรมจับคู่คำพ้องและตัวย่อเข้าสู่ "คำมาตรฐาน" (Canonical Mapping)
# ทุกคำจะถูก Normalize เป็นตัวพิมพ์เล็กและตัดอักขระพิเศษออกก่อนเทียบ
# =========================================================================
SKILL_SYNONYMS: Dict[str, str] = {
    # --- ภาษาโปรแกรมมิ่ง (Programming Languages) ---
    "golang": "go",
    "go lang": "go",
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "python3": "python",
    "c sharp": "c#",
    "csharp": "c#",
    "c#.net": "c#",
    "c++": "c++",
    "cpp": "c++",
    "c plus plus": "c++",
    "net": ".net",
    ".net": ".net",
    "dot net": ".net",
    "dotnet": ".net",
    ".net core": ".net",
    "net core": ".net",
    "core mvc": ".net",
    ".net framework": ".net",
    "net framework": ".net",
    "asp.net": ".net",
    "asp.net core": ".net",
    "asp.net mvc": ".net",
    "rb": "ruby",
    "ruby on rails": "rails",
    "rs": "rust",
    "kt": "kotlin",
    "php8": "php",

    # --- ส่วนติดต่อผู้ใช้และเฟรมเวิร์ก (Frontend / Web Frameworks) ---
    "reactjs": "react",
    "react.js": "react",
    "react native": "react native",
    "vuejs": "vue",
    "vue.js": "vue",
    "nextjs": "next.js",
    "nuxtjs": "nuxt.js",
    "angularjs": "angular",
    "angular.js": "angular",
    "node": "node.js",
    "nodejs": "node.js",
    "express": "express.js",
    "expressjs": "express.js",
    "nest": "nestjs",
    "nest.js": "nestjs",
    "html": "html5",
    "html 5": "html5",
    "css": "css3",
    "css 3": "css3",
    "tailwind": "tailwind css",
    "tailwindcss": "tailwind css",
    "bootstrap5": "bootstrap",
    "bootstrap 5": "bootstrap",

    # --- โครงสร้างพื้นฐาน คลาวด์ และระบบเครือข่าย (DevOps / Cloud / Network) ---
    "k8s": "kubernetes",
    "kube": "kubernetes",
    "amazon web services": "aws",
    "google cloud": "gcp",
    "google cloud platform": "gcp",
    "microsoft azure": "azure",
    "ci/cd": "cicd",
    "ci cd": "cicd",
    "ci-cd": "cicd",
    "continuous integration": "cicd",
    "docker container": "docker",
    "docker containers": "docker",
    "linux server": "linux",
    "linux os": "linux",
    "ubuntu": "linux",
    "centos": "linux",
    "bash shell": "bash",
    "shell script": "bash",
    "shell scripting": "bash",
    "network security": "network security",
    "net security": "network security",
    "firewalls": "firewall",
    "cisco networking": "cisco",

    # --- ฐานข้อมูลและการจัดการข้อมูล (Databases & Big Data) ---
    "postgres": "postgresql",
    "postgres db": "postgresql",
    "mongo": "mongodb",
    "mongo db": "mongodb",
    "ms sql": "sql server",
    "mssql": "sql server",
    "microsoft sql server": "sql server",
    "sql server": "sql server",
    "mysql db": "mysql",
    "mariadb": "mysql",
    "elastic": "elasticsearch",
    "elastic search": "elasticsearch",
    "redis cache": "redis",

    # --- ปัญญาประดิษฐ์และวิทยาการข้อมูล (AI / Machine Learning / Data) ---
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "computer-vision": "computer vision",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "data science": "data science",
    "data sci": "data science",
    "data analytics": "data analysis",
    "data analyst": "data analysis",
    "power bi": "powerbi",
    "power-bi": "powerbi",
    "bi": "business intelligence",

    # --- การออกแบบและกระบวนการทำงาน (UI/UX & Agile / Management) ---
    "ux/ui": "ui/ux",
    "ui ux": "ui/ux",
    "ui/ux design": "ui/ux",
    "user experience": "ui/ux",
    "user interface": "ui/ux",
    "figma design": "figma",
    "adobe xd": "adobe xd",
    "scrum master": "scrum",
    "agile methodology": "agile",
    "agile scrum": "agile",
    "project management": "project management",
    "pm": "project management",
    "system analysis": "system analysis",
    "sa": "system analysis",
    "business analysis": "business analysis",
    "ba": "business analysis",
    "quality assurance": "qa",
    "software tester": "software testing",
    "tester": "software testing"
}

def clean_skill_string(text: str) -> str:
    """ทำความสะอาดคำทักษะ: แปลงเป็นพิมพ์เล็กและตัดอักขระส่วนเกิน"""
    if not text or not isinstance(text, str):
        return ""
    cleaned = text.lower().strip()
    cleaned = re.sub(r'[\(\)\[\]\{\}]', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    # ปกป้องคำที่ขึ้นต้นด้วยจุด เช่น .net, .net core
    is_dot_prefix = cleaned.startswith(".net")
    strip_chars = " ,;:-_/|&" + ("" if is_dot_prefix else ".")
    cleaned = cleaned.strip(strip_chars)
    return cleaned

def normalize_skill(skill: str) -> str:
    """
    แปลงคำศัพท์ทักษะเดี่ยวให้เป็นรูปมาตรฐาน (Canonical Form)
    ทำงานแบบ O(1) Hash Map Lookup
    เช่น:
      'Golang'  -> 'go'
      'JS'      -> 'javascript'
      'K8s'     -> 'kubernetes'
      'Postgres'-> 'postgresql'
    """
    cleaned = clean_skill_string(skill)
    if not cleaned:
        return ""
    return SKILL_SYNONYMS.get(cleaned, cleaned)

def normalize_skills_list(skills: List[str]) -> List[str]:
    """
    แปลงรายการทักษะทั้งหมดเป็นรูปมาตรฐาน พร้อมตัดคำซ้ำ (Deduplication)
    โดยยังคงลำดับเดิมไว้
    """
    if not skills:
        return []
    normalized = []
    seen = set()
    for s in skills:
        norm = normalize_skill(s)
        if norm and norm not in seen:
            seen.add(norm)
            normalized.append(norm)
    return normalized

def parse_and_normalize_skills(skills_text: str) -> List[str]:
    """
    แยกข้อความทักษะที่คั่นด้วยคอมมา/เซมิโคลอน แล้วทำการ Normalize ทุกคำ
    """
    if not skills_text or not isinstance(skills_text, str):
        return []
    raw_tokens = re.split(r'[;\n\r|•,]+', skills_text)
    return normalize_skills_list(raw_tokens)
