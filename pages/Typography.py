import streamlit as st

st.title("✨ Typography")

font = st.selectbox(
    "Font",
    [
        "Poppins",
        "Montserrat",
        "Bebas Neue"
    ]
)

size = st.slider(
    "Ukuran Teks",
    20,
    120,
    60
)

color = st.color_picker(
    "Warna",
    "#FFFFFF"
)

st.session_state["font"] = font
st.session_state["size"] = size
st.session_state["color"] = color

st.markdown(
    f"""
    <div style="
    color:{color};
    font-size:{size}px;
    text-align:center;
    ">
    Contoh Typography
    </div>
    """,
    unsafe_allow_html=True
)
