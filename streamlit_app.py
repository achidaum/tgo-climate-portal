import streamlit as st
import google.generativeai as genai
from streamlit_extras.stylable_container import stylable_container

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="TGO Climate Hub", page_icon="🌱", layout="wide")

# เชื่อมต่อ AI
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-pro')
    except Exception:
        st.error("การเชื่อมต่อ AI ขัดข้อง")
else:
    st.warning("กรุณาตั้งค่า GOOGLE_API_KEY ใน Secrets")

# 2. ปรับแต่ง CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Sarabun', sans-serif; }
    .stButton>button {
        width: 100%; border-radius: 15px; height: 100px;
        font-size: 20px; font-weight: bold; transition: 0.3s;
        background-color: white; color: #2e7d32; border: 2px solid #e0e0e0;
    }
    .stButton>button:hover { 
        transform: translateY(-5px); border: 2px solid #2e7d32; 
        background-color: #f1f8e9;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ส่วนหัวข้อ
st.title("🌱 TGO Climate & GHG Portal")
st.markdown("#### ศูนย์รวมเครื่องมือจัดการก๊าซเรือนกระจกและคาร์บอนเครดิต")
st.write("---")

# 4. เมนู Dashboard
st.subheader("🍃 บริการแนะนำ")

# แก้ไขบรรทัดที่ 50 ให้สั้นลงเพื่อกันก๊อปปี้ขาด
with stylable_container(key="highlight", css_styles="button {background-color: #e8f5e9; border: 2px solid #2e7d32;}"):
    if st.button("✨ ระบบประเมินคาร์บอนรายวัน (Daily Carbon Footprint)"):
        st.link_button("👉 คลิกเพื่อเข้าสู่ระบบประเมิน", "https://6ezbjfuuk36bisipg8y8bh.streamlit.app/")

st.write("---")

st.subheader("📊 ข้อมูลวิเคราะห์และคลังความรู้")
col1, col2 = st.columns(2)

with col1:
    with stylable_container(key="c1", css_styles="button {background-color: #ffffff;}"):
        if st.button("📈 GHG Dashboard\n(วิเคราะห์ก๊าซเรือนกระจก)"):
            st.link_button("👉 ดูข้อมูลวิเคราะห์", "https://gdp-dashboard-bgjbpkmeptcvbrbv5ardrm.streamlit.app/")

with col
