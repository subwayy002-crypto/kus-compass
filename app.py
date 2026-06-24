import streamlit as st
import pandas as pd
import requests
import json

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="KUS COMPASS",
    page_icon="🎓",
    layout="wide"
)

# =========================
# THEME UI (WHITE / GREEN / PURPLE)
# =========================
st.markdown("""
<style>
body {
    background-color: white;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #7C3AED; /* purple */
}

.sub-title {
    text-align: center;
    color: #16A34A; /* green */
    margin-bottom: 30px;
    font-size: 18px;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #F9FAFB;
    border: 1px solid #E5E7EB;
}

.stButton > button {
    background: linear-gradient(90deg, #22C55E, #7C3AED);
    color: white;
    font-weight: bold;
    border-radius: 10px;
    height: 45px;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎓 KUS COMPASS</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">ระบบแนะแนวการศึกษา + วิเคราะห์ความถนัด</div>', unsafe_allow_html=True)

# =========================
# GOOGLE SHEET WEBHOOK (ใส่แล้ว)
# =========================
GOOGLE_SHEET_WEBHOOK = "https://script.google.com/macros/s/AKfycby1F5MUZzVT_BbindiQZMVIEsxNK9lrWbBhIC_V38leA-3DZWIS94bhb3vNQoOYWJkfuA/exec"

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

    for k in ["กีฬา","ฟุตบอล","บาส","วิ่ง","ฟิตเนส"]:
        if k in text:
            sport += 100

    for k in ["คอม","code","python","ai","โปรแกรม"]:
        if k in text:
            tech += 100

    for k in ["ดนตรี","เพลง","วาด","design","ศิลปะ"]:
        if k in text:
            art += 100

    for k in ["ภาษา","english","พูด","สื่อสาร"]:
        if k in text:
            language += 100

    for k in ["ขาย","ธุรกิจ","การตลาด"]:
        if k in text:
            business += 100

    scores = {
        "กีฬา": sport,
        "เทคโนโลยี": tech,
        "ศิลปะ": art,
        "ภาษา": language,
        "ธุรกิจ": business
    }

    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    result = f"""
<div class="card">

<h3>📊 ผลวิเคราะห์</h3>

👤 ชื่อ: {name}  
📈 GPA: {gpa}  
🎯 ความสนใจ: {interest}

<hr>

</div>
"""

    if top[0][0] == "กีฬา":
        result += """
<div class="card">
<h3 style="color:#16A34A;">🏆 สายกีฬา</h3>

🎓 คณะ:
- วิทยาศาสตร์การกีฬา
- พลศึกษา
- Sport Management

💼 อาชีพ:
- นักกีฬา
- โค้ช
- Sport Analyst

🛤 Roadmap:
- ฝึกกีฬา
- ฟิตเนส
- แข่งจริง
</div>
"""

    elif top[0][0] == "เทคโนโลยี":
        result += """
<div class="card">
<h3 style="color:#7C3AED;">💻 สายเทคโนโลยี</h3>

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
</div>
"""

    elif top[0][0] in ["ศิลปะ","ภาษา"]:
        result += """
<div class="card">
<h3 style="color:#F59E0B;">🎨 สายศิลป์/ภาษา</h3>

🎓 คณะ:
- นิเทศ
- อักษร
- ภาษา

💼 อาชีพ:
- Content Creator
- Designer
- Translator

🛤 Roadmap:
- Portfolio
- Communication
</div>
"""

    else:
        result += """
<div class="card">
<h3>📌 สายธุรกิจ</h3>

🎓 คณะ:
- บริหารธุรกิจ
- การตลาด

💼 อาชีพ:
- Marketing
- Business

🛤 Roadmap:
- ฝึกขาย
- ฝึกสื่อสาร
</div>
"""

    return result

# =========================
# MENU
# =========================
menu = st.sidebar.radio("📌 Menu", ["🎓 แนะแนว", "📊 Dashboard"])

# =========================
# PAGE 1
# =========================
if menu == "🎓 แนะแนว":

    st.subheader("กรอกข้อมูลเพื่อวิเคราะห์")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("ชื่อ")

    with col2:
        gpa = st.text_input("GPA")

    interest = st.text_area("ความสนใจ (กีฬา / ดนตรี / ภาษา / คอม)")

    if st.button("🚀 วิเคราะห์"):

        if name and gpa and interest:

            send_to_sheet(name, gpa, interest)

            result = smart_guidance(name, gpa, interest)

            st.success("วิเคราะห์เสร็จแล้ว")
            st.markdown(result, unsafe_allow_html=True)

        else:
            st.warning("กรอกข้อมูลให้ครบ")

# =========================
# PAGE 2
# =========================
elif menu == "📊 Dashboard":

    st.subheader("📊 ข้อมูลนักเรียน")

    try:
        df = pd.read_csv("data.csv")
        st.dataframe(df)

        if "GPA" in df.columns:
            st.metric("GPA เฉลี่ย", round(df["GPA"].astype(float).mean(), 2))

    except:
        st.info("ยังไม่มี data.csv")