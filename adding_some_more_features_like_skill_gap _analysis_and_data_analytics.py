!pip install streamlit plotly pandas PyPDF2 python-docx -q

import os
!mkdir -p /content/career_ai
os.chdir("/content/career_ai")

# 1. config.py
with open("config.py", "w") as f:
    f.write('''INDIAN_METROS = ["Bangalore", "Hyderabad", "Pune", "Mumbai", "Delhi NCR", "Chennai", "Kolkata"]
TIER_2_CITIES = ["Jaipur", "Indore", "Chandigarh", "Kochi", "Ahmedabad", "Nagpur", "Coimbatore", "Lucknow", "Bhubaneswar", "Mysore"]
ALL_CITIES = INDIAN_METROS + TIER_2_CITIES
EXPERIENCE_RANGES = {"Fresher (0-1 years)": (0, 1), "Junior (1-3 years)": (1, 3), "Mid-level (3-5 years)": (3, 5), "Senior (5-8 years)": (5, 8), "Lead (8-12 years)": (8, 12), "Executive (12+ years)": (12, 20)}
SALARY_RANGES = {"0-3 LPA": (0, 3), "3-6 LPA": (3, 6), "6-10 LPA": (6, 10), "10-15 LPA": (10, 15), "15-25 LPA": (15, 25), "25+ LPA": (25, 50)}
NOTICE_PERIODS = ["Immediate", "15 Days", "30 Days", "60 Days", "90 Days"]
WORK_MODES = ["Remote", "Hybrid", "On-site"]
INDIAN_JOB_ROLES = ["Software Engineer", "Data Analyst", "Product Manager", "DevOps Engineer", "UI/UX Designer", "Business Analyst", "Full Stack Developer", "Data Scientist", "QA Engineer", "Technical Lead", "HR Manager", "Sales Executive", "Marketing Manager", "Cloud Architect", "Cybersecurity Analyst"]
TOP_INDIAN_COMPANIES = ["TCS", "Infosys", "Wipro", "HCL Technologies", "Tech Mahindra", "Capgemini", "Cognizant", "Accenture", "IBM India", "Amazon India", "Google India", "Microsoft India", "Flipkart", "Paytm", "Ola", "Zomato", "Swiggy", "BYJU's", "Reliance Jio", "HDFC Bank", "ICICI Bank", "Deloitte India", "KPMG India", "Mindtree", "L&T Infotech", "Mphasis", "Oracle India", "Adobe India"]
INDIAN_BENEFITS = ["Health Insurance", "PF/Gratuity", "Performance Bonus", "ESOPs", "Work From Home", "Flexible Hours", "Gym Membership", "Free Meals", "Cab Facility", "Education Reimbursement", "Relocation Allowance", "Maternity/Paternity Leave", "Sabbatical", "Retirement Benefits"]
LEARNING_PLATFORMS = {"Python": ["Coursera - Python for Everybody", "Udemy - Complete Python Bootcamp", "HackerRank - Python Track"], "SQL": ["Mode Analytics - SQL Tutorial", "LeetCode - SQL Problems", "Khan Academy - SQL"], "AWS": ["AWS Free Tier Tutorials", "A Cloud Guru - AWS Solutions Architect", "Udemy - AWS Certified Cloud Practitioner"], "Machine Learning": ["Coursera - Andrew Ng ML", "Fast.ai - Practical Deep Learning", "Kaggle Learn"], "Data Analysis": ["Coursera - Google Data Analytics", "Udacity - Data Analyst Nanodegree"], "React": ["Scrimba - Learn React", "Epic React by Kent C. Dodds", "React Official Docs"], "Docker": ["Docker Docs - Get Started", "KodeKloud - Docker for Beginners"], "Kubernetes": ["CNCF - Kubernetes Basics", "Udemy - Certified Kubernetes Administrator"], "default": ["Coursera - Skill-specific courses", "Udemy - Practical projects", "YouTube - Free tutorials"]}
''')

# 2. utils.py
with open("utils.py", "w") as f:
    f.write('''def format_salary_lpa(amount: float) -> str: return f"₹{amount:.1f} LPA"
def format_experience(years: int) -> str:
    if years == 0: return "Fresher"
    elif years == 1: return "1 Year"
    else: return f"{years} Years"
def color_score(score: int) -> str:
    if score >= 80: return "green"
    elif score >= 60: return "orange"
    else: return "red"
def notice_days(period: str) -> int: return {"Immediate": 0, "15 Days": 15, "30 Days": 30, "60 Days": 60, "90 Days": 90}.get(period, 30)
def city_tier(city: str) -> str:
    from config import INDIAN_METROS, TIER_2_CITIES
    if city in INDIAN_METROS: return "Metro"
    elif city in TIER_2_CITIES: return "Tier-2"
    return "Other"
''')

