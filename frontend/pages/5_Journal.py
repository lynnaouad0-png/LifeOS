import streamlit as st
import requests
from datetime import date

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Personal Journal", layout="wide", page_icon="✍️")
st.title("✍️ Personal Journal")
st.write("Document reflections, daily standups, review logs, and focus track records.")

st.divider()

# --- SECTION 1: CREATE A NEW JOURNAL ENTRY ---
st.subheader("Write a New Entry")

with st.form("journal_form", clear_on_submit=True):
    user_uuid = st.text_input(
        "Associated User UUID", 
        placeholder="Paste your long UUID here...",
        help="Paste the unique string ID corresponding to your user account."
    )
    
    title = st.text_input("Entry Title", placeholder="e.g., Morning reflection / PyCharm setup notes")
    content = st.text_area("What's on your mind?", placeholder="Write your thoughts, logs, or milestones achieved...")
    
    entry_date = st.date_input("Entry Date", value=date.today())
    
    submitted = st.form_submit_button("Save Journal Entry")
    
    if submitted:
        if not user_uuid.strip():
            st.warning("⚠️ A valid User UUID string is required to submit a journal entry.")
        elif not content.strip():
            st.warning("⚠️ Please write some content before saving.")
        else:
            final_title = title.strip() if title.strip() else f"Log - {entry_date}"
            
            # Structuring journal payload with safe string parsing
            journal_data = {
                "title": final_title,
                "content": content.strip(),
                "date": str(entry_date),
                "user_id": user_uuid.strip().strip('"').strip("'")
            }
            
            try:
                # UPDATED ENDPOINT: Pointing strictly to your verified backend route
                response = requests.post(f"{BACKEND_URL}/api/journals/", json=journal_data)

                if response.status_code in [200, 201]:
                    st.success(f"🎉 Journal entry '{final_title}' saved safely!")
                else:
                    st.error(f"❌ Failed to save entry. Server responded with status code: {response.status_code}")
                    st.json(response.json())
            except Exception as e:
                st.error(f"🔴 Connection error: {e}")

st.divider()

# --- SECTION 2: VIEW JOURNAL ENTRIES ---
st.subheader("Past Reflections")

try:
    # UPDATED ENDPOINT: Pointing strictly to your verified backend route
    response = requests.get(f"{BACKEND_URL}/api/journals/")
        
    if response.status_code == 200:
        entries = response.json()
        
        if not entries:
            st.info("No journal entries found. Start documenting your journey using the form above!")
        else:
            # Display history entries in reverse chronological card blocks
            for entry in reversed(entries):
                with st.container():
                    e_title = entry.get("title") or "Untitled Entry"
                    e_content = entry.get("content") or entry.get("text") or ""
                    e_date = entry.get("date") or entry.get("created_at") or "No date recorded"
                    e_uid = entry.get("user_id", "N/A")
                    
                    st.markdown(f"### {e_title}")
                    st.caption(f"🗓️ {e_date} | Author User UUID: `{e_uid}`")
                    st.write(e_content)
                    st.write("---")
    else:
        st.error("Could not retrieve journal data from database.")
except Exception as e:
    st.error(f"🔴 Connection error fetching journal: {e}")