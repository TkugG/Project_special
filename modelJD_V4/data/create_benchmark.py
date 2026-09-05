"""
create_benchmark.py - Creates the Golden Test Benchmark for Evaluation (NDCG@5, MRR)
Generates 32 real student profiles across all 8 TQF MKO.2 curriculum roles with graded relevance annotations (0-3).
"""

import json
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

BENCHMARK_PROFILES = [
    # 8.1: IT Support / Computer Officer
    {
        "query_id": "Q01",
        "target_role_id": "8.1",
        "profile_title": "IT Support / Helpdesk Specialist",
        "skills": ["windows", "hardware", "troubleshooting", "helpdesk", "active directory", "ms office"],
        "adjacent_roles": ["8.2"]
    },
    {
        "query_id": "Q02",
        "target_role_id": "8.1",
        "profile_title": "Desktop & Systems Support",
        "skills": ["hardware", "troubleshooting", "lan", "tcp/ip", "remote support", "printer support"],
        "adjacent_roles": ["8.2"]
    },
    {
        "query_id": "Q03",
        "target_role_id": "8.1",
        "profile_title": "IT Operations Assistant",
        "skills": ["windows server", "linux", "active directory", "backup", "cctv", "troubleshooting"],
        "adjacent_roles": ["8.2"]
    },
    {
        "query_id": "Q04",
        "target_role_id": "8.1",
        "profile_title": "Service Desk Coordinator",
        "skills": ["helpdesk", "customer service", "troubleshooting", "active directory", "google workspace"],
        "adjacent_roles": ["8.4"]
    },

    # 8.2: Network Administrator & Infrastructure
    {
        "query_id": "Q05",
        "target_role_id": "8.2",
        "profile_title": "Cisco Network Engineer",
        "skills": ["cisco", "routing", "switching", "tcp/ip", "firewall", "vpn", "vlan"],
        "adjacent_roles": ["8.1", "8.8"]
    },
    {
        "query_id": "Q06",
        "target_role_id": "8.2",
        "profile_title": "Network Security Admin",
        "skills": ["firewall", "network security", "vpn", "palo alto", "fortinet", "dns", "dhcp"],
        "adjacent_roles": ["8.8"]
    },
    {
        "query_id": "Q07",
        "target_role_id": "8.2",
        "profile_title": "Linux Systems & Infrastructure Admin",
        "skills": ["linux server", "ubuntu", "centos", "bash", "vmware", "virtualization", "storage"],
        "adjacent_roles": ["8.1", "8.6"]
    },
    {
        "query_id": "Q08",
        "target_role_id": "8.2",
        "profile_title": "DevOps & Cloud Network Engineer",
        "skills": ["docker", "kubernetes", "aws", "terraform", "ci/cd", "linux", "cloud infrastructure"],
        "adjacent_roles": ["8.6", "8.8"]
    },

    # 8.3: Multimedia Designer & Developer
    {
        "query_id": "Q09",
        "target_role_id": "8.3",
        "profile_title": "Product & UI/UX Designer",
        "skills": ["figma", "ui/ux", "wireframing", "user research", "prototyping", "design system", "adobe xd"],
        "adjacent_roles": ["8.7"]
    },
    {
        "query_id": "Q10",
        "target_role_id": "8.3",
        "profile_title": "Graphic & Motion Media Creator",
        "skills": ["photoshop", "illustrator", "premiere pro", "after effects", "motion graphic", "video editing"],
        "adjacent_roles": []
    },
    {
        "query_id": "Q11",
        "target_role_id": "8.3",
        "profile_title": "Unity Game Developer",
        "skills": ["unity", "c#", "game development", "3d animation", "shader", "gameplay physics"],
        "adjacent_roles": ["8.6"]
    },
    {
        "query_id": "Q12",
        "target_role_id": "8.3",
        "profile_title": "3D Artist & Interactive Media",
        "skills": ["blender", "maya", "3d animation", "texturing", "unreal engine", "lighting"],
        "adjacent_roles": []
    },

    # 8.4: IT Project Manager & Coordinator
    {
        "query_id": "Q13",
        "target_role_id": "8.4",
        "profile_title": "Agile Scrum Master / PM",
        "skills": ["agile", "scrum", "jira", "sprint planning", "backlog grooming", "project management"],
        "adjacent_roles": ["8.5"]
    },
    {
        "query_id": "Q14",
        "target_role_id": "8.4",
        "profile_title": "IT Project Coordinator",
        "skills": ["project coordination", "trello", "jira", "communication", "timeline tracking", "risk management"],
        "adjacent_roles": ["8.5"]
    },
    {
        "query_id": "Q15",
        "target_role_id": "8.4",
        "profile_title": "Technical Product Owner",
        "skills": ["product roadmap", "user stories", "jira", "agile", "stakeholder management", "sdlc"],
        "adjacent_roles": ["8.5"]
    },
    {
        "query_id": "Q16",
        "target_role_id": "8.4",
        "profile_title": "IT Delivery Manager",
        "skills": ["budgeting", "resource management", "sdlc", "governance", "kpi tracking", "vendor management"],
        "adjacent_roles": ["8.5"]
    },

    # 8.5: System Analyst & Business Analyst
    {
        "query_id": "Q17",
        "target_role_id": "8.5",
        "profile_title": "System Analyst (SRS & Database Design)",
        "skills": ["system analysis", "uml", "use case", "dfd", "er diagram", "database design", "sql", "srs"],
        "adjacent_roles": ["8.4", "8.6"]
    },
    {
        "query_id": "Q18",
        "target_role_id": "8.5",
        "profile_title": "IT Business Analyst (Requirement & Workflows)",
        "skills": ["business analysis", "requirement gathering", "bpmn", "wireframing", "user stories", "acceptance criteria"],
        "adjacent_roles": ["8.4"]
    },
    {
        "query_id": "Q19",
        "target_role_id": "8.5",
        "profile_title": "Solutions & Data Flow Architect",
        "skills": ["system integration", "rest api", "microservices architecture", "uml", "swagger", "sql"],
        "adjacent_roles": ["8.6"]
    },
    {
        "query_id": "Q20",
        "target_role_id": "8.5",
        "profile_title": "Functional Consultant / BA",
        "skills": ["business requirements", "gap analysis", "uat testing", "user training", "sql queries"],
        "adjacent_roles": ["8.4"]
    },

    # 8.6: Software Developer & Engineer
    {
        "query_id": "Q21",
        "target_role_id": "8.6",
        "profile_title": "Python Backend Engineer",
        "skills": ["python", "fastapi", "django", "postgresql", "docker", "rest api", "git"],
        "adjacent_roles": ["8.7", "8.8"]
    },
    {
        "query_id": "Q22",
        "target_role_id": "8.6",
        "profile_title": "Enterprise .NET / C# Developer",
        "skills": ["c#", ".net", "asp.net core", "entity framework", "sql server", "linq", "rest api"],
        "adjacent_roles": ["8.7"]
    },
    {
        "query_id": "Q23",
        "target_role_id": "8.6",
        "profile_title": "Java Spring Boot Developer",
        "skills": ["java", "spring boot", "microservices", "hibernate", "mysql", "maven", "kafka"],
        "adjacent_roles": ["8.7"]
    },
    {
        "query_id": "Q24",
        "target_role_id": "8.6",
        "profile_title": "Full Stack React & Node Developer",
        "skills": ["javascript", "typescript", "react", "node.js", "express", "mongodb", "rest api", "git"],
        "adjacent_roles": ["8.7"]
    },

    # 8.7: Web Designer & Developer
    {
        "query_id": "Q25",
        "target_role_id": "8.7",
        "profile_title": "Modern Frontend Web Developer",
        "skills": ["html5", "css3", "javascript", "typescript", "react", "tailwind", "responsive web design"],
        "adjacent_roles": ["8.6", "8.3"]
    },
    {
        "query_id": "Q26",
        "target_role_id": "8.7",
        "profile_title": "PHP & Laravel Web Developer",
        "skills": ["php", "laravel", "mysql", "html/css", "javascript", "bootstrap", "rest api"],
        "adjacent_roles": ["8.6"]
    },
    {
        "query_id": "Q27",
        "target_role_id": "8.7",
        "profile_title": "WordPress / CMS Web Developer",
        "skills": ["wordpress", "php", "woocommerce", "elementor", "html5", "css3", "seo basics"],
        "adjacent_roles": ["8.3"]
    },
    {
        "query_id": "Q28",
        "target_role_id": "8.7",
        "profile_title": "Vue.js & Tailwind Web Engineer",
        "skills": ["vue.js", "nuxt.js", "tailwind", "html5", "css3", "javascript", "pinia", "vite"],
        "adjacent_roles": ["8.6"]
    },

    # 8.8: Specialized IT Professional (Data / AI / Cyber)
    {
        "query_id": "Q29",
        "target_role_id": "8.8",
        "profile_title": "Data Scientist / Machine Learning Engineer",
        "skills": ["python", "machine learning", "deep learning", "pandas", "scikit-learn", "pytorch", "nlp", "sql"],
        "adjacent_roles": ["8.6"]
    },
    {
        "query_id": "Q30",
        "target_role_id": "8.8",
        "profile_title": "Cybersecurity & SOC Analyst",
        "skills": ["cybersecurity", "siem", "incident response", "vulnerability assessment", "firewall", "wireshark", "penetration testing"],
        "adjacent_roles": ["8.2"]
    },
    {
        "query_id": "Q31",
        "target_role_id": "8.8",
        "profile_title": "Cloud Architect & DevSecOps",
        "skills": ["aws", "azure", "cloud architecture", "devsecops", "terraform", "docker", "kubernetes", "ci/cd"],
        "adjacent_roles": ["8.2", "8.6"]
    },
    {
        "query_id": "Q32",
        "target_role_id": "8.8",
        "profile_title": "Big Data Engineer",
        "skills": ["python", "spark", "hadoop", "sql", "data warehouse", "airflow", "kafka", "etl"],
        "adjacent_roles": ["8.6"]
    }
]