# 3. database.py
with open("database.py", "w") as f:
    f.write('''import sqlite3, json
from datetime import datetime
from typing import List, Dict, Optional
DB_PATH = "career_agent.db"
def init_db():
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS job_applications (id INTEGER PRIMARY KEY AUTOINCREMENT, job_title TEXT NOT NULL, company TEXT NOT NULL, location TEXT, salary_lpa REAL, work_mode TEXT, applied_date TEXT, status TEXT DEFAULT 'Applied', notes TEXT, job_description TEXT, match_score INTEGER, source TEXT DEFAULT 'mock')""")
    c.execute("""CREATE TABLE IF NOT EXISTS user_profiles (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT UNIQUE, phone TEXT, experience_years INTEGER, current_ctc REAL, expected_ctc REAL, notice_period TEXT, preferred_locations TEXT, skills TEXT, resume_text TEXT, created_at TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS interview_history (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, question TEXT, user_answer TEXT, ai_feedback TEXT, score INTEGER, created_at TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS saved_searches (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, query TEXT, location TEXT, work_mode TEXT, min_salary REAL, experience TEXT, created_at TEXT, alert_enabled INTEGER DEFAULT 0)""")
    c.execute("""CREATE TABLE IF NOT EXISTS resume_versions (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, version_name TEXT, target_role TEXT, resume_text TEXT, ats_score INTEGER, keywords_added TEXT, created_at TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS skills_gap (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, target_role TEXT, missing_skills TEXT, learning_plan TEXT, estimated_weeks INTEGER, created_at TEXT)""")
    conn.commit(); conn.close()
def add_application(job_data: Dict):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("""INSERT INTO job_applications (job_title, company, location, salary_lpa, work_mode, applied_date, status, notes, job_description, match_score, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (job_data['title'], job_data['company'], job_data['location'], job_data.get('salary_lpa'), job_data.get('work_mode'), datetime.now().isoformat(), 'Applied', '', job_data.get('description', ''), job_data.get('match_score', 0), job_data.get('source', 'mock')))
    conn.commit(); conn.close()
def get_applications(status: Optional[str] = None) -> List[Dict]:
    conn = sqlite3.connect(DB_PATH); conn.row_factory = sqlite3.Row; c = conn.cursor()
    if status: c.execute("SELECT * FROM job_applications WHERE status = ? ORDER BY applied_date DESC", (status,))
    else: c.execute("SELECT * FROM job_applications ORDER BY applied_date DESC")
    rows = c.fetchall(); conn.close(); return [dict(row) for row in rows]
def update_application_status(app_id: int, status: str):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor(); c.execute("UPDATE job_applications SET status = ? WHERE id = ?", (status, app_id)); conn.commit(); conn.close()
def save_user_profile(profile: Dict):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor()
    c.execute("""INSERT OR REPLACE INTO user_profiles (id, name, email, phone, experience_years, current_ctc, expected_ctc, notice_period, preferred_locations, skills, resume_text, created_at) VALUES ((SELECT id FROM user_profiles WHERE email = ?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (profile['email'], profile['name'], profile['email'], profile.get('phone'), profile.get('experience'), profile.get('current_ctc'), profile.get('expected_ctc'), profile.get('notice_period'), json.dumps(profile.get('locations', [])), json.dumps(profile.get('skills', [])), profile.get('resume_text', ''), datetime.now().isoformat()))
    conn.commit(); conn.close()
def get_user_profile(email: str) -> Optional[Dict]:
    conn = sqlite3.connect(DB_PATH); conn.row_factory = sqlite3.Row; c = conn.cursor(); c.execute("SELECT * FROM user_profiles WHERE email = ?", (email,)); row = c.fetchone(); conn.close()
    if row: profile = dict(row); profile['preferred_locations'] = json.loads(profile['preferred_locations'] or '[]'); profile['skills'] = json.loads(profile['skills'] or '[]'); return profile
    return None
def save_interview_session(role, question, answer, feedback, score):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor(); c.execute("""INSERT INTO interview_history (role, question, user_answer, ai_feedback, score, created_at) VALUES (?, ?, ?, ?, ?, ?)""", (role, question, answer, feedback, score, datetime.now().isoformat())); conn.commit(); conn.close()
def save_search(email: str, query: str, location: str, work_mode: str, min_salary: float, experience: str, alert: bool = False):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor(); c.execute("""INSERT INTO saved_searches (email, query, location, work_mode, min_salary, experience, created_at, alert_enabled) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (email, query, location, work_mode, min_salary, experience, datetime.now().isoformat(), 1 if alert else 0)); conn.commit(); conn.close()
def get_saved_searches(email: str) -> List[Dict]:
    conn = sqlite3.connect(DB_PATH); conn.row_factory = sqlite3.Row; c = conn.cursor(); c.execute("SELECT * FROM saved_searches WHERE email = ? ORDER BY created_at DESC", (email,)); rows = c.fetchall(); conn.close(); return [dict(row) for row in rows]
def save_resume_version(email: str, version_name: str, target_role: str, resume_text: str, ats_score: int, keywords_added: List[str]):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor(); c.execute("""INSERT INTO resume_versions (email, version_name, target_role, resume_text, ats_score, keywords_added, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)""", (email, version_name, target_role, resume_text, ats_score, json.dumps(keywords_added), datetime.now().isoformat())); conn.commit(); conn.close()
def get_resume_versions(email: str) -> List[Dict]:
    conn = sqlite3.connect(DB_PATH); conn.row_factory = sqlite3.Row; c = conn.cursor(); c.execute("SELECT * FROM resume_versions WHERE email = ? ORDER BY created_at DESC", (email,)); rows = c.fetchall(); conn.close()
    for row in rows: row['keywords_added'] = json.loads(row['keywords_added'] or '[]')
    return [dict(row) for row in rows]
def save_skills_gap(email: str, target_role: str, missing_skills: List[str], learning_plan: Dict, weeks: int):
    conn = sqlite3.connect(DB_PATH); c = conn.cursor(); c.execute("""INSERT INTO skills_gap (email, target_role, missing_skills, learning_plan, estimated_weeks, created_at) VALUES (?, ?, ?, ?, ?, ?)""", (email, target_role, json.dumps(missing_skills), json.dumps(learning_plan), weeks, datetime.now().isoformat())); conn.commit(); conn.close()
def get_skills_gap(email: str) -> List[Dict]:
    conn = sqlite3.connect(DB_PATH); conn.row_factory = sqlite3.Row; c = conn.cursor(); c.execute("SELECT * FROM skills_gap WHERE email = ? ORDER BY created_at DESC", (email,)); rows = c.fetchall(); conn.close()
    for row in rows: row['missing_skills'] = json.loads(row['missing_skills'] or '[]'); row['learning_plan'] = json.loads(row['learning_plan'] or '{}')
    return [dict(row) for row in rows]
init_db()
''')

