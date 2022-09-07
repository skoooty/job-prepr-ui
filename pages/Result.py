import streamlit as st
from pages.Interview import result

def main():
    st.title("Result")

    if "result" in st.session_state:
        result=st.session_state["result"]
        st.write(result)
    else:
        st.write("Please go to the Interview page and record your response.")
if __name__ == "__main__":
    main()
