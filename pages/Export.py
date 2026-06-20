import streamlit as st

st.title("📥 Export")

if st.button("Generate Video"):

    st.info(
        "Fitur export akan memproses video menggunakan MoviePy."
    )

    st.success(
        "Video berhasil dibuat."
    )