# 4. resume_parser.py
with open("resume_parser.py", "w") as f:
    f.write('''import re, io
from typing import Dict, List
try: import PyPDF2; PYPDF_AVAILABLE = True
except: PYPDF_AVAILABLE = False
try: import docx; DOCX_AVAILABLE = True
except: DOCX_AVAILABLE = False
ATS_KEYWORDS = {"Software Engineer": ["python", "java", "javascript", "sql", "git", "agile", "rest api", "microservices", "docker", "aws", "data structures", "algorithms"], "Data Analyst": ["sql", "python", "excel", "tableau", "power bi", "statistics", "pandas", "numpy", "data visualization", "etl", "machine learning"], "Product Manager": ["product strategy", "roadmap", "agile", "scrum", "user stories", "market research", "kpi", "a/b testing", "stakeholder management"], "DevOps Engineer": ["docker", "kubernetes", "aws", "azure", "ci/cd", "jenkins", "terraform", "linux", "python", "bash", "monitoring"], "Full Stack Developer": ["python", "javascript", "react", "node.js", "sql", "mongodb", "html", "css", "git", "aws", "docker"], "Data Scientist": ["python", "machine learning", "deep learning", "tensorflow", "pytorch", "sql", "statistics", "pandas", "numpy", "matplotlib"], "Cloud Architect": ["aws", "azure", "gcp", "kubernetes", "docker", "terraform", "linux", "python", "ci/cd", "microservices"], "default": ["python", "sql", "communication", "teamwork", "problem solving", "project management", "agile", "leadership", "analytics"]}
def extract_text_from_pdf(file_bytes: bytes) -> str:
    if not PYPDF_AVAILABLE: return ""
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes)); text = ""
    for page in reader.pages: text += page.extract_text() or ""
    return text
def extract_text_from_docx(file_bytes: bytes) -> str:
    if not DOCX_AVAILABLE: return ""
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\\n".join([para.text for para in doc.paragraphs])
def parse_resume(file_bytes: bytes, filename: str) -> Dict:
    text = ""
    if filename.endswith('.pdf'): text = extract_text_from_pdf(file_bytes)
    elif filename.endswith('.docx'): text = extract_text_from_docx(file_bytes)
    else: text = file_bytes.decode('utf-8', errors='ignore')
    return {"raw_text": text, "word_count": len(text.split()), "email": extract_email(text), "phone": extract_phone(text), "skills_found": extract_skills(text), "experience_years": extract_experience_years(text)}
def extract_email(text: str) -> str:
    m = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}', text)
    return m.group(0) if m else ""
def extract_phone(text: str) -> str:
    text_clean = text.replace(" ", "").replace("-", "")
    m = re.search(r'(\\+91)?[789]\\d{9}', text_clean)
    return m.group(0) if m else ""
def extract_skills(text: str) -> List[str]:
    text_lower = text.lower(); all_skills = set()
    for skills in ATS_KEYWORDS.values(): all_skills.update(skills)
    return list(set([s for s in all_skills if s in text_lower]))
def extract_experience_years(text: str) -> int:
    for p in [r'(\\d+)\\+?\\s*years?.*experience', r'experience.*?(\\d+)\\+?\\s*years?', r'worked.*?(\\d+)\\+?\\s*years?']:
        m = re.search(p, text.lower())
        if m: return int(m.group(1))
    return 0
def ats_score_resume(resume_text: str, job_description: str, role: str = "default") -> Dict:
    resume_lower = resume_text.lower(); jd_lower = job_description.lower()
    keywords = ATS_KEYWORDS.get(role, ATS_KEYWORDS["default"])
    matched = [kw for kw in keywords if kw in resume_lower]
    keyword_score = (len(matched)/len(keywords))*40 if keywords else 0
    jd_words = set(re.findall(r'\\b\\w+\\b', jd_lower)); resume_words = set(re.findall(r'\\b\\w+\\b', resume_lower)); common = jd_words.intersection(resume_words)
    jd_score = (len(common)/len(jd_words))*30 if jd_words else 0
    format_score = 30
    if len(resume_text) < 200: format_score -= 15
    if not re.search(r'\\b(education|qualification|degree)\\b', resume_lower): format_score -= 5
    if not re.search(r'\\b(skill|technical|technologies)\\b', resume_lower): format_score -= 5
    if not re.search(r'\\b(project|experience|work)\\b', resume_lower): format_score -= 5
    total = min(100, int(keyword_score + jd_score + format_score))
    suggestions = []; missing = [kw for kw in keywords if kw not in resume_lower]
    if missing: suggestions.append(f"Add missing keywords: {', '.join(missing[:5])}")
    if not extract_email(resume_text): suggestions.append("Add a clear contact email")
    if not extract_phone(resume_text): suggestions.append("Add an Indian mobile number (+91 or 10-digit)")
    if len(resume_text.split()) < 150: suggestions.append("Resume seems too short. Aim for 300-500 words.")
    return {"total_score": total, "keyword_score": round(keyword_score,1), "jd_match_score": round(jd_score,1), "format_score": format_score, "matched_keywords": matched, "missing_keywords": missing, "suggestions": suggestions, "is_ats_friendly": total >= 70}
''')

