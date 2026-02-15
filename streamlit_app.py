import streamlit as st
from google import genai
from google.genai import types

# 1. הגדרות תצוגה ועיצוב RTL
st.set_page_config(page_title="מבקר מע\"מ PRO - War Room", layout="wide")

st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    div[data-testid="stSidebar"] { direction: rtl; text-align: right; }
    div.stButton > button { 
        background-color: #28a745; 
        color: white; 
        width: 100%; 
        border-radius: 8px; 
        font-weight: bold;
    }
    .report-container {
        direction: rtl; 
        text-align: right; 
        padding: 25px; 
        background-color: #ffffff; 
        border: 1px solid #dee2e6;
        border-right: 8px solid #28a745;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ זירת מלחמה משפטית: ניתוח מבוסס תאמ"ו ומאגר מקורות")

# 2. חיבור ל-API
api_key = st.secrets.get("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

# 3. פונקציה לשליפת רשימת הקבצים מהמאגר
def get_existing_files():
    try:
        files = client.files.list()
        return list(files)
    except Exception:
        return []

# 4. המוח המשפטי - מבוסס תאמ"ו, פסיקה וספרות
SYSTEM_PROMPT = """
אתה "אסטרטג מס בכיר" המבצע ביקורת עומק לדיווחי מע"מ בגרסת War Room.
תפקידך: לספק ניתוח משפטי שמשלב את כל מקורות הדין בישראל.

המקורות עליהם עליך להתבסס:
1. חוק מע"מ ותקנותיו: דגש על סעיפים 1, 12, 30(א), 38, 41 ותקנות 14, 15א, 16 ו-18.
2. תאמ"ו (תדריך אגף מס ערך מוסף): עליך לציין במפורש מהי עמדת הרשות הרשמית לפי התאמ"ו לכל סוגיה.
3. פסיקת בתי המשפט: הלכות אלקה, פליי-איט, קינטון, סלע, אהרוני, נווה גד ופסיקה מחוזית עדכנית.
4. ספרות מקצועית: נמדר ופרידמן.

הנחיות לביצוע:
- כאשר המשתמש בוחר קבצים מהמאגר, תן להם עדיפות וציין: "על פי המקור [שם הקובץ]...".
- אתר חשיפות לפי השאלון המקצועי: עסקאות בינלאומיות, תשומות עובדים (מבחן הדומיננטיות), חשבוניות עצמיות והתאמות מחזורים.
- בנה "זירת מלחמה": טיעונים משפטיים הסותרים את עמדת התאמ"ו על בסיס פסיקת העליון והמחוזי.

ענה בעברית מיושרת לימין.
"""

# 5. סרגל צד לניהול המאגר
with st.sidebar:
    st.header("📚 מאגר המקורות (War Room)")
    st.write("בחר מקורות מהמאגר הקבוע:")
    
    existing_files = get_existing_files()
    selected_internal_files = []
    
    if existing_files:
        for f in existing_files:
            if st.checkbox(f.display_name, key=f.name):
                selected_internal_files.append(f.display_name)
    else:
        st.warning("לא נמצאו קבצים במאגר.")

    st.divider()
    st.header("📄 ניתוח מסמך חדש")
    uploaded_file = st.file_uploader("העלה שומה/השגה לניתוח (PDF)", type="pdf")

# 6. אזור העבודה המרכזי
user_query = st.text_area(
    "הזן שאלה או דגשים לביקורת:", 
    placeholder="למשל: נתח את סעיף הכיבודים בדו\"ח המצורף מול הוראות התאמ"ו והלכת פליי איט...",
    height=150
)

if st.button("הפעל ניתוח אסטרטגי"):
    if not user_query and not uploaded_file:
        st.warning("אנא הזן שאלה או העלה מסמך.")
    else:
        with st.spinner("סורק את התאמ"ו, הפסיקה ומאגר המקורות..."):
            context = f"הסתמך על הקבצים הבאים מהמאגר: {', '.join(selected_internal_files)}\n\n"
            content_parts = [context + user_query]
            
            if uploaded_file:
                content_parts.append(types.Part.from_bytes(data=uploaded_file.read(), mime_type="application/pdf"))

            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.1),
                    contents=content_parts
                )
                st.markdown("### 🔍 ממצאי ה-War Room (ניתוח תאמ"ו ופסיקה):")
                st.markdown(f'<div class="report-container">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"שגיאה: {e}")
