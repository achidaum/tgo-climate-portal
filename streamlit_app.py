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
        width: 100%; border-radius: 12px;
        font-weight: bold; transition: 0.3s;
    }
    .main-btn {
        background-color: #2e7d32 !important; color: white !important;
        height: 60px !important; font-size: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. ส่วนหัวข้อ
st.title("🌱 บริการแนะนำ")

# Banner ข้อมูล
st.info("🌿 **Thai Carbon Daily Tracker** | เป้าหมายลดผลกระทบจากการใช้ชีวิตประจำวัน")
st.warning("🔍 เกณฑ์การประเมิน: อิงตามค่าเฉลี่ยประชากรไทยที่ปล่อยก๊าซประมาณ 10.4 kgCO2e ต่อวัน")

# 5. ระบบประเมิน (แบบไม่ต้องคลิกเข้าไป)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🚗 พาหนะหลักวันนี้")
    transport = st.selectbox("เลือกยานพาหนะ", ["รถยนต์ส่วนตัว (น้ำมัน)", "รถยนต์ไฟฟ้า (EV)", "รถจักรยานยนต์", "รถเมล์สาธารณะ"], key="trans")
    distance = st.number_input("ระยะทางรวม (กิโลเมตร)", min_value=0.0, value=10.0)
    
    st.write("---")
    st.subheader("💡 พลังงาน")
    air_con = st.slider("เปิดแอร์วันนี้ (ชั่วโมง)", 0, 24, 0)

with col_right:
    st.subheader("🍽️ อาหาร 3 มื้อ")
    breakfast = st.text_input("มื้อเช้า", placeholder="เช่น ข้าวเหนียวหมูปิ้ง")
    lunch = st.text_input("มื้อกลางวัน", placeholder="เช่น ข้าวกะเพราเนื้อ")
    dinner = st.text_input("มื้อเย็น", placeholder="เช่น สลัดผัก")

st.write("")
if st.button("🚀 ประเมินผลลัพธ์และดูแนวทาง", dict(key="main_calc"), use_container_width=True):
    with st.spinner('กำลังวิเคราะห์...'):
        result_prompt = f"ช่วยวิเคราะห์การปล่อยคาร์บอนจากข้อมูลนี้: รถ{transport} {distance}กม., แอร์ {air_con}ชม., อาหาร({breakfast}, {lunch}, {dinner}) ตอบเป็นข้อสรุปสั้นๆ และวิธีลด"
        try:
            res = model.generate_content(result_prompt)
            st.success("✅ ผลการวิเคราะห์จาก AI")
            st.write(res.text)
        except:
            st.error("ไม่สามารถดึงข้อมูลวิเคราะห์ได้")

st.write("---")

# 6. ส่วนถาม-ตอบ AI (ChatBot กลับมาแล้ว!)
st.subheader("💬 สอบถาม AI เกี่ยวกับก๊าซเรือนกระจก")

if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดงประวัติการคุย
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ช่องพิมพ์คำถาม (แชท)
if prompt := st.chat_input("พิมพ์คำถามที่นี่..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            chat_response = model.generate_content(f"คุณคือผู้เชี่ยวชาญ TGO ตอบคำถามนี้แบบเข้าใจง่าย: {prompt}")
            st.markdown(chat_response.text)
            st.session_state.messages.append({"role": "assistant", "content": chat_response.text})
        except Exception as e:
            st.error("AI ขัดข้องเล็กน้อย ลองใหม่อีกครั้งนะครับ")