# 5. resume_builder.py
with open("resume_builder.py", "w") as f:
    f.write('''from typing import Dict, List, Tuple
from resume_parser import ATS_KEYWORDS
from config import LEARNING_PLATFORMS
import re

def skills_gap_analysis(user_skills: List[str], target_role: str) -> Dict:
    keywords = ATS_KEYWORDS.get(target_role, ATS_KEYWORDS["default"])
    user_skills_lower = [s.lower().strip() for s in user_skills]
    missing = [kw for kw in keywords if kw not in user_skills_lower]
    matched = [kw for kw in keywords if kw in user_skills_lower]
    learning_plan = {}
    for skill in missing:
        key = skill.title() if skill.title() in LEARNING_PLATFORMS else "default"
        learning_plan[skill] = LEARNING_PLATFORMS.get(skill.title(), LEARNING_PLATFORMS["default"])
    difficulty_multiplier = {"machine learning": 8, "deep learning": 10, "kubernetes": 6, "docker": 3, "aws": 5, "react": 4, "python": 3, "sql": 3, "default": 2}
    total_weeks = sum(difficulty_multiplier.get(s, difficulty_multiplier["default"]) for s in missing)
    return {"target_role": target_role, "matched_skills": matched, "missing_skills": missing, "match_percentage": round((len(matched) / len(keywords)) * 100, 1) if keywords else 0, "learning_plan": learning_plan, "estimated_weeks": total_weeks, "priority": missing[:3] if missing else []}

def generate_tailored_resume(base_resume: str, target_role: str, job_description: str) -> Tuple[str, List[str]]:
    keywords = ATS_KEYWORDS.get(target_role, ATS_KEYWORDS["default"])
    jd_keywords = set(re.findall(r'\\b\\w+\\b', job_description.lower()))
    resume_lower = base_resume.lower()
    missing_in_resume = [kw for kw in keywords if kw not in resume_lower and kw in jd_keywords]
    if missing_in_resume:
        injection = "\\n\\n---\\n**Tailored Skills Section (Auto-generated for this role):**\\n" + ", ".join(missing_in_resume) + "\\n\\n*Note: Please integrate these skills into your actual experience if you possess them.*"
        tailored = base_resume + injection
    else: tailored = base_resume
    return tailored, missing_in_resume

def linkedin_optimization_suggestions(profile_text: str, target_role: str) -> List[str]:
    suggestions = []; keywords = ATS_KEYWORDS.get(target_role, ATS_KEYWORDS["default"]); profile_lower = profile_text.lower()
    if len(profile_text.split('\\n')[0] if '\\n' in profile_text else profile_text) < 20: suggestions.append("Headline is too short. Use format: 'Target Role | Key Skill | Achievement'")
    missing_keywords = [kw for kw in keywords if kw not in profile_lower]
    if missing_keywords: suggestions.append(f"Add these keywords to your 'About' section: {', '.join(missing_keywords[:5])}")
    if not re.search(r'\\b(increased|improved|reduced|led|built|delivered|achieved)\\b', profile_lower): suggestions.append("Use action verbs and quantifiable achievements in experience bullets")
    if len([s for s in keywords if s in profile_lower]) < 3: suggestions.append("Expand your Skills section to include at least 10 relevant technical skills")
    if "recommendation" not in profile_lower: suggestions.append("Request recommendations from managers/colleagues")
    if "project" not in profile_lower and "portfolio" not in profile_lower: suggestions.append("Add a Featured section with project links, GitHub repos, or portfolio samples")
    return suggestions
''')

