import streamlit as st
import pandas as pd
from utils.emotions import emotions_names, show_strongest_emotion, show_emotion_graph
from utils.db_queries import read_results, get_user_email
from datetime import timedelta

def main():
    st.set_page_config(page_title="JobPrepr: Result history", page_icon="🤖", layout="centered")
    if 'logged_in' not in st.session_state:
        logged_in=False
    else:
        logged_in=st.session_state["logged_in"]

    if 'user_email' in st.session_state:
        st.markdown("<style>[data-testid='stSidebarNav']::after {{ {0} {1} }}</style>".format('content:',f"'Signed in as: {st.session_state.email}';"), unsafe_allow_html=True)

    if not logged_in:
        st.write("Please log in to access your result history.")
    else:
        with st.spinner("Loading..."):
            st.title(f"Result history for {get_user_email(st.session_state['user_id'])}")
            results_stored=read_results(st.session_state["user_id"])
        if results_stored:
            i=1
            for res1 in results_stored:
                emotions=pd.DataFrame(columns=emotions_names)
                for emotion in res1[1]["Emotions"]:
                    emotions=emotions.append(pd.DataFrame([emotion],
                    columns=emotions_names),
                    ignore_index=True)

                st.subheader(i)
                st.markdown(f"The results of your test no {i} on {(res1[0]+ timedelta(hours=1)).strftime('%d/%m/%Y, %H:%M')}:")
                i+=1

                st.subheader("😄")
                st.markdown("Let's analyse your facial expressions...")
                show_strongest_emotion(emotions)

                show_emotion_graph(emotions, emotions_list=res1[1]["Emotions"], images=res1[1]["Images"])
                st.write("")
                st.write("")

                #Voice
                st.subheader("🗣️")
                st.write("Let's analyse what you said...")
                transcription=res1[1]["Text"]
                score=res1[1]["Score"]
                label=res1[1]["Sentiment"]
                if transcription:
                    if label=="POSITIVE":
                        if score>50:
                            st.header(f'Wow! You sounded {score}% **positive**! 😄')
                            st.write("Keep it up!")
                        else:
                            st.header(f'You sounded {score}% **positive**.')
                            st.write("You might want to use more positive words.")

                    if label=="NEGATIVE":
                        if score>50:
                            st.header(f'Why so angry? You sounded {round(score)}% **negative**. 😡')
                            st.write("Next time, try using more positive words.")
                        else:
                            st.header(f'Upss... You sounded {round(score)}% **negative**.')
                            st.write("You might want to use more positive words.")

                    st.markdown(f"Sample sentence you said:")
                    st.markdown(f"""{transcription}""")

                #If the text counldn't be extracted
                else:
                    st.markdown("Sorry, we couldn't hear you... Please record a new response.")
                st.write("")
                st.write("---------------------------------------------------------------------")

    st.session_state["photo_frames"]=[]

if __name__ == "__main__":
    main()
