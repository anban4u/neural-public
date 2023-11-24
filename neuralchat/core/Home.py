import random

import streamlit as st
def main():
    st.set_page_config(page_title="NeuralNextAI", layout="wide", initial_sidebar_state="expanded", menu_items=None)

    st.markdown("""
            <style>
            .circle-image {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                overflow: hidden;
                box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
            }

            .circle-image img {
                width: 50px;
                height: 50px;
                object-fit: cover;
            }
            </style>
            """, unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Chat History")
        history_container = st.container()
        with history_container:
            for i in range(random.randrange(1, 14)):
                st.link_button(label="Yesterday's Chat", url="https://youtube.com", use_container_width=True)

        uploaded_files = st.file_uploader("Choose your Document", accept_multiple_files=True)
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            st.write("filename:", uploaded_file.name)
            st.write(bytes_data)

    st.title("NextAI BOT")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = f"Echo: {prompt}"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
