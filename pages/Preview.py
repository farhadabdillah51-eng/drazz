import streamlit as st

st.title("🎬 Preview")

if "lyrics" not in st.session_state:
    st.warning("Belum ada lirik")
else:

    df = st.session_state["lyrics"]

    for _, row in df.iterrows():

        st.markdown(
            f"""
            <h2 style='text-align:center'>
            {row['Lirik']}
            </h2>
            """,
            unsafe_allow_html=True
        )
