import os
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Product Store", layout="wide")

st.title("🛍️ Product Showcase")

UPLOAD_DIR = "uploaded_photos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Product Upload Form
with st.expander("➕ Add New Product"):
    title = st.text_input("Product Title")
    price = st.text_input("Price (e.g. $25)")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg", "webp"])
    
    if st.button("Save Product"):
        if uploaded_file and title:
            # Save file using product title
            ext = uploaded_file.name.split(".")[-1]
            filename = f"{title} - {price}.{ext}" if price else uploaded_file.name
            file_path = os.path.join(UPLOAD_DIR, filename)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Added '{title}' to gallery!")
            st.rerun()

# Display Gallery
st.subheader("📦 Available Products")
saved_images = [f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

if saved_images:
    cols = st.columns(3)
    for idx, img_name in enumerate(saved_images):
        img_path = os.path.join(UPLOAD_DIR, img_name)
        with cols[idx % 3]:
            st.image(img_path, use_container_width=True)
            # Display name and price parsed from filename
            details = img_name.rsplit(".", 1)[0]
            st.markdown(f"### {details}")
            st.link_button("Buy / Contact via WhatsApp", "https://wa.me/YOUR_PHONE_NUMBER")