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
output_resolution=200

url_api_face_rec="https://jobpreprtest-lbzgzaglla-ew.a.run.app/predict" #API for analysing te facial expressions
frame_rate=15 #If it's e.g.15, this means we analyse each 15th frame

def main():

    st.markdown(get_css(),unsafe_allow_html=True)
    if 'user_email' in st.session_state:
        st.markdown("<style>[data-testid='stSidebarNav']::after {{ {0} {1} }}</style>".format('content:',f"'Signed in as: {st.session_state.email}';"), unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        logged_in=False
    else:
        logged_in=st.session_state["logged_in"]

    if ("photo_frames" not in st.session_state or not len(st.session_state["photo_frames"])):
        st.write("Please go to the Interview page and record your response.")
    else:
        st.markdown("<h1 style='text-align: center; color: black;'>Results</h1>", unsafe_allow_html=True)
        st.subheader("😄")
        st.markdown("Let's analyse your facial expressions...")

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
        st.subheader("🗣️")
        st.markdown("Let's analyse what you said...")
        if transcription:
            if response["label"]=="POSITIVE":
                if score>50:
                    st.header(f'Wow! You sounded {score}% **positive**! 😄')
                    st.write("Keep it up!")
                else:
                    st.header(f'You sounded {score}% **positive**.')
                    st.write("You might want to use more positive words.")

            if response["label"]=="NEGATIVE":
                if score>50:
                    st.header(f'Why so angry? You sounded {score}% **negative**. 😡')
                    st.write("Next time, try using more positive words.")
                else:
                    st.header(f'Upss... You sounded {score}% **negative**.')
                    st.write("You might want to use more positive words.")

            st.markdown(f"Sample sentence you said:")
            st.markdown(f"""{web_transcript}""")

        #If the text counldn't be extracted
        else:
            st.markdown("Sorry, we couldn't hear you... Please record a new response.")

        if logged_in:
            #Saving the result
            #Storing the final output
            #import ipdb; ipdb.set_trace()
            result={"Emotions": emotions, "Sentiment":label, "Score": score, "Text":web_transcript,"Images":images_list}
            st.write(f"You're logged in as {get_user_email(st.session_state['user_id'])}")

            if result["Emotions"]:
                save_results(st.session_state["user_id"], result)
                st.write(f"We've stored your result.")

        result=[]
        st.session_state["photo_frames"]=[]

if __name__ == "__main__":
    main()
