import pyodbc
import streamlit as st
import pandas as pd
import numpy as np
import core.Home as home 

if st.session_state['user']:
    home.main()
else:
    st.title("Welcome to Neural Chat")
    st.write("Please login to continue")


#st.text_input("Your name", key="name")