# 6. scraper.py
with open("scraper.py", "w") as f:
    f.write('''import random, time
from typing import List, Dict
from datetime import datetime
from config import INDIAN_JOB_ROLES, TOP_INDIAN_COMPANIES, INDIAN_METROS, WORK_MODES, NOTICE_PERIODS

def scrape_naukri_mock(query: str, location: str, experience: int) -> List[Dict]:
    jobs = []; companies = [c for c in TOP_INDIAN_COMPANIES if random.random() > 0.3]; roles = [r for r in INDIAN_JOB_ROLES if query.lower() in r.lower()] or [query]
    for i in range(random.randint(5, 12)):
        role = random.choice(roles); company = random.choice(companies); loc = location if location != "All" else random.choice(INDIAN_METROS); work_mode = random.choice(WORK_MODES)
        if experience <= 1: base = random.uniform(3, 5.5)
        elif experience <= 3: base = random.uniform(4.5, 10)
        elif experience <= 5: base = random.uniform(8, 18)
        else: base = random.uniform(15, 35)
        skills = random.sample(["Python", "Java", "SQL", "AWS", "React", "Angular", "Spring Boot", "Hibernate", "Microservices", "Docker"], k=random.randint(3, 5))
        job = {"id": f"naukri_{random.randint(10000, 99999)}", "title": role, "company": company, "location": loc, "work_mode": work_mode, "salary_min": round(base, 1), "salary_max": round(base * 1.4, 1), "salary_lpa": round(base, 1), "experience_min": max(0, experience - random.randint(0, 2)), "experience_max": experience + random.randint(1, 4), "notice_period": random.choice(NOTICE_PERIODS), "posted_date": datetime.now().strftime("%Y-%m-%d"), "description": f"Excellent opportunity at {company} for {role}. {experience}+ years experience preferred. Skills: {', '.join(skills)}. Competitive salary in LPA.", "skills_required": skills, "apply_link": f"https://www.naukri.com/{role.lower().replace(' ', '-')}-jobs-in-{loc.lower().replace(' ', '-')}", "source": "Naukri.com"}
        jobs.append(job); time.sleep(0.05)
    return jobs

def scrape_indeed_mock(query: str, location: str, experience: int) -> List[Dict]:
    jobs = []
    for i in range(random.randint(4, 10)):
        role = query if random.random() > 0.3 else random.choice([r for r in INDIAN_JOB_ROLES if query.lower() in r.lower()] or [query]); company = random.choice(TOP_INDIAN_COMPANIES); loc = location if location != "All" else random.choice(INDIAN_METROS)
        if experience <= 1: base = random.uniform(3, 6)
        elif experience <= 3: base = random.uniform(5, 12)
        else: base = random.uniform(12, 30)
        skills = random.sample(["Python", "SQL", "AWS", "Azure", "GCP", "React", "Node.js", "Django", "Flask", "Kubernetes"], k=random.randint(3, 5))
        job = {"id": f"indeed_{random.randint(10000, 99999)}", "title": role, "company": company, "location": loc, "work_mode": random.choice(WORK_MODES), "salary_min": round(base, 1), "salary_max": round(base * 1.3, 1), "salary_lpa": round(base, 1), "experience_min": max(0, experience - 1), "experience_max": experience + 3, "notice_period": random.choice(NOTICE_PERIODS), "posted_date": datetime.now().strftime("%Y-%m-%d"), "description": f"Hiring at {company}! Looking for {role} with {experience}+ years. Must know: {', '.join(skills)}. Salary as per industry standards (LPA).", "skills_required": skills, "apply_link": f"https://in.indeed.com/jobs?q={role.replace(' ', '+')}&l={loc.replace(' ', '+')}", "source": "Indeed India"}
        jobs.append(job)
    return jobs

def aggregate_scraped_jobs(query: str, location: str, experience: int) -> List[Dict]:
    all_jobs = []; all_jobs.extend(scrape_naukri_mock(query, location, experience)); time.sleep(0.5); all_jobs.extend(scrape_indeed_mock(query, location, experience)); random.shuffle(all_jobs); return all_jobs
''')

# 7. analytics.py
with open("analytics.py", "w") as f:
    f.write('''import random
from typing import List, Dict
from collections import defaultdict
from config import INDIAN_METROS, INDIAN_JOB_ROLES

def get_salary_analytics(jobs: List[Dict]) -> Dict:
    if not jobs: return {}
    role_salaries = defaultdict(list); loc_salaries = defaultdict(list); exp_salaries = defaultdict(list)
    for job in jobs:
        role_salaries[job["title"]].append(job["salary_lpa"]); loc_salaries[job["location"]].append(job["salary_lpa"]); exp_key = f"{job['experience_min']}-{job['experience_max']} Yrs"; exp_salaries[exp_key].append(job["salary_lpa"])
    return {"overall_avg": round(sum(j["salary_lpa"] for j in jobs) / len(jobs), 1), "overall_median": round(sorted(j["salary_lpa"] for j in jobs)[len(jobs)//2], 1), "by_role": {role: {"avg": round(sum(sals)/len(sals), 1), "min": round(min(sals), 1), "max": round(max(sals), 1), "count": len(sals)} for role, sals in role_salaries.items()}, "by_location": {loc: {"avg": round(sum(sals)/len(sals), 1), "count": len(sals)} for loc, sals in loc_salaries.items()}, "by_experience": {exp: {"avg": round(sum(sals)/len(sals), 1), "count": len(sals)} for exp, sals in exp_salaries.items()}}

def get_market_trends() -> List[Dict]:
    return [{"role": "AI/ML Engineer", "growth": "+45%", "avg_lpa": 18.5, "demand": "Very High"}, {"role": "Full Stack Developer", "growth": "+28%", "avg_lpa": 12.0, "demand": "High"}, {"role": "Data Scientist", "growth": "+32%", "avg_lpa": 15.2, "demand": "High"}, {"role": "Cloud Architect", "growth": "+38%", "avg_lpa": 22.0, "demand": "Very High"}, {"role": "DevOps Engineer", "growth": "+25%", "avg_lpa": 14.5, "demand": "High"}, {"role": "Cybersecurity Analyst", "growth": "+40%", "avg_lpa": 16.8, "demand": "Very High"}, {"role": "Product Manager", "growth": "+20%", "avg_lpa": 20.0, "demand": "Medium"}]

def city_cost_of_living() -> Dict:
    return {"Bangalore": {"index": 100, "rent_1bhk": 18000, "note": "Tech hub, highest salaries"}, "Hyderabad": {"index": 85, "rent_1bhk": 14000, "note": "Growing tech scene, lower rent"}, "Pune": {"index": 90, "rent_1bhk": 16000, "note": "Good balance of jobs and lifestyle"}, "Mumbai": {"index": 140, "rent_1bhk": 35000, "note": "Highest rents, finance focus"}, "Delhi NCR": {"index": 120, "rent_1bhk": 22000, "note": "Govt + private sector mix"}, "Chennai": {"index": 80, "rent_1bhk": 13000, "note": "Manufacturing + IT, affordable"}, "Kolkata": {"index": 70, "rent_1bhk": 10000, "note": "Lowest cost, fewer tech roles"}}
''')

