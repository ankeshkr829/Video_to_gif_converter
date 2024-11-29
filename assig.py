import streamlit as st
import tempfile
import os
from moviepy.editor import VideoFileClip


def convert_to_gif(video_file, start_time, duration, fps):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
        tmpfile.write(video_file.read())
        video_path = tmpfile.name

    clip = VideoFileClip(video_path).subclip(start_time, start_time + duration)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.gif') as gif_file:
        clip.write_gif(gif_file.name, fps=fps)
        return gif_file.name


st.title("Video to GIF Converter")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    st.video(uploaded_file)

    start_time = st.slider("Start time (seconds)", 0, 150, 0)
    duration = st.slider("Duration (seconds)", 1, 10, 5)
    fps = st.slider("Frames per second", 1, 30, 10)

    if st.button("Convert to GIF"):
        gif_path = convert_to_gif(uploaded_file, start_time, duration, fps)

        with open(gif_path, "rb") as file:
            btn = st.download_button(
                label="Download GIF",
                data=file,
                file_name="converted.gif",
                mime="image/gif"
            )

        st.image(gif_path)

        # Clean up temporary files
        os.unlink(gif_path)

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and MoviePy")