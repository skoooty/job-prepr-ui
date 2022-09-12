from fcntl import DN_DELETE
from xml.sax.handler import DTDHandler
import streamlit as st
import imageio
from utils.db_queries import login_user, create_new_user

logged_in=False

def main():
    logged_in=False

    st.title("Welcome!")

    st.subheader("I'm Samantha and I'll help you to prepare for your next interview.")
    im = imageio.imread('robot.png')
    st.image(im)

    if st.checkbox("Sign Up"):
        st.markdown("Create a new account, or untick the **Sign Up** checkbox to log in.")

        email_new = st.text_input('Email ', '', key=1)
        password1 = st.text_input('Password ', '', key=2)
        password2 = st.text_input('Confirm password', '', key=3)

        if password1==password2:
            if "@" in email_new:
                if st.button('Sign Up'):
                    log=login_user(email_new, password1)
                    if log == 1:
                        st.write("This email is already in use.")
                    else:
                        if create_new_user(email_new, password1):
                            st.subheader("You've created a new account! Please, log in")
                        else:
                            st.write("This email is already in use.")
            else:
                st.write("This is not a proper email adress.")
        else:
            st.write("Passwords don't match.")

    else:
        st.markdown("Please type in your email and password to log in, or tick the **Sign Up** checkbox to create a new account.")
        email = st.text_input('Email', '', key=4)
        password = st.text_input('Password', '', key=5)
        if st.button('Log In'):
            logged_in=False
            log=login_user(email, password)
            if log == 1:
                logged_in=True
                st.subheader("You're logged in, let'go!")

            else:
                st.write("The email and password don't match.")

    st.session_state["logged_in"]=logged_in



if __name__ == "__main__":
    main()
