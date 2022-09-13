import streamlit as st
import imageio
from utils.get_css import get_css


def main():

    row1= st.empty()
    st.markdown(get_css(),unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        logged_in=False
    else:
        logged_in=st.session_state["logged_in"]

    if 'index' not in st.session_state:
        st.session_state['index'] = 0

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
        st.button('Previous')

    if col1 and st.session_state['index'] != 0:
        st.session_state['index'] -= 1

    with col2:
        st.write(f"Step {st.session_state['index']+1}")

    with col3:
        st.button('Next')

    if col2:
        st.session_state['index'] += 1

    with page.container():
        st.markdown(text[st.session_state['index']])
        im = imageio.imread(images[st.session_state['index']])
        st.image(im)


if __name__ == "__main__":
    main()
