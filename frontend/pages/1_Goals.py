import streamlit as st
import requests
from datetime import date

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Goals Management", layout="wide", page_icon="🎯")
st.title("🎯 Goals Management")
st.write("Track, manage, and execute your long-term strategic milestones.")

st.divider()

# --- SECTION 1: CREATE A NEW GOAL ---
st.subheader("Add a New Goal")

with st.form("goal_form", clear_on_submit=True):
    # CHANGED TO TEXT INPUT: Allows you to paste your 36-character backend UUID string
    user_uuid = st.text_input(
        "Associated User UUID", 
        placeholder="Paste your long UUID here (from http://127.0.0.1:8000/api/users/)",
        help="Paste the unique string ID corresponding to your user account."
    )
    
    title = st.text_input("Goal Title", placeholder="e.g., Build AI Trading Bot")
    description = st.text_area("Description / Why is this important?", 
                               placeholder="Detail the milestones, motivations, or criteria for success...")
    
    target_date = st.date_input("Target Completion Date", value=date.today())
    
    submitted = st.form_submit_button("Save Goal")
    
    if submitted:
        if not user_uuid.strip():
            st.warning("⚠️ A valid User UUID string is required to save this goal.")
        elif not title.strip():
            st.warning("⚠️ Please provide at least a goal title.")
        else:
            # Structuring payload with the clean UUID string text
            goal_data = {
                "title": title.strip(),
                "description": description.strip(),
                "target_date": str(target_date),
                "is_completed": False,
                "user_id": user_uuid.strip()  # Passed directly as a valid string payload
            }
            
            try:
                response = requests.post(f"{BACKEND_URL}/api/goals/", json=goal_data)
                if response.status_code in [200, 201]:
                    st.success(f"🎉 Goal '{title}' created successfully!")
                else:
                    st.error(f"❌ Failed to create goal. Server responded with status code: {response.status_code}")
                    st.json(response.json())  # Displays error arrays for diagnostic safety
            except Exception as e:
                st.error(f"🔴 Connection error: {e}")

st.divider()

# --- SECTION 2: VIEW CURRENT GOALS ---
st.subheader("Your Strategic Goals")

try:
    response = requests.get(f"{BACKEND_URL}/api/goals/")
    if response.status_code == 200:
        goals = response.json()
        
        if not goals:
            st.info("No goals tracked yet. Use the form above to add your first one!")
        else:
            for goal in goals:
                with st.container():
                    g_title = goal.get("title", "Untitled Goal")
                    g_desc = goal.get("description", "")
                    g_date = goal.get("target_date", "No date set")
                    g_uid = goal.get("user_id", "N/A")
                    g_status = "✅ Completed" if goal.get("is_completed") else "⏳ In Progress"
                    
                    st.markdown(f"### {g_title} ({g_status})")
                    st.caption(f"Assigned to User UUID: `{g_uid}`")
                    if g_desc:
                        st.write(f"**Description:** {g_desc}")
                    st.write(f"**Target Date:** {g_date}")
                    st.write("---")
    else:
        st.error("Could not fetch goals from database.")
except Exception as e:
    st.error(f"🔴 Connection error fetching goals: {e}")