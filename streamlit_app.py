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
    st.warning("กรุณาตั้งค่า GOOGLE_API_KEY ใน Secrets เพื่อใช้งาน AI Chat")

# 3. ปรับแต่ง CSS
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

# 4. ส่วนหัวข้อ
st.title("🌱 TGO Climate & GHG Portal")
st.markdown("#### ศูนย์รวมเครื่องมือจัดการก๊าซเรือนกระจกและคาร์บอนเครดิต")
st.write("---")

# 5. เมนู Dashboard
st.subheader("🍃 บริการแนะนำ")

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

with col2:
    with stylable_container(key="c2", css_styles="button {background-color: #ffffff;}"):
        if st.button("📚 คลังความรู้ TGO\n(Knowledge Center)"):
            st.link_button("👉 เข้าสู่คลังความรู้", "https://www.tgo.or.th/")

st.write("---")

# 6. ระบบ AI ChatBot (ส่วนที่เพิ่มกลับมา)
st.subheader("💬 สอบถามเพิ่มเติม")

if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดงประวัติการแชท
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ช่องรับคำถาม
if prompt := st.chat_input("พิมพ์คำถามที่นี่... (เช่น คาร์บอนเครดิตคืออะไร?)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ให้ AI ตอบโดยเน้นบริบทเรื่อง Climate/TGO
            full_prompt = f"คุณคือผู้เชี่ยวชาญด้านก๊าซเรือนกระจกของ TGO จงตอบคำถามนี้: {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"AI ไม่สามารถตอบได้ในขณะนี้: {e}")
