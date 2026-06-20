import streamlit as st
import os

st.title("📂 Upload")

audio = st.file_uploader(
    "Upload Audio",
    type=["mp3"]
)

video = st.file_uploader(
    "Upload Background Video",
    type=["mp4"]
)

if audio:
    os.makedirs("uploads", exist_ok=True)

    with open(
        f"uploads/{audio.name}",
        "wb"
    ) as f:
        f.write(audio.getbuffer())

    st.success("Audio berhasil diupload")

if video:
    with open(
        f"uploads/{video.name}",
        "wb"
    ) as f:
        f.write(video.getbuffer())

    st.success("Video berhasil diupload")
