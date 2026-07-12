import streamlit as st
import requests
from datetime import date, time

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Calendar & Events", layout="wide", page_icon="📅")
st.title("📅 Calendar & Events")
st.write("Schedule milestones, tracking deadlines, and key timeblocks.")

st.divider()

# --- SECTION 1: CREATE A NEW EVENT ---
st.subheader("Schedule an Event")

with st.form("calendar_form", clear_on_submit=True):
    user_uuid = st.text_input(
        "Associated User UUID", 
        placeholder="Paste your long UUID here...",
        help="Paste the unique string ID corresponding to your user account."
    )
    
    title = st.text_input("Event Title", placeholder="e.g., Code Review / Strategy Session")
    description = st.text_area("Event Description / Notes", placeholder="Location, links, or agenda items...")
    
    # Grid layout for managing start and end parameters
    st.markdown("#### Event Timing")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date.today())
        start_time = st.time_input("Start Time", value=time(9, 0))
    with col2:
        end_date = st.date_input("End Date", value=date.today())
        end_time = st.time_input("End Time", value=time(10, 0))

    submitted = st.form_submit_button("Schedule Event")
    
    if submitted:
        if not user_uuid.strip():
            st.warning("⚠️ A valid User UUID string is required to schedule an event.")
        elif not title.strip():
            st.warning("⚠️ Please provide at least an event title.")
        else:
            # Combine date and time inputs into the ISO 8601 strings expected by FastAPI
            iso_start = f"{start_date}T{start_time}"
            iso_end = f"{end_date}T{end_time}"
            
            event_data = {
                "title": title.strip(),
                "description": description.strip(),
                "start_time": iso_start,
                "end_time": iso_end,
                "user_id": user_uuid.strip().strip('"').strip("'")
            }
            
            try:
                response = requests.post(f"{BACKEND_URL}/api/events/", json=event_data)
                
                # Check for alternate fallback endpoint if /api/events/ returns 404
                if response.status_code == 404:
                    response = requests.post(f"{BACKEND_URL}/api/calendar/", json=event_data)

                if response.status_code in [200, 201]:
                    st.success(f"🎉 Event '{title}' scheduled successfully!")
                else:
                    st.error(f"❌ Failed to schedule event. Server responded with status code: {response.status_code}")
                    st.json(response.json())
            except Exception as e:
                st.error(f"🔴 Connection error: {e}")

st.divider()

# --- SECTION 2: VIEW SCHEDULED EVENTS ---
st.subheader("Upcoming Agenda Items")

try:
    response = requests.get(f"{BACKEND_URL}/api/events/")
    if response.status_code == 404:
        response = requests.get(f"{BACKEND_URL}/api/calendar/")
        
    if response.status_code == 200:
        events = response.json()
        
        if not events:
            st.info("Your calendar is completely clear! Use the form above to add an item.")
        else:
            for event in events:
                with st.container():
                    e_title = event.get("title") or event.get("name") or "Untitled Event"
                    e_desc = event.get("description", "")
                    
                    # Target the updated start and end keys safely
                    e_start = event.get("start_time") or event.get("date") or "No start time"
                    e_end = event.get("end_time") or "No end time"
                    e_uid = event.get("user_id", "N/A")
                    
                    # Clean up "T" symbol from ISO strings if present for visual appeal
                    display_start = str(e_start).replace("T", " ")
                    display_end = str(e_end).replace("T", " ")
                    
                    st.markdown(f"### {e_title}")
                    st.markdown(f"⏳ **From:** `{display_start}`  \n⏳ **To:** `{display_end}`")
                    st.caption(f"Organizer User UUID: `{e_uid}`")
                    
                    if e_desc:
                        st.write(f"**Details:** {e_desc}")
                    st.write("---")
    else:
        st.error("Could not fetch calendar entries from database.")
except Exception as e:
    st.error(f"🔴 Connection error fetching calendar: {e}")