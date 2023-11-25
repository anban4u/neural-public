import os
import json
import asyncio
import streamlit as st
from azure.cosmos import PartitionKey
from azure.cosmos.aio import CosmosClient


ENDPOINT = st.secrets["cosmosEndpoint"]
KEY = st.secrets["cosmosKey"]

DATABASE_NAME = "neural"
CONTAINER_NAME = "Users"



def get_container(name):
    client = CosmosClient(url=ENDPOINT, credential=KEY)
    database = client.get_database_client(DATABASE_NAME)
    #st.write(type(database))
    #key_path = PartitionKey(path="/userId")
    container = database.get_container_client(name)
    #st.write("Container\t" + container.id)
    return container


