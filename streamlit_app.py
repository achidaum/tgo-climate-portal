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
    breakfast = st.text_input("มื้อเช้า", placeholder="เช่น ข้าวเหนียวหมูปิ้ง")
    lunch = st.text_input("มื้อกลางวัน", placeholder="เช่น ข้าวกะเพราเนื้อ")
    dinner = st.text_input("มื้อเย็น", placeholder="เช่น สลัดผัก")

# ปุ่มประเมินผล
if st.button("🚀 ประเมินผลลัพธ์และดูแนวทาง", use_container_width=True):
    with st.spinner('AI กำลังวิเคราะห์ข้อมูลของคุณ...'):
        calc_prompt = f"วิเคราะห์การปล่อยคาร์บอน: {transport} {distance}กม., แอร์ {air_con}ชม., อาหาร({breakfast}, {lunch}, {dinner}) ให้คำแนะนำสั้นๆ"
        try:
            res = model.generate_content(calc_prompt)
            st.success("✅ ผลการวิเคราะห์จาก AI")
            st.write(res.text)
        except:
            st.error("ไม่สามารถเชื่อมต่อ AI เพื่อประเมินผลได้")

st.write("---")

# 6. ส่วนข้อมูลวิเคราะห์และคลังความรู้ TGO (กลับมาแล้ว!)
st.subheader("📊 ข้อมูลวิเคราะห์และคลังความรู้")
c1, c2 = st.columns(2)

with c1:
    with stylable_container(key="c1", css_styles="button {background-color: #ffffff;}"):
        if st.button("📈 GHG Dashboard\n(วิเคราะห์ก๊าซเรือนกระจก)"):
            st.link_button("👉 ดูข้อมูลวิเคราะห์", "https://gdp-dashboard-bgjbpkmeptcvbrbv5ardrm.streamlit.app/")

with c2:
    with stylable_container(key="c2", css_styles="button {background-color: #ffffff;}"):
        if st.button("📚 คลังความรู้ TGO\n(Knowledge Center)"):
            st.link_button("👉 เข้าสู่คลังความรู้", "https://www.tgo.or.th/")

st.write("---")

# 7. ระบบ AI ChatBot (ช่องถามคำถาม)
st.subheader("💬 สอบถาม AI เกี่ยวกับก๊าซเรือนกระจก")

if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดงประวัติการสนทนา
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ช่องรับคำถาม (จะอยู่ล่างสุดเสมอ)
if prompt := st.chat_input("พิมพ์คำถามที่นี่..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            chat_response = model.generate_content(f"คุณคือผู้เชี่ยวชาญจาก TGO ตอบคำถามนี้: {prompt}")
            st.markdown(chat_response.text)
            st.session_state.messages.append({"role": "assistant", "content": chat_response.text})
        except:
            st.error("AI ขัดข้องเล็กน้อย")
