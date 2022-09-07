import streamlit as st
from pages.Interview import result
import pandas as pd
import numpy as np

emotinos_names = [
        'angry',
        'disgusted',
        'affraid',
        'happy',
        'neutral',
        'sad',
        'surprised']

def show_strongest_emotion(emotions):
    strongest_emotion={"Emotion":"angry", "Perc": 0}
    for emotion in emotinos_names:
        perc=round(emotions[emotion].mean()*100)
        if strongest_emotion["Perc"]<perc:
            strongest_emotion["Perc"]=perc
            strongest_emotion["Emotion"]=emotion
    st.markdown(f'You seemed mostly **{strongest_emotion["Emotion"]}** ({strongest_emotion["Perc"]}%).\n')

def most_emotional_face(emotion, result):
    emotion_index=emotinos_names.index(emotion)
    index_most=0
    perc_most=0
    for i, v in enumerate(result["Emotions"]):
        if v[emotion_index]>perc_most:
            perc_most=v[emotion_index]
            index_most=i
    return result["Frames"][index_most]


def show_emotion_perc(emotions):
    for emotion in emotinos_names:
        perc=round(emotions[emotion].mean()*100)
        st.write(f"You were **{perc}%** {emotion}.\n")


def show_emotion_graph(emotions, result):
    for emotion in emotinos_names:
        st.subheader(emotion)
        st.line_chart(emotions[emotion]*100)
        st.write(f"You were **{round(emotions[emotion].mean()*100)}%** {emotion}.\n This is your most {emotion} face:")
        image=most_emotional_face(emotion, result)
        st.image(image)
def main():


    if "result" not in st.session_state:
        st.write("Please go to the Interview page and record your response.")
    else:
        st.title("Good job!")
        st.subheader("Let's analyse your facial expressions...")
        result=st.session_state["result"]

        emotions=pd.DataFrame(columns=emotinos_names)
        for emotion in result["Emotions"]:
            emotions=emotions.append(pd.DataFrame([emotion],
            columns=emotinos_names),
            ignore_index=True)
        #st.dataframe(emotions)

        show_strongest_emotion(emotions)
        show_emotion_graph(emotions, result)








if __name__ == "__main__":
    main()
