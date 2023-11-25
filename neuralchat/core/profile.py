import json
import streamlit as st
import pandas as pd
import asyncio
from core.cosmos import get_container

from pydantic import BaseModel
from auth0_component import login_button

from core.azure import CreateContainer
from core.azureai import AddDataSource, AddIndex, AddIndexer, GetIndexerStatus

#define class User having name, avatar, id, email, idp, and other attributes
class User(BaseModel):
    name: str
    avatar: str
    id: str
    email: str
    idp: str
    
    
def main():
    
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
    #container = get_container("Users")
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
            user = User(name = user_info['name'], 
                        avatar=user_info['picture'], 
                        id=id, 
                        email=user_info['email'], 
                        idp=idp)
            
            # dump = user.toJSON()
            st.write(user.model_dump())
            # st.write(type(user))
            # st.write(user)
            asyncio.run(GetOrCreateUser(user))

            
            #reload the page
            st.experimental_rerun()

    
    #st.write(user_info)


def GetOrCreateProfile(user):
    GetOrCreateUser(user)
    st.session_state['user'] = user
    CreateContainer(id)
    st.success("Created storage container " + id)
    # AddDataSource()
    # st.success("Created data source")
    # AddIndex()
    # st.success("Created index")
    # AddIndexer()
    # st.success("Created indexer")



async def GetOrCreateUser(user: User):
    container = get_container("Users")
    #st.write("Container\t" + container.id)
    await container.upsert_item(user.model_dump())
    st.toast("upserted")

#read user data from cosmos into a pandas dataframe
async def get_user_data(container):
    
    items = container.read_all_items()
    #st.write(type(items))
    users = [item async for item in items]
    df = pd.DataFrame(users)
    df



#asyncio.run(get_user_data())



