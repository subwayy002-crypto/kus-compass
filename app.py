import streamlit as st
import requests

st.set_page_config(page_title="KUS COMPASS", page_icon="🎓", layout="wide")

# =========================
# MODERN DARK UI (SaaS STYLE)
# =========================
st.markdown("""
<style>
body {
    background: #0a0a0f;
    color: white;
    font-family: Inter;
}

.main {
    background: #0a0a0f;
}

.card {
    background: linear-gradient(145deg,#111827,#0f172a);
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #1f2937;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    margin-top: 20px;
}

.title {
    font-size: 40px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg,#22c55e,#a855f7,#38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align:center;
    color:#9ca3af;
    margin-bottom:20px;
}

.stButton>button {
    width:100%;
    background: linear-gradient(90deg,#22c55e,#a855f7);
    color:white;
    font-weight:bold;
    border-radius:12px;
    height:45px;
    border:none;
}

.progress-bar > div > div {
    background: linear-gradient(90deg,#22c55e,#a855f7);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">KUS COMPASS</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI Career Intelligence System</div>', unsafe_allow_html=True)

# =========================
# STATE
# =========================
if "i" not in st.session_state:
    st.session_state.i = 0

if "data" not in st.session_state:
    st.session_state.data = {}

# =========================
# QUESTIONS (CORE 20+)
# =========================
questions = [
    "ชื่อของคุณ",
    "GPA",
    "คณิตศาสตร์",
    "วิทยาศาสตร์",
    "ภาษาอังกฤษ",
    "การเขียนโปรแกรม",
    "AI / เทคโนโลยี",
    "ความคิดวิเคราะห์",
    "ความคิดสร้างสรรค์",
    "การสื่อสาร",
    "ภาวะผู้นำ",
    "ธุรกิจ",
    "ศิลปะ",
    "ดนตรี",
    "กีฬา",
    "เล่นเกม / Tech",
    "ชอบทำงานคนเดียว",
    "ชอบทำงานเป็นทีม",
    "ความสนใจแพทย์",
    "ความสนใจกฎหมาย",
    "ความชัดเจนอนาคต",
    "อยากรวย / ธุรกิจ",
    "ชอบสร้างสิ่งใหม่",
    "ชอบวิเคราะห์ข้อมูล"
]

keys = [
    "name","gpa",
    "math","science","eng","code","ai","logic","creative","speech",
    "lead","biz","art","music","sport","game","solo","team",
    "med","law","goal","money","build","data"
]

# =========================
# UI FLOW
# =========================
i = st.session_state.i
st.progress(i/len(questions))

st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader(questions[i])

if i == 0:
    val = st.text_input("Input")
elif i == 1:
    val = st.selectbox("GPA", ["3.5-4.0","3.0-3.49","2.5-2.99","2.0-2.49"])
else:
    val = st.slider("Level",1,5,3)

st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("⬅ Back") and i > 0:
        st.session_state.i -= 1

with col2:
    if st.button("Next ➡"):

        st.session_state.data[keys[i]] = val

        if i < len(questions)-1:
            st.session_state.i += 1
        else:
            st.session_state.i = 0
            st.success("Done")

# =========================
# AI ENGINE (REAL SCORING)
# =========================
def ai(d):

    score = {
        "Software Engineer / AI": d["code"]*2 + d["ai"] + d["logic"] + d["data"],
        "Doctor / Health": d["science"]*2 + d["med"],
        "Designer / Creative": d["art"]*2 + d["creative"],
        "Business / Startup": d["biz"]*2 + d["money"],
        "Law / Politics": d["law"]*2,
        "Media / Content": d["speech"]*2 + d["creative"]
    }

    top = sorted(score.items(), key=lambda x: x[1], reverse=True)[:3]

    return f"""
<div class="card">

<h2>📊 AI Career Report</h2>

🏆 1. {top[0][0]}  
🥈 2. {top[1][0]}  
🥉 3. {top[2][0]}

---

🧠 Insight:
You are strongest in <b>{top[0][0]}</b> based on 24-factor analysis.

</div>
"""

if len(st.session_state.data) == len(keys):
    st.markdown(ai(st.session_state.data), unsafe_allow_html=True)