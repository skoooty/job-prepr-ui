import streamlit as st
import threading
import time
import pathlib
from aiortc.contrib.media import MediaRecorder
from streamlit_webrtc import (
    VideoProcessorBase,
    webrtc_streamer,
    VideoHTMLAttributes
)
from utils.video import find_face
from utils.questions import load_questions, get_rand_question

from utils.page_switch import switch_page

from utils.get_css import get_css



#Defining the variables
lock = threading.Lock()
img_container = {"frames":[]}

s_per_question=60 #maximum duration of the video input in s

#Extracting frames from the video input
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.style = 'color'

    def video_frame_callback(self):
        img = self.to_ndarray(format="bgr24")
        img = find_face(img)
        with lock:
            if img is not None:
                img_container["frames"].append(img)

#Saving the audio input
def recorder_factory():
    return MediaRecorder("record.mp3")

def main():
    st.set_page_config(page_title="JobPrepr: Interview", page_icon="💼", layout="centered")
    st.markdown(get_css(),unsafe_allow_html=True)
    if 'email' in st.session_state:
        st.markdown("<style>[data-testid='stSidebarNav']::after {{ {0} {1} }}</style>".format('content:',f"'Signed in as: {st.session_state.email}';"), unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        logged_in=False
    else:
        logged_in=st.session_state["logged_in"]

    #Button code
    file_path=pathlib.Path(__file__).resolve().parent.parent.joinpath("styles", "main.css")
    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    #Questions and area selection
    questions=load_questions()
    job_list = questions["Area"].unique()

    #Title, text, page setup
    st.markdown("<h1 style='text-align: center; color: black;'>How confident are you?</h1>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.markdown("<h5 style='text-align: left; color: black;'>Select your job area below:</h5>", unsafe_allow_html=True)
    job_name = st.selectbox("", job_list)
    st.markdown(f"<p style=text-align:left;>Let's practice for your {job_name} interview.</p>",unsafe_allow_html=True)
    st.markdown(f"<p style=text-align:left;>You have {s_per_question}s to answer the question that will pop up on the screen.</p>",unsafe_allow_html=True)
    st.markdown(f"<b style=text-align:left;>Good luck!</b>", unsafe_allow_html=True)
    playing = st.checkbox("Start/Stop", value=False)
    analysing=False

    #Recording the video
    if playing:
        st.session_state["photo_frames"]=[]
        if 'question' not in st.session_state or st.session_state["question"] == None:
            st.session_state['question'] = get_rand_question(questions, job_name)
        st.markdown(f"<h3 style=text-align:left;>{st.session_state['question']}</h3>", unsafe_allow_html=True)
        webrtc_streamer(
            key="object-detection",
            video_frame_callback=VideoProcessor.video_frame_callback,
            media_stream_constraints={
                "video": True,
                "audio": True
            },
            desired_playing_state=playing #link to Start/Stop button
            , in_recorder_factory=recorder_factory
            , video_html_attrs = VideoHTMLAttributes(muted=True, volume=0, autoPlay=True, controls=False, stop=False #unabling the user to control video input
                                                    #,style={"border": "5px red solid", "margin": "0 auto", "width":"50%"}
                                                    )
            ,  rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                            }
        )
        st.markdown("""
                    <style>
                    [class=MuiButtonBase-root Mui-disabled MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium css-1dm0a9e] {
                    visibility: hidden;
                    }</style>""", unsafe_allow_html=True)

    #Storing photo frames
    if 'photo_frames' not in st.session_state:
        st.session_state['photo_frames'] = img_container["frames"]
    else:
        if len(st.session_state['photo_frames']) < 1:
            st.session_state['photo_frames'] = img_container["frames"]

    #Clock ticking
    if playing:
        ph = st.empty()
        for secs in range(s_per_question,0,-1):
            mm, ss = secs//60, secs%60
            ph.metric("", f"{mm:02d}:{ss:02d}")
            time.sleep(1)
        playing=False

    #When the video input is done
    if not playing:
        #Extracting the frames
        full_frames=st.session_state["photo_frames"]

        if len(full_frames):
            analysing=True
        st.session_state["question"] = None
        if analysing:
            analysing=False
            switch_page("Result")




if __name__ == "__main__":
    main()
