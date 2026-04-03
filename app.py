import streamlit as st
import json
import os
import base64

st.set_page_config(layout="wide", page_title="Mana Hakku Studio")

DATA_FILE = "data.json"

# --- DATABASE LOGIC ---
def get_last_id():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f: json.dump({"last_id": 35}, f)
        return 35
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f).get("last_id", 35)
    except: return 35

def increment_id():
    current = get_last_id()
    new_id = current + 1
    with open(DATA_FILE, "w") as f:
        json.dump({"last_id": new_id}, f)
    st.toast(f"✅ ID {new_id} locked in database!")

# --- UI HEADER ---
last_id = get_last_id()
active_id = last_id + 1

st.title("Mana Hakku Poster Studio")

# THE EXPLICIT BUTTON
# This is a NATIVE Streamlit button. It is 100% reliable.
col1, col2 = st.columns([2, 1])
with col1:
    st.info(f"Currently Designing News ID: **IMH-2026-{str(active_id).zfill(3)}**")
with col2:
    if st.button("🚀 SAVE & LOCK THIS ID", type="primary", use_container_width=True):
        increment_id()
        st.rerun()

# --- PREPARE HTML ---
with open("postergem5.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Logo injection
if os.path.exists("logo.png"):
    with open("logo.png", "rb") as img:
        logo_base = base64.b64encode(img.read()).decode()
    html_content = html_content.replace('logo.src = "logo.png";', f'logo.src = "data:image/png;base64,{logo_base}";')

# Inject active_id into JS
html_content = html_content.replace(
    "let activeID = parseInt(localStorage.getItem('newsCounter')) || 35;",
    f"let activeID = {active_id};"
)

st.components.v1.html(html_content, height=2200, scrolling=True)