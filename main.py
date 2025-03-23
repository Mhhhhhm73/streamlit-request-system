import streamlit as st

st.title("نظام إدارة طلبات المواد التالفة")
st.write("مرحبًا بك في صفحة تسجيل الدخول.")

username = st.text_input("ادخل اسمك:")

if st.button("دخول"):
    st.success(f"مرحبًا {username}!")
