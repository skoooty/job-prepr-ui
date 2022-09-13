import streamlit as st
import imageio
from utils.get_css import get_css


def main():

    st.markdown(get_css(),unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        logged_in=False
    else:
        logged_in=st.session_state["logged_in"]

    st.markdown("<h1 style='text-align: center; color: black;'>Room Setup</h1>", unsafe_allow_html=True)

    #Quiet
    st.subheader("Quiet room")
    im = imageio.imread('tutorial_pics/too_many_people.jpg')
    st.image(im)
    st.header("❌")
    st.write("Find a quiet room. You don't want the voices in the background to disturb the algorithm.")

    #Lighting
    st.subheader("Lighting")

    columns = st.columns(2)

    im = imageio.imread('tutorial_pics/too_dark.jpg')
    columns[0].image(im)
    columns[0].header("❌")
    columns[0].write("Make sure there is enough light in the room.")

    im = imageio.imread('tutorial_pics/bad_light.jpg')
    columns[1].image(im)
    columns[1].header("❌")
    columns[1].write("Make sure the source of light is in front of you, not behind.")

    #Position
    st.subheader("Position")
    im = imageio.imread('tutorial_pics/far_away.jpg')
    st.image(im)
    st.header("❌")
    st.write("Make sure you are not too far away from the camera.")

    #One person
    st.subheader("One person")
    im = imageio.imread('tutorial_pics/two_people.jpg')
    st.image(im)
    st.header("❌")
    st.write("Make sure you are the only person visible on camera. The algoritham won't know which face to analyse otherwise.")

    #Good
    st.subheader("Ready?")
    im = imageio.imread('tutorial_pics/good.jpg')
    st.image(im)
    st.header("✅")
    st.write("Good! You're all set for the interview!")

if __name__ == "__main__":
    main()
