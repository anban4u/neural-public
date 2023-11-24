import json
import streamlit as st
import pandas as pd
import asyncio
from core.cosmos import get_container, GetOrCreateUser

from auth0_component import login_button

#define class User having name, avatar, id, email, idp, and other attributes
class User(dict):
    
    def __init__(self, name, avatar, id, email, idp):
        dict.__init__(self, name=name, avatar=avatar, id=id, email=email, idp=idp)
    #tojson method
    def toJSON(self):
        return json.dumps(self)
    

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
container = get_container("Users")
clientId = st.secrets["clientId"]
domain = st.secrets["domain"]
#st.write(type(container))
with st.sidebar:
    
    user_info = login_button(clientId, domain = domain)
    if(user_info == False):
        st.toast("You must login to continue")
    else:
        cola, colb = st.columns([0.2, 0.8])

        with cola:
            st.markdown('''
            <div class="circle-image">
                <img src ="''' + user_info['picture'] + '''">
            </div>
            ''', unsafe_allow_html=True)
        with colb:
            st.title("Hi " + user_info['given_name'] + "👋")

        st.divider()
        st.write(user_info)
        'Hi ' + user_info['given_name'] + '!'
        #split  google-oauth2|111834916048421935454 into google-oauth2 and 111834916048421935454
        idp = user_info['sub'].split('|')[0]
        id = user_info['sub'].split('|')[1]
        user = User(user_info['name'], 
                    user_info['picture'], 
                    id, 
                    user_info['email'], 
                    idp)
        
        # dump = user.toJSON()
        # st.write(dump)
        # st.write(type(user))
        # st.write(user)
        asyncio.run(GetOrCreateUser(user))
        st.session_state['user'] = user

    
    #st.write(user_info)


def GetOrCreateProfile(user):
    GetOrCreateUser(user)


#read user data from cosmos into a pandas dataframe
async def get_user_data():
    
    items = container.read_all_items()
    #st.write(type(items))
    users = [item async for item in items]
    df = pd.DataFrame(users)
    df



asyncio.run(get_user_data())



