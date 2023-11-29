import random
import core.azure as az
import streamlit as st
import core.profile as profile


def main():

    st.markdown("""
            <style>
            [data-testid="stSidebarNav"] {
                background-image: url('static/neuralnextLogo.png');
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "My Company Name";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
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
            [data-testid="stMetric"]{
                border-left:8px solid green;
                border-right:1px solid darkgray;
                border-top:1px solid darkgray;
                border-bottom:1px solid darkgray;
                border-radius: 4px;
                padding: 20px;
                box-shadow: 0px 6px 10px -4px darkslategrey
            }
            </style>
            """, unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Chat History")
        history_container = st.container()
        with history_container:
            for i in range(random.randrange(1, 2)):
                st.link_button(label="Yesterday's Chat",
                               url="https://youtube.com", use_container_width=True)

        # uploaded_files = st.file_uploader("Choose your Document", accept_multiple_files=True)
        # for uploaded_file in uploaded_files:
        #     bytes_data = uploaded_file.read()
        #     st.write("filename:", uploaded_file.name)
        #     st.write(bytes_data)
        az.main()

    col1, col2 = st.columns(2)
    col1.metric("Total Documents Uploaded", "8")
    col2.metric("Available Tokens", "1000 Tokens")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Whatsup?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = f"Echo: {prompt}"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
