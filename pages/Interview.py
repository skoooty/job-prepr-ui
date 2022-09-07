import streamlit as st
from streamlit_webrtc import (
    RTCConfiguration,
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

RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})


lock = threading.Lock()
img_container = {"frames":[]}
url_api_face_rec="https://jobpreprtest-lbzgzaglla-ew.a.run.app/predict"
language = 'en'

result = {}

y_label_dict = {
    'angry':0,
    'disgust':1,
    'fear':2,
    'happy':3,
    'neutral':4,
    'sad':5,
    'surprise':6
}


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
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

        faces = face_cascade.detectMultiScale(
                                                image,
                                                scaleFactor=1.3,
                                                minNeighbors=3,
                                                minSize=(30, 30)
                                                        )
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            just_face = image[y:y + h, x:x + w]
            just_face=np.array(Image.fromarray(just_face).resize((48,48)))
            return just_face
    except:
        return None

def load_questions():
    questions = pd.read_csv('interview_questions.csv',
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
    questions=load_questions()
    job_list = questions["Area"].unique()

    with st.sidebar:
        st.title('Area Selection')
        job_name = st.selectbox("Select the job that you are applying for:", job_list)
    st.title("How confident are you?")
    st.write(f"Let's practice for your {job_name} interview.")
    playing = st.checkbox("Start a new session.", value=False)
    analysing=False

    if playing:
        st.session_state["photo_frames"]=[]

        if 'question' not in st.session_state or st.session_state["question"] == None:
            st.session_state['question'] = get_rand_question(questions, job_name)
        st.write(st.session_state['question'])

        webrtc_streamer(
            key="object-detection",
            video_frame_callback=VideoProcessor.video_frame_callback,
            media_stream_constraints={
                "video": True,
                "audio": True
            },
            desired_playing_state=playing
            , in_recorder_factory=recorder_factory
            , video_html_attrs = VideoHTMLAttributes(muted=True, volume=0, autoPlay=True, controls=False)
        )
        print(img_container)

    if 'photo_frames' not in st.session_state:
        st.session_state['photo_frames'] = img_container["frames"]

    else:
        if len(st.session_state['photo_frames']) < 1:
            st.session_state['photo_frames'] = img_container["frames"]


    if 'all_faces' not in st.session_state:
        st.session_state['all_faces'] = []

    if not playing:

        frames=st.session_state["photo_frames"]
        frames=frames[::15]
        if len(frames):
            #st.write(f"We've collected {len(frames)} frames...")
            analysing=True
        if analysing:
            emotions=[]
            for frame in frames:
                frame=frame.reshape(48,48,1)
                #st.image(frame)
                emotion=requests.post(url_api_face_rec,json=json.dumps(frame.tolist())).json()[0]
                emotions.append(emotion)
            for i,v in enumerate(frames):
                result[i] = {"Frame": v, "Emotions": emotions[i]}
            #st.write(result)


        st.session_state["question"] = None
    st.write(result)
    st.session_state["result"]=result


if __name__ == "__main__":
    main()
