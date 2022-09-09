from multiprocessing.resource_sharer import stop
from tkinter.tix import ButtonBox
import streamlit as st
from streamlit_webrtc import (
    VideoProcessorBase,
    webrtc_streamer,
    VideoHTMLAttributes
)

from PIL import Image
import numpy as np
import cv2
import threading
import pandas as pd
from random import randint
import requests
import json
from aiortc.contrib.media import MediaRecorder
import imageio
import time


lock = threading.Lock()
img_container = {"frames":[]}
url_api_face_rec="https://jobpreprtest-lbzgzaglla-ew.a.run.app/predict"
language = 'en'
result = {}
interview_questions='interview_questions.csv'
frame_rate=15
resolution=48
s_per_question=60


def recorder_factory():
    return MediaRecorder("record.mp3")

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.style = 'color'

    def video_frame_callback(self):
        img = self.to_ndarray(format="bgr24")
        img = find_face(img)
        with lock:
            if img is not None:
                img_container["frames"].append(img)

def find_face(image):
    try:
        image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

        faces = face_cascade.detectMultiScale(
                                                image1,
                                                scaleFactor=1.3,
                                                minNeighbors=3,
                                                minSize=(30, 30)
                                                        )
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            just_face = image[y:y + h, x:x + w]
            just_face=np.array(Image.fromarray(just_face)
            )
            return just_face
    except:
        return None

def load_questions():
    questions = pd.read_csv(interview_questions,
                            header=0,
                            names=["Area", "Question"],
                            on_bad_lines='skip',
                            delimiter=";")
    return questions

def get_rand_question(questions, job_name):
    questions=questions[questions["Area"]==job_name]
    no_of_q=questions.shape[0]
    index=randint(0, no_of_q-1)
    return questions["Question"].iloc[index]

def main():
    #st.set_page_config()
    questions=load_questions()
    job_list = questions["Area"].unique()

    with st.sidebar:
        st.title('Area Selection')
        job_name = st.selectbox("Select the job that you are applying for:", job_list)
    st.title("How confident are you?")
    st.markdown(f"Let's practice for your {job_name} interview.")
    st.markdown(f"You have {s_per_question}s to answer the question that will pop up on the screen.")
    st.markdown(f"**Good luck!**")
    playing = st.checkbox("Start/Stop", value=False)
    analysing=False

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
            desired_playing_state=playing
            , in_recorder_factory=recorder_factory
            , video_html_attrs = VideoHTMLAttributes(muted=True, volume=0, autoPlay=True, controls=False, stop=False)
            ,
        )

        print(img_container)

    if 'photo_frames' not in st.session_state:
        st.session_state['photo_frames'] = img_container["frames"]

    else:
        if len(st.session_state['photo_frames']) < 1:
            st.session_state['photo_frames'] = img_container["frames"]

    if playing:
        ph = st.empty()
        for secs in range(s_per_question,0,-1):
            mm, ss = secs//60, secs%60
            ph.metric("", f"{mm:02d}:{ss:02d}")
            time.sleep(1)
        playing=False

    if 'all_faces' not in st.session_state:
        st.session_state['all_faces'] = []

    if not playing:

        full_frames=st.session_state["photo_frames"]
        frames=full_frames[::frame_rate]
        if len(frames):
            analysing=True
        if analysing:
            emotions=[]
            for frame in frames:
                frame_res=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame_res=cv2.resize(frame_res, dsize=(resolution,resolution), interpolation=cv2.INTER_CUBIC)
                emotion=requests.post(url_api_face_rec,json=json.dumps(frame_res.tolist())).json()[0]
                emotions.append(emotion)
            result={"Frames": frames, "Emotions": emotions}
            st.session_state["result"]=result
            st.header("Amazing!")
            st.markdown("We have analysed your response.\n Go to the **Result** page to check it out :)")
            im = imageio.imread('rep_pg.png')
            st.image(im)
            st.markdown("...or start a new session.")

        st.session_state["question"] = None



if __name__ == "__main__":
    main()
