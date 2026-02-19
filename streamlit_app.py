import streamlit as st
import google.generativeai as genai
from streamlit_extras.stylable_container import stylable_container

# 1. การตั้งค่าหน้าเว็บ (Web Configuration)
st.set_page_config(page_title="TGO Climate Hub", page_icon="🌱", layout="wide")

# เชื่อมต่อ AI (ดึง API Key จาก Streamlit Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"การเชื่อมต่อ AI ขัดข้อง: {e}")
else:
    st.warning("กรุณาตั้งค่า GOOGLE_API_KEY ในหน้า Secrets ของ Streamlit Cloud")

# 2. ปรับแต่งความสวยงามด้วย CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Sarabun', sans-serif; }
    .main { background-color: #f8faf9; }
    .stButton>button {
        width: 100%; border-radius: 15px; height: 120px;
        font-size: 20px; font-weight: bold; transition: 0.3s;
        background-color: white; color: #2e7d32; border: 2px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stButton>button:hover { 
        transform: translateY(-5px); border: 2px solid #2e7d32; 
        background-color: #f1f8e9; box-shadow: 0 10px 15px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ส่วนหัวข้อหลัก (Header)
st.title("🌱 TGO Climate & GHG Portal")
st.markdown("#### ศูนย์รวมเครื่องมือจัดการก๊าซเรือนกระจกและคาร์บอนเครดิตแบบครบวงจร")
st.write("---")

# 4. ส่วนปุ่มทางลัด (Dashboard Cards) - เชื่อมลิงก์แอปที่คุณทำไว้
st.header("📊 เมนูบริการและแดชบอร์ด")
col1, col2, col3 = st.columns(3)

with col1:
    with stylable_container(key="c1", css_styles="button {background-color: #e8f5e9;}"):
        if st.button("📈 Green House Gas ก๊าซเรือนกระจก"):
            st.link_button("👉 คลิกเพื่อดู", "https://gdp-dashboard-bgjbpkmeptcvbrbv5ardrm.streamlit.app/")

with col2:
    with stylable_container(key="c2", css_styles="button {background-color: #fff3e0;}"):
        if st.button("🏢 TGO "):
            st.link_button("👉 คลิกเพื่อดู", "https://tgo-website-nzgnbksnlc2zc2nzf8yeec.streamlit.app/")

with col3:
    with stylable_container(key="c3", css_styles="button {background-color: #e3f2fd;}"):
        if st.button("🍃 ประเมินคาร์บอนรายวัน"):
            # ลิงก์ไปยังแอปประเมินคาร์บอนรายวันของคุณ
            st.link_button("👉 คลิกเพื่อดู", "https://tgo-website-nzgnbksnlc2zc2nzf8yeec.streamlit.app/")

st.write("---")

# 5. ส่วน AI Expert Chat (TGO Smart Consultant)
st.header("🤖 TGO Smart Consultant")
st.markdown("##### สงสัยเรื่อง T-VER หรือคาร์บอนเครดิต? ปรึกษาผู้เชี่ยวชาญ AI ได้ที่นี่")

if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดงประวัติการสนทนา
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ช่องรับคำถาม
if prompt := st.chat_input("ถามคำถามเกี่ยวกับ GHG หรือ คาร์บอนเครดิต..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # การตั้งค่าบริบทให้ AI ฉลาดอิงตามข้อมูล TGO
        context = f"""
        คุณคือ 'TGO Smart Consultant' ผู้เชี่ยวชาญจากองค์การบริหารจัดการก๊าซเรือนกระจก (อบก.) 
        หน้าที่ของคุณคือให้ข้อมูลที่ถูกต้องเกี่ยวกับ:
        1. โครงการ T-VER (Thailand Voluntary Emission Reduction Program)
        2. การซื้อขายและโอนคาร์บอนเครดิตในประเทศไทย
        3. การคำนวณคาร์บอนฟุตพริ้นท์ตามมาตรฐาน TGO
        4. เป้าหมาย Carbon Neutrality และ Net Zero ของประเทศ
        
        กฎการตอบ: ตอบเป็นภาษาไทยที่สุภาพ ทันสมัย และกระชับ หากไม่ทราบข้อมูลแน่ชัดให้แนะนำให้ติดต่อเว็บไซต์ tgo.or.th
        
        คำถาม: {prompt}
        """
        
        try:
            response = model.generate_content(context)
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error("ขออภัย ระบบประมวลผลขัดข้อง กรุณาลองใหม่อีกครั้ง")
