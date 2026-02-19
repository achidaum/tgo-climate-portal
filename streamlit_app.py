import streamlit as st
import google.generativeai as genai
from streamlit_extras.stylable_container import stylable_container

# 1. การตั้งค่าหน้าเว็บ
st.set_page_config(page_title="TGO Climate Hub", page_icon="🌱", layout="wide")

# เชื่อมต่อ AI (ดึง API Key จาก Streamlit Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("กรุณาตั้งค่า API Key ใน Settings")

# 2. ปรับแต่งความสวยงาม (CSS)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%; border-radius: 15px; height: 120px;
        font-size: 18px; font-weight: bold; transition: 0.3s;
        background-color: white; color: #2e7d32; border: 2px solid #e0e0e0;
    }
    .stButton>button:hover { 
        transform: translateY(-5px); border: 2px solid #2e7d32; 
        background-color: #f1f8e9;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ส่วนหัวข้อ (Header)
st.title("🌱 TGO Climate & GHG Portal")
st.markdown("#### รวมทุกเครื่องมือด้านก๊าซเรือนกระจกไว้ในที่เดียว")
st.write("---")

# 4. ส่วนปุ่มทางลัดไปแอปเดิม (Dashboard Cards)
st.header("📊 เมนูบริการหลัก")
col1, col2, col3 = st.columns(3)

with col1:
    with stylable_container(key="c1", css_styles="button {background-color: #e8f5e9;}"):
        if st.button("📈 GHG Dashboard\n(วิเคราะห์ก๊าซเรือนกระจก)"):
            st.link_button("เปิดแอป", "https://gdp-dashboard-bgjbpkmeptcvbrbv5ardrm.streamlit.app/")

with col2:
    with stylable_container(key="c2", css_styles="button {background-color: #fff3e0;}"):
        if st.button("🏢 TGO Knowledge\n(คลังข้อมูล T-VER)"):
            st.link_button("เปิดแอป", "https://tgo-website-nzgnbksnlc2zc2nzf8yeec.streamlit.app/")

with col3:
    with stylable_container(key="c3", css_styles="button {background-color: #e3f2fd;}"):
        if st.button("🍃 Carbon Daily\n(ประเมินคาร์บอนรายวัน)"):
            # เปลี่ยน URL เป็นแอปที่ 3 ของคุณ (ถ้ามี)
            st.link_button("เปิดแอป", "https://tgo-website-nzgnbksnlc2zc2nzf8yeec.streamlit.app/")

st.write("---")

# 5. ส่วน AI Chatbot
st.header("🤖 สอบถาม AI ผู้เชี่ยวชาญด้าน GHG")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("พิมพ์คำถามที่นี่ เช่น คาร์บอนเครดิตคืออะไร?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # สั่งให้ AI ตอบในฐานะผู้เชี่ยวชาญ TGO
        context = f"คุณคือ AI ผู้เชี่ยวชาญจาก TGO (องค์การบริหารจัดการก๊าซเรือนกระจก) ตอบคำถามเรื่อง GHG และคาร์บอนเครดิตเป็นภาษาไทยแบบเข้าใจง่าย: {prompt}"
        try:
            response = model.generate_content(context)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.error("เกิดข้อผิดพลาดในการเชื่อมต่อ
