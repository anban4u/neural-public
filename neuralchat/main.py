import streamlit as st
import pandas as pd
import numpy as np
import core.Home as home
import core.profile as profile
import core.login as login


if st.session_state.get('user') is None:
    st.title("Welcome to Neural Chat")
    st.write("Please login to continue")
    login.main()

else:
    home.main()


# st.text_input("Your name", key="name")
