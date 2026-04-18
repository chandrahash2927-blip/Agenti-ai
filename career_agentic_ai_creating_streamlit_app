# CELL 3: Create Streamlit app and launch
app_code = '''
import streamlit as st
import plotly.express as px
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
</style>
""", unsafe_allow_html=True)

from config import *
from database import *
from resume_parser import *
from job_engine import *
from company_intel import *
from interview_agent import *
from utils import *

if 'jobs' not in st.session_state:
    st.session_state.jobs = generate_mock_jobs(60)
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'interview_answers' not in st.session_state:
    st.session_state.interview_answers = []
if 'current_questions' not in st.session_state:
    st.session_state.current_questions = []

with st.sidebar:
    st.markdown("### 🎯 CareerAI Agent")
    st.markdown("*AI-powered career assistant for Indian job market*")
    st.markdown("---")
    st.markdown("#### Your Profile")
    
    with st.form("profile_form"):
        name = st.text_input("Full Name", value=st.session_state.user_profile.get("name", ""))
        email = st.text_input("Email", value=st.session_state.user_profile.get("email", ""))
        exp = st.selectbox("Experience", list(EXPERIENCE_RANGES.keys()))
        notice = st.selectbox("Notice Period", NOTICE_PERIODS)
        locations = st.multiselect("Preferred Locations", INDIAN_METROS + TIER_2_CITIES, default=["Bangalore"])
        skills = st.text_area("Skills (comma separated)", value="Python, SQL")
        
        submitted = st.form_submit_button("💾 Save Profile")
        if submitted:
            profile = {
                "name": name, "email": email,
                "experience": list(EXPERIENCE_RANGES[exp])[0],
                "notice_period": notice, "locations": locations,
                "skills": [s.strip() for s in skills.split(",") if s.strip()]
            }
            st.session_state.user_profile = profile
            save_user_profile(profile)
            st.success("Profile saved!")

st.markdown('<p class="main-header">💼 CareerAI: Indian Job Search Agent</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Automate your job search, optimize your resume, and prepare for interviews</p>', unsafe_allow_html=True)

tabs = st.tabs(["🔍 Job Search", "📄 Resume ATS", "📊 Tracker", "🏢 Company Intel", "🎤 Mock Interview"])

with tabs[0]:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        search_role = st.text_input("Job Title", "Software Engineer")
    with col2:
        search_location = st.selectbox("Location", ["All"] + INDIAN_METROS + TIER_2_CITIES)
    with col3:
        search_mode = st.selectbox("Work Mode", ["All"] + WORK_MODES)
    with col4:
        salary_filter = st.selectbox("Min Salary", ["Any"] + list(SALARY_RANGES.keys()))
    
    filters = {
        "location": search_location if search_location != "All" else None,
        "work_mode": search_mode if search_mode != "All" else None,
        "skills": st.session_state.user_profile.get("skills", []),
        "notice_period": st.session_state.user_profile.get("notice_period"),
        "salary_min": SALARY_RANGES[salary_filter][0] if salary_filter != "Any" else None,
        "experience": st.session_state.user_profile.get("experience")
    }
    
    filtered_jobs = filter_jobs(st.session_state.jobs, filters)
    if search_role:
        filtered_jobs = [j for j in filtered_jobs if search_role.lower() in j["title"].lower()]
    
    st.markdown(f"**Found {len(filtered_jobs)} jobs**")
    
    for job in filtered_jobs[:10]:
        with st.container():
            cols = st.columns([3, 1, 1])
            with cols[0]:
                st.markdown(f"### {job['title']}")
                st.markdown(f"**{job['company']}** · {job['location']} · {job['work_mode']}")
                st.markdown(f"💰 ₹{job['salary_min']:.1f} - ₹{job['salary_max']:.1f} LPA | 📅 {job['experience_min']}-{job['experience_max']} Yrs | ⏱️ {job['notice_period']}")
                st.markdown(f"🔧 {', '.join(job['skills_required'])}")
                with st.expander("Job Description"):
                    st.write(job['description'])
            with cols[1]:
                match = job.get("match_score", 0)
                color = color_score(match)
                st.markdown(f"<h2 style='color:{color}; text-align:center'>{match}%</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align:center'>Match Score</p>", unsafe_allow_html=True)
            with cols[2]:
                if st.button("Apply", key=f"apply_{job['id']}"):
                    add_application(job)
                    st.success("Saved!")
                st.link_button("View Job", job['apply_link'])
            st.divider()

with tabs[1]:
    st.markdown("### 📄 Resume ATS Optimization")
    uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])
    
    if uploaded_file:
        file_bytes = uploaded_file.read()
        parsed = parse_resume(file_bytes, uploaded_file.name)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Word Count", parsed["word_count"])
        col2.metric("Experience (Est.)", format_experience(parsed["experience_years"]))
        col3.metric("Skills Found", len(parsed["skills_found"]))
        col4.metric("Email Found", "Yes" if parsed["email"] else "No")
        
        st.markdown("#### Detected Skills")
        st.write(", ".join(parsed["skills_found"]) if parsed["skills_found"] else "None detected")
        
        target_role = st.selectbox("Target Job Role", INDIAN_JOB_ROLES)
        jd_input = st.text_area("Paste Job Description (optional)", height=150)
        
        if st.button("Analyze ATS Score"):
            with st.spinner("Analyzing..."):
                from resume_parser import ats_score_resume
                ats_result = ats_score_resume(
                    parsed["raw_text"], 
                    jd_input if jd_input else f"Join us as {target_role}. Requires Python, SQL, AWS.",
                    target_role
                )
                
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = ats_result["total_score"],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "ATS Score"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#10B981" if ats_result["is_ats_friendly"] else "#F59E0B"},
                        'steps': [
                            {'range': [0, 50], 'color': "#FEE2E2"},
                            {'range': [50, 70], 'color': "#FEF3C7"},
                            {'range': [70, 100], 'color': "#D1FAE5"}
                        ],
                        'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 70}
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Keyword Match", f"{ats_result['keyword_score']}/40")
                c2.metric("JD Match", f"{ats_result['jd_match_score']}/30")
                c3.metric("Format Score", f"{ats_result['format_score']}/30")
                
                if ats_result["is_ats_friendly"]:
                    st.success("✅ ATS-friendly resume!")
                else:
                    st.warning("⚠️ Needs optimization")
                
                st.markdown("#### 💡 Suggestions")
                for suggestion in ats_result["suggestions"]:
                    st.markdown(f"- {suggestion}")

with tabs[2]:
    st.markdown("### 📊 Application Tracker")
    applications = get_applications()
    
    if not applications:
        st.info("No applications tracked yet!")
    else:
        df = pd.DataFrame(applications)
        st.dataframe(df[['job_title', 'company', 'location', 'salary_lpa', 'work_mode', 'status', 'applied_date']], use_container_width=True, hide_index=True)
        
        st.markdown("#### Update Status")
        col1, col2 = st.columns(2)
        with col1:
            app_id = st.selectbox("Select Application", [f"{a['id']}: {a['job_title']} at {a['company']}" for a in applications])
            selected_id = int(app_id.split(":")[0])
        with col2:
            new_status = st.selectbox("New Status", ["Applied", "Screening", "Interview", "Offer", "Rejected", "Accepted"])
        
        if st.button("Update Status"):
            update_application_status(selected_id, new_status)
            st.success("Updated!")
            st.rerun()

with tabs[3]:
    st.markdown("### 🏢 Company Intelligence")
    company_search = st.selectbox("Select Company", TOP_INDIAN_COMPANIES)
    
    if company_search:
        info = get_company_info(company_search)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rating", f"⭐ {info['rating']}/5")
        col2.metric("Reviews", info['reviews_count'])
        col3.metric("Founded", info['founded'])
        col4.metric("Employees", info['employees'])
        
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("#### ✅ Pros")
            for pro in info['pros']:
                st.markdown(f"- {pro}")
            st.markdown("#### 📊 Culture Metrics")
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['Culture', 'Work-Life Balance'],
                y=[info['culture_score'], info['work_life_balance']],
                marker_color=['#3B82F6', '#10B981']
            ))
            fig.update_layout(height=300, yaxis_range=[0,5])
            st.plotly_chart(fig, use_container_width=True)
        
        with col_right:
            st.markdown("#### ❌ Cons")
            for con in info['cons']:
                st.markdown(f"- {con}")
            
            exp_years = st.session_state.user_profile.get("experience", 3)
            salary_info = get_salary_insight(company_search, exp_years)
            
            st.markdown("#### 💰 Salary Benchmark")
            st.markdown(f"For **{exp_years} years** experience:")
            st.markdown(f"**Median: ₹{salary_info['median_lpa']:.1f} LPA**")
            st.markdown(f"Range: ₹{salary_info['range_min']:.1f} - ₹{salary_info['range_max']:.1f} LPA")

with tabs[4]:
    st.markdown("### 🎤 AI Mock Interview")
    interview_role = st.selectbox("Select Role for Interview", INDIAN_JOB_ROLES)
    
    if st.button("Start New Interview") or not st.session_state.current_questions:
        st.session_state.current_questions = get_questions(interview_role)
        st.session_state.interview_answers = []
        st.rerun()
    
    if st.session_state.current_questions:
        q_index = len(st.session_state.interview_answers)
        
        if q_index < len(st.session_state.current_questions):
            q_type, question = st.session_state.current_questions[q_index]
            
            st.markdown(f"**Question {q_index + 1} of {len(st.session_state.current_questions)}**")
            st.markdown(f"**Type:** {q_type}")
            st.markdown(f"### {question}")
            
            answer = st.text_area("Your Answer", height=150, key=f"ans_{q_index}")
            
            if st.button("Submit Answer"):
                if len(answer.strip()) < 5:
                    st.error("Please provide a more detailed answer.")
                else:
                    score, feedback = evaluate_answer(q_type, question, answer)
                    from database import save_interview_session
                    save_interview_session(interview_role, question, answer, feedback, score)
                    
                    st.session_state.interview_answers.append({
                        "type": q_type, "question": question, "answer": answer,
                        "score": score, "feedback": feedback
                    })
                    
                    st.markdown("---")
                    st.markdown(f"**Score:** {score}/10")
                    st.markdown(f"**Feedback:** {feedback}")
                    
                    if st.button("Next Question", key=f"next_{q_index}"):
                        st.rerun()
        else:
            st.success("Interview Complete!")
            report = generate_interview_report(st.session_state.interview_answers)
            
            col1, col2 = st.columns(2)
            with col1:
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = report["total_score"],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Overall Score"},
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
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown(f"**Verdict:** {report['verdict']}")
                st.markdown("**Strengths:**")
                for s in report["strengths"]:
                    st.markdown(f"- {s}")
                st.markdown("**Areas to Improve:**")
                for i in report["improvements"]:
                    st.markdown(f"- {i}")
            
            if st.button("Start New Interview"):
                st.session_state.current_questions = []
                st.session_state.interview_answers = []
                st.rerun()

st.markdown("---")
st.markdown("*CareerAI Agent - Capabl. Project | Running on Google Colab*")
'''

with open("app.py", "w") as f:
    f.write(app_code)

print("✅ Streamlit app created!")