def generate_benchmark_json():
    csv_path = DATA_DIR / "thai_jobs_dataset.csv"
    if not csv_path.exists():
        csv_path = DATA_DIR / "job_dataset.csv"
    df = pd.read_csv(csv_path)

    benchmark_data = []

    for prof in BENCHMARK_PROFILES:
        target_role = prof["target_role_id"]
        adj_roles = prof["adjacent_roles"]
        user_skills_set = set(s.lower() for s in prof["skills"])
        query_text = f"{prof['profile_title']} {' '.join(prof['skills'])}"

        relevance_grades = {}

        for _, row in df.iterrows():
            job_id = str(row["JobID"]).strip()
            job_role = str(row.get("CurriculumRoleID", "")).strip()
            job_skills_raw = str(row.get("Skills", "")).lower()
            job_skills_set = set(s.strip() for s in job_skills_raw.replace(";", ",").split(",") if s.strip())

            overlap = len(user_skills_set.intersection(job_skills_set))

            # Graded Relevance scale (0, 1, 2, 3) for NDCG
            if job_role == target_role:
                if overlap >= 3:
                    grade = 3  # Highly relevant (perfect match)
                elif overlap >= 1:
                    grade = 2  # Relevant
                else:
                    grade = 1  # Role match but different sub-stack
            elif job_role in adj_roles and overlap >= 2:
                grade = 1      # Adjacent role with transferable skills
            else:
                grade = 0      # Irrelevant

            if grade > 0:
                relevance_grades[job_id] = grade

        benchmark_data.append({
            "query_id": prof["query_id"],
            "target_role_id": target_role,
            "profile_title": prof["profile_title"],
            "query_text": query_text,
            "skills": prof["skills"],
            "relevance_grades": relevance_grades
        })

    out_path = DATA_DIR / "eval_benchmark.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(benchmark_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Generated {len(benchmark_data)} evaluation test queries saved to '{out_path}'")

if __name__ == "__main__":
    generate_benchmark_json()
