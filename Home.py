import streamlit as st
import imageio
from utils.db_queries import login_user, create_new_user, get_user_id
from utils.get_css import get_css

def main():

    # logo = imageio.imread('./Logo.png')
    # st.sidebar.image(logo)

    st.markdown(get_css(),unsafe_allow_html=True)
    logged_in=False
    st.session_state['index'] = 0
    st.markdown("<h1 style='text-align: center; color: #0E27C8;'>Welcome to JobPrepr!</h1>", unsafe_allow_html=True)


    st.markdown("Please type in your email and password to log in, or tick the **Sign Up** checkbox to create a new account.")
    chk = st.checkbox("Sign Up")
    if chk:
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
        email = st.text_input('Email', '', key=4)
        password = st.text_input('Password', '', key=5)
        if st.button('Log In'):
            logged_in=False
            log=login_user(email, password)
            if log == 1:
                logged_in=True
                st.subheader("You're logged in, let'go!")
                st.session_state["user_id"] = get_user_id(email)
            else:
                st.write("The email and password don't match.")

    st.session_state["logged_in"]=logged_in
    st.session_state["photo_frames"]=[]

if __name__ == "__main__":
    main()
