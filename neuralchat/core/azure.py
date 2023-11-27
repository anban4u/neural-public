import mimetypes
import os, uuid
import traceback
from typing import Optional
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, generate_blob_sas, ContentSettings
import charset_normalizer
import streamlit as st
import pandas as pd

from core.User import User

try:
    "Azure Blob Storage"

    # Quickstart code goes here

except Exception as ex:
    "Exception: " + ex

def CreateContainer(user: User):
    try:
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(st.secrets["storageContainerConnectionString"])
        #st.write(user)
        # Create a unique name for the container
        container_name = user.id

        # Create the container
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()
            st.toast("Created storage container " + container_name)
        user.container = container_name
        return container_client
    except Exception as ex:
        st.toast(ex)

def upload_file(bytes_data: bytes, file_name: str, content_type: Optional[str] = None, container_name: str = ""):    
    # Upload a new file
    st.session_state['filename'] = file_name
    if content_type == None:
        content_type = mimetypes.MimeTypes().guess_type(file_name)[0]
        charset = f"; charset={charset_normalizer.detect(bytes_data)['encoding']}" if content_type == 'text/plain' else ''
        content_type = content_type if content_type != None else 'text/plain'
    blob_service_client : BlobServiceClient = BlobServiceClient.from_connection_string(st.secrets["storageContainerConnectionString"])
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
    # Upload the created file
    blob_client.upload_blob(bytes_data, overwrite=True, content_settings=ContentSettings(content_type=content_type+charset))
    # Generate a SAS URL to the blob and return it
    #st.session_state['file_url'] = blob_client.url + '?' + generate_blob_sas(account_name, container_name, file_name,account_key=account_key,  permission="r", expiry=datetime.utcnow() + timedelta(hours=3))
def main():
    sessionUser = st.session_state.get('user')
    if sessionUser is None:
        st.error("Please login to continue")
        return
    user = User(**sessionUser)
    container_name = user.container
    try:
        with st.expander("Add documents in Batch", expanded=True):
            # config = ConfigHelper.get_active_config_or_default()
            # file_type = [processor.document_type for processor in config.document_processors]
            uploaded_files = st.file_uploader("Upload a document to add it to the Azure Storage Account, compute embeddings and add them to the Azure Cognitive Search index. Check your configuration for available document processors.", 
                                            #type=file_type, 
                                            accept_multiple_files=True)
            if uploaded_files is not None:
                for up in uploaded_files:
                    # To read file as bytes:
                    bytes_data = up.getvalue()
                    if st.session_state.get('filename', '') != up.name:
                        # Upload a new file
                        upload_file(bytes_data, up.name, container_name=container_name)
                if len(uploaded_files) > 0:
                    st.success(f"{len(uploaded_files)} documents uploaded. Embeddings computation in progress. \nPlease note this is an asynchronous process and may take a few minutes to complete.\nYou can check for further details in the Azure Function logs.")

            col1, col2, col3 = st.columns([2,1,2])
            # with col1:
            #     st.button("Process and ingest new files", on_click=remote_convert_files_and_add_embeddings)
            with col3:
                #st.button("Reprocess all documents in the Azure Storage account", on_click=remote_convert_files_and_add_embeddings, args=(True,))
                st.write("Reprocess all documents in the Azure Storage account")

        with st.expander("Add URLs to the knowledge base", expanded=True):
            col1, col2 = st.columns([3,1])
            with col1: 
                st.text_area("Add a URLs and than click on 'Compute Embeddings'", placeholder="PLACE YOUR URLS HERE SEPARATED BY A NEW LINE", height=100, key="urls")

            with col2:
                st.selectbox('Embeddings models', [os.getenv('AZURE_OPENAI_EMBEDDING_MODEL')], disabled=True)
                #st.button("Process and ingest web pages", on_click=add_urls, key="add_url")

    except Exception as e:
        st.error(traceback.format_exc())