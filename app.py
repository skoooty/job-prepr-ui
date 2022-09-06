import streamlit as st
from streamlit_webrtc import (
    RTCConfiguration,
    VideoProcessorBase,
    webrtc_streamer,
)

from PIL import Image
import numpy as np
import cv2
import threading
import pandas as pd
from random import randint


RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

lock = threading.Lock()
img_container = {"frames":[]}

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

language = 'en'

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
        st.session_state["frames"]=[]
        if 'question' not in st.session_state or st.session_state["question"] == None:
            st.session_state['question'] = get_rand_question(questions, job_name)
        st.write(st.session_state['question'])

        webrtc_streamer(
            key="object-detection",
            video_frame_callback=VideoProcessor.video_frame_callback,
            media_stream_constraints={
                "video": True,
                "audio": False
            },
            desired_playing_state=playing
        )

    if 'frames' not in st.session_state:
        st.session_state['frames'] = img_container["frames"]

    if 'all_faces' not in st.session_state:
        st.session_state['all_faces'] = []

    else:
        if len(st.session_state['frames']) < 1:
            st.session_state['frames'] = img_container["frames"]

    if not playing:
        frames=st.session_state["frames"]
        frames=frames[::15]
        if len(frames):
            st.write(f"We've collected {len(frames)} frames...")
            analysing=True
        for frame in frames:
            st.image(frame)
        if analysing:
            st.button("Get the report")
        st.session_state["question"] = None




if __name__ == "__main__":
    main()
