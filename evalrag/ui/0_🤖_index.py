import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()


st.title("🦜🔗 Quickstart App")
st.write("provider: ", os.getenv("HF_TOKEN"))

with st.form("my_form"):

    text = st.text_area(
        "Enter text:",
        "What are the three key pieces of advice for learning how to code?",
    )
    submitted = st.form_submit_button("Submit")

