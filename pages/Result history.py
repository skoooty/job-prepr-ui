from http.client import UnknownTransferEncoding
import streamlit as st
import pandas as pd
from utils.emotions import emotions_names, show_strongest_emotion, show_emotion_graph
from utils.db_queries import read_results, get_user_email
from utils.get_css import get_css
from datetime import timedelta

def main():
    st.set_page_config(page_title="JobPrepr: Result history", page_icon="💼")
    st.markdown(get_css(), unsafe_allow_html=True)
    if 'logged_in' not in st.session_state:
        logged_in=False
    else:
        logged_in=st.session_state["logged_in"]

    if 'user_email' in st.session_state:
        st.markdown("<style>[data-testid='stSidebarNav']::after {{ {0} {1} }}</style>".format('content:',f"'Signed in as: {st.session_state.email}';"), unsafe_allow_html=True)

    if not logged_in:
        st.markdown("<p style=text-align:left>Please log in to access your result history.</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h1 style=text-align:center>Result history for {get_user_email(st.session_state['user_id'])}</h1>", unsafe_allow_html=True)
        with st.spinner("Loading..."):
            results_stored=read_results(st.session_state["user_id"])
        if results_stored:
            i=1
            for res1 in results_stored:
                emotions=pd.DataFrame(columns=emotions_names)
                for emotion in res1[1]["Emotions"]:
                    emotions=emotions.append(pd.DataFrame([emotion],
                    columns=emotions_names),
                    ignore_index=True)

                st.markdown(f"<h2 style=text-align:left>{i}</h2>", unsafe_allow_html=True)
                st.markdown(f"<p style=text-align:left>The results of your test no {i} on {(res1[0]+ timedelta(hours=1)).strftime('%d/%m/%Y, %H:%M')}:</h4>", unsafe_allow_html=True)

                i+=1

                st.markdown("<h2 style=text-align:left>😄</p>", unsafe_allow_html=True)
                st.markdown("<p style=text-align:left;>Let's analyse your facial expressions...</p>", unsafe_allow_html=True)
                show_strongest_emotion(emotions)

                show_emotion_graph(emotions, emotions_list=res1[1]["Emotions"], images=res1[1]["Images"])
                st.write("")
                st.write("")

                #Voice
                st.markdown("<h2 style=text-align:left>🗣️</p>", unsafe_allow_html=True)
                st.markdown("<p style=text-align:left;>Let's analyse what you said...</p>", unsafe_allow_html=True)
                transcription=res1[1]["Text"]
                score=res1[1]["Score"]
                label=res1[1]["Sentiment"]
                if transcription:
                    if label=="POSITIVE":
                        if score>50:
                            st.markdown(f'<h2 style=text-align:left;>Wow! You sounded {score}% <b>positive</b>! 😄</h2>', unsafe_allow_html=True)
                            st.markdown("<p style=text-align:left;>Keep it up!</p>", unsafe_allow_html=True)
                        else:
                            st.markdown(f'<h2 style=text-align:left;>You sounded {score}% **positive**.</h2>', unsafe_allow_html=True)
                            st.markdown("<p style=text-align:left;>You might want to use more positive words.", unsafe_allow_html=True)

                    if label=="NEGATIVE":
                        if score>50:
                            st.markdown(f'<h2 style=text-align:left;>Why so angry? You sounded {score}% negative. 😡</h2>', unsafe_allow_html=True)
                            st.markdown("<p style=text-align:left;>Next time, try using more positive words.</p>", unsafe_allow_html=True)
                        else:
                            st.markdown(f'<h2 style=text-align:left;>Oops... You sounded {score}% negative.</h2>', unsafe_allow_html=True)
                            st.marldown("<p style=text-align:left;>You might want to use more positive words.</p>", unsafe_allow_html=True)

                    st.markdown(f"<p style=text-align:left;>Sample sentence you said:</p>", unsafe_allow_html=True)
                    st.markdown(f"""<p style=text-align:left>{transcription} </p>""", unsafe_allow_html=True)

                #If the text counldn't be extracted
                else:
                    st.markdown("Sorry, we couldn't hear you... Please record a new response.")
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("-----------------------------------------------------------------------------------")

    st.session_state["photo_frames"]=[]

if __name__ == "__main__":
    main()
