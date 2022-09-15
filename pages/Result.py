import streamlit as st
import pandas as pd
import requests
import json
import cv2
from utils.emotions import emotions_names, show_strongest_emotion, show_emotion_graph
from utils.voice import transcribe
from utils.get_css import get_css
from utils.db_queries import save_results, get_user_email


resolution=48 #e.g.48 means that the resolution is (48,48,1)
output_resolution = 200
url_api_face_rec="https://jobpreprtest-lbzgzaglla-ew.a.run.app/predict" #API for analysing te facial expressions
frame_rate=15 #If it's e.g.15, this means we analyse each 15th frame

def main():
    st.set_page_config(page_title="JobPrepr: Result", page_icon="💼", layout="centered")
    st.markdown(get_css(),unsafe_allow_html=True)
    if 'email' in st.session_state:
        st.markdown("<style>[data-testid='stSidebarNav']::after {{ {0} {1} }}</style>".format('content:',f"'Signed in as: {st.session_state.email}';"), unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        logged_in=False
    else:
        logged_in=st.session_state["logged_in"]

    if ("photo_frames" not in st.session_state or not len(st.session_state["photo_frames"])):
        st.markdown("<p style=text-align:left;>Please go to the Interview page and record your response.</p>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align: center; color: black;'>Results</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style=text-align:center>😄</p>", unsafe_allow_html=True)
        st.markdown("<p style=text-align:left;>Let's analyse your facial expressions...</p>", unsafe_allow_html=True)


        with st.spinner("Loading..."):
            #Extracting the frames
            full_frames=st.session_state["photo_frames"]
            frames=full_frames[::frame_rate]

            #Storing emotions
            emotions=[]
            frames_as_list=[]
            for frame in frames:
                frame_res=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame_res=cv2.resize(frame_res, dsize=(resolution,resolution), interpolation=cv2.INTER_CUBIC)
                emotion=requests.post(url_api_face_rec,json=json.dumps(frame_res.tolist())).json()[0]
                emotions.append(emotion)
                frames_as_list.append(cv2.resize(frame,dsize=(output_resolution,output_resolution)).tolist()) #frames_as_list.append(frame.tolist())


            #Storing sentiment
            transcription, web_transcript = transcribe("record.mp3")
            score = 0
            label=""
            if transcription:
                #Getting text from voice
                response = requests.get(f'https://npapi-lbzgzaglla-ew.a.run.app/predictnlp?text={transcription}').json()[0]


                #Analysing the score
                score=round(response["score"]*100)

                label=response["label"]




            emotions_pd=pd.DataFrame(columns=emotions_names)

            for emotion in emotions:
                emotions_pd=emotions_pd.append(pd.DataFrame([emotion],
                columns=emotions_names),
                ignore_index=True)

        #Printing the report
        show_strongest_emotion(emotions_pd)
        images_list = show_emotion_graph(emotions_pd, emotions, frames_as_list, images=None)

        #Voice
        st.write(" ")
        st.write(" ")
        st.markdown("<h2 style=text-align:center>🗣️</p>", unsafe_allow_html=True)
        st.markdown("<p style=text-align:left;>Let's analyse what you said...</p>", unsafe_allow_html=True)
        if transcription:
            if response["label"]=="POSITIVE":
                if score>50:
                    st.markdown(f'<h2 style=text-align:left;>Wow! You sounded {score}% <b>positive</b>! 😄</h2>', unsafe_allow_html=True)
                    st.markdown("<p style=text-align:left;>Keep it up!</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f'<h2 style=text-align:left;>You sounded {score}% **positive**.</h2>', unsafe_allow_html=True)
                    st.markdown("<p style=text-align:left;>You might want to use more positive words.", unsafe_allow_html=True)

            if response["label"]=="NEGATIVE":
                if score>50:
                    st.markdown(f'<h2 style=text-align:left;>Why so angry? You sounded {score}% negative. 😡</h2>', unsafe_allow_html=True)
                    st.markdown("<p style=text-align:left;>Next time, try using more positive words.</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f'<h2 style=text-align:left;>Oops... You sounded {score}% negative.</h2>', unsafe_allow_html=True)
                    st.marldown("<p style=text-align:left;>You might want to use more positive words.</p>", unsafe_allow_html=True)

            st.markdown(f"<p style=text-align:left;>Sample sentence you said:</p>", unsafe_allow_html=True)
            st.markdown(f"""<p style=text-align:left>{web_transcript} </p>""", unsafe_allow_html=True)

        #If the text counldn't be extracted
        else:
            st.markdown("<p style=text-align:left;>Sorry, we couldn't hear you... Please record a new response.</p>", unsafe_allow_html=True)

        if logged_in:
            #Saving the result
            result={"Emotions": emotions, "Sentiment":label, "Score": score, "Text":web_transcript,"Images":images_list}
            st.markdown(f"<p style=text-align:left;>You're logged in as {get_user_email(st.session_state['user_id'])}</p>", unsafe_allow_html=True)

            if result["Emotions"]:
                save_results(st.session_state["user_id"], result)
                st.markdown(f"<p style=text-align:left;>We've stored your result.</p>", unsafe_allow_html=True)

        result=[]
        st.session_state["photo_frames"]=[]

if __name__ == "__main__":
    main()
