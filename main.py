import streamlit as st
import pandas as pd
import os
from datetime import datetime
reviewers = ["سامي", "ندى", "عبدالله", "فهد", "ريم", "نورة"]
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if st.session_state.username == "":
    st.title("نظام إدارة طلبات المواد التالفة")
    st.write("مرحباً بك في صفحة تسجيل الدخول.")
    username_input = st.text_input("ادخل اسم المستخدم:")
    if st.button("دخول"):
        if username_input.strip() == "":
            st.warning("الرجاء إدخال اسمك.")
        else:
            st.session_state.username = username_input.strip()
            st.session_state.role = "reviewer" if username_input in reviewers else "employee"
            st.success(f"تم تسجيل الدخول كـ {st.session_state.username}")
st.write("هل تظهر هذه الرسالة؟ إذا نعم، فإن الجلسة تعمل.")
else:
    st.sidebar.success(f"مرحبًا، {st.session_state.username}")
    page = st.sidebar.selectbox("انتقل إلى:", ["رفع طلب جديد", "الطلبات المعلقة", "الطلبات الموافق عليها"])
    if page == "رفع طلب جديد":
        def show_request_form(username):
            st.subheader("رفع طلب جديد")
            region = st.text_input("المنطقة")
            department = st.selectbox("القسم", ["الإمداد", "الصيانة", "التشغيل", "الأمن", "الموارد البشرية", "الشؤون المالية"])
            request_type = st.selectbox("نوع الطلب", ["أصول", "مخزون", "مركبات"])
            excel_file = st.file_uploader("ارفع ملف Excel", type=["xlsx"])
            pdf_files = st.file_uploader("ارفع ملفات PDF", type=["pdf"], accept_multiple_files=True)
            if st.button("إرسال الطلب"):
                if not region or not department or not request_type:
                    st.warning("يرجى تعبئة جميع الحقول.")
                    return
                if not excel_file:
                    st.warning("يرجى رفع ملف Excel.")
                    return
                if not pdf_files:
                    st.warning("يرجى رفع ملفات PDF.")
                    return
                request_id = f"REQ-{datetime.now().strftime('%Y%m%d%H%M%S')}"
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
                file_path = "طلبات_معلقة.csv"
                if os.path.exists(file_path):
                    df = pd.read_csv(file_path)
                else:
                    df = pd.DataFrame()
                df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
                df.to_csv(file_path, index=False)
                st.success(f"تم إرسال الطلب بنجاح برقم: {request_id}")
        show_request_form(st.session_state.username)
    elif page == "الطلبات المعلقة":
        st.info("هذه الصفحة سيتم تجهيزها لعرض الطلبات المعلقة الخاصة بك.")
    elif page == "الطلبات الموافق عليها":
        st.info("هذه الصفحة سيتم تجهيزها لعرض الطلبات الموافق عليها الخاصة بك.")
