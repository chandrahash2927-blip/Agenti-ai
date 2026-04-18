# CELL 1: Install dependencies
!pip install streamlit pyngrok plotly pandas PyPDF2 python-docx -q

# CELL 2: Write all project files
import os
os.makedirs("/content/career_ai", exist_ok=True)
os.chdir("/content/career_ai")

# config.py
config_content = '''
INDIAN_METROS = ["Bangalore", "Hyderabad", "Pune", "Mumbai", "Delhi NCR", "Chennai", "Kolkata"]
TIER_2_CITIES = ["Jaipur", "Indore", "Chandigarh", "Kochi", "Ahmedabad", "Nagpur", "Coimbatore"]

EXPERIENCE_RANGES = {
    "Fresher (0-1 years)": (0, 1),
    "Junior (1-3 years)": (1, 3),
    "Mid-level (3-5 years)": (3, 5),
    "Senior (5-8 years)": (5, 8),
    "Lead (8-12 years)": (8, 12),
    "Executive (12+ years)": (12, 20)
}

SALARY_RANGES = {
    "0-3 LPA": (0, 3),
    "3-6 LPA": (3, 6),
    "6-10 LPA": (6, 10),
    "10-15 LPA": (10, 15),
    "15-25 LPA": (15, 25),
    "25+ LPA": (25, 50)
}

NOTICE_PERIODS = ["Immediate", "15 Days", "30 Days", "60 Days", "90 Days"]
WORK_MODES = ["Remote", "Hybrid", "On-site"]

INDIAN_JOB_ROLES = [
    "Software Engineer", "Data Analyst", "Product Manager", "DevOps Engineer",
    "UI/UX Designer", "Business Analyst", "Full Stack Developer", "Data Scientist",
    "QA Engineer", "Technical Lead", "HR Manager", "Sales Executive",
    "Marketing Manager", "Cloud Architect", "Cybersecurity Analyst"
]

TOP_INDIAN_COMPANIES = [
    "TCS", "Infosys", "Wipro", "HCL Technologies", "Tech Mahindra", "Capgemini",
    "Cognizant", "Accenture", "IBM India", "Amazon India", "Google India",
    "Microsoft India", "Flipkart", "Paytm", "Ola", "Zomato", "Swiggy", "BYJU's",
    "Reliance Jio", "HDFC Bank", "ICICI Bank", "Deloitte India", "KPMG India"
]
'''

with open("config.py", "w") as f:
    f.write(config_content)

# database.py
db_content = '''
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

DB_PATH = "career_agent.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS job_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT,
            salary_lpa REAL,
            work_mode TEXT,
            applied_date TEXT,
            status TEXT DEFAULT 'Applied',
            notes TEXT,
            job_description TEXT,
            match_score INTEGER
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            experience_years INTEGER,
            current_ctc REAL,
            expected_ctc REAL,
            notice_period TEXT,
            preferred_locations TEXT,
            skills TEXT,
            resume_text TEXT,
            created_at TEXT
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS interview_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            question TEXT,
            user_answer TEXT,
            ai_feedback TEXT,
            score INTEGER,
            created_at TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def add_application(job_data: Dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO job_applications 
        (job_title, company, location, salary_lpa, work_mode, applied_date, status, notes, job_description, match_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        job_data['title'], job_data['company'], job_data['location'],
        job_data.get('salary_lpa'), job_data.get('work_mode'),
        datetime.now().isoformat(), 'Applied', '',
        job_data.get('description', ''), job_data.get('match_score', 0)
    ))
    conn.commit()
    conn.close()

def get_applications(status: Optional[str] = None) -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    if status:
        c.execute("SELECT * FROM job_applications WHERE status = ? ORDER BY applied_date DESC", (status,))
    else:
        c.execute("SELECT * FROM job_applications ORDER BY applied_date DESC")
    
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_application_status(app_id: int, status: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE job_applications SET status = ? WHERE id = ?", (status, app_id))
    conn.commit()
    conn.close()

def save_user_profile(profile: Dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO user_profiles 
        (id, name, email, phone, experience_years, current_ctc, expected_ctc, 
         notice_period, preferred_locations, skills, resume_text, created_at)
        VALUES ((SELECT id FROM user_profiles WHERE email = ?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        profile['email'], profile['name'], profile['email'], profile.get('phone'),
        profile.get('experience'), profile.get('current_ctc'), profile.get('expected_ctc'),
        profile.get('notice_period'), json.dumps(profile.get('locations', [])),
        json.dumps(profile.get('skills', [])), profile.get('resume_text', ''),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def get_user_profile(email: str) -> Optional[Dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM user_profiles WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    if row:
        profile = dict(row)
        profile['preferred_locations'] = json.loads(profile['preferred_locations'] or '[]')
        profile['skills'] = json.loads(profile['skills'] or '[]')
        return profile
    return None

def save_interview_session(role: str, question: str, answer: str, feedback: str, score: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO interview_history (role, question, user_answer, ai_feedback, score, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (role, question, answer, feedback, score, datetime.now().isoformat()))
    conn.commit()
    conn.close()

init_db()
'''

