import streamlit as st
import pandas as pd
import requests
import json

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="KUS COMPASS", layout="wide")

st.title("🎓 KUS COMPASS - AI แนะแนว + Dashboard + Google Sheet")

# =========================
# LOAD CSV
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
GOOGLE_SHEET_WEBHOOK = "ใส่_URL_APPS_SCRIPT_ตรงนี้"

def send_to_sheet(name, gpa, interest):
    try:
        payload = {
            "name": name,
            "gpa": gpa,
            "interest": interest
        }

        requests.post(
            GOOGLE_SHEET_WEBHOOK,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=10
        )
    except:
        pass

# =========================
# SMART AI (NO ERROR VERSION)
# =========================
def smart_guidance(name, gpa, interest):

    text = interest.lower()

    sport = 0
    tech = 0
    art = 0
    business = 0

    # scoring
    if "กีฬา" in text or "ฟุตบอล" in text or "บาส" in text:
        sport += 100

    if "คอม" in text or "code" in text or "โปรแกรม" in text:
        tech += 100

    if "ดนตรี" in text or "เพลง" in text:
        art += 100

    if "ภาษา" in text or "english" in text:
        art += 50

    if "ขาย" in text or "ธุรกิจ" in text:
        business += 100

    result = f"""
📊 วิเคราะห์นักเรียน: {name}

GPA: {gpa}
ความสนใจ: {interest}

---

"""

    if sport >= max(tech, art, business):
        result += """
🏆 คณะที่เหมาะ:
- วิทยาศาสตร์การกีฬา
- พลศึกษา
- Sport Management
- นิเทศศาสตร์สายกีฬา

🎯 อาชีพ:
- นักกีฬา
- โค้ช
- Sport Analyst
- Content กีฬา

📌 เหตุผล:
เหมาะกับกิจกรรมร่างกาย + การแข่งขัน

🛤 Roadmap:
- ฝึกกีฬาเฉพาะทาง
- ฟิตเนส / โภชนาการ
- แข่ง / ทำ portfolio กีฬา
"""

    elif tech > sport:
        result += """
💻 คณะที่เหมาะ:
- วิศวะคอม
- IT
- Data Science

🎯 อาชีพ:
- Programmer
- Developer
- Data Analyst

📌 เหตุผล:
เหมาะกับ logic + เทคโนโลยี

🛤 Roadmap:
- Python
- GitHub
- Project
"""

    elif art > sport:
        result += """
🎨 คณะที่เหมาะ:
- นิเทศ
- ดนตรี
- ภาษา

🎯 อาชีพ:
- Content Creator
- Designer
- นักดนตรี

📌 เหตุผล:
เหมาะกับ creativity + การสื่อสาร

🛤 Roadmap:
- Portfolio
- ฝึกสื่อสาร
"""

    else:
        result += """
📌 คณะที่เหมาะ:
- บริหารธุรกิจ
- มนุษยศาสตร์

🎯 อาชีพ:
- Business
- Office work

🛤 Roadmap:
- ลองค้นหาความสนใจเพิ่ม
"""

    return result

# =========================
# MENU
# =========================
menu = st.sidebar.radio(
    "เลือกโหมด",
    ["🎓 AI แนะแนว", "📊 Dashboard"]
)

# =========================
# MODE 1: AI
# =========================
if menu == "🎓 AI แนะแนว":

    st.subheader("ระบบแนะแนว KUS COMPASS")

    name = st.text_input("ชื่อ")
    gpa = st.text_input("GPA")
    interest = st.text_area("ความสนใจ")

    if st.button("วิเคราะห์"):

        if not name or not gpa or not interest:
            st.error("กรอกข้อมูลให้ครบ")
        else:

            # 🔥 ส่งเข้า Google Sheet
            send_to_sheet(name, gpa, interest)

            # 🔥 วิเคราะห์
            result = smart_guidance(name, gpa, interest)

            st.success("เสร็จแล้ว")
            st.markdown(result)

# =========================
# MODE 2: DASHBOARD
# =========================
elif menu == "📊 Dashboard":

    st.subheader("ข้อมูลนักเรียน")

    if df is None:
        st.error("ไม่เจอ data.csv")
    else:
        st.dataframe(df)

        st.markdown("---")

        if "GPA" in df.columns:
            st.metric("GPA เฉลี่ย", round(df["GPA"].astype(float).mean(), 2))

        col1, col2 = st.columns(2)

        with col1:
            if "เพศ" in df.columns:
                st.bar_chart(df["เพศ"].value_counts())

        with col2:
            if "ห้องเรียน ม.4" in df.columns:
                st.bar_chart(df["ห้องเรียน ม.4"].value_counts())