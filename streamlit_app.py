import streamlit as st
import os
from google import genai
from google.genai import types

# הגדרת כיוון כתיבה לימין (RTL)
st.markdown('<div style="direction: rtl; text-align: right;">', unsafe_allow_html=True)

st.title("🛡️ מערכת מבקר מע״מ וזירת מלחמה")

# תפריט צד (Sidebar)
with st.sidebar:
    st.header("היסטוריה")
    st.write('כאן תופיע היסטוריית הדו"חות שלך') # השורה המתוקנת

# חיבור ל-API Key מתוך ה-Secrets
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("שגיאה בחיבור למפתח ה-API. וודא שהגדרת אותו ב-Secrets.")

# ממשק המשתמש
user_input = st.text_area("פרט את המקרה או הדבק טענות מהצד השני:")

if st.button("הפעל ניתוח מקצועי"):
    if user_input:
        with st.spinner("מנתח על בסיס ספרות מקצועית..."):
            try:
                response = client.models.generate_content(
                    model="gemini-1.5-flash" # המודל העדכני ביותר
                    contents=user_input
                )
                st.markdown(f'<div style="direction: rtl;">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"שגיאה בהרצת הניתוח: {e}")
    else:
        st.error("אנא הזן טקסט לניתוח")

st.markdown('</div>', unsafe_allow_html=True)
