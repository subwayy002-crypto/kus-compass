import streamlit as st
import requests

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="KUS COMPASS QUIZ", page_icon="🎓", layout="wide")

st.markdown("""
<style>
.title {
    text-align:center;
    font-size:42px;
    font-weight:800;
    color:#7C3AED;
}

.card {
    background:#F9FAFB;
    padding:20px;
    border-radius:12px;
    border:1px solid #E5E7EB;
    margin-bottom:15px;
}

.stButton>button {
    background: linear-gradient(90deg,#22C55E,#7C3AED);
    color:white;
    font-weight:bold;
    border-radius:10px;
    height:45px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎓 KUS COMPASS QUIZ</div>', unsafe_allow_html=True)

# =========================
# GOOGLE SHEET
# =========================
GOOGLE_SHEET_WEBHOOK = "https://script.google.com/macros/s/AKfycby1F5MUZzVT_BbindiQZMVIEsxNK9lrWbBhIC_V38leA-3DZWIS94bhb3vNQoOYWJkfuA/exec"

def send_to_sheet(data):
    try:
        requests.post(GOOGLE_SHEET_WEBHOOK, json=data, timeout=10)
    except:
        pass

# =========================
# AI SUMMARY
# =========================
def ai_result(data):

    text = " ".join([
        str(data["subjects"]),
        str(data["activities"]),
        str(data["personality"])
    ]).lower()

    score = {
        "วิศวะ/IT": sum(k in text for k in ["คอม","code","python","ai","โปรแกรม"]),
        "ศิลปะ": sum(k in text for k in ["ดนตรี","เพลง","วาด","design"]),
        "กีฬา": sum(k in text for k in ["กีฬา","ฟุตบอล","บาส"]),
        "ภาษา": sum(k in text for k in ["ภาษา","english","พูด"]),
        "ธุรกิจ": sum(k in text for k in ["ขาย","ธุรกิจ","การตลาด"])
    }

    top = sorted(score.items(), key=lambda x: x[1], reverse=True)

    return f"""
<div class="card">

<h3>📊 ผลวิเคราะห์</h3>

👤 {data['name']}  
📈 GPA: {data['gpa']}

---

🏆 สายที่เหมาะที่สุด: <b>{top[0][0]}</b>

</div>
"""

# =========================
# QUIZ FORM
# =========================
st.markdown("### 📋 แบบทดสอบแนะแนว")

name = st.text_input("ชื่อ")
gpa = st.selectbox("GPA", ["3.5-4.0","3.0-3.49","2.5-2.99","2.0-2.49"])

st.markdown("#### 📚 วิชาที่ชอบ")
subjects = st.multiselect(
    "",
    ["คณิต","วิทย์","อังกฤษ","คอม","ศิลปะ","สังคม","ภาษา"]
)

st.markdown("#### 🎯 กิจกรรมที่ชอบ")
activities = st.multiselect(
    "",
    ["กีฬา","เกม","ดนตรี","วาดภาพ","โค้ด","ธุรกิจ","Content"]
)

personality = st.text_area("อธิบายตัวเอง")

# =========================
# SUBMIT
# =========================
if st.button("🚀 ส่งแบบทดสอบ + วิเคราะห์"):

    if not name:
        st.warning("กรอกชื่อก่อน")
    else:

        data = {
            "name": name,
            "gpa": gpa,
            "subjects": subjects,
            "activities": activities,
            "personality": personality
        }

        # ส่ง Google Sheet
        send_to_sheet(data)

        # วิเคราะห์ AI
        result = ai_result(data)

        st.success("วิเคราะห์เสร็จแล้ว")
        st.markdown(result, unsafe_allow_html=True)