with open("database.py", "w") as f:
    f.write(db_content)

# utils.py
utils_content = '''
def format_salary_lpa(amount: float) -> str:
    return f"₹{amount:.1f} LPA"

def format_experience(years: int) -> str:
    if years == 0:
        return "Fresher"
    elif years == 1:
        return "1 Year"
    else:
        return f"{years} Years"

def color_score(score: int) -> str:
    if score >= 80:
        return "green"
    elif score >= 60:
        return "orange"
    else:
        return "red"
'''

with open("utils.py", "w") as f:
    f.write(utils_content)

# resume_parser.py
resume_content = '''
import re
import io
from typing import Dict, List, Tuple

try:
    import PyPDF2
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

ATS_KEYWORDS = {
    "Software Engineer": [
        "python", "java", "javascript", "sql", "git", "agile", "rest api", 
        "microservices", "docker", "aws", "data structures", "algorithms"
    ],
    "Data Analyst": [
        "sql", "python", "excel", "tableau", "power bi", "statistics", 
        "pandas", "numpy", "data visualization", "etl", "machine learning"
    ],
    "Product Manager": [
        "product strategy", "roadmap", "agile", "scrum", "user stories", 
        "market research", "kpi", "a/b testing", "stakeholder management"
    ],
    "DevOps Engineer": [
        "docker", "kubernetes", "aws", "azure", "ci/cd", "jenkins", 
        "terraform", "linux", "python", "bash", "monitoring"
    ],
    "default": [
        "python", "sql", "communication", "teamwork", "problem solving", 
        "project management", "agile", "leadership", "analytics"
    ]
}

def extract_text_from_pdf(file_bytes: bytes) -> str:
    if not PYPDF_AVAILABLE:
        return ""
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_bytes: bytes) -> str:
    if not DOCX_AVAILABLE:
        return ""
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\\\\n".join([para.text for para in doc.paragraphs])

def parse_resume(file_bytes: bytes, filename: str) -> Dict:
    text = ""
    if filename.endswith('.pdf'):
        text = extract_text_from_pdf(file_bytes)
    elif filename.endswith('.docx'):
        text = extract_text_from_docx(file_bytes)
    else:
        text = file_bytes.decode('utf-8', errors='ignore')
    
    return {
        "raw_text": text,
        "word_count": len(text.split()),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills_found": extract_skills(text),
        "experience_years": extract_experience_years(text)
    }

def extract_email(text: str) -> str:
    match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\\\.[a-zA-Z]{2,}', text)
    return match.group(0) if match else ""

def extract_phone(text: str) -> str:
    patterns = [
        r'(\\\\+91[\\\\-\\\\s]?)?[0]?(91)?[789]\\\\d{9}',
        r'(\\\\+91[\\\\-\\\\s]?)?\\\\d{10}'
    ]
    for pattern in patterns:
        match = re.search(pattern, text.replace(" ", "").replace("-", ""))
        if match:
            return match.group(0)
    return ""

def extract_skills(text: str) -> List[str]:
    text_lower = text.lower()
    all_skills = set()
    for skills in ATS_KEYWORDS.values():
        all_skills.update(skills)
    
    found = [skill for skill in all_skills if skill in text_lower]
    return list(set(found))

def extract_experience_years(text: str) -> int:
    patterns = [
        r'(\\\\d+)\\\\+?\\\\s*years?.*experience',
        r'experience.*?(\\\\d+)\\\\+?\\\\s*years?',
        r'worked.*?(\\\\d+)\\\\+?\\\\s*years?'
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return int(match.group(1))
    return 0

def ats_score_resume(resume_text: str, job_description: str, role: str = "default") -> Dict:
    resume_lower = resume_text.lower()
    jd_lower = job_description.lower()
    
    keywords = ATS_KEYWORDS.get(role, ATS_KEYWORDS["default"])
    
    matched_keywords = [kw for kw in keywords if kw in resume_lower]
    keyword_score = (len(matched_keywords) / len(keywords)) * 40 if keywords else 0
    
    jd_words = set(re.findall(r'\\\\b\\\\w+\\\\b', jd_lower))
    resume_words = set(re.findall(r'\\\\b\\\\w+\\\\b', resume_lower))
    common_words = jd_words.intersection(resume_words)
    jd_score = (len(common_words) / len(jd_words)) * 30 if jd_words else 0
    
    format_score = 30
    if len(resume_text) < 200:
        format_score -= 15
    if not re.search(r'\\\\b(education|qualification|degree)\\\\b', resume_lower):
        format_score -= 5
    if not re.search(r'\\\\b(skill|technical|technologies)\\\\b', resume_lower):
        format_score -= 5
    if not re.search(r'\\\\b(project|experience|work)\\\\b', resume_lower):
        format_score -= 5
    
    total_score = min(100, int(keyword_score + jd_score + format_score))
    
    suggestions = []
    missing_keywords = [kw for kw in keywords if kw not in resume_lower]
    if missing_keywords:
        suggestions.append(f"Add missing keywords: {', '.join(missing_keywords[:5])}")
    if not extract_email(resume_text):
        suggestions.append("Add a clear contact email")
    if not extract_phone(resume_text):
        suggestions.append("Add an Indian mobile number (+91 or 10-digit)")
    if len(resume_text.split()) < 150:
        suggestions.append("Resume seems too short. Aim for 300-500 words.")
    
    return {
        "total_score": total_score,
        "keyword_score": round(keyword_score, 1),
        "jd_match_score": round(jd_score, 1),
        "format_score": format_score,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "suggestions": suggestions,
        "is_ats_friendly": total_score >= 70
    }
'''

