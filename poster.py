import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Poster Generator", layout="centered")

st.title("🖼️ Telugu Poster Generator")

st.write("Upload an image and add Telugu headline and matter text.")

# Inputs
uploaded_image = st.file_uploader("Upload Background Image", type=["png","jpg","jpeg"])

headline = st.text_input("Enter Headline (Telugu supported)")

matter = st.text_area("Enter Matter / Description (Telugu supported)")

# Telugu font (download NotoSansTelugu-Regular.ttf)
font_path = "C:\\Users\\PrasadThipparthi\\Downloads\\Noto_Sans_Telugu\\NotoSansTelugu-VariableFont_wdth,wght.ttf"

if uploaded_image is not None:

    image = Image.open(uploaded_image).convert("RGB")

    draw = ImageDraw.Draw(image)

    width, height = image.size

    # Fonts
    headline_font = ImageFont.truetype(font_path, 60)
    matter_font = ImageFont.truetype(font_path, 35)

    # Headline position
    headline_position = (50, 50)

    # Matter position
    matter_position = (50, 150)

    # Draw text
    draw.text(headline_position, headline, font=headline_font, fill="black")
    draw.text(matter_position, matter, font=matter_font, fill="black")

    st.image(image, caption="Generated Poster", use_column_width=True)

    # Download option
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")

    st.download_button(
        label="⬇ Download Image",
        data=img_bytes.getvalue(),
        file_name="poster.png",
        mime="image/png"
    )