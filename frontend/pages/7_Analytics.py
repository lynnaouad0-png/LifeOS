import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Executive Analytics", layout="wide", page_icon="📊")
st.title("📊 Executive Analytics Dashboard")
st.write("Real-time performance metrics, project completion rates, and routine consistency tracking.")

st.divider()

# --- USER PROFILE ASSIGNMENT ---
user_uuid = st.text_input(
    "Enter User UUID for Analysis", 
    placeholder="Paste your long UUID here to compile your dashboard data...",
    help="Analyzing specific records assigned to this user profile."
).strip().strip('"').strip("'")

if not user_uuid:
    st.info("💡 Paste your User UUID above to dynamically calculate your execution analytics metrics!")
else:
    # Containers to hold filtered metrics
    user_goals = []
    user_projects = []
    user_tasks = []
    user_habits = []
    
    # 1. Fetch & Filter Goals
    try:
        r = requests.get(f"{BACKEND_URL}/api/goals/")
        if r.status_code == 200:
            user_goals = [g for g in r.json() if g.get("user_id") == user_uuid]
    except Exception:
        pass

    # 2. Fetch & Filter Projects
    try:
        r = requests.get(f"{BACKEND_URL}/api/projects/")
        if r.status_code == 200:
            user_projects = [p for p in r.json() if p.get("user_id") == user_uuid]
    except Exception:
        pass

    # 3. Fetch & Filter Tasks
    try:
        r = requests.get(f"{BACKEND_URL}/api/tasks/")
        if r.status_code == 200:
            user_tasks = [t for t in r.json() if t.get("user_id") == user_uuid]
    except Exception:
        pass

    # 4. Fetch & Filter Habits
    try:
        r = requests.get(f"{BACKEND_URL}/api/habits/")
        if r.status_code == 200:
            user_habits = [h for h in r.json() if h.get("user_id") == user_uuid]
    except Exception:
        pass

    # --- CALCULATION LAYER ---
    total_goals = len(user_goals)
    completed_goals = sum(1 for g in user_goals if g.get("is_completed"))
    
    total_projects = len(user_projects)
    completed_projects = sum(1 for p in user_projects if p.get("is_completed"))
    
    total_tasks = len(user_tasks)
    completed_tasks = sum(1 for t in user_tasks if t.get("is_completed"))
    pending_tasks = total_tasks - completed_tasks
    
    total_habits = len(user_habits)

    # --- RENDER DASHBOARD LAYOUT ---
    st.subheader("📋 Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Strategic Goals", value=total_goals)
    with col2:
        st.metric(label="Active Projects", value=total_projects)
    with col3:
        st.metric(label="Pending Action Tasks", value=pending_tasks)
    with col4:
        st.metric(label="Monitored Habits", value=total_habits)
        
    st.divider()
    
    st.subheader("🎯 Execution & Progress Tracking")
    
    # Progress Calculation and Render for Tasks
    st.markdown("#### Task Completion Rate")
    if total_tasks > 0:
        task_ratio = completed_tasks / total_tasks
        st.progress(task_ratio)
        st.caption(f"**{completed_tasks} out of {total_tasks}** daily action items completed ({int(task_ratio * 100)}%)")
    else:
        st.info("Log tasks in the Tasks Management page to calculate completion performance ratios.")
        
    # Progress Calculation and Render for Projects
    st.markdown("#### Project Milestones Rate")
    if total_projects > 0:
        proj_ratio = completed_projects / total_projects
        st.progress(proj_ratio)
        st.caption(f"**{completed_projects} out of {total_projects}** structural initiatives completed ({int(proj_ratio * 100)}%)")
    else:
        st.info("Launch projects in the Projects Management page to track milestone progression.")