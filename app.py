import streamlit as st
import requests

st.set_page_config(page_title="KUS COMPASS", page_icon="🎓", layout="centered")

# =========================
# STYLE (GOOGLE FORM STYLE)
# =========================
st.markdown("""
<style>
body {
    background-color:#F3F4F6;
}

.block {
    background:white;
    padding:20px;
    border-radius:12px;
    margin-bottom:15px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
}

.title {
    font-size:32px;
    font-weight:800;
    color:#7C3AED;
    text-align:center;
}

.subtitle {
    text-align:center;
    color:#16A34A;
    margin-bottom:20px;
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

st.markdown('<div class="title">🎓 KUS COMPASS</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">แบบทดสอบแนะแนว (Google Form Style)</div>', unsafe_allow_html=True)

# =========================
# GOOGLE SHEET
# =========================
WEBHOOK = "https://script.google.com/macros/s/AKfycby1F5MUZzVT_BbindiQZMVIEsxNK9lrWbBhIC_V38leA-3DZWIS94bhb3vNQoOYWJkfuA/exec"

def send(data):
    try:
        requests.post(WEBHOOK, json=data, timeout=10)
    except:
        pass

# =========================
# AI (CLEAN + NOT RANDOM)
# =========================
def ai(data):

    text = " ".join([str(v) for v in data.values()]).lower()

    score = {
        "วิศวะ/IT": sum(k in text for k in ["คอม","code","ai","tech","วิทย์","คณิต"]),
        "ศิลปะ/นิเทศ": sum(k in text for k in ["ศิลปะ","ดนตรี","วาด","design","content"]),
        "ภาษา/อักษร": sum(k in text for k in ["ภาษา","english","พูด","สื่อสาร"]),
        "ธุรกิจ": sum(k in text for k in ["ธุรกิจ","ขาย","การตลาด","startup"]),
        "กีฬา": sum(k in text for k in ["กีฬา","ฟิตเนส","ฟุตบอล"])
    }

    sorted_score = sorted(score.items(), key=lambda x: x[1], reverse=True)
    top1, top2, top3 = sorted_score[:3]

    return f"""
<div class="block">

<h2>📊 ผลวิเคราะห์</h2>

👤 {data['name']}  
📈 GPA: {data['gpa']}

---

🏆 อันดับที่เหมาะ:

1️⃣ {top1[0]}  
2️⃣ {top2[0]}  
3️⃣ {top3[0]}

---

🧠 วิเคราะห์:

ระบบดูจากความสัมพันธ์ของ
- วิชา
- กิจกรรม
- ความสนใจ

แล้วสรุปว่า <b>{top1[0]}</b> คือสายที่เด่นที่สุด

</div>
"""

# =========================
# FORM UI (GOOGLE FORM STYLE)
# =========================

st.header("📋 แบบฟอร์ม")

with st.container():
    st.markdown('<div class="block">', unsafe_allow_html=True)
    name = st.text_input("ชื่อ-นามสกุล")
    st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="block">', unsafe_allow_html=True)
    classroom = st.selectbox("ห้อง", ["ม.4/1","ม.4/2","ม.4/3","ม.4/4","ม.4/5","ม.4/6","ม.4/7","ม.4/8"])
    gender = st.radio("เพศ", ["ชาย","หญิง","ไม่ระบุ"])
    gpa = st.selectbox("GPA", ["3.5-4.0","3.0-3.49","2.5-2.99","2.0-2.49"])
    st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="block">', unsafe_allow_html=True)
    subjects = st.multiselect("วิชาที่ชอบ", ["คณิต","วิทย์","อังกฤษ","คอม","ศิลปะ","สังคม"])
    st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="block">', unsafe_allow_html=True)
    activities = st.multiselect("กิจกรรม", ["กีฬา","เกม","ดนตรี","วาดภาพ","โค้ด","ธุรกิจ","Content"])
    st.markdown('</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="block">', unsafe_allow_html=True)
    personality = st.text_area("อธิบายตัวเอง")
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# SUBMIT
# =========================
if st.button("🚀 ส่งแบบทดสอบ"):

    if not name:
        st.warning("กรอกชื่อก่อน")
    else:

        data = {
            "name": name,
            "classroom": classroom,
            "gender": gender,
            "gpa": gpa,
            "subjects": subjects,
            "activities": activities,
            "personality": personality
        }

        send(data)

        st.success("ส่งสำเร็จ")

        st.markdown(ai(data), unsafe_allow_html=True)