if menu == "🎓 แนะแนว":

    st.subheader("📋 KUS COMPASS แบบสำรวจ")

    # =========================
    # BASIC INFO
    # =========================
    name = st.text_input("ชื่อ-นามสกุล")

    classroom = st.selectbox("ห้องเรียน", [
        "ม.4/1","ม.4/2","ม.4/3","ม.4/4",
        "ม.4/5","ม.4/6","ม.4/7","ม.4/8"
    ])

    gender = st.radio("เพศ", ["ชาย","หญิง","ไม่ระบุ"])

    gpa = st.selectbox("GPA", [
        "3.50 – 4.00","3.00 – 3.49",
        "2.50 – 2.99","2.00 – 2.49","ต่ำกว่า 2.00"
    ])

    st.markdown("---")

    # =========================
    # SUBJECTS
    # =========================
    subjects = st.multiselect(
        "วิชาที่ชอบ (เลือกได้หลายข้อ)",
        ["คณิตศาสตร์","ฟิสิกส์","เคมี","ชีววิทยา",
         "ภาษาไทย","ภาษาอังกฤษ","คอมพิวเตอร์",
         "ศิลปะ","ดนตรี","พลศึกษา","สังคม"]
    )

    st.markdown("---")

    # =========================
    # INTEREST
    # =========================
    activities = st.multiselect(
        "กิจกรรมที่ชอบ",
        ["กีฬา","เล่นเกม","ฟังเพลง","วาดภาพ",
         "ดูซีรีส์","เขียนโปรแกรม","Content","ธุรกิจ"]
    )

    personality = st.text_area("อธิบายตัวเอง")

    st.markdown("---")

    # =========================
    # GOALS
    # =========================
    faculty = st.multiselect(
        "คณะที่สนใจ",
        ["แพทย์","วิศวะ","IT","นิเทศ","บริหาร",
         "ศิลปะ","ครุ","ยังไม่แน่ใจ"]
    )

    future = st.radio(
        "อนาคตอยากทำงานแบบไหน",
        ["บริษัท","ธุรกิจตัวเอง","ฟรีแลนซ์","ราชการ","ยังไม่แน่ใจ"]
    )

    # =========================
    # BUTTON
    # =========================
    if st.button("🚀 วิเคราะห์"):

        if not name:
            st.warning("กรอกชื่อก่อน")
        else:

            interest_all = f"{subjects} {activities} {personality} {faculty}"

            # ส่ง sheet
            send_to_sheet(name, gpa, interest_all)

            # วิเคราะห์
            result = smart_guidance(name, gpa, interest_all)

            st.success("วิเคราะห์เสร็จแล้ว")
            st.markdown(result, unsafe_allow_html=True)