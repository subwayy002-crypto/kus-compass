import streamlit as st
import time

st.set_page_config(page_title="KUS COMPASS", page_icon="🎓", layout="centered")

# =========================
# ANIMATED MODERN UI
# =========================
st.markdown("""
<style>
body {
    background: #0b0f19;
    color: white;
    animation: fadeIn 0.6s ease-in;
}

@keyframes fadeIn {
    from {opacity:0; transform: translateY(10px);}
    to {opacity:1; transform: translateY(0);}
}

.card {
    background: #111827;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #1f2937;
    margin-top: 20px;

    animation: pop 0.4s ease;
}

@keyframes pop {
    from {transform: scale(0.98); opacity:0;}
    to {transform: scale(1); opacity:1;}
}

.title {
    font-size: 38px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg,#22c55e,#a855f7,#38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation: slideDown 0.6s ease;
}

@keyframes slideDown {
    from {transform: translateY(-10px); opacity:0;}
    to {transform: translateY(0); opacity:1;}
}

.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 45px;
    font-weight: bold;
    background: linear-gradient(90deg,#22c55e,#a855f7);
    color: white;

    transition: all 0.2s ease;
}

.stButton>button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 15px rgba(168,85,247,0.5);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎓 KUS COMPASS</div>', unsafe_allow_html=True)

# =========================
# STATE
# =========================
if "step" not in st.session_state:
    st.session_state.step = 0

if "data" not in st.session_state:
    st.session_state.data = {}

# =========================
# QUESTIONS
# =========================
questions = [
    ("ชื่อของคุณ", ["text"]),
    ("GPA", ["3.5-4.0","3.0-3.49","2.5-2.99","2.0-2.49"]),
    ("ชอบคณิตไหม", ["ไม่ชอบ","เฉยๆ","ชอบ","ชอบมาก"]),
    ("ชอบเขียนโปรแกรมไหม", ["ไม่เคย","ลองแล้ว","พอได้","ชอบ","โคตรชอบ"]),
    ("ชอบศิลปะไหม", ["ไม่ชอบ","เฉยๆ","ชอบ","ชอบมาก"]),
    ("ชอบธุรกิจไหม", ["ไม่ชอบ","เฉยๆ","สนใจ","ชอบ","อยากรวย"]),
]

keys = ["name","gpa","math","code","art","biz"]

# =========================
# ANIMATION STEP CHANGE
# =========================
def animate_sleep():
    with st.spinner("กำลังโหลด..."):
        time.sleep(0.25)

# =========================
# UI FLOW
# =========================
step = st.session_state.step
q, options = questions[step]

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader(q)

if options == ["text"]:
    val = st.text_input("ตอบ")
else:
    val = st.radio("เลือก", options)

st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("⬅ Back") and step > 0:
        animate_sleep()
        st.session_state.step -= 1
        st.rerun()

with col2:
    if st.button("Next ➡"):

        st.session_state.data[keys[step]] = val

        animate_sleep()

        if step < len(questions)-1:
            st.session_state.step += 1
        else:
            st.session_state.step = 0

        st.rerun()

# =========================
# RESULT
# =========================
def ai(d):

    score = {
        "วิศวะ/IT": d.get("code","").count("ชอบ"),
        "ศิลปะ": d.get("art","").count("ชอบ"),
        "ธุรกิจ": d.get("biz","").count("ชอบ")
    }

    top = sorted(score.items(), key=lambda x: x[1], reverse=True)[0]

    return f"""
<div class="card">

<h2>📊 Result</h2>

🏆 {top[0]}

</div>
"""

if len(st.session_state.data) == len(keys):
    st.markdown(ai(st.session_state.data), unsafe_allow_html=True)