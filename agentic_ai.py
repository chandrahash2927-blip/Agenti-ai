import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool

# Setup - Replace with your key
os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"

# --- TOOL: Indian Job Scraper (Added for Week 1 Final) ---
def search_indian_jobs(query):
    """Scrapes basic job data from TimesJobs for Indian listings."""
    # This fulfills the "Implement simple job listing scraper" checklist item
    url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={query}&txtLocation=India"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
        
        results = []
        for job in jobs[:3]: # Return top 3 results
            company = job.find('h3', class_='joblist-comp-name').text.strip()
            # Fulfills "Indian Specific Features" like location/salary mentions
            details = job.find('ul', class_='top-jd-dtl clearfix').text.strip()
            results.append(f"Company: {company}\nDetails: {details}")
        
        return "\n---\n".join(results) if results else "No specific Indian jobs found for that role."
    except Exception as e:
        return f"Scraping error: {str(e)}"

# Define Tools
tools = [
    Tool(
        name="IndianJobSearch", 
        func=search_indian_jobs, 
        description="Search for live job openings in India. Input should be a job title."
    )
]

# LLM and Prompt
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
prompt = hub.pull("hwchase17/react")

# Agent Construction
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# UI
st.title("🚀 Career AI Agent - Week 1 Demo")
st.info("Goal: Basic job search functionality for the Indian market.")

user_input = st.text_input("What role are you looking for in India?", placeholder="e.g. Data Analyst in Mumbai")

if st.button("Search"):
    if user_input:
        with st.spinner("Searching Indian job boards..."):
            response = agent_executor.invoke({"input": user_input})
            st.markdown("### Results:")
            st.write(response["output"])
