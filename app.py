import streamlit as st
import requests

st.set_page_config(page_title="KUS COMPASS", page_icon="🎓", layout="centered")

# =========================
# STYLE
# =========================
st.markdown("""
<style>
body {background:#F3F4F6;}

.block {
    background:white;
    padding:18px;
    border-radius:12px;
    margin-bottom:12px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
}

.title {
    text-align:center;
    font-size:34px;
    font-weight:800;
    color:#7C3AED;
}

.stButton>button {
    background:linear-gradient(90deg,#22C55E,#7C3AED);
    color:white;
    font-weight:bold;
    height:45px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎓 KUS COMPASS QUIZ</div>', unsafe_allow_html=True)

# =========================
# SHEET
# =========================
WEBHOOK = "https://script.google.com/macros/s/AKfycby1F5MUZzVT_BbindiQZMVIEsxNK9lrWbBhIC_V38leA-3DZWIS94bhb3vNQoOYWJkfuA/exec"

def send(data):
    try:
        requests.post(WEBHOOK, json=data, timeout=10)
    except:
        pass

# =========================
# AI (SMART SCORE)
# =========================
def ai(data):

    text = " ".join([str(v) for v in data.values()]).lower()

    score = {
        "วิศวะ/IT": sum(k in text for k in ["คอม","python","ai","tech","code","robot","data"]),
        "แพทย์/สุขภาพ": sum(k in text for k in ["แพทย์","พยาบาล","ชีวะ","สุขภาพ","ยา"]),
        "ศิลปะ/นิเทศ": sum(k in text for k in ["ศิลปะ","design","วาด","ดนตรี","content","film"]),
        "ภาษา/อักษร": sum(k in text for k in ["ภาษา","english","พูด","สื่อสาร","แปล"]),
        "ธุรกิจ/บริหาร": sum(k in text for k in ["ธุรกิจ","ขาย","การตลาด","startup","เงิน"]),
        "กฎหมาย/รัฐศาสตร์": sum(k in text for k in ["กฎหมาย","รัฐ","การเมือง","สังคม"])
    }

    top = sorted(score.items(), key=lambda x: x[1], reverse=True)[:3]

    return f"""
<div class="block">

<h2>📊 ผลวิเคราะห์</h2>

👤 {data['name']}  
📈 GPA: {data['gpa']}

---

🏆 Top Career Paths:

1️⃣ {top[0][0]}  
2️⃣ {top[1][0]}  
3️⃣ {top[2][0]}

---

🧠 วิเคราะห์จากข้อมูล 20+ ข้อ:
- วิชา
- บุคลิก
- กิจกรรม
- เป้าหมาย

สรุปว่า <b>{top[0][0]}</b> เหมาะที่สุด

</div>
"""

# =========================
# FORM (20+ QUESTIONS)
# =========================

st.header("📋 ข้อมูลพื้นฐาน")
name = st.text_input("ชื่อ")
gpa = st.selectbox("GPA", ["3.5-4.0","3.0-3.49","2.5-2.99","2.0-2.49"])

st.header("📚 วิชาที่ชอบ (0-5)")

math = st.slider("คณิตศาสตร์",1,5,3)
science = st.slider("วิทยาศาสตร์",1,5,3)
english = st.slider("ภาษาอังกฤษ",1,5,3)
thai = st.slider("ภาษาไทย",1,5,3)
social = st.slider("สังคม",1,5,3)
it = st.slider("คอม/IT",1,5,3)

st.header("🎯 บุคลิก")

logic = st.slider("คิดวิเคราะห์",1,5,3)
creative = st.slider("ความคิดสร้างสรรค์",1,5,3)
communication = st.slider("การสื่อสาร",1,5,3)
leadership = st.slider("ภาวะผู้นำ",1,5,3)

st.header("🎮 กิจกรรม")

gaming = st.slider("เล่นเกม/เทค",1,5,3)
sports = st.slider("กีฬา",1,5,3)
music = st.slider("ดนตรี",1,5,3)
art = st.slider("ศิลปะ",1,5,3)
coding = st.slider("เขียนโปรแกรม",1,5,3)
business = st.slider("ธุรกิจ",1,5,3)
content = st.slider("ทำคอนเทนต์",1,5,3)

st.header("🎓 เป้าหมาย")

interest_med = st.slider("สนใจแพทย์/สุขภาพ",1,5,3)
interest_eng = st.slider("สนใจวิศวะ/IT",1,5,3)
interest_art = st.slider("สนใจศิลปะ/นิเทศ",1,5,3)
interest_law = st.slider("สนใจกฎหมาย/รัฐศาสตร์",1,5,3)
interest_biz = st.slider("สนใจธุรกิจ",1,5,3)

# =========================
# AI ENGINE
# =========================
def analyze(data):

    score = {
        "วิศวะ/IT": data["it"]*2 + data["coding"] + data["logic"] + data["interest_eng"],
        "แพทย์/สุขภาพ": data["science"]*2 + data["interest_med"],
        "ศิลปะ/นิเทศ": data["art"]*2 + data["music"] + data["content"] + data["interest_art"],
        "ภาษา/อักษร": data["english"]*2 + data["communication"],
        "ธุรกิจ": data["business"]*2 + data["leadership"] + data["interest_biz"],
        "กฎหมาย/รัฐศาสตร์": data["social"]*2 + data["interest_law"],
        "กีฬา/สุขภาพ": data["sports"]*2
    }

    top = sorted(score.items(), key=lambda x: x[1], reverse=True)[:3]

    return f"""
<div class="block">

<h2>📊 ผลวิเคราะห์</h2>

👤 {data['name']}  
📈 GPA: {data['gpa']}

---

🏆 Top 3 สายอาชีพ

1️⃣ {top[0][0]}  
2️⃣ {top[1][0]}  
3️⃣ {top[2][0]}

---

🧠 สรุป:
ระบบวิเคราะห์จาก 20+ คำถาม
ทั้งวิชา + บุคลิก + เป้าหมาย

สายที่เหมาะที่สุดคือ <b>{top[0][0]}</b>

</div>
"""

# =========================
# SUBMIT
# =========================
if st.button("🚀 ส่งแบบทดสอบ"):

    if not name:
        st.warning("กรอกชื่อก่อน")
    else:

        data = {
            "name": name,
            "gpa": gpa,

            "math": math,
            "science": science,
            "english": english,
            "thai": thai,
            "social": social,
            "it": it,

            "logic": logic,
            "creative": creative,
            "communication": communication,
            "leadership": leadership,

            "gaming": gaming,
            "sports": sports,
            "music": music,
            "art": art,
            "coding": coding,
            "business": business,
            "content": content,

            "interest_med": interest_med,
            "interest_eng": interest_eng,
            "interest_art": interest_art,
            "interest_law": interest_law,
            "interest_biz": interest_biz
        }

        send(data)

        st.success("ส่งแล้ว")

        st.markdown(analyze(data), unsafe_allow_html=True)