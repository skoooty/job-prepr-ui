import streamlit as st
import imageio
from utils.db_queries import login_user, create_new_user, get_user_id
from utils.get_css import get_css
import streamlit.components.v1 as components

def main():

    logo = imageio.imread('./Logo.png')

    st.set_page_config(page_title="JobPrepr: Home", page_icon="💼", layout="centered")
    st.markdown(get_css(),unsafe_allow_html=True)
    logged_in=False
    st.session_state['index'] = 0
    st.markdown("<h1 style='text-align: center; color: #0E27C8;'>Welcome to JobPrepr!</h1>", unsafe_allow_html=True)


    st.markdown("Please type in your email and password to log in, or tick the **Sign Up** checkbox to create a new account.")
    chk = st.checkbox("Sign Up")
    if chk:
        email_new = st.text_input('Email ', '', key=1)
        password1 = st.text_input('Password ', '', key=2, type='password')
        password2 = st.text_input('Confirm password', '', key=3, type='password')

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
        password = st.text_input('Password', '', key=5, type='password')
        if st.button('Log In'):
            logged_in=False
            log=login_user(email, password)
            if log == 1:
                logged_in=True
                st.subheader("You're logged in, let's go!")
                st.session_state['email'] = email
                st.markdown("<style>[data-testid='stSidebarNav']::after {{ {0} {1} }}</style>".format('content:',f"'Signed in as: {st.session_state.email}';"), unsafe_allow_html=True)
                st.session_state["user_id"] = get_user_id(email)
            else:
                st.write("The email and password don't match.")

    st.session_state["logged_in"]=logged_in
    st.session_state["photo_frames"]=[]

if __name__ == "__main__":
    main()
