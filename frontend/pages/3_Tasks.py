import streamlit as st
import requests
from datetime import date

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Tasks Management", layout="wide", page_icon="✅")
st.title("✅ Tasks Management")
st.write("Manage your daily to-dos, action items, and micro-milestones.")

st.divider()

# --- SECTION 1: CREATE A NEW TASK ---
st.subheader("Add a New Task")

with st.form("task_form", clear_on_submit=True):
    user_uuid = st.text_input(
        "Associated User UUID", 
        placeholder="Paste your long UUID here...",
        help="Paste the unique string ID corresponding to your user account."
    )
    
    title = st.text_input("Task Title", placeholder="e.g., Review database schema indexing")
    description = st.text_area("Notes / Details", placeholder="Any specific sub-tasks or reminders...")
    
    submitted = st.form_submit_button("Add Task")
    
    if submitted:
        if not user_uuid.strip():
            st.warning("⚠️ A valid User UUID string is required to add a task.")
        elif not title.strip():
            st.warning("⚠️ Please provide at least a task title.")
        else:
            # Structuring task payload with automated quote protection
            task_data = {
                "title": title.strip(),
                "description": description.strip(),
                "is_completed": False,
                "user_id": user_uuid.strip().strip('"').strip("'")
            }
            
            try:
                response = requests.post(f"{BACKEND_URL}/api/tasks/", json=task_data)
                if response.status_code in [200, 201]:
                    st.success(f"🎉 Task '{title}' added successfully!")
                else:
                    st.error(f"❌ Failed to add task. Server responded with status code: {response.status_code}")
                    st.json(response.json())
            except Exception as e:
                st.error(f"🔴 Connection error: {e}")

st.divider()

# --- SECTION 2: VIEW CURRENT TASKS ---
st.subheader("Your Action Items")

try:
    response = requests.get(f"{BACKEND_URL}/api/tasks/")
    if response.status_code == 200:
        tasks = response.json()
        
        if not tasks:
            st.info("No tasks logged yet. Time to clear the slate or add a new item!")
        else:
            for task in tasks:
                with st.container():
                    t_title = task.get("title") or task.get("name") or "Untitled Task"
                    t_desc = task.get("description", "")
                    t_uid = task.get("user_id", "N/A")
                    t_status = "✅ Done" if task.get("is_completed") else "⏳ Pending"
                    
                    st.markdown(f"### {t_title} ({t_status})")
                    st.caption(f"Assigned to User UUID: `{t_uid}`")
                    if t_desc:
                        st.write(f"**Notes:** {t_desc}")
                    st.write("---")
    else:
        st.error("Could not fetch tasks from database.")
except Exception as e:
    st.error(f"🔴 Connection error fetching tasks: {e}")