# 8. company_intel.py
with open("company_intel.py", "w") as f:
    f.write('''from typing import Dict, List
from config import TOP_INDIAN_COMPANIES, INDIAN_BENEFITS
import random

COMPANY_DATABASE = {"TCS": {"rating": 3.8, "reviews_count": "125k+", "headquarters": "Mumbai, Maharashtra", "employees": "600k+", "founded": 1968, "pros": ["Job security", "Brand value", "Global exposure", "Work-life balance"], "cons": ["Slow growth", "Bureaucracy", "Average salary hikes"], "culture_score": 3.7, "work_life_balance": 3.9, "salary_benchmark": {"fresher": 3.5, "3_years": 6.5, "5_years": 9.0, "senior": 18.0}, "benefits": ["Health Insurance", "PF/Gratuity", "Performance Bonus", "Work From Home", "Cab Facility"], "growth_rating": 3.2}, "Infosys": {"rating": 3.9, "reviews_count": "98k+", "headquarters": "Bangalore, Karnataka", "employees": "340k+", "founded": 1981, "pros": ["Training programs", "Campus facilities", "Ethical management"], "cons": ["Politics", "Slow promotions", "Average food"], "culture_score": 4.0, "work_life_balance": 4.1, "salary_benchmark": {"fresher": 3.6, "3_years": 6.8, "5_years": 9.5, "senior": 19.0}, "benefits": ["Health Insurance", "ESOPs", "Education Reimbursement", "Gym Membership"], "growth_rating": 3.5}, "Amazon India": {"rating": 4.1, "reviews_count": "45k+", "headquarters": "Bangalore, Karnataka", "employees": "100k+", "founded": 1994, "pros": ["High compensation", "Fast-paced", "Learning opportunities", "Stock options"], "cons": ["Long hours", "High pressure", "On-call duties"], "culture_score": 3.9, "work_life_balance": 3.2, "salary_benchmark": {"fresher": 8.0, "3_years": 18.0, "5_years": 28.0, "senior": 50.0}, "benefits": ["Health Insurance", "ESOPs", "Relocation Allowance", "Free Meals", "Maternity/Paternity Leave"], "growth_rating": 4.5}, "Google India": {"rating": 4.5, "reviews_count": "32k+", "headquarters": "Hyderabad, Telangana", "employees": "10k+", "founded": 1998, "pros": ["Perks", "Innovation", "Smart colleagues", "Impact"], "cons": ["Competitive", "Interview difficulty", "Visibility pressure"], "culture_score": 4.6, "work_life_balance": 4.2, "salary_benchmark": {"fresher": 12.0, "3_years": 25.0, "5_years": 40.0, "senior": 80.0}, "benefits": ["Health Insurance", "ESOPs", "Free Meals", "Gym Membership", "Flexible Hours", "Sabbatical"], "growth_rating": 4.8}, "Wipro": {"rating": 3.7, "reviews_count": "85k+", "headquarters": "Bangalore, Karnataka", "employees": "250k+", "founded": 1945, "pros": ["Stable company", "Good training", "Diverse projects"], "cons": ["Low salary hikes", "Bureaucracy", "Slow decision making"], "culture_score": 3.6, "work_life_balance": 3.8, "salary_benchmark": {"fresher": 3.4, "3_years": 6.2, "5_years": 8.8, "senior": 17.0}, "benefits": ["Health Insurance", "PF/Gratuity", "Performance Bonus"], "growth_rating": 3.0}, "HCL Technologies": {"rating": 3.6, "reviews_count": "72k+", "headquarters": "Noida, UP", "employees": "220k+", "founded": 1976, "pros": ["On-site opportunities", "Product-based work", "Learning"], "cons": ["Average pay", "Politics", "Work pressure"], "culture_score": 3.5, "work_life_balance": 3.4, "salary_benchmark": {"fresher": 3.5, "3_years": 6.0, "5_years": 9.0, "senior": 16.5}, "benefits": ["Health Insurance", "Performance Bonus", "Work From Home"], "growth_rating": 3.3}, "default": {"rating": 3.7, "reviews_count": "N/A", "headquarters": "India", "employees": "Unknown", "founded": 2000, "pros": ["Growing company", "Learning opportunities"], "cons": ["Processes evolving", "Work in progress"], "culture_score": 3.5, "work_life_balance": 3.5, "salary_benchmark": {"fresher": 3.0, "3_years": 5.5, "5_years": 8.0, "senior": 15.0}, "benefits": ["Health Insurance", "PF/Gratuity"], "growth_rating": 3.5}}

def get_company_info(company_name: str) -> Dict:
    for key in COMPANY_DATABASE:
        if key.lower() in company_name.lower() or company_name.lower() in key.lower(): return {"name": key, **COMPANY_DATABASE[key]}
    return {"name": company_name, **COMPANY_DATABASE["default"]}

def get_salary_insight(company_name: str, experience_years: int) -> Dict:
    info = get_company_info(company_name); benchmarks = info.get("salary_benchmark", {})
    if experience_years <= 1: level = "fresher"
    elif experience_years <= 4: level = "3_years"
    elif experience_years <= 7: level = "5_years"
    else: level = "senior"
    median = benchmarks.get(level, 5.0)
    return {"company": info["name"], "experience_level": level.replace("_", " "), "median_lpa": median, "range_min": round(median * 0.8, 1), "range_max": round(median * 1.3, 1), "rating": info["rating"], "culture_score": info["culture_score"], "growth_rating": info.get("growth_rating", 3.5)}

def compare_companies(names: List[str]) -> List[Dict]: return [get_company_info(n) for n in names]

def get_company_benefits_analysis(company_name: str) -> Dict:
    info = get_company_info(company_name); company_benefits = set(info.get("benefits", [])); all_benefits = set(INDIAN_BENEFITS); missing = list(all_benefits - company_benefits); score = round((len(company_benefits) / len(all_benefits)) * 100, 1)
    return {"company": info["name"], "offered_benefits": list(company_benefits), "missing_benefits": missing, "benefits_score": score, "rating": info["rating"], "verdict": "Excellent" if score >= 70 else "Good" if score >= 50 else "Average"}
''')

