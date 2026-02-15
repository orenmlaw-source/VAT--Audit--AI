import streamlit as st
from google import genai
from google.genai import types

# הגדרות תצוגה לימין (RTL) ועיצוב מקצועי
st.set_page_config(page_title="מבקר מע\"מ PRO", layout="wide")
st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    div[data-testid="stSidebar"] { direction: rtl; text-align: right; }
    div.stButton > button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ מערכת מבקר מע״מ וזירת מלחמה - PRO")

# חיבור ל-API Key מתוך ה-Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("שגיאה: מפתח ה-API לא נמצא בהגדרות ה-Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# הוראות מערכת אסטרטגיות (ה"מוח" של המערכת)
SYSTEM_PROMPT = """
אתה "מבקר מע"מ חכם" ואסטרטג משפטי בכיר המתמחה בחוק מע"מ הישראלי.
תפקידך: לנתח מקרים ומסמכים אל מול ספרות מקצועית (נמדר, פרידמן) וסעיפי החוק (דגש על סעיפים 38 ו-41).
בצע ניתוח בשני ערוצים:
1. ביקורת יזומה: זיהוי חשיפות מס פוטנציאליות.
2. זירת מלחמה: מציאת פרצות וטענות נגד לטענות רשות המסים.
דרישות: עברית רשמית, תשובות מנומקות עם הפניות לחוק, יישור לימין.
"""

# סרגל צד לניהול תיק
with st.sidebar:
    st.header("🗂️ ניהול תיק לקוח")
    uploaded_file = st.file_uploader("העלה שומה, השגה או פסק דין (PDF)", type="pdf")
    st.divider()
    st.success("סטטוס מערכת: PRO מחובר")
    st.info("המודל הפעיל: Gemini 2.0 Flash")

# אזור הקלט המרכזי
user_query = st.text_area("פרט את המקרה המשפטי או בקש ניתוח למסמך שהעלית:", 
                          placeholder="למשל: האם ניתן לנכות תשומות על רכב ספורט בנסיבות של...", height=200)

if st.button("הפעל ניתוח אסטרטגי"):
    if not user_query:
        st.warning("אנא הזן טקסט או העלה מסמך לניתוח.")
    else:
        with st.spinner("מבצע ניתוח משפטי מעמיק..."):
            # הכנת התוכן (טקסט + קובץ PDF אם הועלה)
            content_parts = [user_query]
            if uploaded_file:
                content_parts.append(types.Part.from_bytes(data=uploaded_file.read(), mime_type="application/pdf"))

            try:
                # הרצת המודל עם הגדרות PRO
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.2 # דיוק גבוה
                    ),
                    contents=content_parts
                )
                st.markdown("### 📝 תוצאות הניתוח:")
                st.markdown(f'<div style="direction: rtl; text-align: right; background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-right: 5px solid #007bff;">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"שגיאה בהרצת הניתוח: {e}")

st.markdown('---')
st.caption("פיתוח: זירת מלחמה משפטית - בינה מלאכותית בשירות המס")
