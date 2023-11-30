import streamlit as st
import base64
import os
import streamlit.components.v1 as components
import core.profile as loginbutton
# from streamlit_modal import Modal`    `
# Replace with the correct relative path to your image
brand_icon_path = "app/static/robot.png"
benefits_image_path = "app/static/benefits.png"

stylesheet_file_path = os.path.join("styles", "login.css")

with open(stylesheet_file_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown(
    '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" '
    'integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" '
    'crossorigin="anonymous"></script>',
    unsafe_allow_html=True)

st.markdown(
    '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" '
    'integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
    unsafe_allow_html=True)


def main():
    # st.markdown("""
    # <nav class="navbar fixed-top navbar-expand-lg navbar-dark " style="background-color: #262626;">
    # <a class="navbar-brand" href="https://youtube.com/dataprofessor" target="_blank">Neural Next AI</a>
    # <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    #     <span class="navbar-toggler-icon"></span>
    # </button>
    # <div class="collapse navbar-collapse justify-content-center" id="navbarNav">
    #     <ul class="navbar-nav">
    #     <li class="nav-item active">
    #         <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
    #     </li>
    #     <li class="nav-item">
    #         <a class="nav-link" href="#" target="_blank">Pricing</a>
    #     </li>
    #     <li class="nav-item">
    #         <button type="button" class="btn btn-info">Sign In / Sign Up</button>
    #     </li>
    #     </ul>
    # </div>
    # </nav>
    # """, unsafe_allow_html=True)

    # with open(brand_icon_path, "rb") as img_file:
    #     img_bytes = img_file.read()
    #     encoded_image = base64.b64encode(img_bytes).decode()

    # with open(benefits_image_path, "rb") as img_file:
    #     img_bytes = img_file.read()
    #     benefits_image = base64.b64encode(img_bytes).decode()

    # Create a container to wrap col1 and col2
    container_hero = st.container()

    with container_hero:
        cola, col1, col2, cols = st.columns([0.2, 0.5, 0.3, 0.2], gap="large")

        with col1:
            st.markdown('''
            <div class="login_app_tag">
            <p>Chat with your PDFs like you do with your friends</p>
            </div>
            ''', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            cola, cols = st.columns(2)
            loginbutton.main()
            # with cola:
            #     loginbutton.main()

            # with cols:
            #     st.button("Try For Free", type="secondary",
            #               use_container_width=True)

        with col2:
            st.markdown(f'''
            <div class="login_brand_icon_wrapper">
            <img src="{brand_icon_path}" class="login_brand_icon">
            ''', unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)

    container_about = st.container()

    with container_about:
        st.markdown('<p class="subHeading">How it works ?</p>',
                    unsafe_allow_html=True)

        st.markdown("<br/>", unsafe_allow_html=True)

        with st.expander("Select and upload PDF"):
            st.write('''
            Locate the PDF file on your computer.
            Click and hold the mouse button on the PDF file.
            Drag the file over to the designated area on the web page labeled for file upload.
            ''')

        with st.expander("Select the configurations to use"):
            st.write('''
        Explore the options or settings provided in the configurations section.
        These configurations might include choices related to the app's behavior, appearance, or functionality.''')

        with st.expander("Upgrade plan for hassle free experience"):
            st.write('''
            Choose the plan that best suits your needs or offers the features you require for a hassle-free experience.
            Plans might include options for additional functionalities, higher usage limits, or exclusive benefits.
            ''')

        with st.expander("Ask questions and get meaningful insights"):
            st.write('''
            For complex or in-depth inquiries, consider refining your question or seeking guidance from the application's support or documentation.
            Experiment with different types of questions or queries to explore various aspects and gain diverse insights from the application.
            ''')

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)

    container_benefits = st.container()

    with container_benefits:
        st.markdown('<p class="subHeading">Benefits</p>',
                    unsafe_allow_html=True)

        st.markdown("<br/>", unsafe_allow_html=True)
        left_co, cent_co, last_co = st.columns(3)
        with cent_co:
            st.markdown(f'<img src="{benefits_image_path}" class="login_brand_icon">', unsafe_allow_html=True)
            #st.image(benefits_image_path)


# modal = Modal(
#     "Demo Modal",
#     key="demo-modal",

#     # Optional
#     padding=20,    # default value
#     max_width=744  # default value
# )


# open_modal = st.button("Open")
# if open_modal:
#     modal.open()

# if modal.is_open():
#     with modal.container():
#         st.write("Text goes here")

#         html_string = '''
#         <h1>HTML string in RED</h1>

#         <script language="javascript">
#           document.querySelector("h1").style.color = "red";
#         </script>
#         '''
#         components.html(html_string)

#         st.write("Some fancy text")
#         value = st.checkbox("Check me")
#         st.write(f"Checkbox checked: {value}")
