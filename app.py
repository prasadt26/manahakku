import streamlit as st
import base64

st.set_page_config(layout="wide")

st.title("Mana Hakku Poster Generator")

# read HTML file
with open("postergem2.html", "r", encoding="utf-8") as f:
    html = f.read()

# convert logo to base64
with open("logo.png", "rb") as img:
    logo_base64 = base64.b64encode(img.read()).decode()

# replace logo path inside HTML
html = html.replace(
    'logo.src = "logo.png";',
    f'logo.src = "data:image/png;base64,{logo_base64}";'
)

# render HTML
st.components.v1.html(
    html,
    height=1900,
    scrolling=True
)