with open("resume_parser.py", "w") as f:
    f.write(resume_content)

# job_engine.py
job_engine_content = '''
import random
from typing import List, Dict
from datetime import datetime, timedelta
from config import (
    INDIAN_METROS, TIER_2_CITIES, EXPERIENCE_RANGES, SALARY_RANGES,
    WORK_MODES, NOTICE_PERIODS, INDIAN_JOB_ROLES, TOP_INDIAN_COMPANIES
)

def generate_mock_jobs(count: int = 50) -> List[Dict]:
    jobs = []
    all_locations = INDIAN_METROS + TIER_2_CITIES
    
    for i in range(count):
        role = random.choice(INDIAN_JOB_ROLES)
        company = random.choice(TOP_INDIAN_COMPANIES)
        location = random.choice(all_locations)
        work_mode = random.choice(WORK_MODES)
        
        base_salary = random.uniform(3, 20)
        if "Lead" in role or "Architect" in role or "Manager" in role:
            base_salary += random.uniform(8, 15)
        if location in INDIAN_METROS[:3]:
            base_salary *= 1.2
            
        exp_min, exp_max = random.choice(list(EXPERIENCE_RANGES.values()))
        
        job = {
            "id": i + 1000,
            "title": role,
            "company": company,
            "location": location,
            "work_mode": work_mode,
            "salary_min": round(base_salary, 1),
            "salary_max": round(base_salary * 1.4, 1),
            "salary_lpa": round(base_salary, 1),
            "experience_min": exp_min,
            "experience_max": exp_max,
            "notice_period": random.choice(NOTICE_PERIODS),
            "posted_date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
            "description": f"Join {company} as a {role}. Exciting opportunity in {location}. Requires {exp_min}-{exp_max} years experience. Skills needed: Python, SQL, Cloud.",
            "skills_required": random.sample([
                "Python", "Java", "SQL", "AWS", "React", "Node.js", "Docker", 
                "Kubernetes", "Machine Learning", "Data Analysis", "Agile", 
                "Communication", "Leadership"
            ], k=random.randint(3, 6)),
            "apply_link": f"https://www.linkedin.com/jobs/search/?keywords={role.replace(' ', '%20')}"
        }
        jobs.append(job)
    
    return jobs

def filter_jobs(jobs: List[Dict], filters: Dict) -> List[Dict]:
    filtered = jobs
    
    if filters.get("location"):
        filtered = [j for j in filtered if filters["location"].lower() in j["location"].lower()]
    
    if filters.get("work_mode"):
        filtered = [j for j in filtered if j["work_mode"] == filters["work_mode"]]
    
    if filters.get("experience"):
        user_exp = filters["experience"]
        filtered = [j for j in filtered if j["experience_min"] <= user_exp <= j["experience_max"]]
    
    if filters.get("salary_min"):
        filtered = [j for j in filtered if j["salary_max"] >= filters["salary_min"]]
    
    if filters.get("notice_period"):
        user_notice = filters["notice_period"]
        if user_notice != "Immediate":
            filtered = [j for j in filtered if j["notice_period"] != "Immediate" or user_notice == "Immediate"]
    
    if filters.get("skills"):
        user_skills = [s.lower() for s in filters["skills"]]
        scored_jobs = []
        for job in filtered:
            job_skills = [s.lower() for s in job["skills_required"]]
            match_count = sum(1 for s in user_skills if s in job_skills)
            score = (match_count / len(job_skills)) * 100 if job_skills else 0
            job_copy = job.copy()
            job_copy["match_score"] = round(score, 1)
            scored_jobs.append(job_copy)
        filtered = scored_jobs
    
    return filtered
'''

