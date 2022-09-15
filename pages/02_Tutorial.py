import streamlit as st
import imageio
from utils.get_css import get_css


def main():
    st.set_page_config(page_title="JobPrepr: Tutorial", page_icon="💼", layout="centered")
    row1= st.empty()
    st.markdown(get_css(),unsafe_allow_html=True)
    if 'user_email' in st.session_state:
        st.markdown("<style>[data-testid='stSidebarNav']::after {{ {0} {1} }}</style>".format('content:',f"'Signed in as: {st.session_state.email}';"), unsafe_allow_html=True)
    if 'logged_in' not in st.session_state:
        logged_in=False
    else:
        logged_in=st.session_state["logged_in"]

    if 'tutorial_index' not in st.session_state:
        st.session_state['tutorial_index'] = 0

    with row1.container():
        st.markdown("<h1 style='text-align: center; color: black;'>How to use JobPrepr</h1>", unsafe_allow_html=True)
        st.write("Our app will help you feel more confident at your next video interview. You'll get a chance to practice interview questions and we'll give you feedback for each interview you film.")

    text = ["* Go to the **Interview** page.",
            "* Select the **area** that you are applying for from the drop down list. You will be able to see the selected area in the text on the page.",
            "* When you're ready to start the interview, click the **Start/Stop** checkbox.",
            "* A question will pop up on the screen and the video will start recording. You should answer the question you see on the screen. The clock at the bottom of the page indicates how many seconds you have left. If you run out of time, the recording will stop automatically. If you want to stop it earlier, click the **Start/Stop** checkbox.",
            "* Wait a couple of seconds for the result to be generated.",
            "* Once the result is generated, go to the **Result page**."
            ]
    images = ['screenshots/open_interview.png',
                'screenshots/area_selection.png',
                'screenshots/start_stop.png',
                'screenshots/video_recording.png',
                'screenshots/report_ready.png',
                'screenshots/open_result.png',
              ]
    page = st.empty()
    col1, col2, col3 = st.columns([1,1,1])

    with col1:
        if st.session_state['tutorial_index'] != 0:
            if st.button('Previous'):
                st.session_state['tutorial_index'] -= 1
                st.experimental_rerun()

    with col3:
        if st.session_state['tutorial_index'] != 5:
            if st.button('Next'):
                st.session_state['tutorial_index'] += 1
                st.experimental_rerun()

    with page.container():
        st.markdown(text[st.session_state['tutorial_index']])
        im = imageio.imread(images[st.session_state['tutorial_index']])
        st.image(im)
    st.session_state["photo_frames"]=[]

if __name__ == "__main__":
    main()
