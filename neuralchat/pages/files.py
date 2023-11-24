import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import streamlit as st
import pandas as pd

try:
    "Azure Blob Storage"

    # Quickstart code goes here

except Exception as ex:
    "Exception: " + ex