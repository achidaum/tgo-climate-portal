import streamlit as st
import google.generativeai as genai
from streamlit_extras.stylable_container import stylable_container

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
    st.warning("กรุณาตั้งค่า GOOGLE_API_KEY ในหน้า Secrets ของ Streamlit Cloud")

# 2. ปรับแต่งความสวยงามด้วย CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Sarabun', sans-serif; }
    .main { background-color: #f8faf9; }
    .stButton>button {
        width: 100%; border-radius: 15px; height: 100px;
        font-size: 20px; font-weight: bold; transition: 0.3s;
        background-color: white; color: #2e7d32; border: 2px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stButton>button:hover { 
        transform: translateY(-5px); border: 2px solid #2e7d32; 
        background-color: #f1f8e9; box-shadow: 0 10px 15px rgba(0,0,0,0.1);
    }
    .highlight-card > div {
        border: 2px solid #2e7d32 !important;
        background-color: #f1f8e9 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ส่วนหัวข้อหลัก
st.title("🌱 TGO Climate & GHG Portal")
st.markdown("#### ศูนย์รวมเครื่องมือจัดการก๊าซเรือนกระจกและคาร์บอนเครดิตแบบครบวงจร")
st.write("---")

# 4. เมนูบริการและแดชบอร์ด

# --- ส่วนที่ 1: ประเมินคาร์บอนรายวัน (โดดเด่นอยู่บรรทัดแรก) ---
st.subheader("🍃 บริการแนะนำ")
with stylable_container(key="highlight", css_styles="button {background-color: #e8f5e9; border: 2px solid #2e7d
