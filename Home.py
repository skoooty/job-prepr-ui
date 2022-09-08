import streamlit as st
import imageio

def main():
    st.title("Welcome!")

    st.subheader("I'm Samantha and I'll help you to prepare for your next interview.")
    im = imageio.imread('robot.png')
    st.image(im)
    # im = imageio.imread('job-prepr-logo.jpg')
    # st.image(im)
    st.subheader("Let'go!")

if __name__ == "__main__":
    main()
