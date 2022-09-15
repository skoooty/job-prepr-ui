from email.headerregistry import UniqueSingleAddressHeader
import streamlit as st
import imageio
from utils.db_queries import login_user, create_new_user, get_user_id
from utils.get_css import get_css
import streamlit.components.v1 as components

def main():




    st.set_page_config(page_title="JobPrepr: Home", page_icon="💼")

    st.markdown(get_css(),unsafe_allow_html=True)
    logged_in=False
    st.session_state['index'] = 0
    if 'email' in st.session_state:
        st.markdown("<style>[data-testid='stSidebarNav']::after {{ {0} {1} }}</style>".format('content:',f"'Signed in as: {st.session_state.email}';"), unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #0E27C8;'>Welcome to JobPrepr!</h1>", unsafe_allow_html=True)


    st.markdown("<p style=text-align:left;>Type in your email and password to log in, or click Sign Up to create a new account.</p>", unsafe_allow_html=True)
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
                        st.markdown("<p style=text-align:left;>This email is already in use.</p>", unsafe_allow_html=True)
                    else:
                        if create_new_user(email_new, password1):
                            st.markdown("<h3 style=text-align:left;>You've created a new account! Please, log in</h3>", unsafe_allow_html=True)
                        else:
                            st.markdown("<p style=text-align:left;>This email is already in use.</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style=text-align:left;>This is not a proper email adress.</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style=text-align:left;>Passwords don't match.</p>", unsafe_allow_html=True)

    else:
        email = st.text_input('Email', '', key=4)
        password = st.text_input('Password', '', key=5, type='password')
        if st.button('Log In'):
            logged_in=False
            log=login_user(email, password)
            if log == 1:
                logged_in=True

                st.markdown("<h3 style=text-align:left;>You're logged in, let's go!</h3>", unsafe_allow_html=True)

                st.session_state['email'] = email
                st.markdown("<style>[data-testid='stSidebarNav']::after {{ {0} {1} }}</style>".format('content:',f"'Signed in as: {st.session_state.email}';"), unsafe_allow_html=True)
                st.session_state["user_id"] = get_user_id(email)
            else:
                st.markdown("<p style=text-align:left;>The email and password don't match.</p>", unsafe_allow_html=True)

    st.session_state["logged_in"]=logged_in
    st.session_state["photo_frames"]=[]

if __name__ == "__main__":
    main()
