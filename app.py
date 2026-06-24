import streamlit as st
import requests

st.set_page_config(page_title="KUS COMPASS", page_icon="🎓", layout="centered")

st.title("🎓 KUS COMPASS - Career Quiz")

# =========================
# STATE
# =========================
if "i" not in st.session_state:
    st.session_state.i = 0

if "data" not in st.session_state:
    st.session_state.data = {}

# =========================
# QUESTIONS (25 ข้อจริง)
# =========================
questions = [
    "ชื่อของคุณคืออะไร?",
    "GPA ของคุณ",
    "คุณชอบคณิตศาสตร์แค่ไหน (1-5)",
    "คุณชอบวิทยาศาสตร์แค่ไหน (1-5)",
    "คุณชอบภาษาอังกฤษแค่ไหน (1-5)",
    "คุณชอบภาษาไทยแค่ไหน (1-5)",
    "คุณชอบสังคม/ประวัติศาสตร์แค่ไหน (1-5)",
    "คุณชอบเขียนโปรแกรมแค่ไหน (1-5)",
    "คุณชอบศิลปะ/ดนตรีแค่ไหน (1-5)",
    "คุณชอบกีฬาแค่ไหน (1-5)",
    "คุณชอบเล่นเกม/เทคโนโลยีแค่ไหน (1-5)",
    "คุณชอบทำธุรกิจแค่ไหน (1-5)",
    "คุณชอบพูด/นำเสนอแค่ไหน (1-5)",
    "คุณชอบทำงานเป็นทีมแค่ไหน (1-5)",
    "คุณเป็นคนคิดวิเคราะห์แค่ไหน (1-5)",
    "คุณเป็นคนสร้างสรรค์แค่ไหน (1-5)",
    "คุณชอบใช้คอมพิวเตอร์บ่อยแค่ไหน (1-5)",
    "คุณสนใจ AI / เทคโนโลยีใหม่แค่ไหน (1-5)",
    "คุณสนใจแพทย์/สุขภาพแค่ไหน (1-5)",
    "คุณสนใจกฎหมาย/การเมืองแค่ไหน (1-5)",
    "คุณชอบทำคอนเทนต์/ถ่ายวิดีโอแค่ไหน (1-5)",
    "คุณชอบทำงานอิสระแค่ไหน (1-5)",
    "คุณชอบทำงานในองค์กรแค่ไหน (1-5)",
    "คุณมีเป้าหมายอนาคตชัดแค่ไหน (1-5)",
    "คุณอยากรวย/ธุรกิจตัวเองแค่ไหน (1-5)"
]

keys = [
    "name","gpa",
    "math","science","eng","thai","social","code","art","sport",
    "game","biz","speech","team","logic","creative","computer","ai",
    "health","law","content","freelance","office","goal","money"
]

# =========================
# INPUT
# =========================
i = st.session_state.i
st.progress(i/len(questions))

st.subheader(questions[i])

if i == 0:
    val = st.text_input("ตอบ")
elif i == 1:
    val = st.selectbox("เลือก", ["3.5-4.0","3.0-3.49","2.5-2.99","2.0-2.49"])
else:
    val = st.slider("ระดับ",1,5,3)

# =========================
# BUTTONS
# =========================
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅ กลับ") and i > 0:
        st.session_state.i -= 1

with col2:
    if st.button("➡ ต่อไป"):

        st.session_state.data[keys[i]] = val

        if i < len(questions)-1:
            st.session_state.i += 1
        else:
            st.success("เสร็จแล้ว")
            st.session_state.i = 0

# =========================
# AI ANALYSIS
# =========================
def ai(d):

    score = {
        "วิศวะ/IT": d["code"]*2 + d["logic"] + d["ai"] + d["computer"],
        "แพทย์": d["science"]*2 + d["health"],
        "ศิลปะ/นิเทศ": d["art"]*2 + d["content"] + d["creative"],
        "ภาษา": d["eng"]*2 + d["speech"],
        "ธุรกิจ": d["biz"]*2 + d["money"] + d["office"],
        "กฎหมาย": d["social"]*2 + d["law"],
        "กีฬา": d["sport"]*2
    }

    top = sorted(score.items(), key=lambda x: x[1], reverse=True)[:3]

    return f"""
<div style="background:#111827;color:white;padding:20px;border-radius:12px;margin-top:20px">

<h2>📊 ผลวิเคราะห์</h2>

🏆 1️⃣ {top[0][0]}  
🥈 2️⃣ {top[1][0]}  
🥉 3️⃣ {top[2][0]}

---

🧠 สรุป:
คุณเหมาะกับ <b>{top[0][0]}</b> มากที่สุด

</div>
"""

# =========================
# SHOW RESULT
# =========================
if len(st.session_state.data) == len(keys):
    st.markdown(ai(st.session_state.data), unsafe_allow_html=True)