import streamlit as st
import requests

# =========================
# CONFIG UI
# =========================
st.set_page_config(page_title="KUS COMPASS", page_icon="🎓", layout="wide")

st.markdown("""
<style>
body {background-color:white;}
.title {text-align:center;font-size:40px;font-weight:bold;color:#7C3AED;}
.subtitle {text-align:center;color:#16A34A;margin-bottom:20px;}
.stButton>button {
    background: linear-gradient(90deg,#22C55E,#7C3AED);
    color:white;
    font-weight:bold;
    border-radius:10px;
    height:45px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎓 KUS COMPASS</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI แนะแนวการศึกษา</div>', unsafe_allow_html=True)

# =========================
# MENU (FIX ERROR ตรงนี้)
# =========================
menu = st.sidebar.radio("📌 Menu", ["🎓 แนะแนว", "📊 Dashboard"])

# =========================
# GOOGLE SHEET WEBHOOK
# =========================
GOOGLE_SHEET_WEBHOOK = "https://script.google.com/macros/s/AKfycby1F5MUZzVT_BbindiQZMVIEsxNK9lrWbBhIC_V38leA-3DZWIS94bhb3vNQoOYWJkfuA/exec"

def send_to_sheet(name, gpa, interest):
    try:
        requests.post(
            GOOGLE_SHEET_WEBHOOK,
            json={"name": name, "gpa": gpa, "interest": interest},
            timeout=10
        )
    except:
        pass

# =========================
# AI LOGIC (SAFE)
# =========================
def smart_guidance(name, gpa, interest):

    text = interest.lower()

    sport = sum(k in text for k in ["กีฬา","ฟุตบอล","บาส","วิ่ง"])
    tech = sum(k in text for k in ["คอม","code","python","ai"])
    art = sum(k in text for k in ["ดนตรี","เพลง","วาด","design"])
    lang = sum(k in text for k in ["ภาษา","english","พูด"])
    biz = sum(k in text for k in ["ขาย","ธุรกิจ","การตลาด"])

    scores = {
        "กีฬา": sport,
        "เทค": tech,
        "ศิลป์": art,
        "ภาษา": lang,
        "ธุรกิจ": biz
    }

    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[0][0]

    return f"""
📊 ผลวิเคราะห์

ชื่อ: {name}
GPA: {gpa}
ความสนใจ: {interest}

---

สายที่เหมาะ: {top}

✔ วิเคราะห์เรียบร้อย
"""

# =========================
# PAGE 1
# =========================
if menu == "🎓 แนะแนว":

    st.subheader("📋 กรอกข้อมูล")

    name = st.text_input("ชื่อ")
    gpa = st.text_input("GPA")
    interest = st.text_area("ความสนใจ")

    if st.button("🚀 วิเคราะห์"):

        if name and gpa and interest:

            send_to_sheet(name, gpa, interest)

            result = smart_guidance(name, gpa, interest)

            st.success("สำเร็จ")
            st.markdown(result)

        else:
            st.warning("กรอกข้อมูลให้ครบ")

# =========================
# PAGE 2
# =========================
elif menu == "📊 Dashboard":
    st.subheader("📊 Dashboard")
    st.info("ยังไม่มี data.csv")