import streamlit as st
import pandas as pd
import requests
import json

# =========================
# PAGE CONFIG (UI)
# =========================
st.set_page_config(
    page_title="KUS COMPASS",
    page_icon="🎓",
    layout="wide"
)

# =========================
# HEADER UI
# =========================
st.markdown("""
    <style>
    .title {
        font-size:40px;
        font-weight:bold;
        text-align:center;
        color:#4F8BF9;
    }
    .subtitle {
        text-align:center;
        color:gray;
        margin-bottom:30px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎓 KUS COMPASS</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">ระบบแนะแนวการศึกษา + วิเคราะห์ความถนัด</div>', unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
def load_data():
    try:
        return pd.read_csv("data.csv")
    except:
        return None

df = load_data()

# =========================
# GOOGLE SHEET WEBHOOK
# =========================
GOOGLE_SHEET_WEBHOOK = "ใส่_URL_APPS_SCRIPT"

def send_to_sheet(name, gpa, interest):
    try:
        requests.post(
            GOOGLE_SHEET_WEBHOOK,
            json={
                "name": name,
                "gpa": gpa,
                "interest": interest
            },
            timeout=10
        )
    except:
        pass

# =========================
# SMART AI (SCORING SYSTEM)
# =========================
def smart_guidance(name, gpa, interest):

    text = interest.lower()

    sport = 0
    tech = 0
    art = 0
    language = 0
    business = 0

    # keywords
    for k in ["กีฬา","ฟุตบอล","บาส","วิ่ง","fitness"]:
        if k in text:
            sport += 100

    for k in ["คอม","code","โปรแกรม","ai","python"]:
        if k in text:
            tech += 100

    for k in ["ดนตรี","เพลง","วาด","design"]:
        if k in text:
            art += 100

    for k in ["ภาษา","english","พูด"]:
        if k in text:
            language += 100

    for k in ["ขาย","ธุรกิจ","การตลาด"]:
        if k in text:
            business += 100

    scores = {
        "กีฬา": sport,
        "เทค": tech,
        "ศิลป์": art,
        "ภาษา": language,
        "ธุรกิจ": business
    }

    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    result = f"""
# 📊 ผลวิเคราะห์

👤 ชื่อ: {name}  
📈 GPA: {gpa}  
🎯 ความสนใจ: {interest}

---

"""

    if top[0][0] == "กีฬา":
        result += """
## 🏆 สายที่เหมาะ: กีฬา

🎓 คณะ:
- วิทยาศาสตร์การกีฬา
- พลศึกษา
- Sport Management

💼 อาชีพ:
- นักกีฬา
- โค้ช
- Sport Analyst

🛤 Roadmap:
- ฝึกกีฬาเฉพาะทาง
- ฟิตเนส + โภชนาการ
- ลงแข่งจริง
"""

    elif top[0][0] == "เทค":
        result += """
## 💻 สายที่เหมาะ: เทคโนโลยี

🎓 คณะ:
- วิศวะคอม
- IT
- Data Science

💼 อาชีพ:
- Programmer
- Developer

🛤 Roadmap:
- Python
- GitHub
- Project
"""

    elif top[0][0] in ["ศิลป์","ภาษา"]:
        result += """
## 🎨 สายที่เหมาะ: ศิลป์ / ภาษา

🎓 คณะ:
- นิเทศศาสตร์
- อักษรศาสตร์
- ภาษา

💼 อาชีพ:
- Content Creator
- Designer
- Translator

🛤 Roadmap:
- Portfolio
- ฝึกสื่อสาร
- ทำ content
"""

    else:
        result += """
## 📌 สายที่เหมาะ: ธุรกิจ / ทั่วไป

🎓 คณะ:
- บริหารธุรกิจ
- การตลาด

💼 อาชีพ:
- Marketing
- Business

🛤 Roadmap:
- ฝึกสื่อสาร
- เรียนรู้การขาย
"""

    return result

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.radio("📌 Menu", ["🎓 แนะแนว", "📊 Dashboard"])

# =========================
# PAGE 1 - AI
# =========================
if menu == "🎓 แนะแนว":

    st.subheader("ระบบวิเคราะห์ความถนัด")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("ชื่อ")
        gpa = st.text_input("GPA")

    with col2:
        interest = st.text_area("ความสนใจ (เช่น กีฬา ดนตรี ภาษา)")

    if st.button("🚀 วิเคราะห์"):

        if name and gpa and interest:

            send_to_sheet(name, gpa, interest)

            result = smart_guidance(name, gpa, interest)

            st.success("วิเคราะห์เสร็จแล้ว")
            st.markdown(result)

        else:
            st.warning("กรอกข้อมูลให้ครบ")

# =========================
# PAGE 2 - DASHBOARD
# =========================
elif menu == "📊 Dashboard":

    st.subheader("📊 ข้อมูลนักเรียน")

    if df is not None:
        st.dataframe(df)

        st.markdown("### 📈 สถิติ")

        if "GPA" in df.columns:
            st.metric("GPA เฉลี่ย", round(df["GPA"].astype(float).mean(), 2))

        col1, col2 = st.columns(2)

        with col1:
            if "เพศ" in df.columns:
                st.bar_chart(df["เพศ"].value_counts())

        with col2:
            if "ห้องเรียน ม.4" in df.columns:
                st.bar_chart(df["ห้องเรียน ม.4"].value_counts())

    else:
        st.info("ยังไม่มี data.csv")