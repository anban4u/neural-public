import http.client
import json

def AddDataSource():
    conn = http.client.HTTPSConnection("{{searchservice}}.search.windows.net")
    payload = json.dumps({
    "description": "Datasource for testing indexer",
    "type": "azureblob",
    "credentials": {
        "connectionString": "{{storageaccountconnection}}"
    },
    "container": {
        "name": "{{container}}"
    },
    "dataChangeDetectionPolicy": {
        "@odata.type": "#Microsoft.Azure.Search.HighWaterMarkChangeDetectionPolicy",
        "highWaterMarkColumnName": "metadata_storage_last_modified"
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'api-key': '{{searchadminkey}}'
    }
    conn.request("PUT", "/datasources/{{datasource}}?api-version=%7B%7Bdatasource-api-version%7D%7D", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

def AddIndex():
    conn = http.client.HTTPSConnection("{{searchservice}}.search.windows.net")
    payload = json.dumps({
    "name": "{{vectorindex}}",
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
        "vectorSearchProfile": "{{vectorindex}}-profile",
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
            "name": "{{vectorindex}}-algorithm",
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
            "name": "{{vectorindex}}-profile",
            "algorithm": "{{vectorindex}}-algorithm",
            "vectorizer": "{{vectorindex}}-vectorizer"
        }
        ],
        "vectorizers": [
        {
            "name": "{{vectorindex}}-vectorizer",
            "kind": "azureOpenAI",
            "azureOpenAIParameters": {
            "resourceUri": "https://{{azureopenaiservice}}.openai.azure.com",
            "deploymentId": "{{embeddingmodel}}",
            "apiKey": "{{azureopenaiservicekey}}",
            "authIdentity": None
            },
            "customWebApiParameters": None
        }
        ]
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'api-key': '{{searchadminkey}}'
    }
    conn.request("PUT", "/indexes/{{vectorindex}}?api-version=%7B%7Bindex-api-version%7D%7D", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

def AddIndexer():
    conn = http.client.HTTPSConnection("{{searchservice}}.search.windows.net")
    payload = json.dumps({
    "name": "{{vectorindexer}}",
    "description": None,
    "dataSourceName": "{{datasource}}",
    "skillsetName": "{{skillsetname}}",
    "targetIndexName": "{{vectorindex}}",
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
    headers = {
    'Content-Type': 'application/json',
    'api-key': '{{searchadminkey}}'
    }
    conn.request("POST", "/indexers?api-version=%7B%7Bindex-api-version%7D%7D", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

def GetIndexerStatus():
    conn = http.client.HTTPSConnection(".search.windows.net")
    payload = ''
    headers = {
    'Content-Type': 'application/json',
    'api-key': ''
    }
    conn.request("GET", "/indexers/test-img-idxr/status?api-version=2020-06-30", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

def Query():
    conn = http.client.HTTPSConnection(".search.windows.net")
    payload = ''
    headers = {
    'Content-Type': 'application/json',
    'api-key': ''
    }
    conn.request("GET", "/indexes/test-img-idx/docs?search=*&$count=true&api-version=2020-06-30", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))