# 9. job_engine.py
with open("job_engine.py", "w") as f:
    f.write('''import random
from typing import List, Dict
from datetime import datetime, timedelta
from config import INDIAN_METROS, TIER_2_CITIES, EXPERIENCE_RANGES, SALARY_RANGES, WORK_MODES, NOTICE_PERIODS, INDIAN_JOB_ROLES, TOP_INDIAN_COMPANIES

def generate_mock_jobs(count_per_role: int = 25) -> List[Dict]:
    jobs = []; all_locations = INDIAN_METROS + TIER_2_CITIES; exp_ranges = list(EXPERIENCE_RANGES.values()); job_id = 1000
    skill_pool = ["Python", "Java", "SQL", "AWS", "React", "Node.js", "Docker", "Kubernetes", "Machine Learning", "Data Analysis", "Agile", "Communication", "Leadership", "JavaScript", "HTML", "CSS", "TensorFlow", "PyTorch", "Excel", "Tableau", "Power BI", "Git", "Linux", "Azure", "GCP", "MongoDB", "PostgreSQL", "Redis"]
    for role in INDIAN_JOB_ROLES:
        for i in range(count_per_role):
            exp_min, exp_max = exp_ranges[i % len(exp_ranges)]; company = random.choice(TOP_INDIAN_COMPANIES); location = random.choice(all_locations); work_mode = random.choice(WORK_MODES)
            if exp_max <= 1: base = random.uniform(3, 6)
            elif exp_max <= 3: base = random.uniform(4, 10)
            elif exp_max <= 5: base = random.uniform(8, 18)
            elif exp_max <= 8: base = random.uniform(15, 30)
            elif exp_max <= 12: base = random.uniform(25, 45)
            else: base = random.uniform(40, 80)
            if location in INDIAN_METROS[:3]: base *= 1.25
            if any(x in role for x in ["Lead", "Architect", "Manager", "Principal"]): base *= 1.4
            if "Data" in role or "Analyst" in role: preferred = ["Python", "SQL", "Excel", "Tableau", "Power BI", "Statistics", "Machine Learning"]
            elif "Engineer" in role or "Developer" in role: preferred = ["Python", "Java", "JavaScript", "React", "Node.js", "Docker", "AWS", "Git", "SQL"]
            elif "Manager" in role or "Product" in role: preferred = ["Agile", "Communication", "Leadership", "Roadmap", "Stakeholder Management"]
            elif "DevOps" in role or "Cloud" in role: preferred = ["Docker", "Kubernetes", "AWS", "Azure", "Linux", "Python", "CI/CD"]
            else: preferred = skill_pool
            num_skills = random.randint(4, 7); skills_required = random.sample(preferred, min(len(preferred), num_skills))
            if len(skills_required) < num_skills: skills_required += random.sample([s for s in skill_pool if s not in skills_required], num_skills - len(skills_required))
            job = {"id": job_id, "title": role, "company": company, "location": location, "work_mode": work_mode, "salary_min": round(base, 1), "salary_max": round(base * 1.35, 1), "salary_lpa": round(base, 1), "experience_min": exp_min, "experience_max": exp_max, "notice_period": random.choice(NOTICE_PERIODS), "posted_date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"), "description": f"Join {company} as a {role}. Based in {location}. Requires {exp_min}-{exp_max} years experience. Skills: {', '.join(skills_required)}.", "skills_required": skills_required, "apply_link": f"https://www.linkedin.com/jobs/search/?keywords={role.replace(' ', '%20')}", "source": "Mock Database"}
            jobs.append(job); job_id += 1
    random.shuffle(jobs); return jobs

def calculate_match_score(job: Dict, user_skills: List[str]) -> float:
    if not user_skills: return 0.0
    job_skills = [s.lower() for s in job["skills_required"]]; user_skills_lower = [s.lower().strip() for s in user_skills if s.strip()]
    if not user_skills_lower: return 0.0
    matches = sum(1 for s in user_skills_lower if s in job_skills)
    return round((matches / len(job_skills)) * 100, 1) if job_skills else 0.0

def get_matching_skills(job: Dict, user_skills: List[str]) -> List[str]:
    if not user_skills: return []
    job_skills = [s.lower() for s in job["skills_required"]]
    return [s for s in user_skills if s.lower().strip() in job_skills]

def filter_jobs(jobs: List[Dict], filters: Dict, user_profile: Dict = None) -> List[Dict]:
    filtered = jobs.copy()
    if filters.get("location"): filtered = [j for j in filtered if filters["location"].lower() in j["location"].lower()]
    if filters.get("work_mode"): filtered = [j for j in filtered if j["work_mode"] == filters["work_mode"]]
    if filters.get("experience") is not None:
        user_exp = filters["experience"]
        filtered = [j for j in filtered if j["experience_min"] <= user_exp <= j["experience_max"]]
    if filters.get("salary_min") is not None: filtered = [j for j in filtered if j["salary_max"] >= filters["salary_min"]]
    if filters.get("notice_period") and filters["notice_period"] != "Immediate":
        filtered = [j for j in filtered if not (j["notice_period"] == "Immediate" and filters["notice_period"] != "Immediate")]
    user_skills = filters.get("skills", [])
    if not user_skills and user_profile: user_skills = user_profile.get("skills", [])
    user_locations = user_profile.get("locations", []) if user_profile else []
    scored_jobs = []
    for job in filtered:
        job_copy = job.copy(); job_copy["match_score"] = calculate_match_score(job, user_skills); job_copy["matched_skills"] = get_matching_skills(job, user_skills); job_copy["location_match"] = any(loc.lower() in job["location"].lower() for loc in user_locations)
        scored_jobs.append(job_copy)
    scored_jobs.sort(key=lambda x: (x["location_match"], x["match_score"], x["salary_max"]), reverse=True)
    return scored_jobs
''')

