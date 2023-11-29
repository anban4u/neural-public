import mimetypes
import os
import uuid
import traceback
from typing import Optional
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, generate_blob_sas, ContentSettings
import charset_normalizer
import streamlit as st
import pandas as pd
import humanize

from core.User import User

try:
    "Azure Blob Storage"

    # Quickstart code goes here

except Exception as ex:
    "Exception: " + ex


ALLOWED_EXTENSIONS = [
    'png', 'jpg', 'jpeg', 'gif',  # Images
    'txt', 'pdf',  # Text and PDFs
    'doc', 'docx',  # Microsoft Word
    'xls', 'xlsx',  # Microsoft Excel
    # Add any other file extensions as needed
]

st.markdown("""
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
            .stMarkdown .list_wrapper{
            display:flex;
            align-items:center;
            gap:12px
            }
            .list_style{
            display:flex;
            flex-direction:column;
            }
            .list_item_size{
            color:#818181;
            }
        .file-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px;
            background-color: #f0f0f0;
            border-radius: 10px;
            margin-bottom: 5px;
        }
        .file-name {
            flex-grow: 1;
            display: flex;
            align-items: center;
        }
        .file-name span {
            margin-right: 10px;
        }
        .material-icons {
            color: #4caf50; /* Change color as needed */
        }
        /* Add more custom styles as needed */
    </style>
    """, unsafe_allow_html=True)


def CreateContainer(user: User):
    try:
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(
            st.secrets["storageContainerConnectionString"])
        # st.write(user)
        # Create a unique name for the container
        container_name = user.id

        # Create the container
        container_client = blob_service_client.get_container_client(
            container_name)
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
    blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(
        st.secrets["storageContainerConnectionString"])
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=file_name)
    # Upload the created file
    blob_client.upload_blob(bytes_data, overwrite=True, content_settings=ContentSettings(
        content_type=content_type+charset))
    # Generate a SAS URL to the blob and return it
    # st.session_state['file_url'] = blob_client.url + '?' + generate_blob_sas(account_name, container_name, file_name,account_key=account_key,  permission="r", expiry=datetime.utcnow() + timedelta(hours=3))


def main():
    sessionUser = st.session_state.get('user')
    if sessionUser is None:
        st.error("Please login to continue")
        return
    user = User(**sessionUser)
    container_name = user.container
    try:
        with st.expander("Add documents in Batch", expanded=True):

            blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(
                st.secrets["storageContainerConnectionString"])
            container_client = blob_service_client.get_container_client(
                container_name)
            blobs = container_client.list_blobs()
            df = pd.DataFrame([{'name': blob.name, 'size': humanize.naturalsize(
                blob.size), 'type': get_file_type(blob.name)} for blob in blobs])

            for index, row in df.iterrows():
                # Make sure that 'type' is the correct column name and it exists in your DataFrame
                icon_class = get_file_icon(row['name'])
                st.markdown(
                    f'''<div class="list_wrapper"><span class='material-icons'>{icon_class}</span> <div class="list_style"><span>{row['name']}</span> <span class="list_item_size">{row['size']}</span></div></div><hr/> ''', unsafe_allow_html=True)

            # config = ConfigHelper.get_active_config_or_default()
            # file_type = [processor.document_type for processor in config.document_processors]
            uploaded_files = st.file_uploader("Upload Files",
                                              type=ALLOWED_EXTENSIONS,
                                              accept_multiple_files=True)
            if uploaded_files is not None:
                for up in uploaded_files:
                    # To read file as bytes:
                    bytes_data = up.getvalue()
                    if st.session_state.get('filename', '') != up.name:
                        # Upload a new file
                        upload_file(bytes_data, up.name,
                                    container_name=container_name)
                if len(uploaded_files) > 0:
                    st.success(f"{len(uploaded_files)} documents uploaded. Embeddings computation in progress. \nPlease note this is an asynchronous process and may take a few minutes to complete.\nYou can check for further details in the Azure Function logs.")

            col1, col2, col3 = st.columns([2, 1, 2])
            with col1:
                st.button("Process new files", on_click=None)
            with col3:
                st.button("Reprocess all documents",
                          on_click=None, args=(True,))
                # st.write("Reprocess")

        # with st.expander("Add URLs to the knowledge base", expanded=True):
        #     col1, col2 = st.columns([3,1])
        #     with col1:
        #         st.text_area("Add a URLs and than click on 'Compute Embeddings'", placeholder="PLACE YOUR URLS HERE SEPARATED BY A NEW LINE", height=100, key="urls")

        #     with col2:
        #         st.selectbox('Embeddings models', [os.getenv('AZURE_OPENAI_EMBEDDING_MODEL')], disabled=True)
        #         #st.button("Process and ingest web pages", on_click=add_urls, key="add_url")

    except Exception as e:
        st.error(traceback.format_exc())


def get_file_type(blob_name):
    mime_type, _ = mimetypes.guess_type(blob_name)
    return mime_type if mime_type is not None else 'Unknown'


def get_file_icon(blob_name):
    mime_type, _ = mimetypes.guess_type(blob_name)
    mime_to_icon = {
        'image/jpeg': 'image',
        'image/png': 'image',
        'image/gif': 'image',
        'text/plain': 'article',
        'application/pdf': 'picture_as_pdf',
        # ... other MIME types
        'default': 'insert_drive_file'
    }
    return mime_to_icon.get(mime_type, mime_to_icon['image/png'])
