import os
import json
import urllib.parse
import streamlit as st

st.set_page_config(page_title="Evaa Store", layout="wide")

st.title("🛍️ Evaa Store")

# --- CONFIGURATION SETTINGS ---
ADMIN_PASSWORD = "123"
WHATSAPP_NUMBER = "YOUR_PHONE_NUMBER_HERE"

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

def get_product_images(item):
    if "images" in item and item["images"]:
        return item["images"]
    elif "image" in item and item["image"]:
        return [item["image"]]
    return []

products = load_products()

# --- SIDEBAR: ADMIN PANEL ---
st.sidebar.title("🔐 Admin Panel")
input_password = st.sidebar.text_input("Enter Admin Password", type="password")

if input_password == ADMIN_PASSWORD:
    st.sidebar.success("Logged in as Admin")
    
    # 1. ADD PRODUCT SECTION
    st.sidebar.subheader("➕ Add New Product")
    with st.sidebar.form("upload_form", clear_on_submit=True):
        title = st.text_input("Product Name")
        price = st.text_input("Price (e.g., $25)")
        uploaded_files = st.file_uploader(
            "Choose Photos (Select up to 4)", 
            type=["jpg", "png", "jpeg", "webp"], 
            accept_multiple_files=True
        )
        submit_button = st.form_submit_button("Publish Product")

        if submit_button:
            if title and price and uploaded_files:
                image_paths = []
                for idx, uploaded_file in enumerate(uploaded_files):
                    filename = f"{title}_{idx}_{uploaded_file.name}"
                    file_path = os.path.join(UPLOAD_DIR, filename)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    image_paths.append(file_path)

                products.append({
                    "title": title,
                    "price": price,
                    "images": image_paths
                })
                save_products(products)

                st.sidebar.success(f"Published '{title}' with {len(image_paths)} photo(s)!")
                st.rerun()
            else:
                st.sidebar.warning("Please fill in all fields and choose at least 1 image.")

    st.sidebar.divider()

    # 2. EDIT PRICE SECTION
    st.sidebar.subheader("✏️ Update Product Price")
    if products:
        product_names = [p["title"] for p in products]
        selected_title_to_edit = st.sidebar.selectbox("Select product to edit:", product_names, key="edit_select")
        
        current_item = next((p for p in products if p["title"] == selected_title_to_edit), None)
        
        if current_item:
            new_price = st.sidebar.text_input("New Price:", value=current_item["price"], key="edit_price_input")
            if st.sidebar.button("Update Price"):
                current_item["price"] = new_price
                save_products(products)
                st.sidebar.success(f"Price updated for '{selected_title_to_edit}'!")
                st.rerun()
    else:
        st.sidebar.info("No products available to edit.")

    st.sidebar.divider()

    # 3. DELETE PRODUCT SECTION
    st.sidebar.subheader("🗑️ Delete Product")
    if products:
        product_names = [p["title"] for p in products]
        selected_title = st.sidebar.selectbox("Select product to remove:", product_names, key="delete_select")
        
        if st.sidebar.button("Delete Product", type="primary"):
            item_to_delete = next((p for p in products if p["title"] == selected_title), None)
            
            if item_to_delete:
                for img_path in get_product_images(item_to_delete):
                    if os.path.exists(img_path):
                        os.remove(img_path)
                
                products = [p for p in products if p["title"] != selected_title]
                save_products(products)
                
                st.sidebar.success(f"Deleted '{selected_title}'!")
                st.rerun()
    else:
        st.sidebar.info("No products available to delete.")

elif input_password != "":
    st.sidebar.error("Incorrect password!")

# --- PUBLIC GALLERY ---
st.subheader("📦 Products")
if products:
    cols = st.columns(3)
    for idx, item in enumerate(products):
        with cols[idx % 3]:
            images = get_product_images(item)
            valid_images = [img for img in images if os.path.exists(img)]
            
            if valid_images:
                if len(valid_images) == 1:
                    st.image(valid_images[0], use_container_width=True)
                else:
                    tabs = st.tabs([f"Photo {i+1}" for i in range(len(valid_images))])
                    for t_idx, tab in enumerate(tabs):
                        with tab:
                            st.image(valid_images[t_idx], use_container_width=True)
                            
                st.markdown(f"### {item['title']}")
                st.markdown(f"**Price:** {item['price']}")
                
                message = f"Hello! I am interested in buying '{item['title']}' for {item['price']}."
                encoded_message = urllib.parse.quote(message)
                whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_message}"
                
                st.link_button("Buy / Contact Seller", whatsapp_url)
else:
    st.info("No products listed yet.")
