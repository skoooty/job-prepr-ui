import streamlit as st
import pandas as pd
import requests
import json
import cv2
from utils.emotions import emotions_names, show_strongest_emotion, show_emotion_graph
from utils.voice import transcribe
from utils.get_css import get_css


resolution=48 #e.g.48 means that the resolution is (48,48,1)
url_api_face_rec="https://jobpreprtest-lbzgzaglla-ew.a.run.app/predict" #API for analysing te facial expressions
frame_rate=15 #If it's e.g.15, this means we analyse each 15th frame

def main():

    st.markdown(get_css(),unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        logged_in=False
    else:
        logged_in=st.session_state["logged_in"]

    if "photo_frames" not in st.session_state:
        st.write("Please go to the Interview page and record your response.")
    else:
        st.markdown("<h1 style='text-align: center; color: black;'>Results</h1>", unsafe_allow_html=True)
        st.markdown("😄 Let's analyse your facial expressions...")

        full_frames=st.session_state["photo_frames"]
        frames=full_frames[::frame_rate]
        st.write(len(frames))

        emotions=[]
        for frame in frames:
            frame_res=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_res=cv2.resize(frame_res, dsize=(resolution,resolution), interpolation=cv2.INTER_CUBIC)
            emotion=requests.post(url_api_face_rec,json=json.dumps(frame_res.tolist())).json()[0]
            emotions.append(emotion)

        #Storing the final output
        result={"Frames": frames, "Emotions": emotions}
        st.session_state["result"]=result

        emotions=pd.DataFrame(columns=emotions_names)
        for emotion in result["Emotions"]:
            emotions=emotions.append(pd.DataFrame([emotion],
            columns=emotions_names),
            ignore_index=True)

        show_strongest_emotion(emotions)
        show_emotion_graph(emotions, result)

        #Voice
        st.write(" ")
        st.write(" ")
        st.write("🗣️ Let's analyse what you said...")

        transcription, web_transcript = transcribe("record.mp3")

        if transcription:
            st.markdown(f"Sample sentence you said:")
            st.markdown(f"""{web_transcript}""")

            #Getting text from voice
            response = requests.get(f'https://npapi-lbzgzaglla-ew.a.run.app/predictnlp?text={transcription}').json()[0]

            #Analysing the score
            score=round(response["score"]*100)

            if response["label"]=="POSITIVE":
                if score>50:
                    st.header(f'Wow! You sounded {score}% **positive**! 😄')
                    st.write("Keep it up!")
                else:
                    st.header(f'You sounded {score}% **positive**.')
                    st.write("You might want to use more positive words.")

            if response["label"]=="NEGATIVE":
                if score>50:
                    st.header(f'Why so angry? You sounded {round(response["score"]*100)}% **negative**. 😡')
                    st.write("Next time, try using more positive words.")
                else:
                    st.header(f'Upss... You sounded {round(response["score"]*100)}% **negative**.')
                    st.write("You might want to use more positive words.")

        #If the text counldn't be extracted
        else:
            st.markdown("Sorry, we couldn't hear you... Please record a new response.")

if __name__ == "__main__":
    main()
