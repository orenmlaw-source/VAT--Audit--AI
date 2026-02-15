import streamlit as st

# הגדרת כיוון כתיבה לימין (RTL)
st.markdown('<div style="direction: rtl; text-align: right;">', unsafe_allow_html=True)

st.title("🛡️ מערכת מבקר מע״מ וזירת מלחמה משפטית")

# תפריט צד (Sidebar) להיסטוריה והגדרות
with st.sidebar:
    st.header("היסטוריית בקשות")
    st.write("כאן תופיע היסטוריית הדו"חות שלך")

# אזור העלאת קבצים
uploaded_file = st.file_uploader("העלה קובץ לביקורת (PDF)", type=['pdf'])

# חלון כתיבת שאלה/מקרה
user_input = st.text_area("תאר את מקרה המס או הדבק כתב טענות של הצד השני:")

# כפתורי פעולה
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("בצע ביקורת מע״מ יזומה"):
        st.info("מנתח את הנתונים אל מול ספר נמדר...")
with col2:
    if st.button("זירת מלחמה: ניתוח יריב"):
        st.warning("מחפש סתירות משפטיות בכתב הטענות...")
with col3:
    if st.button("הכן טיוטת השגה"):
        st.success("מנסח השגה משפטית רשמית...")

# כפתור שליחה לוואטסאפ (יופעל בהמשך)
if st.button("📱 שלח דו״ח סופי לוואטסאפ"):
    st.write("שולח את הנתונים ל-API של WhatsApp...")

st.markdown('</div>', unsafe_allow_html=True)
