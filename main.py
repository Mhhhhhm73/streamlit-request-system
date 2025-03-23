import streamlit as st

# -----------------------------
# 1. تعريف قائمة المراجعين
# -----------------------------
reviewers = ["سامي", "ندى", "عبدالله", "فهد", "ريم", "نورة"]

# -----------------------------
# 2. تهيئة الجلسة
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""

# -----------------------------
# 3. صفحة تسجيل الدخول
# -----------------------------
def login_page():
    st.title("تسجيل الدخول")
    username_input = st.text_input("ادخل اسم المستخدم:")

    if st.button("دخول"):
        if username_input.strip() == "":
            st.warning("يرجى إدخال اسمك.")
        else:
            st.session_state.username = username_input.strip()
            st.session_state.role = "reviewer" if username_input in reviewers else "employee"
            st.session_state.page = "home"
            st.experimental_rerun()

# -----------------------------
# 4. الصفحة الرئيسية بعد تسجيل الدخول
# -----------------------------
def home_page():
    st.sidebar.success(f"مرحبًا، {st.session_state.username}")
    page = st.sidebar.selectbox("انتقل إلى:", ["رفع طلب جديد", "الطلبات المعلقة", "الطلبات الموافق عليها"])

    if page == "رفع طلب جديد":
        st.subheader("رفع طلب جديد")
        st.info("سيتم بناء صفحة رفع الطلب هنا.")

    elif page == "الطلبات المعلقة":
        st.subheader("الطلبات المعلقة")
        st.info("سيتم عرض الطلبات المعلقة الخاصة بك هنا.")

    elif page == "الطلبات الموافق عليها":
        st.subheader("الطلبات الموافق عليها")
        st.info("سيتم عرض الطلبات الموافق عليها هنا.")

    st.sidebar.button("تسجيل الخروج", on_click=logout)

# -----------------------------
# 5. تسجيل الخروج
# -----------------------------
def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# -----------------------------
# 6. التحكم في التنقل
# -----------------------------
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "home":
    home_page()