with open("job_engine.py", "w") as f:
    f.write(job_engine_content)

# company_intel.py
company_content = '''
from typing import Dict, List
from config import TOP_INDIAN_COMPANIES

COMPANY_DATABASE = {
    "TCS": {
        "rating": 3.8,
        "reviews_count": "125k+",
        "headquarters": "Mumbai, Maharashtra",
        "employees": "600k+",
        "founded": 1968,
        "pros": ["Job security", "Brand value", "Global exposure", "Work-life balance"],
        "cons": ["Slow growth", "Bureaucracy", "Average salary hikes"],
        "culture_score": 3.7,
        "work_life_balance": 3.9,
        "salary_benchmark": {"fresher": 3.5, "3_years": 6.5, "5_years": 9.0, "senior": 18.0}
    },
    "Infosys": {
        "rating": 3.9,
        "reviews_count": "98k+",
        "headquarters": "Bangalore, Karnataka",
        "employees": "340k+",
        "founded": 1981,
        "pros": ["Training programs", "Campus facilities", "Ethical management"],
        "cons": ["Politics", "Slow promotions", "Average food"],
        "culture_score": 4.0,
        "work_life_balance": 4.1,
        "salary_benchmark": {"fresher": 3.6, "3_years": 6.8, "5_years": 9.5, "senior": 19.0}
    },
    "Amazon India": {
        "rating": 4.1,
        "reviews_count": "45k+",
        "headquarters": "Bangalore, Karnataka",
        "employees": "100k+",
        "founded": 1994,
        "pros": ["High compensation", "Fast-paced", "Learning opportunities", "Stock options"],
        "cons": ["Long hours", "High pressure", "On-call duties"],
        "culture_score": 3.9,
        "work_life_balance": 3.2,
        "salary_benchmark": {"fresher": 8.0, "3_years": 18.0, "5_years": 28.0, "senior": 50.0}
    },
    "Google India": {
        "rating": 4.5,
        "reviews_count": "32k+",
        "headquarters": "Hyderabad, Telangana",
        "employees": "10k+",
        "founded": 1998,
        "pros": ["Perks", "Innovation", "Smart colleagues", "Impact"],
        "cons": ["Competitive", "Interview difficulty", "Visibility pressure"],
        "culture_score": 4.6,
        "work_life_balance": 4.2,
        "salary_benchmark": {"fresher": 12.0, "3_years": 25.0, "5_years": 40.0, "senior": 80.0}
    },
    "default": {
        "rating": 3.7,
        "reviews_count": "N/A",
        "headquarters": "India",
        "employees": "Unknown",
        "founded": 2000,
        "pros": ["Growing company", "Learning opportunities"],
        "cons": ["Processes evolving", "Work in progress"],
        "culture_score": 3.5,
        "work_life_balance": 3.5,
        "salary_benchmark": {"fresher": 3.0, "3_years": 5.5, "5_years": 8.0, "senior": 15.0}
    }
}

def get_company_info(company_name: str) -> Dict:
    for key in COMPANY_DATABASE:
        if key.lower() in company_name.lower() or company_name.lower() in key.lower():
            return {"name": key, **COMPANY_DATABASE[key]}
    return {"name": company_name, **COMPANY_DATABASE["default"]}

def get_salary_insight(company_name: str, experience_years: int) -> Dict:
    info = get_company_info(company_name)
    benchmarks = info.get("salary_benchmark", {})
    
    if experience_years <= 1:
        level = "fresher"
    elif experience_years <= 4:
        level = "3_years"
    elif experience_years <= 7:
        level = "5_years"
    else:
        level = "senior"
    
    median_salary = benchmarks.get(level, 5.0)
    
    return {
        "company": info["name"],
        "experience_level": level.replace("_", " "),
        "median_lpa": median_salary,
        "range_min": round(median_salary * 0.8, 1),
        "range_max": round(median_salary * 1.3, 1),
        "rating": info["rating"],
        "culture_score": info["culture_score"]
    }
'''

with open("company_intel.py", "w") as f:
    f.write(company_content)

