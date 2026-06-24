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
# AI FUNCTION
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

        return "⚠️ AI ยังไม่พร้อม / token หรือ model มีปัญหา"

    except Exception as e:
        return "❌ AI ใช้ไม่ได้\n" + str(e)

# =========================
# FALLBACK AI (กันพัง)
# =========================
def fallback_ai():
    return """
📌 ระบบแนะแนวพื้นฐาน KUS COMPASS

1. คณะที่เหมาะ:
   - วิศวกรรมคอมพิวเตอร์
   - IT / Data Science
   - นิเทศ / ดนตรี (ถ้ามีความสนใจศิลป์)

2. อาชีพ:
   - Programmer
   - Designer
   - Content Creator

3. เหตุผล:
   - ผสมระหว่าง logic + ความคิดสร้างสรรค์

4. Roadmap:
   - ฝึก Python
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

            # 🔥 PROMPT (FIXED)
            prompt = f"""
คุณคือระบบแนะแนวอาชีพของ KUS COMPASS

หน้าที่:
- วิเคราะห์จากข้อมูลนักเรียนอย่างรอบคอบ
- ห้ามเดาสุ่ม
- ต้องอิงจากความสนใจจริงเท่านั้น

ข้อมูลนักเรียน:
ชื่อ: {name}
GPA: {gpa}
ความสนใจ: {interest}

กติกา:
- ถ้าความสนใจไม่เกี่ยวกับวิศวะ/คณิต ห้ามแนะนำวิศวะเป็นอันดับแรก
- ต้องมีอย่างน้อย 2 สายอาชีพที่แตกต่างกัน
- ต้องมีสายศิลปะ/ภาษา ถ้ามีข้อมูลเกี่ยวข้อง

กรุณาตอบ:
1. คณะที่เหมาะสม (อย่างน้อย 2 ตัวเลือก)
2. อาชีพที่เหมาะสม
3. เหตุผล
4. Roadmap
"""

            with st.spinner("AI กำลังวิเคราะห์..."):

                result = ask_ai(prompt)

                # ถ้า AI ล่ม → ใช้ fallback
                if "❌" in result or "⚠️" in result:
                    result = fallback_ai()

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