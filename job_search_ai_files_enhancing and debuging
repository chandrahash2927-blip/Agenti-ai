import os
os.chdir("/content/career_ai")

# ===================== FIXED job_engine.py =====================
job_engine_fixed = '''
import random
from typing import List, Dict
from datetime import datetime, timedelta
from config import (
    INDIAN_METROS, TIER_2_CITIES, EXPERIENCE_RANGES, SALARY_RANGES,
    WORK_MODES, NOTICE_PERIODS, INDIAN_JOB_ROLES, TOP_INDIAN_COMPANIES
)

def generate_mock_jobs(count_per_role: int = 25) -> List[Dict]:
    """Generate guaranteed variety: 25 jobs per role across all experience levels."""
    jobs = []
    all_locations = INDIAN_METROS + TIER_2_CITIES
    exp_ranges = list(EXPERIENCE_RANGES.values())
    job_id = 1000

    # Skill pool for realistic matching
    skill_pool = [
        "Python", "Java", "SQL", "AWS", "React", "Node.js", "Docker",
        "Kubernetes", "Machine Learning", "Data Analysis", "Agile",
        "Communication", "Leadership", "JavaScript", "HTML", "CSS",
        "TensorFlow", "PyTorch", "Excel", "Tableau", "Power BI", "Git",
        "Linux", "Azure", "GCP", "MongoDB", "PostgreSQL", "Redis"
    ]

    for role in INDIAN_JOB_ROLES:
        for i in range(count_per_role):
            # Cycle through experience ranges so every role has all levels
            exp_min, exp_max = exp_ranges[i % len(exp_ranges)]
            company = random.choice(TOP_INDIAN_COMPANIES)
            location = random.choice(all_locations)
            work_mode = random.choice(WORK_MODES)

            # Realistic salary based on experience
            if exp_max <= 1:
                base = random.uniform(3, 6)
            elif exp_max <= 3:
                base = random.uniform(4, 10)
            elif exp_max <= 5:
                base = random.uniform(8, 18)
            elif exp_max <= 8:
                base = random.uniform(15, 30)
            elif exp_max <= 12:
                base = random.uniform(25, 45)
            else:
                base = random.uniform(40, 80)

            # Location premium
            if location in INDIAN_METROS[:3]:
                base *= 1.25

            # Role premium
            if any(x in role for x in ["Lead", "Architect", "Manager", "Principal"]):
                base *= 1.4

            # Pick role-relevant skills (ensure at least 2 always match common skills)
            if "Data" in role or "Analyst" in role:
                preferred = ["Python", "SQL", "Excel", "Tableau", "Power BI", "Statistics", "Machine Learning"]
            elif "Engineer" in role or "Developer" in role:
                preferred = ["Python", "Java", "JavaScript", "React", "Node.js", "Docker", "AWS", "Git", "SQL"]
            elif "Manager" in role or "Product" in role:
                preferred = ["Agile", "Communication", "Leadership", "Roadmap", "Stakeholder Management"]
            elif "DevOps" in role or "Cloud" in role:
                preferred = ["Docker", "Kubernetes", "AWS", "Azure", "Linux", "Python", "CI/CD"]
            else:
                preferred = skill_pool

            # Ensure we pick from preferred + some random
            num_skills = random.randint(4, 7)
            skills_required = random.sample(preferred, min(len(preferred), num_skills))
            # Fill rest with random if needed
            if len(skills_required) < num_skills:
                skills_required += random.sample([s for s in skill_pool if s not in skills_required],
                                                num_skills - len(skills_required))

            job = {
                "id": job_id,
                "title": role,
                "company": company,
                "location": location,
                "work_mode": work_mode,
                "salary_min": round(base, 1),
                "salary_max": round(base * 1.35, 1),
                "salary_lpa": round(base, 1),
                "experience_min": exp_min,
                "experience_max": exp_max,
                "notice_period": random.choice(NOTICE_PERIODS),
                "posted_date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                "description": f"Join {company} as a {role}. Based in {location}. Requires {exp_min}-{exp_max} years experience. Skills: {', '.join(skills_required)}.",
                "skills_required": skills_required,
                "apply_link": f"https://www.linkedin.com/jobs/search/?keywords={role.replace(' ', '%20')}"
            }
            jobs.append(job)
            job_id += 1

    random.shuffle(jobs)
    return jobs

def calculate_match_score(job: Dict, user_skills: List[str]) -> float:
    """Calculate skill match percentage."""
    if not user_skills:
        return 0.0
    job_skills = [s.lower() for s in job["skills_required"]]
    user_skills_lower = [s.lower().strip() for s in user_skills if s.strip()]
    if not user_skills_lower:
        return 0.0
    matches = sum(1 for s in user_skills_lower if s in job_skills)
    return round((matches / len(job_skills)) * 100, 1) if job_skills else 0.0

def get_matching_skills(job: Dict, user_skills: List[str]) -> List[str]:
    """Return list of skills that match between job and user."""
    if not user_skills:
        return []
    job_skills = [s.lower() for s in job["skills_required"]]
    return [s for s in user_skills if s.lower().strip() in job_skills]

def filter_jobs(jobs: List[Dict], filters: Dict, user_profile: Dict = None) -> List[Dict]:
    """Apply filters and calculate match scores."""
    filtered = jobs.copy()

    # Location filter (only if specific location selected)
    if filters.get("location"):
        filtered = [j for j in filtered if filters["location"].lower() in j["location"].lower()]

    # Work mode filter
    if filters.get("work_mode"):
        filtered = [j for j in filtered if j["work_mode"] == filters["work_mode"]]

    # Experience filter - FIX: explicitly check None because 0 is falsy
    if filters.get("experience") is not None:
        user_exp = filters["experience"]
        filtered = [j for j in filtered if j["experience_min"] <= user_exp <= j["experience_max"]]

    # Salary filter
    if filters.get("salary_min") is not None:
        filtered = [j for j in filtered if j["salary_max"] >= filters["salary_min"]]

    # Notice period filter (Immediate candidates can apply anywhere, others filter out Immediate-required jobs)
    if filters.get("notice_period") and filters["notice_period"] != "Immediate":
        user_notice = filters["notice_period"]
        # Map notice to days for comparison
        notice_days = {"15 Days": 15, "30 Days": 30, "60 Days": 60, "90 Days": 90}
        user_days = notice_days.get(user_notice, 30)
        filtered = [j for j in filtered if j["notice_period"] in ["Immediate", "15 Days", "30 Days", "60 Days", "90 Days"]]
        # Simple logic: if job requires Immediate and user is not Immediate, filter out
        filtered = [j for j in filtered if not (j["notice_period"] == "Immediate" and user_notice != "Immediate")]

    # Skills matching + scoring
    user_skills = filters.get("skills", [])
    if not user_skills and user_profile:
        user_skills = user_profile.get("skills", [])

    user_locations = user_profile.get("locations", []) if user_profile else []

    scored_jobs = []
    for job in filtered:
        job_copy = job.copy()
        job_copy["match_score"] = calculate_match_score(job, user_skills)
        job_copy["matched_skills"] = get_matching_skills(job, user_skills)
        job_copy["location_match"] = any(loc.lower() in job["location"].lower() for loc in user_locations)
        scored_jobs.append(job_copy)

    # Sort: location match first, then match score, then salary
    scored_jobs.sort(key=lambda x: (x["location_match"], x["match_score"], x["salary_max"]), reverse=True)
    return scored_jobs
'''

