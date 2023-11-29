import json
import streamlit as st
import pandas as pd
import asyncio
from core.cosmos import get_container
import pdb as pdb

from auth0_component import login_button

from core.azure import CreateContainer, ContainerClient
from core.azureai import AddDataSource, AddIndex, AddIndexer, GetIndexerStatus
from core.User import User

# define class User having name, avatar, id, email, idp, and other attributes


def main():
    # container = get_container("Users")
    clientId = st.secrets["clientId"]
    domain = st.secrets["domain"]
    # st.write(type(container))

    user_info = login_button(clientId, domain=domain)
    if (user_info == False):
        st.toast("You must login to continue")
    else:
        with st.sidebar:

            cola, colb = st.columns([0.2, 0.8])

            with cola:
                st.write(user_info)
                'Hi ' + user_info['given_name'] + '!'

                idp = user_info['sub'].split('|')[0]
                id = user_info['sub'].split('|')[1]
                user = User(name=user_info['name'],
                            avatar=user_info['picture'],
                            id=id,
                            email=user_info['email'],
                            idp=idp)

                st.write(user.model_dump())

                asyncio.run(GetOrCreateProfile(user))

    # st.write(user_info)


async def GetOrCreateProfile(user: User):

    try:
        user = await GetOrCreateUser(user)
        st.session_state['user'] = user
        if len(user.container) == 0:
            client = CreateContainer(user)
            user.container = client.container_name
            st.success("Created storage container " + user.container)
            st.session_state['user'] = user
        if len(user.datasource) == 0:
            AddDataSource(user)
            st.success("Created data source")
            st.session_state['user'] = user
        if len(user.index) == 0:
            AddIndex(user=user)
            st.success("Created index")
            st.session_state['user'] = user
        if len(user.indexer) == 0:
            AddIndexer(user)
            st.success("Created indexer")
            st.session_state['user'] = user

        container = get_container("Users")
        user = await container.upsert_item(user.model_dump())
        st.session_state['user'] = user
        st.success("Profile created")
        st.rerun()
    except Exception as ex:
        st.error(ex)


async def GetOrCreateUser(user: User):
    container = get_container("Users")
    # check if user exists in container
    try:
        existing = await container.read_item(user.id, user.id)
        if existing:
            st.warning("User already exists")
            st.write(existing)

            user = User(**existing)
            return user
    except Exception as ex:
        st.warning("User does not exist. Creating new one")
    # st.write("Container\t" + container.id)
    user = await container.upsert_item(user.model_dump())
    user = User(**user)
    st.success("upserted")
    return user


# read user data from cosmos into a pandas dataframe
async def get_user_data(container):

    items = container.read_all_items()
    # st.write(type(items))
    users = [item async for item in items]
    df = pd.DataFrame(users)
    df


# asyncio.run(get_user_data())