# 10. interview_agent.py
with open("interview_agent.py", "w") as f:
    f.write('''import random
from typing import Dict, List, Tuple
INTERVIEW_QUESTIONS = {"Software Engineer": [("Technical", "Explain the difference between REST and GraphQL. When would you use each?"), ("Coding", "Write a function to find the first non-repeating character in a string."), ("System Design", "Design a URL shortening service like bit.ly. How would you handle scaling?"), ("Behavioral", "Tell me about a time you had to debug a production issue under pressure."), ("DSA", "Given an array, find the maximum sum of any contiguous subarray (Kadane's algorithm).")], "Data Analyst": [("Technical", "What is the difference between INNER JOIN and LEFT JOIN? Give an example."), ("Statistics", "Explain p-value in simple terms. Why is 0.05 commonly used?"), ("Python/SQL", "How would you handle missing values in a dataset? Compare different methods."), ("Case Study", "Our conversion rate dropped 15% this month. How would you investigate?"), ("Behavioral", "How do you explain technical findings to non-technical stakeholders?")], "Product Manager": [("Product Sense", "How would you improve Zomato's food delivery app for tier-2 cities?"), ("Metrics", "What KPIs would you track for a ride-sharing app like Ola?"), ("Prioritization", "You have limited engineering capacity. How do you prioritize features?"), ("Behavioral", "Tell me about a product you launched that failed. What did you learn?"), ("Strategy", "Should Swiggy enter the grocery delivery market? Why or why not?")], "default": [("Behavioral", "Why do you want to leave your current job?"), ("Behavioral", "Where do you see yourself in 5 years?"), ("Technical", "Explain your most challenging project and your role in it."), ("Situational", "How do you handle conflict with a team member?"), ("General", "What are your salary expectations?")]}

def get_questions(role: str, count: int = 5) -> List[Tuple[str, str]]:
    questions = INTERVIEW_QUESTIONS.get(role, INTERVIEW_QUESTIONS["default"])
    if len(questions) <= count: return questions
    return random.sample(questions, count)

def evaluate_answer(question_type: str, question: str, answer: str) -> Tuple[int, str]:
    answer_length = len(answer.split())
    if answer_length < 10: return (2, "Your answer is too brief. Try to provide specific examples and structure your response using the STAR method (Situation, Task, Action, Result).")
    score = min(10, 4 + (answer_length // 20))
    feedback_parts = []
    if any(word in answer.lower() for word in ["example", "instance", "case", "situation"]):
        score = min(10, score + 2); feedback_parts.append("Good use of specific examples.")
    else: feedback_parts.append("Try to include a concrete example from your experience.")
    if question_type == "Technical" and any(word in answer.lower() for word in ["because", "since", "as", "therefore"]):
        score = min(10, score + 1); feedback_parts.append("Good explanation of reasoning.")
    if answer_length > 100: feedback_parts.append("Answer is comprehensive but ensure you stay focused on the question.")
    if score >= 8: feedback_parts.append("Excellent response! You demonstrated strong communication and domain knowledge.")
    elif score >= 6: feedback_parts.append("Good response. With a bit more specificity, this would be excellent.")
    else: feedback_parts.append("Consider structuring your answer better and adding more technical depth.")
    return (score, " ".join(feedback_parts))

def generate_interview_report(answers: List[Dict]) -> Dict:
    total_score = sum(a["score"] for a in answers); avg_score = total_score / len(answers) if answers else 0
    strengths = []; improvements = []
    for ans in answers:
        if ans["score"] >= 8: strengths.append(f"Strong {ans['type'].lower()} answer")
        elif ans["score"] <= 4: improvements.append(f"Need work on {ans['type'].lower()} questions")
    return {"total_score": round(avg_score, 1), "max_score": 10, "strengths": list(set(strengths)) if strengths else ["Consistent effort across questions"], "improvements": list(set(improvements)) if improvements else ["Add more specific examples"], "verdict": "Strong Hire" if avg_score >= 8 else "Hire" if avg_score >= 6 else "Consider" if avg_score >= 4 else "Reject", "preparation_tips": ["Practice the STAR method for behavioral questions", "Review system design fundamentals for technical rounds", "Prepare 3-4 detailed stories from your past experience", "Research the company's recent products and news"]}
''')

print("✅ Helper files 1-10 created. Now creating app.py...")
