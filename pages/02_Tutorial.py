import streamlit as st
import imageio
from Home import logged_in

def main():
    logged_in=st.session_state["logged_in"]

    st.title("How to use our app?")
    st.write("Our app will help you feel more confident at your next video interview. You'll get a chance to practice interview questions and we'll give you feedback for each interview you film.")

    st.subheader("Interview")

    st.markdown("* Go to the **Interview** page.")
    im = imageio.imread('screenshots/open_interview.png')
    st.image(im)

    st.write("")
    st.write("")
    st.markdown("* Select the **area** that you are applying for from the drop down list. You will be able to see the selected area in the text on the page.")
    im = imageio.imread('screenshots/area_selection.png')
    st.image(im)

    st.write("")
    st.write("")
    st.markdown("* When you're ready to start the interview, click the **Start/Stop** checkbox.")
    im = imageio.imread('screenshots/start_stop.png')
    st.image(im)

    st.write("")
    st.write("")
    st.markdown("* A question will pop up on the screen and the video will start recording. You should answer the question you see on the screen. The clock at the bottom of the page indicates how many seconds you have left. If you run out of time, the recording will stop automatically. If you want to stop it earlier, click the **Start/Stop** checkbox.")
    im = imageio.imread('screenshots/video_recording.png')
    st.image(im)

    st.write("")
    st.write("")
    st.markdown("* Wait a couple of seconds for the result to be generated.")
    im = imageio.imread('screenshots/report_ready.png')
    st.image(im)

    st.write("")
    st.write("")
    st.markdown("* Once the result is generated, go to the **Result page**.")
    im = imageio.imread('screenshots/open_result.png')
    st.image(im)


if __name__ == "__main__":
    main()
