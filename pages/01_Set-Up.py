import streamlit as st
import imageio
from utils.get_css import get_css


def main():
    st.set_page_config(page_title="JobPrepr: Set-Up", page_icon="💼", layout="centered")
    st.markdown(get_css(),unsafe_allow_html=True)
    if 'email' in st.session_state:
        st.markdown("<style>[data-testid='stSidebarNav']::after {{ {0} {1} }}</style>".format('content:',f"'Signed in as: {st.session_state.email}';"), unsafe_allow_html=True)
    if 'logged_in' not in st.session_state:
        logged_in=False
    else:
        logged_in=st.session_state["logged_in"]

    if 'setup_index' not in st.session_state:
        st.session_state['setup_index'] = 0

    st.markdown("<h1 style='text-align: center; color: black;'>Room Setup</h1>", unsafe_allow_html=True)

    headers=[
            'Quiet room',
            '',
            'Position',
            'One person',
            'Ready?'
            ]

    images =[
            'tutorial_pics/too_many_people.jpg',
            '',
            'tutorial_pics/far_away.jpg',
            'tutorial_pics/two_people.jpg',
            'tutorial_pics/good.jpg'
            ]

    text =[
        "Find a quiet room. You don't want the voices in the background to disturb the algorithm.",
        "",
        "Make sure you are not too far away from the camera.",
        "Make sure you are the only person visible on camera. The algoritham won't know which face to analyse otherwise.",
        "Good! You're all set for the interview!"
    ]

    page = st.empty()
    col1, col2, col3 = st.columns([1,1,1])



    with col1:
        if st.session_state['setup_index'] != 0:
            if st.button('Previous'):
                st.session_state['setup_index'] -= 1
                st.experimental_rerun()

    with col3:
        if st.session_state['setup_index'] != 4:
            if st.button('Next'):
                st.session_state['setup_index'] += 1
                st.experimental_rerun()

    with page.container():
        if st.session_state['setup_index'] == 1:
            st.markdown("Lighting")

            col1, col2= st.columns(2)

            with col1:
                im = imageio.imread('tutorial_pics/too_dark.jpg')
                st.image(im)
                st.markdown("<p style=text-align:left;> ❌ </p>", unsafe_allow_html=True)
                st.markdown("<p style=text-align:left;> Make sure there is enough light in the room.  </p>", unsafe_allow_html=True)

            with col2:
                im = imageio.imread('tutorial_pics/bad_light.jpg')
                st.image(im)
                st.markdown("<p style=text-align:left;> ❌ </p>", unsafe_allow_html=True)
                st.markdown("<p style=text-align:left;> Make sure the source of light is in front of you, not behind.  </p>", unsafe_allow_html=True)
        else:
            st.markdown(headers[st.session_state['setup_index']])
            im = imageio.imread(images[st.session_state['setup_index']])
            st.image(im)
            if st.session_state['setup_index'] == 4:
                st.markdown("<p style=text-align:left;> ✅ </p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style=text-align:left;> ❌ </p>", unsafe_allow_html=True)
            st.markdown(f"<p style=text-align:left;> {text[st.session_state['setup_index']]} </p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
