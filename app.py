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

poster_file = "poster_gem6.html"
logo_file = "Idi_Mana_Hakku_Header_4K_Transparent_Standard.png"
# --- BREAKING NEWS FEATURE (delete this block to remove) ---
poster_type = st.radio(
    "Poster Type",
    ["📰 Standard News", "⚡ Breaking News", "🎨 Multi-Template Studio", "🎨 Standard News — Colorful", "✨ Standard News — Gold"],
    horizontal=True,
)
if poster_type == "⚡ Breaking News":
    poster_file = os.path.join("breaking_news", "breaking_news.html")
    logo_file = "Idi_Mana_Hakku_Logo_Transparent.png"
elif poster_type == "🎨 Multi-Template Studio":
    poster_file = os.path.join("templates_studio", "poster_studio.html")
    logo_file = "Idi_Mana_Hakku_Logo_Transparent.png"
elif poster_type == "🎨 Standard News — Colorful":
    poster_file = os.path.join("standard_news_colorful", "standard_news_colorful.html")
    logo_file = "Idi_Mana_Hakku_Logo_Transparent.png"
elif poster_type == "✨ Standard News — Gold":
    poster_file = os.path.join("standard_news_gold", "standard_news_gold.html")
    logo_file = "Idi_Mana_Hakku_Logo_Transparent.png"
# --- END BREAKING NEWS FEATURE ---

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
with open(poster_file, "r", encoding="utf-8") as f:
    html_content = f.read()

# Logo injection
if os.path.exists(logo_file):
    with open(logo_file, "rb") as img:
        logo_base = base64.b64encode(img.read()).decode()
    logo_data_uri = f'data:image/png;base64,{logo_base}'
    # Handles both the root posters (logo.png) and the studio in its own folder (../logo.png)
    html_content = html_content.replace('logo.src = "logo.png";', f'logo.src = "{logo_data_uri}";')
    html_content = html_content.replace('logo.src = "../logo.png";', f'logo.src = "{logo_data_uri}";')

# Multi-Template Studio also uses the breaking-news logo (logoAlt) for its Dark & Magazine designs
alt_logo_file = os.path.join("breaking_news", "Final_Logo.png")
if os.path.exists(alt_logo_file):
    with open(alt_logo_file, "rb") as img:
        alt_logo_base = base64.b64encode(img.read()).decode()
    alt_logo_uri = f'data:image/png;base64,{alt_logo_base}'
    html_content = html_content.replace('logoAlt.src = "../breaking_news/Final_Logo.png";', f'logoAlt.src = "{alt_logo_uri}";')

# Standard News — Colorful AND Multi-Template Studio both use the transparent Idi Mana Hakku logo
# at the repo root, for both the primary `logo` and the alternate `logoAlt` references.
final_logo_file = "Idi_Mana_Hakku_Logo_Transparent.png"
if os.path.exists(final_logo_file):
    with open(final_logo_file, "rb") as img:
        final_logo_base = base64.b64encode(img.read()).decode()
    final_logo_uri = f'data:image/png;base64,{final_logo_base}'
    html_content = html_content.replace('logo.src = "../Idi_Mana_Hakku_Logo_Transparent.png";', f'logo.src = "{final_logo_uri}";')
    html_content = html_content.replace('logoAlt.src = "../Idi_Mana_Hakku_Logo_Transparent.png";', f'logoAlt.src = "{final_logo_uri}";')

# Inject active_id into JS
html_content = html_content.replace(
    "let activeID = parseInt(localStorage.getItem('newsCounter')) || 35;",
    f"let activeID = {active_id};"
)

st.components.v1.html(html_content, height=2200, scrolling=True)