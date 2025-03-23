import pandas as pd
import streamlit as st
from datetime import datetime
import os

def show_request_form(username):
    st.subheader("رفع طلب جديد")

    # إدخال البيانات
    region = st.text_input("المنطقة")
    department = st.selectbox("القسم", ["الإمداد", "الصيانة", "التشغيل", "الأمن", "الموارد البشرية", "الشؤون المالية"])
    request_type = st.selectbox("نوع الطلب", ["أصول", "مخزون", "مركبات"])

    # رفع ملف Excel
    excel_file = st.file_uploader("ارفع ملف Excel", type=["xlsx"])

    # رفع ملفات PDF
    pdf_files = st.file_uploader("ارفع ملفات PDF", type=["pdf"], accept_multiple_files=True)

    # زر الإرسال
    if st.button("إرسال الطلب"):
        if not region or not department or not request_type:
            st.warning("الرجاء تعبئة جميع الحقول.")
            return
        if not excel_file:
            st.warning("يرجى رفع ملف Excel.")
            return
        if not pdf_files:
            st.warning("يرجى رفع ملفات PDF.")
            return

        # توليد رقم مرجعي
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        request_id = f"REQ-{timestamp}"

        # تجهيز بيانات الطلب
        row = {
            "رقم الطلب": request_id,
            "اسم المستخدم": username,
            "المنطقة": region,
            "القسم": department,
            "نوع الطلب": request_type,
            "ملف Excel": excel_file.name,
            "ملفات PDF": ", ".join([f.name for f in pdf_files]),
            "تاريخ الطلب": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "الحالة": "معلق"
        }

        # تحميل البيانات القديمة إن وُجد
        file_path = "طلبات_معلقة.csv"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
        else:
            df = pd.DataFrame()

        # إضافة الطلب الجديد
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        df.to_csv(file_path, index=False)

        st.success(f"تم إرسال الطلب بنجاح برقم مرجعي: {request_id}")
