import streamlit as st
import requests

st.set_page_config(page_title="KUS COMPASS", page_icon="🎓", layout="wide")

st.title("🎓 KUS COMPASS QUIZ")

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
# QUIZ SECTION
# =========================
st.header("📋 แบบทดสอบ")

name = st.text_input("ชื่อ")
gpa = st.selectbox("GPA", ["3.5-4.0","3.0-3.49","2.5-2.99","2.0-2.49"])

st.subheader("📚 วิชาที่ชอบ")

math = st.slider("คณิต",1,5,3)
science = st.slider("วิทย์",1,5,3)
language = st.slider("ภาษา",1,5,3)
art = st.slider("ศิลปะ",1,5,3)
it = st.slider("คอม/IT",1,5,3)

st.subheader("🎯 บุคลิก")

logic = st.slider("ชอบคิดวิเคราะห์",1,5,3)
creative = st.slider("ชอบสร้างสรรค์",1,5,3)
social = st.slider("ชอบสื่อสาร",1,5,3)
sport = st.slider("ชอบกีฬา",1,5,3)

st.subheader("🎮 กิจกรรม")

gaming = st.slider("เล่นเกม/เทค",1,5,3)
business = st.slider("ธุรกิจ/ขาย",1,5,3)
content = st.slider("ทำคอนเทนต์",1,5,3)

# =========================
# AI FUNCTION (REAL SCORING)
# =========================
def ai(data):

    score = {
        "วิศวะ/IT": data["it"]*2 + data["logic"] + data["gaming"],
        "ศิลปะ/นิเทศ": data["art"]*2 + data["creative"] + data["content"],
        "ภาษา/สื่อสาร": data["language"]*2 + data["social"],
        "ธุรกิจ": data["business"]*2 + data["social"],
        "กีฬา/สุขภาพ": data["sport"]*2
    }

    sorted_score = sorted(score.items(), key=lambda x: x[1], reverse=True)

    top1, top2, top3 = sorted_score[:3]

    return f"""
<h2>📊 ผลวิเคราะห์</h2>

👤 {data['name']}  
📈 GPA: {data['gpa']}

---

🏆 สายที่เหมาะที่สุด:

1️⃣ {top1[0]} ({top1[1]} คะแนน)  
2️⃣ {top2[0]} ({top2[1]} คะแนน)  
3️⃣ {top3[0]} ({top3[1]} คะแนน)

---

🧠 เหตุผล:

ระบบวิเคราะห์จาก “พฤติกรรม + ความชอบ + บุคลิก”

- ถ้าคะแนน IT สูง → เหมาะสายเทคโนโลยี
- ถ้าคะแนน creative สูง → เหมาะสายศิลปะ/นิเทศ
- ถ้าคะแนน social สูง → เหมาะสายภาษา/ธุรกิจ

---

🎯 คำแนะนำ:
- โฟกัสอันดับ 1
- ลองทำโปรเจกต์ในสายที่ 2
- ใช้สายที่ 3 เป็น backup
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
            "language": language,
            "art": art,
            "it": it,
            "logic": logic,
            "creative": creative,
            "social": social,
            "sport": sport,
            "gaming": gaming,
            "business": business,
            "content": content
        }

        send(data)

        st.success("วิเคราะห์เสร็จแล้ว")

        result = ai(data)
        st.markdown(result, unsafe_allow_html=True)