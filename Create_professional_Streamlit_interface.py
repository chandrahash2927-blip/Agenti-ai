import streamlit as st

# Assuming 'menu' is defined elsewhere, e.g., menu = st.sidebar.selectbox('Menu', ['Resume Analysis', 'ATS Score', 'Interview Prep', 'Analytics'])
# Adding an 'if' condition to properly start the conditional block for the menu options.
if 'menu' not in st.session_state:
    st.session_state['menu'] = 'Resume Analysis' # Default value, adjust as needed

menu = st.session_state['menu'] # Ensure 'menu' is defined if not done elsewhere

if menu == "Resume Analysis":
    st.subheader("Resume Text")
    # Make sure resume_text is defined before this point, or handle its absence
    if 'resume_text' in locals(): # Check if resume_text exists in the current scope
        st.write(resume_text[:1500])
    else:
        st.write("Resume text not loaded yet. Please upload a resume in the ATS Score section.")

    # Make sure match_jobs is defined and resume_text is available
    if 'match_jobs' in globals() and 'resume_text' in locals():
        skills = match_jobs(resume_text)
        st.subheader("Detected Skills")
        st.write(skills)
    elif 'resume_text' not in locals():
        st.write("Cannot detect skills without resume text.")
    else:
        st.write("Function 'match_jobs' not defined.")

# ATS SCORE
elif menu == "ATS Score":

    st.header("ATS Resume Score")

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )

    if uploaded_file:

        with open("resume.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Ensure extract_resume_text is defined
        if 'extract_resume_text' in globals():
            resume_text = extract_resume_text("resume.pdf")
            st.session_state['resume_text'] = resume_text # Store resume_text in session_state

            # Ensure calculate_ats_score is defined
            if 'calculate_ats_score' in globals():
                score = calculate_ats_score(resume_text)
                st.metric("ATS Score", f"{score}%")
            else:
                st.write("Function 'calculate_ats_score' not defined.")
        else:
            st.write("Function 'extract_resume_text' not defined.")

# INTERVIEW PREP
elif menu == "Interview Prep":

    st.header("Interview Questions")

    role = st.text_input("Enter Role")

    if st.button("Generate Questions"):
        # Ensure generate_interview_questions is defined
        if 'generate_interview_questions' in globals():
            questions = generate_interview_questions(role)

            for q in questions:
                st.write("-", q)
        else:
            st.write("Function 'generate_interview_questions' not defined.")

# ANALYTICS
elif menu == "Analytics":

    st.header("Skill Analytics")

    skills = [
        "python",
        "sql",
        "machine learning",
        "c++",
        "embedded systems"
    ]
    # Ensure plot_skills is defined
    if 'plot_skills' in globals():
        plot_skills(skills)
    else:
        st.write("Function 'plot_skills' not defined.")
