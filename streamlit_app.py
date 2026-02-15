import streamlit as st
from google import genai
from google.genai import types

# הגדרות עיצוב RTL ו-PRO
st.set_page_config(page_title="מבקר מע\"מ PRO", layout="wide")
st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    div[data-testid="stSidebar"] { direction: rtl; text-align: right; }
    div.stButton > button { background-color: #007bff; color: white; width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ מבקר מע״מ וזירת מלחמה - גרסת PRO")

# חיבור למפתח ה-API
api_key = st.secrets.get("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

# סרגל צד להעלאת מסמכים
with st.sidebar:
    st.header("🗂️ ניהול תיק לקוח")
    uploaded_file = st.file_uploader("העלה שומה, השגה או פסיקה (PDF)", type="pdf")
    st.success("סטטוס: מחובר למסלול PAID TIER")
    st.info("מודל פעיל: Gemini 2.0 Flash")

# אזור הקלט
user_input = st.text_area("פרט את המקרה או בקש ניתוח למסמך שהעלית:", height=200, 
                          placeholder="למשל: נתח האם ניתן לנכות מס תשומות על רכישת רכב ספורט בנסיבות הבאות...")

if st.button("הפעל ניתוח אסטרטגי"):
    if not user_input:
        st.warning("אנא הזן טקסט לניתוח.")
    else:
        with st.spinner("מבצע ניתוח משפטי עמוק מול ספרות נמדר..."):
            parts = [user_input]
            if uploaded_file:
                parts.append(types.Part.from_bytes(data=uploaded_file.read(), mime_type="application/pdf"))

            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    config=types.GenerateContentConfig(
                        system_instruction="אתה מומחה מס ישראלי בכיר. נתח את המקרה מול חוק מע\"מ וספרות נמדר. ענה בעברית מיושרת לימין עם סעיפי חוק רלוונטיים."
                    ),
                    contents=parts
                )
                st.markdown("---")
                st.markdown(f'<div style="direction: rtl; text-align: right; padding: 15px; background: #f0f2f6; border-radius: 10px;">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"שגיאה: {e}")
