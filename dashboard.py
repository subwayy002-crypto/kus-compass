import streamlit as st
import pandas as pd

st.set_page_config(page_title="KUS COMPASS Dashboard", layout="wide")

st.title("🎓 KUS COMPASS - Dashboard ทั้งห้อง")

st.markdown("---")

# 🔥 โหลดไฟล์ CSV (ต้องชื่อ data.csv)
try:
    df = pd.read_csv("data.csv")
    st.success("โหลดข้อมูลสำเร็จ")

    # 📋 ข้อมูลดิบ
    st.subheader("📋 ข้อมูลนักเรียนทั้งหมด")
    st.dataframe(df)

    st.markdown("---")

    # 📊 GPA เฉลี่ย
    st.subheader("📊 สถิติพื้นฐาน")

    if "GPA" in df.columns:
        st.write("📌 GPA เฉลี่ย:", round(df["GPA"].astype(float).mean(), 2))

    # 🏫 ห้องเรียน
    if "ห้องเรียน ม.4" in df.columns:
        st.write("📌 จำนวนแต่ละห้อง")
        st.bar_chart(df["ห้องเรียน ม.4"].value_counts())

    # 👥 เพศ
    if "เพศ" in df.columns:
        st.write("📌 เพศของนักเรียน")
        st.bar_chart(df["เพศ"].value_counts())

    # 📚 วิชาที่ชอบ
    if "วิชาที่ชอบ" in df.columns:
        st.write("📌 วิชาที่นิยม")
        st.bar_chart(df["วิชาที่ชอบ"].value_counts())

    # 🎯 ความชัดเจนอนาคต
    if "ตอนนี้มีความชัดเจนเรื่องเส้นทางการเรียนต่อแค่ไหน?" in df.columns:
        st.write("📌 ความชัดเจนเรื่องอนาคต")
        st.bar_chart(df["ตอนนี้มีความชัดเจนเรื่องเส้นทางการเรียนต่อแค่ไหน?"].value_counts())

except FileNotFoundError:
    st.error("ไม่เจอไฟล์ data.csv ให้เอาไฟล์ CSV มาไว้ในโฟลเดอร์เดียวกับ dashboard.py")

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")