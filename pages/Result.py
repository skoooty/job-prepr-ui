import streamlit as st
import pandas as pd
import requests
from utils.emotions import emotions_names, show_strongest_emotion, show_emotion_graph
from utils.voice import transcribe
from pages.Interview import result

def main():
    if "result" not in st.session_state:
        st.write("Please go to the Interview page and record your response.")
    else:
        st.title("Good job!")
        st.markdown("😄 Let's analyse your facial expressions...")
        result=st.session_state["result"]

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

        transcription=transcribe("record.mp3")

        if transcription:
            st.markdown(f"You said:")
            st.markdown(f"""{transcription}""")

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
