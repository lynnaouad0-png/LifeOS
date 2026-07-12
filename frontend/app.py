import streamlit as st
import requests

# The live URL where your FastAPI backend is running
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="LifeOS Dashboard", layout="wide")

st.title("📊 LifeOS Core Dashboard")
st.write("Welcome to your central orchestration hub. Pure data, pure functionality.")

st.divider()

# --- BACKEND HEALTH CHECK ---
st.subheader("System Status")
try:
    response = requests.get(f"{BACKEND_URL}/")
    if response.status_code == 200:
        st.success(f"🟢 Connected to Backend: {response.json().get('message')}")
except requests.exceptions.ConnectionError:
    st.error("🔴 Cannot connect to backend. Is your Uvicorn server running on port 8000?")

st.divider()

# --- DATABASE COUNT METRICS ---
st.subheader("Database Overview")
col1, col2, col3 = st.columns(3)

# Fetch Users count
with col1:
    try:
        users_res = requests.get(f"{BACKEND_URL}/api/users/")
        if users_res.status_code == 200:
            st.metric(label="Registered Users", value=len(users_res.json()))
    except Exception:
        st.write("User metrics unavailable.")

# Fetch Active Projects count
with col2:
    try:
        projects_res = requests.get(f"{BACKEND_URL}/api/projects/")
        if projects_res.status_code == 200:
            st.metric(label="Active Projects", value=len(projects_res.json()))
    except Exception:
        st.write("Project metrics unavailable.")

# Fetch Active Goals count
with col3:
    try:
        goals_res = requests.get(f"{BACKEND_URL}/api/goals/")
        if goals_res.status_code == 200:
            st.metric(label="Tracked Goals", value=len(goals_res.json()))
    except Exception:
        st.write("Goal metrics unavailable.")