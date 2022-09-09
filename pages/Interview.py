import streamlit as st
from streamlit_webrtc import (
    VideoProcessorBase,
    webrtc_streamer,
    VideoHTMLAttributes
)
import threading
import requests
import json
from streamlit_webrtc import (
    VideoProcessorBase
)
import cv2
from aiortc.contrib.media import MediaRecorder
import imageio
import time
from utils.video import find_face
from utils.questions import load_questions, get_rand_question
import pathlib

#Defining the variables
lock = threading.Lock()
img_container = {"frames":[]}
url_api_face_rec="https://jobpreprtest-lbzgzaglla-ew.a.run.app/predict" #API for analysing te facial expressions
result = {}
frame_rate=15 #If it's e.g.15, this means we analyse each 15th frame
resolution=48 #e.g.48 means that the resolution is (48,48,1)
s_per_question=60 #maximum duration of the video input in s

#Saving the audio input
def recorder_factory():
    return MediaRecorder("record.mp3")

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

def main():
    #Button code
    file_path=pathlib.Path(__file__).resolve().parent.parent.joinpath("styles", "main.css")
    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    #Questions and area selection
    questions=load_questions()
    job_list = questions["Area"].unique()

    #Sidebar
    with st.sidebar:
        st.title('Area Selection')
        job_name = st.selectbox("Select the job that you are applying for:", job_list)

    #Title, text, page setup
    st.title("How confident are you?")
    st.markdown(f"Let's practice for your {job_name} interview.")
    st.markdown(f"You have {s_per_question}s to answer the question that will pop up on the screen.")
    st.markdown(f"**Good luck!**")
    playing = st.checkbox("Start/Stop", value=False)
    analysing=False

    #Recording the video
    if playing:
        st.session_state["photo_frames"]=[]
        if 'question' not in st.session_state or st.session_state["question"] == None:
            st.session_state['question'] = get_rand_question(questions, job_name)
        st.subheader(st.session_state['question'])
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
        frames=full_frames[::frame_rate]
        if len(frames):
            analysing=True

        #Storing emotions
        if analysing:
            emotions=[]
            for frame in frames:
                frame_res=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame_res=cv2.resize(frame_res, dsize=(resolution,resolution), interpolation=cv2.INTER_CUBIC)
                emotion=requests.post(url_api_face_rec,json=json.dumps(frame_res.tolist())).json()[0]
                emotions.append(emotion)

            #Storing the final output
            result={"Frames": frames, "Emotions": emotions}
            st.session_state["result"]=result

            #Message to the user
            st.header("Amazing!")
            st.markdown("We have analysed your response.\n Go to the **Result** page to check it out :)")
            im = imageio.imread('screenshots/rep_pg.png')
            st.image(im)
            st.markdown("...or start a new session.")

        st.session_state["question"] = None

if __name__ == "__main__":
    main()