with open("job_engine.py", "w") as f:
    f.write(job_engine_fixed)

# ===================== FIXED app.py =====================
app_fixed = '''
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

st.set_page_config(
    page_title="CareerAI - Indian Job Search Agent",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: bold; color: #1E3A8A; }
    .sub-header { font-size: 1.2rem; color: #64748B; margin-bottom: 20px; }
    .skill-match { color: #059669; font-weight: 600; }
    .skill-missing { color: #6B7280; }
    .badge { padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }
    .badge-warn { background: #FEF3C7; color: #92400E; }
    .badge-info { background: #DBEAFE; color: #1E40AF; }
    .badge-success { background: #D1FAE5; color: #065F46; }
</style>
""", unsafe_allow_html=True)

from config import *
from database import *
from resume_parser import *
from job_engine import *
from company_intel import *
from interview_agent import *
from utils import *

# Initialize session state
if 'jobs' not in st.session_state:
    st.session_state.jobs = generate_mock_jobs()
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'interview_answers' not in st.session_state:
    st.session_state.interview_answers = []
if 'current_questions' not in st.session_state:
    st.session_state.current_questions = []
if 'search_reset' not in st.session_state:
    st.session_state.search_reset = False

# Sidebar Profile
with st.sidebar:
    st.markdown("### 🎯 CareerAI Agent")
    st.markdown("*AI-powered career assistant for Indian job market*")
    st.markdown("---")
    st.markdown("#### Your Profile")

    default_name = st.session_state.user_profile.get("name", "")
    default_email = st.session_state.user_profile.get("email", "")
    default_exp = 0
    if st.session_state.user_profile.get("experience") is not None:
        for idx, (k, v) in enumerate(EXPERIENCE_RANGES.items()):
            if v[0] <= st.session_state.user_profile["experience"] <= v[1]:
                default_exp = idx
                break
    default_notice = st.session_state.user_profile.get("notice_period", "30 Days")
    default_locations = st.session_state.user_profile.get("locations", ["Bangalore"])
    default_skills = ", ".join(st.session_state.user_profile.get("skills", ["Python", "SQL"]))

    with st.form("profile_form"):
        name = st.text_input("Full Name", value=default_name)
        email = st.text_input("Email", value=default_email)
        exp = st.selectbox("Experience", list(EXPERIENCE_RANGES.keys()), index=default_exp)
        notice = st.selectbox("Notice Period", NOTICE_PERIODS,
                             index=NOTICE_PERIODS.index(default_notice) if default_notice in NOTICE_PERIODS else 2)
        locations = st.multiselect("Preferred Locations", INDIAN_METROS + TIER_2_CITIES, default=default_locations)
        skills = st.text_area("Skills (comma separated)", value=default_skills, height=100)

        submitted = st.form_submit_button("💾 Save Profile")
        if submitted:
            profile = {
                "name": name,
                "email": email,
                "experience": list(EXPERIENCE_RANGES[exp])[0],
                "notice_period": notice,
                "locations": locations,
                "skills": [s.strip() for s in skills.split(",") if s.strip()]
            }
            st.session_state.user_profile = profile
            save_user_profile(profile)
            st.success("Profile saved! Refreshing...")
            st.rerun()

# Header
st.markdown('<p class="main-header">💼 CareerAI: Indian Job Search Agent</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Automate your job search, optimize your resume, and prepare for interviews with AI</p>', unsafe_allow_html=True)

tabs = st.tabs(["🔍 Job Search", "📄 Resume ATS Analyzer", "📊 Application Tracker", "🏢 Company Intel", "🎤 Mock Interview"])

# ==================== TAB 1: JOB SEARCH ====================
with tabs[0]:
    if not st.session_state.user_profile.get("skills"):
        st.warning("⚠️ Please save your profile in the sidebar to see personalized match scores!")

    # Filters
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    with col1:
        search_role = st.text_input("Job Title / Keywords", "" if st.session_state.search_reset else "Software Engineer")
    with col2:
        search_location = st.selectbox("Location", ["All"] + INDIAN_METROS + TIER_2_CITIES, key="loc_filter")
    with col3:
        search_mode = st.selectbox("Work Mode", ["All"] + WORK_MODES, key="mode_filter")
    with col4:
        salary_filter = st.selectbox("Min Salary", ["Any"] + list(SALARY_RANGES.keys()), key="sal_filter")

    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("🔄 Reset Filters"):
            st.session_state.search_reset = not st.session_state.search_reset
            st.rerun()
    with c2:
        # Quick stats
        total_jobs = len(st.session_state.jobs)
        st.caption(f"Database: {total_jobs} jobs across {len(INDIAN_JOB_ROLES)} roles | Last updated: Today")

    # Build filters
    filters = {
        "location": search_location if search_location != "All" else None,
        "work_mode": search_mode if search_mode != "All" else None,
        "skills": st.session_state.user_profile.get("skills", []),
        "notice_period": st.session_state.user_profile.get("notice_period"),
        "salary_min": None,
        "experience": st.session_state.user_profile.get("experience")
    }
    if salary_filter != "Any":
        filters["salary_min"] = SALARY_RANGES[salary_filter][0]

    filtered_jobs = filter_jobs(st.session_state.jobs, filters, st.session_state.user_profile)

    # Text search
    if search_role and search_role.strip():
        filtered_jobs = [j for j in filtered_jobs if search_role.lower() in j["title"].lower()]

    st.markdown(f"### Found {len(filtered_jobs)} jobs")

    if not filtered_jobs:
        st.info("No jobs match your current filters. Try: 1) Resetting filters, 2) Searching for a different role, or 3) Adjusting your profile experience level.")
    else:
        for job in filtered_jobs[:20]:
            with st.container():
                cols = st.columns([3, 1, 1])
                with cols[0]:
                    st.markdown(f"### {job['title']}")

                    # Badges row
                    badge_html = f'<span class="badge badge-info">{job["company"]}</span> '
                    badge_html += f'<span class="badge badge-info">{job["location"]}</span> '
                    badge_html += f'<span class="badge badge-success">{job["work_mode"]}</span> '

                    if not job.get("location_match", True):
                        badge_html += f'<span class="badge badge-warn">📍 Away from preferred</span> '

                    if job.get("notice_period") == "Immediate" and st.session_state.user_profile.get("notice_period") != "Immediate":
                        badge_html += f'<span class="badge badge-warn">⚡ Immediate join</span> '

                    st.markdown(badge_html, unsafe_allow_html=True)

                    st.markdown(
                        f"💰 **₹{job['salary_min']:.1f} - ₹{job['salary_max']:.1f} LPA** | "
                        f"📅 {job['experience_min']}-{job['experience_max']} Yrs | "
                        f"⏱️ {job['notice_period']}"
                    )

                    # Skills with highlighting
                    skills_html = "🔧 "
                    user_skills_lower = [s.lower() for s in st.session_state.user_profile.get("skills", [])]
                    for skill in job["skills_required"]:
                        if skill.lower() in user_skills_lower:
                            skills_html += f'<span class="skill-match">{skill}</span> · '
                        else:
                            skills_html += f'<span class="skill-missing">{skill}</span> · '
                    st.markdown(skills_html[:-3], unsafe_allow_html=True)

                    with st.expander("📄 Job Description"):
                        st.write(job["description"])

                with cols[1]:
                    match = job.get("match_score", 0)
                    color = color_score(int(match))
                    st.markdown(f"<h2 style='color:{color}; text-align:center; margin-bottom:0'>{match}%</h2>", unsafe_allow_html=True)
                    st.markdown("<p style='text-align:center; font-size: 0.85rem; color: #6B7280'>Match Score</p>", unsafe_allow_html=True)

                    matched = job.get("matched_skills", [])
                    if matched:
                        st.markdown(f"<p style='text-align:center; font-size: 0.8rem; color: #059669'>✓ {', '.join(matched)}</p>", unsafe_allow_html=True)

                with cols[2]:
                    if st.button("💾 Save", key=f"apply_{job['id']}"):
                        add_application(job)
                        st.success("Saved!", icon="✅")
                    st.link_button("🔗 View", job["apply_link"])

                st.divider()

# ==================== TAB 2: RESUME ATS ====================
with tabs[1]:
    st.markdown("### 📄 Resume ATS Optimization")
    st.info("Upload your resume to check ATS compatibility and get optimization suggestions for Indian job market.")

    uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])

    if uploaded_file:
        file_bytes = uploaded_file.read()
        parsed = parse_resume(file_bytes, uploaded_file.name)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📝 Words", parsed["word_count"])
        col2.metric("📅 Experience", format_experience(parsed["experience_years"]))
        col3.metric("⚡ Skills Found", len(parsed["skills_found"]))
        col4.metric("📧 Email", "✅" if parsed["email"] else "❌")

        st.markdown("#### Detected Skills")
        if parsed["skills_found"]:
            st.write(", ".join(parsed["skills_found"]))
        else:
            st.warning("No specific skills detected. Make sure your resume has a 'Skills' section.")

        target_role = st.selectbox("Target Job Role", INDIAN_JOB_ROLES)
        jd_input = st.text_area("Paste Job Description (optional) - for better accuracy", height=150)

        if st.button("🔍 Analyze ATS Score"):
            with st.spinner("Analyzing your resume..."):
                default_jd = f"Join us as {target_role}. Requires Python, SQL, AWS, React, Agile, Communication, Teamwork."
                ats_result = ats_score_resume(
                    parsed["raw_text"],
                    jd_input if jd_input else default_jd,
                    target_role
                )

                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = ats_result["total_score"],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "ATS Compatibility Score"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#10B981" if ats_result["is_ats_friendly"] else "#EF4444"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "#E5E7EB",
                        'steps': [
                            {'range': [0, 50], 'color': "#FEE2E2"},
                            {'range': [50, 70], 'color': "#FEF3C7"},
                            {'range': [70, 100], 'color': "#D1FAE5"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 70
                        }
                    }
                ))
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)

                c1, c2, c3 = st.columns(3)
                c1.metric("Keywords", f"{ats_result['keyword_score']}/40")
                c2.metric("JD Match", f"{ats_result['jd_match_score']}/30")
                c3.metric("Format", f"{ats_result['format_score']}/30")

                if ats_result["is_ats_friendly"]:
                    st.success("✅ Your resume is ATS-friendly! (Score ≥ 70)")
                else:
                    st.error("❌ Your resume needs optimization to pass ATS filters.")

                st.markdown("#### 💡 Improvement Suggestions")
                for suggestion in ats_result["suggestions"]:
                    st.markdown(f"- {suggestion}")

                st.markdown("#### 🔍 Missing Keywords")
                if ats_result["missing_keywords"]:
                    st.write(", ".join(ats_result["missing_keywords"][:10]))
                else:
                    st.write("✅ All major keywords found!")

# ==================== TAB 3: TRACKER ====================
with tabs[2]:
    st.markdown("### 📊 Job Application Tracker")

    applications = get_applications()

    if not applications:
        st.info("📭 No applications tracked yet. Save jobs from the Job Search tab!")
    else:
        status_counts = {}
        for app in applications:
            status_counts[app['status']] = status_counts.get(app['status'], 0) + 1

        cols = st.columns(len(status_counts) + 1)
        cols[0].metric("Total", len(applications))
        for i, (status, count) in enumerate(status_counts.items(), 1):
            cols[i].metric(status, count)

        df = pd.DataFrame(applications)
        st.dataframe(
            df[['job_title', 'company', 'location', 'salary_lpa', 'work_mode', 'status', 'applied_date']],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("#### 📝 Update Application Status")
        col1, col2 = st.columns(2)
        with col1:
            app_options = [f"{a['id']}: {a['job_title']} at {a['company']}" for a in applications]
            app_id = st.selectbox("Select Application", app_options)
            selected_id = int(app_id.split(":")[0])
        with col2:
            new_status = st.selectbox("New Status", ["Applied", "Screening", "Interview", "Offer", "Rejected", "Accepted"])

        if st.button("Update Status"):
            update_application_status(selected_id, new_status)
            st.success("Status updated successfully!")
            st.rerun()

# ==================== TAB 4: COMPANY INTEL ====================
with tabs[3]:
    st.markdown("### 🏢 Company Intelligence")
    st.markdown("Research Indian companies before your application or interview.")

    company_search = st.selectbox("Select Company", TOP_INDIAN_COMPANIES)

    if company_search:
        info = get_company_info(company_search)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("⭐ Rating", f"{info['rating']}/5")
        col2.metric("📝 Reviews", info['reviews_count'])
        col3.metric("📅 Founded", info['founded'])
        col4.metric("👥 Employees", info['employees'])

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("#### ✅ Pros")
            for pro in info['pros']:
                st.markdown(f"- {pro}")

            st.markdown("#### 📊 Culture & Work-Life Balance")
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['Culture Score', 'Work-Life Balance'],
                y=[info['culture_score'], info['work_life_balance']],
                marker_color=['#3B82F6', '#10B981'],
                text=[info['culture_score'], info['work_life_balance']],
                textposition='auto'
            ))
            fig.update_layout(height=300, yaxis_range=[0,5], showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.markdown("#### ❌ Cons")
            for con in info['cons']:
                st.markdown(f"- {con}")

            exp_years = st.session_state.user_profile.get("experience", 3)
            salary_info = get_salary_insight(company_search, exp_years)

            st.markdown("#### 💰 Salary Benchmark (India)")
            st.markdown(f"For **{exp_years} years** experience at **{salary_info['company']}**:")
            st.markdown(f"### ₹{salary_info['median_lpa']:.1f} LPA")
            st.markdown(f"**Range:** ₹{salary_info['range_min']:.1f} - ₹{salary_info['range_max']:.1f} LPA")

            fig2 = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = salary_info['rating'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Company Rating"},
                gauge = {'axis': {'range': [None, 5]}, 'bar': {'color': "#F59E0B"}}
            ))
            fig2.update_layout(height=250)
            st.plotly_chart(fig2, use_container_width=True)

# ==================== TAB 5: MOCK INTERVIEW ====================
with tabs[4]:
    st.markdown("### 🎤 AI Mock Interview")
    st.markdown("Practice with role-specific questions tailored for Indian tech interviews.")

    interview_role = st.selectbox("Select Role for Interview", INDIAN_JOB_ROLES, key="interview_role")

    if st.button("🚀 Start New Interview") or not st.session_state.current_questions:
        st.session_state.current_questions = get_questions(interview_role)
        st.session_state.interview_answers = []
        st.rerun()

    if st.session_state.current_questions:
        q_index = len(st.session_state.interview_answers)

        if q_index < len(st.session_state.current_questions):
            q_type, question = st.session_state.current_questions[q_index]

            st.progress((q_index) / len(st.session_state.current_questions))
            st.markdown(f"**Question {q_index + 1} of {len(st.session_state.current_questions)}** | **Type:** {q_type}")
            st.markdown(f"### {question}")

            answer = st.text_area("Your Answer", height=150, key=f"ans_{q_index}")

            if st.button("Submit Answer"):
                if len(answer.strip()) < 10:
                    st.error("Please provide a more detailed answer (at least 10 words).")
                else:
                    score, feedback = evaluate_answer(q_type, question, answer)
                    save_interview_session(interview_role, question, answer, feedback, score)

                    st.session_state.interview_answers.append({
                        "type": q_type,
                        "question": question,
                        "answer": answer,
                        "score": score,
                        "feedback": feedback
                    })

                    st.markdown("---")
                    if score >= 8:
                        st.success(f"**Score:** {score}/10")
                    elif score >= 5:
                        st.warning(f"**Score:** {score}/10")
                    else:
                        st.error(f"**Score:** {score}/10")

                    st.markdown(f"**Feedback:** {feedback}")

                    if st.button("Next Question →", key=f"next_{q_index}"):
                        st.rerun()
        else:
            st.balloons()
            st.success("🎉 Interview Complete! Here's your performance report:")

            report = generate_interview_report(st.session_state.interview_answers)

            col1, col2 = st.columns([1, 1])
            with col1:
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = report["total_score"],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Overall Interview Score"},
                    gauge = {
                        'axis': {'range': [None, 10]},
                        'bar': {'color': "#10B981"},
                        'steps': [
                            {'range': [0, 4], 'color': "#FEE2E2"},
                            {'range': [4, 6], 'color': "#FEF3C7"},
                            {'range': [6, 8], 'color': "#DBEAFE"},
                            {'range': [8, 10], 'color': "#D1FAE5"}
                        ]
                    }
                ))
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                verdict_colors = {"Strong Hire": "green", "Hire": "blue", "Consider": "orange", "Reject": "red"}
                vc = verdict_colors.get(report['verdict'], 'black')
                st.markdown(f"### Verdict: <span style='color:{vc}'>{report['verdict']}</span>", unsafe_allow_html=True)

                st.markdown("**💪 Strengths:**")
                for s in report["strengths"]:
                    st.markdown(f"- {s}")

                st.markdown("**🎯 Areas to Improve:**")
                for i in report["improvements"]:
                    st.markdown(f"- {i}")

            st.markdown("#### 📚 Preparation Tips for Next Time")
            for tip in report["preparation_tips"]:
                st.info(tip)

            if st.button("🔄 Start New Interview"):
                st.session_state.current_questions = []
                st.session_state.interview_answers = []
                st.rerun()

st.markdown("---")
st.markdown("*CareerAI Agent - Built for Indian Job Market | Capabl. Project*")
'''

with open("app.py", "w") as f:
    f.write(app_fixed)

print("✅ FILES FIXED! Now do this:")
print("1. Restart Streamlit: Run the cell with '!pkill -f streamlit' then launch again")
print("2. Or click 'Rerun' in the top right of your Streamlit app")
print("")
print("What's fixed:")
print("• 375 jobs generated (25 per role) so you'll see 10-15 Software Engineer jobs")
print("• Experience levels distributed evenly (1-3 years guaranteed for every role)")
print("• Skills highlighted: matched ones in GREEN, missing ones in gray")
print("• Location mismatch badge shows when job is outside your preferred cities")
print("• Reset Filters button added")
print("• Sorted by location match first, then skill match")
