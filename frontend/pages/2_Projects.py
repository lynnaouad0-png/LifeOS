import streamlit as st
import requests
from datetime import date

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Projects Management", layout="wide", page_icon="📁")
st.title("📁 Projects Management")
st.write("Organize, track, and execute your core projects and initiatives.")

st.divider()

# --- SECTION 1: CREATE A NEW PROJECT ---
st.subheader("Launch a New Project")

with st.form("project_form", clear_on_submit=True):
    # Safe text input that will accept your UUID string
    user_uuid = st.text_input(
        "Associated User UUID", 
        placeholder="Paste your long UUID here...",
        help="Paste the unique string ID corresponding to your user account."
    )
    
    title = st.text_input("Project Title", placeholder="e.g., Build Independent AI Trading Bot")
    description = st.text_area("Description / Scope", placeholder="Outline project scope, tech stack, or milestones...")
    
    target_date = st.date_input("Target Completion Date", value=date.today())
    
    submitted = st.form_submit_button("Save Project")
    
    if submitted:
        if not user_uuid.strip():
            st.warning("⚠️ A valid User UUID string is required to save this project.")
        elif not title.strip():
            st.warning("⚠️ Please provide at least a project title.")
        else:
            # Structuring payload with automated quote protection
            project_data = {
                "title": title.strip(),
                "description": description.strip(),
                "target_date": str(target_date),
                "is_completed": False,
                "user_id": user_uuid.strip().strip('"').strip("'")
            }
            
            try:
                response = requests.post(f"{BACKEND_URL}/api/projects/", json=project_data)
                if response.status_code in [200, 201]:
                    st.success(f"🎉 Project '{title}' created successfully!")
                else:
                    st.error(f"❌ Failed to create project. Server responded with status code: {response.status_code}")
                    st.json(response.json())  # Catches field mismatches (like name vs title) instantly
            except Exception as e:
                st.error(f"🔴 Connection error: {e}")

st.divider()

# --- SECTION 2: VIEW CURRENT PROJECTS ---
st.subheader("Your Active Projects")

try:
    response = requests.get(f"{BACKEND_URL}/api/projects/")
    if response.status_code == 200:
        projects = response.json()
        
        if not projects:
            st.info("No projects tracked yet. Use the form above to launch your first one!")
        else:
            for project in projects:
                with st.container():
                    # Defensive parsing: checks both 'title' and 'name' variations automatically
                    p_title = project.get("title") or project.get("name") or "Untitled Project"
                    p_desc = project.get("description", "")
                    p_date = project.get("target_date") or project.get("due_date") or "No date set"
                    p_uid = project.get("user_id", "N/A")
                    p_status = "✅ Completed" if project.get("is_completed") else "⏳ Active"
                    
                    st.markdown(f"### {p_title} ({p_status})")
                    st.caption(f"Assigned to User UUID: `{p_uid}`")
                    if p_desc:
                        st.write(f"**Description:** {p_desc}")
                    st.write(f"**Target Date:** {p_date}")
                    st.write("---")
    else:
        st.error("Could not fetch projects from database.")
except Exception as e:
    st.error(f"🔴 Connection error fetching projects: {e}")