# interview_agent.py
interview_content = '''
import random
from typing import Dict, List, Tuple

INTERVIEW_QUESTIONS = {
    "Software Engineer": [
        ("Technical", "Explain the difference between REST and GraphQL. When would you use each?"),
        ("Coding", "Write a function to find the first non-repeating character in a string."),
        ("System Design", "Design a URL shortening service like bit.ly. How would you handle scaling?"),
        ("Behavioral", "Tell me about a time you had to debug a production issue under pressure."),
        ("DSA", "Given an array, find the maximum sum of any contiguous subarray (Kadane's algorithm).")
    ],
    "Data Analyst": [
        ("Technical", "What is the difference between INNER JOIN and LEFT JOIN? Give an example."),
        ("Statistics", "Explain p-value in simple terms. Why is 0.05 commonly used?"),
        ("Python/SQL", "How would you handle missing values in a dataset? Compare different methods."),
        ("Case Study", "Our conversion rate dropped 15% this month. How would you investigate?"),
        ("Behavioral", "How do you explain technical findings to non-technical stakeholders?")
    ],
    "Product Manager": [
        ("Product Sense", "How would you improve Zomato's food delivery app for tier-2 cities?"),
        ("Metrics", "What KPIs would you track for a ride-sharing app like Ola?"),
        ("Prioritization", "You have limited engineering capacity. How do you prioritize features?"),
        ("Behavioral", "Tell me about a product you launched that failed. What did you learn?"),
        ("Strategy", "Should Swiggy enter the grocery delivery market? Why or why not?")
    ],
    "default": [
        ("Behavioral", "Why do you want to leave your current job?"),
        ("Behavioral", "Where do you see yourself in 5 years?"),
        ("Technical", "Explain your most challenging project and your role in it."),
        ("Situational", "How do you handle conflict with a team member?"),
        ("General", "What are your salary expectations?")
    ]
}

def get_questions(role: str, count: int = 5) -> List[Tuple[str, str]]:
    questions = INTERVIEW_QUESTIONS.get(role, INTERVIEW_QUESTIONS["default"])
    if len(questions) <= count:
        return questions
    return random.sample(questions, count)

def evaluate_answer(question_type: str, question: str, answer: str) -> Tuple[int, str]:
    answer_length = len(answer.split())
    
    if answer_length < 10:
        return (2, "Your answer is too brief. Try to provide specific examples and structure your response using the STAR method (Situation, Task, Action, Result).")
    
    score = min(10, 4 + (answer_length // 20))
    
    feedback_parts = []
    
    if any(word in answer.lower() for word in ["example", "instance", "case", "situation"]):
        score = min(10, score + 2)
        feedback_parts.append("Good use of specific examples.")
    else:
        feedback_parts.append("Try to include a concrete example from your experience.")
    
    if question_type == "Technical" and any(word in answer.lower() for word in ["because", "since", "as", "therefore"]):
        score = min(10, score + 1)
        feedback_parts.append("Good explanation of reasoning.")
    
    if answer_length > 100:
        feedback_parts.append("Answer is comprehensive but ensure you stay focused on the question.")
    
    if score >= 8:
        feedback_parts.append("Excellent response! You demonstrated strong communication and domain knowledge.")
    elif score >= 6:
        feedback_parts.append("Good response. With a bit more specificity, this would be excellent.")
    else:
        feedback_parts.append("Consider structuring your answer better and adding more technical depth.")
    
    return (score, " ".join(feedback_parts))

def generate_interview_report(answers: List[Dict]) -> Dict:
    total_score = sum(a["score"] for a in answers)
    avg_score = total_score / len(answers) if answers else 0
    
    strengths = []
    improvements = []
    
    for ans in answers:
        if ans["score"] >= 8:
            strengths.append(f"Strong {ans['type'].lower()} answer")
        elif ans["score"] <= 4:
            improvements.append(f"Need work on {ans['type'].lower()} questions")
    
    return {
        "total_score": round(avg_score, 1),
        "max_score": 10,
        "strengths": list(set(strengths)) if strengths else ["Consistent effort across questions"],
        "improvements": list(set(improvements)) if improvements else ["Add more specific examples"],
        "verdict": "Strong Hire" if avg_score >= 8 else "Hire" if avg_score >= 6 else "Consider" if avg_score >= 4 else "Reject",
        "preparation_tips": [
            "Practice the STAR method for behavioral questions",
            "Review system design fundamentals for technical rounds",
            "Prepare 3-4 detailed stories from your past experience",
            "Research the company's recent products and news"
        ]
    }
'''

with open("interview_agent.py", "w") as f:
    f.write(interview_content)

print("✅ All files written successfully!")
