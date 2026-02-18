import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image

# --- 1. ตั้งค่าหน้าเว็บและ Theme สีพาสเทล ---
st.set_page_config(page_title="Lost & Found Community", page_icon="🧸", layout="centered")

# Custom CSS เพื่อความน่ารักและสีพาสเทล
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Kanit', sans-serif;
    }
    
    /* พื้นหลัง */
    .stApp {
        background-color: #FDFBF7;
    }
    
    /* หัวข้อหลัก */
    h1 {
        color: #88B3C8;
        text-align: center;
        text-shadow: 2px 2px #FFF;
    }
    
    /* การ์ดสินค้า */
    .css-card {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 2px solid #F0F0F0;
    }
    
    /* ปุ่มกด */
    .stButton>button {
        border-radius: 20px;
        background-color: #FFB7B2;
        color: white;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #FF9E99;
        color: white;
    }
    
    /* Badges */
    .badge-lost {
        background-color: #FFB7B2;
        color: white;
        padding: 5px 10px;
        border-radius: 10px;
        font-size: 0.8rem;
    }
    .badge-found {
        background-color: #B5EAD7;
        color: #555;
        padding: 5px 10px;
        border-radius: 10px;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. ระบบจัดการข้อมูล (จำลอง Database) ---
if 'data' not in st.session_state:
    st.session_state['data'] = [
        # ข้อมูลตัวอย่าง
        {"type": "Lost", "name": "น้องแมวส้ม", "location": "หน้าหมู่บ้าน", "desc": "ปลอกคอสีแดง", "contact": "081-234-5678", "time": "10 นาทีที่แล้ว", "img": None},
        {"type": "Found", "name": "กระเป๋าตังค์", "location": "โรงอาหาร", "desc": "ลายการ์ตูน", "contact": "ครูเวร", "time": "1 ชม. ที่แล้ว", "img": None}
    ]

def add_item(type_, name, loc, desc, contact, img_file):
    img_data = None
    if img_file is not None:
        # แปลงรูปภาพเป็น Base64 เพื่อเก็บใน Session (แบบง่าย)
        img = Image.open(img_file)
        # ย่อรูปก่อนเก็บ
        img.thumbnail((300, 300))
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_data = base64.b64encode(buffered.getvalue()).decode()

    new_item = {
        "type": type_,
        "name": name,
        "location": loc,
        "desc": desc,
        "contact": contact,
        "time": datetime.now().strftime("%d/%m %H:%M"),
        "img": img_data
    }
    st.session_state['data'].insert(0, new_item) # เพิ่มข้อมูลใหม่ไว้บนสุด

# --- 3. ส่วนแสดงผล (UI) ---

st.title("🧸 Lost & Found")
st.caption("ศูนย์รวมแจ้งของหาย-เก็บได้ (Community)")

# เมนูเปลี่ยนหน้า (Tabs)
tab1, tab2 = st.tabs(["📢 หน้าฟีดข่าว", "➕ แจ้งเรื่องใหม่"])

# --- TAB 1: หน้าฟีด ---
with tab1:
    st.subheader("รายการล่าสุด")
    
    # ตัวกรอง
    filter_option = st.radio("เลือกดูรายการ:", ["ทั้งหมด", "ของหาย (Lost)", "เก็บได้ (Found)"], horizontal=True)
    
    # Loop แสดงข้อมูล
    for item in st.session_state['data']:
        # Logic การกรอง
        if filter_option == "ของหาย (Lost)" and item['type'] != "Lost": continue
        if filter_option == "เก็บได้ (Found)" and item['type'] != "Found": continue

        # การ์ดแสดงผล
        with st.container():
            st.markdown('<div class="css-card">', unsafe_allow_html=True)
            
            # Badge สี
            badge_class = "badge-lost" if item['type'] == "Lost" else "badge-found"
            badge_text = "😭 ของหาย" if item['type'] == "Lost" else "🥰 เก็บได้"
            
            c1, c2 = st.columns([1, 2])
            
            with c1:
                if item['img']:
                    st.markdown(f'<img src="data:image/jpeg;base64,{item["img"]}" style="width:100%; border-radius:10px;">', unsafe_allow_html=True)
                else:
                    st.info("ไม่มีรูป")
            
            with c2:
                st.markdown(f'<span class="{badge_class}">{badge_text}</span>', unsafe_allow_html=True)
                st.markdown(f"### {item['name']}")
                st.markdown(f"📍 **สถานที่:** {item['location']}")
                st.markdown(f"📝 {item['desc']}")
                st.markdown(f"📞 **ติดต่อ:** `{item['contact']}`")
                st.caption(f"🕒 {item['time']}")

            st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: หน้าแจ้งเรื่อง ---
with tab2:
    st.subheader("กรอกข้อมูล")
    
    with st.form("post_form", clear_on_submit=True):
        col_type1, col_type2 = st.columns(2)
        with col_type1:
            is_lost = st.checkbox("😭 ของหาย (Lost)")
        with col_type2:
            is_found = st.checkbox("🥰 เก็บได้ (Found)")
            
        # Logic เลือกประเภท (ถ้าไม่เลือกเลย ให้เป็น Lost)
        post_type = "Found" if is_found and not is_lost else "Lost"
        
        name = st.text_input("ชื่อสิ่งของ", placeholder="เช่น กุญแจรถ, แมว")
        loc = st.text_input("สถานที่ (หาย/เจอ)", placeholder="เช่น โรงอาหาร")
        desc = st.text_area("รายละเอียด", placeholder="ลักษณะเด่น สี...")
        contact = st.text_input("ช่องทางติดต่อ", placeholder="Line ID หรือ เบอร์โทร")
        uploaded_file = st.file_uploader("รูปภาพ (ถ้ามี)", type=['png', 'jpg', 'jpeg'])
        
        submitted = st.form_submit_button("✨ โพสต์ประกาศ")
        
        if submitted:
            if not name or not contact:
                st.error("กรุณากรอกชื่อสิ่งของและช่องทางติดต่อ")
            else:
                add_item(post_type, name, loc, desc, contact, uploaded_file)
                st.success("โพสต์เรียบร้อย! กลับไปดูที่หน้าฟีดได้เลย")
