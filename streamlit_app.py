import streamlit as st
import google.generativeai as genai

# 1. การตั้งค่าหน้าเว็บ
st.set_page_config(page_title="TGO Climate Hub", page_icon="🌱", layout="wide")

# เชื่อมต่อ AI
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"การเชื่อมต่อ AI ขัดข้อง")
else:
    st.warning("กรุณาตั้งค่า API Key ใน Secrets")

# 2. ส่วนหัวข้อหลัก
st.title("🌱 TGO Climate & GHG Portal")
st.markdown("#### ศูนย์รวมเครื่องมือจัดการก๊าซเรือนกระจกและคาร์บอนเครดิตแบบครบวงจร")
st.write("---")

# 3. ส่วน AI Chatbot (ย้ายขึ้นมาให้เข้าถึงง่าย)
with st.expander("🤖 ปรึกษาผู้เชี่ยวชาญ AI ด้านคาร์บอน (คลิกเพื่อเปิด/ปิด)", expanded=False):
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("ถามคำถามเกี่ยวกับ GHG หรือ คาร์บอนเครดิต..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            context = f"คุณคือผู้เชี่ยวชาญจาก TGO ตอบคำถามเรื่อง GHG และคาร์บอนเครดิตเป็นภาษาไทยแบบมืออาชีพ: {prompt}"
            try:
                response = model.generate_content(context)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error("AI ไม่สามารถตอบได้ในขณะนี้")

st.write("---")

# 4. ส่วน Dashboard (แบบโชว์หน้าเว็บเลย)

# --- แถวที่ 1: ประเมินคาร์บอนรายวัน (เด่นที่สุด) ---
st.header("🍃 ระบบประเมินคาร์บอนรายวัน")
# ฝังหน้าเว็บแอปประเมินคาร์บอน
st.components.v1.iframe("https://tgo-website-nzgnbksnlc2zc2nzf8yeec.streamlit.app/?embed=true", height=600, scrolling=True)

st.write("---")

# --- แถวที่ 2: อีก 2 แอปวางคู่กัน ---
st.header("📊 ข้อมูลวิเคราะห์และคลังความรู้")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Green House Gas Dashboard")
    # ฝังหน้าเว็บแอป GHG
    st.components.v1.iframe("https://gdp-dashboard-bgjbpkmeptcvbrbv5ardrm.streamlit.app/?embed=true", height=500, scrolling=True)

with col2:
    st.subheader("🏢 TGO Knowledge Base")
    # ฝังหน้าเว็บแอป TGO Knowledge
    st.components.v1.iframe("https://tgo-website-nzgnbksnlc2zc2nzf8yeec.streamlit.app/?embed=true", height=500, scrolling=True)

# 5. ส่วนท้าย
st.write("---")
st.caption("© 2026 TGO Climate Hub | ข้อมูลอ้างอิงมาตรฐานองค์การบริหารจัดการก๊าซเรือนกระจก")
