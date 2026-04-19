requirements = """streamlit>=1.28.0
plotly>=5.15.0
pandas>=2.0.0
PyPDF2>=3.0.0
python-docx>=0.8.11
"""

with open("/content/career_ai/requirements.txt", "w") as f:
    f.write(requirements)

print("✅ requirements.txt created")
# CELL 1: Configure Git
!git config --global user.email "chandrahash2927@gmail.com"
!git config --global user.name "chandrahash2927"
# CELL 2: Initialize repo and commit
import os
os.chdir("/content/career_ai")

!git init
!git add .
!git commit -m "Initial commit - CareerAI Job Search Agent"
# CELL 3: Connect to GitHub (replace with your repo URL)
# First create a new empty repo on GitHub: https://github.com/new
# Name it: career-ai-agent
# Do NOT initialize with README

!git branch -M main
!git remote add origin https://github.com/chandrahash2927-blip/Agenti-ai.git
# CELL 4: Push (you'll need a Personal Access Token)
# Go to https://github.com/settings/tokens → Generate new token (classic)
# Select 'repo' scope, copy the token

!git push -u origin main
# When it asks for password, paste your Personal Access Token
import os
os.chdir("/content/career_ai")

required_files = ['app.py', 'config.py', 'database.py', 'resume_parser.py',
                  'job_engine.py', 'company_intel.py', 'interview_agent.py',
                  'utils.py', 'requirements.txt']

print("📁 Deployment Checklist:")
for f in required_files:
    exists = "✅" if os.path.exists(f) else "❌ MISSING"
    print(f"{exists} {f}")

print("\n⚠️  Make sure:")
print("1. No API keys are hardcoded in any .py file")
print("2. requirements.txt has all packages")
print("3. You have committed and pushed to GitHub")
print("4. Your GitHub repo is PUBLIC (or Streamlit can't access it)")
