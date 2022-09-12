from xml.sax.handler import DTDHandler
import streamlit as st
import imageio

def existing_user(email, password):
    """Checks if a username exist and the pasword is correct.
        0 - doesn't exist
        1 - wrong password
        2 - right password"""
    return 0

def main():
    st.title("Welcome!")

    st.subheader("I'm Samantha and I'll help you to prepare for your next interview.")
    im = imageio.imread('robot.png')
    st.image(im)
    login_active=False
    columns = st.columns(2)

    columns[0].subheader("Log In")

    email = columns[0].text_input('Email', '')
    password = columns[0].text_input('Password', '')
    loged_in=False

    if columns[0].button('Log In'):
        log=existing_user(email, password)
        if log == 2:
            loged_in=True
            columns[0].subheader("Let'go!")
        else:
            if log == 1:
                columns[0].write("Wrong password.")
            else:
                columns[0].write("The email and password don't match.")

    columns[1].subheader('Sign Up')

    email1 = columns[1].text_input('Email ', '')
    password1 = columns[1].text_input('Password ', '')
    password2 = columns[1].text_input('Confirm password', '')

    if columns[1].button('Sign Up'):
        log=existing_user(email1, password1)
        if log:
            columns[1].write("This email is already in use.")
        else:
            columns[1].write("We've created an account for you.")
            columns[1].write("Please, log in.")

if __name__ == "__main__":
    main()
