import http.client
import json
import uuid
import streamlit as st

from core.User import User

storageConnectionString = st.secrets["storageContainerConnectionString"]
searchService = st.secrets["searchService"]
searchAdminKey = st.secrets["searchAdminKey"]
embeddingModel = st.secrets["embeddingModel"]
openAiServiceKey = st.secrets["openAiServiceKey"]
apiVersion = "2023-10-01-Preview"
headers = {
    'Content-Type': 'application/json',
    'api-key': f'{searchAdminKey}'
    }

def AddDataSource(user: User):
    datasource = "ds-" + user.container.lower()
    st.write("datasource name is " + datasource)

    conn = http.client.HTTPSConnection(f"{searchService}.search.windows.net")
    payload = json.dumps({
    "description": f"Datasource for {user.name}",
    "type": "azureblob",
    "credentials": {
        "connectionString": f"{storageConnectionString}"
    },
    "container": {
        "name": f"{user.container}"
    },
    "dataChangeDetectionPolicy": {
        "@odata.type": "#Microsoft.Azure.Search.HighWaterMarkChangeDetectionPolicy",
        "highWaterMarkColumnName": "metadata_storage_last_modified"
    }
    })
   
    conn.request("PUT", f"/datasources/{datasource}?api-version={apiVersion}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    if res.code > 299:
        #st.error(data.decode("utf-8"))
        raise Exception("Error creating datasource " + data.decode("utf-8") + " " + str(res.code) + " " + str(res.reason))
        
    user.datasource = datasource
    st.success(data.decode("utf-8"))

def AddIndex(user: User):
    conn = http.client.HTTPSConnection(f"{searchService}.search.windows.net")
    vectorindex = f"{user.id}-idx"
    payload = json.dumps({
    "name": vectorindex,
    "defaultScoringProfile": None,
    "fields": [
        {
        "name": "chunk_id",
        "type": "Edm.String",
        "searchable": True,
        "filterable": True,
        "retrievable": True,
        "sortable": True,
        "facetable": True,
        "key": True,
        "indexAnalyzer": None,
        "searchAnalyzer": None,
        "analyzer": "keyword",
        "normalizer": None,
        "dimensions": None,
        "vectorSearchProfile": None,
        "synonymMaps": []
        },
        {
        "name": "parent_id",
        "type": "Edm.String",
        "searchable": True,
        "filterable": True,
        "retrievable": True,
        "sortable": True,
        "facetable": True,
        "key": False,
        "indexAnalyzer": None,
        "searchAnalyzer": None,
        "analyzer": None,
        "normalizer": None,
        "dimensions": None,
        "vectorSearchProfile": None,
        "synonymMaps": []
        },
        {
        "name": "chunk",
        "type": "Edm.String",
        "searchable": True,
        "filterable": False,
        "retrievable": True,
        "sortable": False,
        "facetable": False,
        "key": False,
        "indexAnalyzer": None,
        "searchAnalyzer": None,
        "analyzer": None,
        "normalizer": None,
        "dimensions": None,
        "vectorSearchProfile": None,
        "synonymMaps": []
        },
        {
        "name": "title",
        "type": "Edm.String",
        "searchable": True,
        "filterable": True,
        "retrievable": True,
        "sortable": False,
        "facetable": False,
        "key": False,
        "indexAnalyzer": None,
        "searchAnalyzer": None,
        "analyzer": None,
        "normalizer": None,
        "dimensions": None,
        "vectorSearchProfile": None,
        "synonymMaps": []
        },
        {
        "name": "vector",
        "type": "Collection(Edm.Single)",
        "searchable": True,
        "filterable": False,
        "retrievable": True,
        "sortable": False,
        "facetable": False,
        "key": False,
        "indexAnalyzer": None,
        "searchAnalyzer": None,
        "analyzer": None,
        "normalizer": None,
        "dimensions": 1536,
        "vectorSearchProfile": f"{vectorindex}-profile",
        "synonymMaps": []
        },
        {
        "name": "keyPhrases",
        "type": "Collection(Edm.String)",
        "searchable": True,
        "filterable": True,
        "retrievable": True,
        "sortable": False,
        "facetable": False,
        "key": False,
        "indexAnalyzer": None,
        "searchAnalyzer": None,
        "analyzer": "en.microsoft",
        "normalizer": None,
        "dimensions": None,
        "vectorSearchProfile": None,
        "synonymMaps": []
        }
    ],
    "scoringProfiles": [],
    "corsOptions": None,
    "suggesters": [],
    "analyzers": [],
    "normalizers": [],
    "tokenizers": [],
    "tokenFilters": [],
    "charFilters": [],
    "encryptionKey": None,
    "similarity": {
        "@odata.type": "#Microsoft.Azure.Search.BM25Similarity",
        "k1": None,
        "b": None
    },
    "semantic": {
        "defaultConfiguration": None,
        "configurations": [
        {
            "name": "default",
            "prioritizedFields": {
            "titleField": None,
            "prioritizedContentFields": [
                {
                "fieldName": "chunk"
                }
            ],
            "prioritizedKeywordsFields": []
            }
        }
        ]
    },
    "vectorSearch": {
        "algorithms": [
        {
            "name": f"{vectorindex}-algorithm",
            "kind": "hnsw",
            "hnswParameters": {
            "metric": "cosine",
            "m": 4,
            "efConstruction": 400,
            "efSearch": 500
            },
            "exhaustiveKnnParameters": None
        }
        ],
        "profiles": [
        {
            "name": f"{vectorindex}-profile",
            "algorithm": f"{vectorindex}-algorithm",
            "vectorizer": f"{vectorindex}-vectorizer"
        }
        ],
        "vectorizers": [
        {
            "name": f"{vectorindex}-vectorizer",
            "kind": "azureOpenAI",
            "azureOpenAIParameters": {
            "resourceUri": f"https://{searchService}.openai.azure.com",
            "deploymentId": f"{embeddingModel}",
            "apiKey": f"{openAiServiceKey}",
            "authIdentity": None
            },
            "customWebApiParameters": None
        }
        ]
    }
    })
    
    conn.request("PUT", f"/indexes/{vectorindex}?api-version={apiVersion}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    user.index = vectorindex
    st.success(data.decode("utf-8"))

def AddIndexer(user: User):
    conn = http.client.HTTPSConnection(f"{searchService}.search.windows.net")
    vectorindexer = f"{user.id}-idxr"
    payload = json.dumps({
    "name": f"{vectorindexer}",
    "description": None,
    "dataSourceName": f"{user.datasource}",
    "skillsetName": f"myskillset",
    "targetIndexName": f"{user.index}",
    "disabled": None,
    "schedule": None,
    "parameters": {
        "batchSize": None,
        "maxFailedItems": None,
        "maxFailedItemsPerBatch": None,
        "base64EncodeKeys": None,
        "configuration": {
        "dataToExtract": "contentAndMetadata",
        "parsingMode": "default",
        "imageAction": "generateNormalizedImages"
        }
    },
    "fieldMappings": [
        {
        "sourceFieldName": "metadata_storage_name",
        "targetFieldName": "title",
        "mappingFunction": None
        }
    ],
    "outputFieldMappings": [],
    "cache": None,
    "encryptionKey": None
    })
    
    conn.request("POST", f"/indexers?api-version={apiVersion}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    user.indexer = vectorindexer
    st.success(data.decode("utf-8"))

def RunIndexer(user: User):
    conn = http.client.HTTPSConnection("{{searchservice}}.search.windows.net")
    payload = ''
    headers = {
    'x-ms-client-request-id': f'{uuid()}'
    }
    conn.request("POST", f"/indexers('{user.indexer}')/search.run?api-version={apiVersion}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

def GetIndexerStatus(user: User):
    conn = http.client.HTTPSConnection(f"{searchService}.search.windows.net")
    payload = ''
    
    conn.request("GET", f"/indexers/{user.indexer}/status?api-version={apiVersion}", payload, headers)
    res = conn.getresponse()
    data = res.read()

    st.success(data.decode("utf-8"))

def Query(query: str, user: User):
    conn = http.client.HTTPSConnection(f"{searchService}.search.windows.net")
    payload = query
    
    conn.request("GET", f"/indexes/{user.index}/docs?search=*&$count=true&api-version={apiVersion}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    st.success(data.decode("utf-8"))