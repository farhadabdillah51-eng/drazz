import streamlit as st
import pandas as pd

st.title("📝 Editor Lirik")

lyrics = st.text_area(
    "Masukkan lirik",
    height=300
)

if lyrics:

    lines = lyrics.split("\n")

    data = []

    for i, line in enumerate(lines):

        data.append({
            "Lirik": line,
            "Mulai": i * 3,
            "Selesai": (i + 1) * 3
        })

    df = pd.DataFrame(data)

    edited = st.data_editor(
        df,
        use_container_width=True
    )

    st.session_state["lyrics"] = edited
