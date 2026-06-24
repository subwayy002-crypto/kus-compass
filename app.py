import streamlit as st
import pandas as pd
import requests

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="KUS COMPASS", layout="wide")

st.title("🎓 KUS COMPASS - AI แนะแนว + Dashboard")

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
# AI CONFIG
# =========================
HF_TOKEN = "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"

# =========================
# AI FUNCTION (SAFE VERSION)
# =========================
def ask_ai(prompt):
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct",
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 500
                }
            },
            timeout=30
        )

        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            return data[0].get("generated_text", "AI ไม่ตอบ")

        return "⚠️ AI ยังโหลดอยู่หรือ token มีปัญหา"

    except Exception as e:
        return f"""❌ AI ใช้ไม่ได้ตอนนี้

Error: {e}

👉 ระบบ fallback ทำงานแทน"""

# =========================
# FALLBACK (กันพัง)
# =========================
def fallback_ai(prompt):
    return """
📌 ระบบแนะแนวพื้นฐาน (Fallback Mode)

1. คณะที่เหมาะ: วิศวกรรม / IT / Data Science
2. อาชีพ: Programmer / Engineer / Analyst
3. เหตุผล: เหมาะกับคนชอบ logic + คณิต + เทคโนโลยี
4. Roadmap:
   - ฝึก Python
   - ฝึก Math / Physics
   - ทำ Portfolio
   - ทำโปรเจกต์ GitHub
"""

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

            prompt = f"""
คุณคือที่ปรึกษาแนะแนว

ข้อมูลนักเรียน:
ชื่อ: {name}
GPA: {gpa}
ความสนใจ: {interest}

ช่วยวิเคราะห์:
1. คณะที่เหมาะสม
2. อาชีพที่เหมาะสม
3. เหตุผล
4. Roadmap
"""

            with st.spinner("AI กำลังคิด..."):

                result = ask_ai(prompt)

                # ถ้า AI พัง → ใช้ fallback
                if "❌" in result:
                    result = fallback_ai(prompt)

            st.success("เสร็จแล้ว")
            st.markdown(result)

# =========================
# MODE 2: DASHBOARD
# =========================
elif menu == "📊 Dashboard":

    st.subheader("📊 ข้อมูลนักเรียน")

    if df is None:
        st.error("ไม่เจอ data.csv")
    else:
        st.dataframe(df)

        st.markdown("---")

        # GPA
        if "GPA" in df.columns:
            st.metric("GPA เฉลี่ย", round(df["GPA"].astype(float).mean(), 2))

        col1, col2 = st.columns(2)

        with col1:
            if "เพศ" in df.columns:
                st.bar_chart(df["เพศ"].value_counts())

        with col2:
            if "ห้องเรียน ม.4" in df.columns:
                st.bar_chart(df["ห้องเรียน ม.4"].value_counts())