import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Habit Tracker", layout="wide", page_icon="🌿")
st.title("🌿 Habit Tracker")
st.write("Build consistency, track daily routines, and look after your compounding streaks.")

st.divider()

# --- SECTION 1: CREATE A NEW HABIT ---
st.subheader("Define a New Habit")

with st.form("habit_form", clear_on_submit=True):
    user_uuid = st.text_input(
        "Associated User UUID", 
        placeholder="Paste your long UUID here...",
        help="Paste the unique string ID corresponding to your user account."
    )
    
    title = st.text_input("Habit Name", placeholder="e.g., Practice Violin, Python Coding, Morning Review")
    description = st.text_area("Why this habit matters / Frequency rules", 
                               placeholder="e.g., 30 minutes every morning to stay consistent...")
    
    submitted = st.form_submit_button("Create Habit")
    
    if submitted:
        if not user_uuid.strip():
            st.warning("⚠️ A valid User UUID string is required to save a habit.")
        elif not title.strip():
            st.warning("⚠️ Please provide a habit name.")
        else:
            # FIXED KEY: Changed 'title' to 'name' to pass backend Pydantic validation
            habit_data = {
                "name": title.strip(),
                "description": description.strip(),
                "is_completed": False,
                "user_id": user_uuid.strip().strip('"').strip("'")
            }
            
            try:
                response = requests.post(f"{BACKEND_URL}/api/habits/", json=habit_data)
                
                if response.status_code in [200, 201]:
                    st.success(f"🎉 Habit '{title}' initialized successfully!")
                else:
                    st.error(f"❌ Failed to create habit. Server responded with status code: {response.status_code}")
                    st.json(response.json())
            except Exception as e:
                st.error(f"🔴 Connection error: {e}")

st.divider()

# --- SECTION 2: VIEW ACTIVE HABITS ---
st.subheader("Your Routine Trackers")

try:
    response = requests.get(f"{BACKEND_URL}/api/habits/")
    if response.status_code == 200:
        habits = response.json()
        
        if not habits:
            st.info("No routine habits tracked yet. Establish your first one above!")
        else:
            for habit in habits:
                with st.container():
                    # Prioritize pulling the 'name' key from database return array
                    h_title = habit.get("name") or habit.get("title") or "Unnamed Habit"
                    h_desc = habit.get("description", "")
                    h_uid = habit.get("user_id", "N/A")
                    
                    st.markdown(f"### 🏃‍♂️ {h_title}")
                    st.caption(f"Tracked by User UUID: `{h_uid}`")
                    if h_desc:
                        st.write(f"**Routine Details:** {h_desc}")
                    st.write("---")
    else:
        st.error("Could not fetch habits from database.")
except Exception as e:
    st.error(f"🔴 Connection error fetching habits: {e}")