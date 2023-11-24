from langchain.chat_models import ChatOpenAI
import streamlit as st

llm = ChatOpenAI(st.secrets["openaiKey"])
