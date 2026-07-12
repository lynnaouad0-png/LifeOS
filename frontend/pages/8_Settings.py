import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="System Settings", layout="wide", page_icon="⚙️")
st.title("⚙️ System Configuration & Settings")
st.write("Manage your LifeOS environment variables, backend connectivity, and profile defaults.")

st.divider()

# --- SECTION 1: SYSTEM HEALTH CHECK ---
st.subheader("System Status & Connectivity")

try:
    # Ping the base FastAPI endpoint to verify connectivity
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        st.success("🟢 Connected: Frontend is communicating perfectly with the FastAPI Backend Server.")
    else:
        st.warning(f"🟡 Warning: Backend found at {BACKEND_URL} but returned status code {response.status_code}.")
except Exception as e:
    st.error(f"🔴 Disconnected: Unable to reach the backend server at {BACKEND_URL}. Ensure your terminal is running the uvicorn process.")

# Quick connection diagnostics table
st.markdown("#### Environment Diagnostics")
st.json({
    "Frontend Framework": "Streamlit",
    "Backend Engine": "FastAPI (Python)",
    "Target Gateway URL": BACKEND_URL,
    "API Docs Endpoint": f"{BACKEND_URL}/docs"
})

st.divider()

# --- SECTION 2: PROFILE DEFAULTS ---
st.subheader("Profile Configuration Defaults")
st.write("Configure persistent environment properties to optimize your workflow.")

# Check if a UUID is already saved in session state, otherwise use blank
default_uuid = st.session_state.get("saved_user_uuid", "b2156f03-4753-484e-abad-ced4371ebfb5")

user_uuid_input = st.text_input(
    "Primary User UUID Token", 
    value=default_uuid,
    placeholder="Paste your active user profile token here...",
    help="Saving your UUID here pins it to your global app environment session."
)

if st.button("Save Profile Settings"):
    clean_uuid = user_uuid_input.strip().strip('"').strip("'")
    if not clean_uuid:
        st.error("Please enter a valid UUID token string.")
    else:
        # Commit token to the background session state
        st.session_state["saved_user_uuid"] = clean_uuid
        st.success(f"🔒 Active Session Profile set to: `{clean_uuid}`")
        st.info("Your application profile is locked into temporary local memory.")