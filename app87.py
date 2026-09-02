import os
import json
import urllib.parse
import streamlit as st


st.set_page_config(page_title="Evaa Store", layout="wide")

st.title("🛍️ Evaa Store")

# --- CONFIGURATION SETTINGS ---
# Set your custom admin password here
ADMIN_PASSWORD = "mysecretpassword123"

# Set your WhatsApp number here (Country code + phone number, no plus, no spaces)
# Example: "967712345678"
WHATSAPP_NUMBER = "+967777322267"

DATA_FILE = "products.json"
UPLOAD_DIR = "uploaded_photos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def load_products():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_products(products):
    with open(DATA_FILE, "w") as f:
        json.dump(products, f, indent=2)

products = load_products()

# --- SIDEBAR: ADMIN LOGIN & UPLOAD FORM ---
st.sidebar.title("🔐 Admin Panel")
input_password = st.sidebar.text_input("Enter Admin Password", type="password")

if input_password == ADMIN_PASSWORD:
    st.sidebar.success("Logged in as Admin")
    st.sidebar.subheader("➕ Add New Product")
    
    with st.sidebar.form("upload_form", clear_on_submit=True):
        title = st.text_input("Product Name")
        price = st.text_input("Price (e.g., $25)")
        uploaded_file = st.file_uploader("Choose Photo", type=["jpg", "png", "jpeg", "webp"])
        submit_button = st.form_submit_button("Publish Product")

        if submit_button:
            if title and price and uploaded_file:
                file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                products.append({
                    "title": title,
                    "price": price,
                    "image": file_path
                })
                save_products(products)

                st.sidebar.success(f"Published '{title}'!")
                st.rerun()
            else:
                st.sidebar.warning("Please fill in all fields.")

elif input_password != "":
    st.sidebar.error("Incorrect password!")

# --- PUBLIC GALLERY (VISIBLE TO EVERYONE) ---
st.subheader("📦 Products")
if products:
    cols = st.columns(3)
    for idx, item in enumerate(products):
        with cols[idx % 3]:
            if os.path.exists(item["image"]):
                st.image(item["image"], use_container_width=True)
                st.markdown(f"### {item['title']}")
                st.markdown(f"**Price:** {item['price']}")
                
                # Direct WhatsApp redirect with pre-filled message
                message = f"Hello! I am interested in buying '{item['title']}' for {item['price']}."
                encoded_message = urllib.parse.quote(message)
                whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_message}"
                
                st.link_button("Buy / Contact Seller", whatsapp_url)
else:
    st.info("No products listed yet.")
