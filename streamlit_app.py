import streamlit as st
import google.generativeai as genai
from streamlit_extras.stylable_container import stylable_container

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="TGO Climate Hub", page_icon="🌱", layout="wide")

# 2. เชื่อมต่อ AI (Gemini)
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-pro')
    except Exception:
        st.error("การเชื่อมต่อ AI ขัดข้อง")
else:
    st.warning("กรุณาตั้งค่า GOOGLE_API_KEY ใน Secrets เพื่อใช้งาน AI")

# 3. ปรับแต่ง CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Sarabun', sans-serif; }
    .stButton>button {
        width: 100%; border-radius: 15px; height: 80px;
        font-size: 18px; font-weight: bold; transition: 0.3s;
        background-color: white; color: #2e7d32; border: 2px solid #e0e0e0;
    }
    .stButton>button:hover { 
        transform: translateY(-3px); border: 2px solid #2e7d32; 
        background-color: #f1f8e9;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. ส่วนหัวข้อ
st.title("🌱 TGO Climate & GHG Portal")
st.markdown("#### ศูนย์รวมเครื่องมือจัดการก๊าซเรือนกระจกและคาร์บอนเครดิต")
st.write("---")

# 5. ระบบประเมินคาร์บอนรายวัน (Daily Tracker) - ตามรูปที่คุณต้องการ
st.subheader("🍃 บริการแนะนำ: Thai Carbon Daily Tracker")
st.info("เป้าหมายลดผลกระทบจากการใช้ชีวิตประจำวัน และร่วมกันปรับลดการปล่อยก๊าซเรือนกระจก")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🚗 พาหนะหลักวันนี้")
    transport = st.selectbox("เลือกประเภทการเดินทาง", ["รถยนต์ส่วนตัว (น้ำมัน)", "รถยนต์ไฟฟ้า (EV)", "รถจักรยานยนต์", "รถเมล์สาธารณะ/ไฟฟ้า"], key="trans")
    distance = st.number_input("ระยะทางรวม (กิโลเมตร)", min_value=0.0, value=10.0)
    
    st.write("---")
    st.subheader("💡 พลังงาน")
    air_con = st.slider("เปิดแอร์วันนี้ (ชั่วโมง)", 0, 24, 0)

with col_right:
    st.subheader("🍽️ อาหาร 3 มื้อ")
    breakfast = st.text
