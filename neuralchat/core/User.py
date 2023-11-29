from pydantic import BaseModel

class User(BaseModel):
    name: str
    avatar: str
    id: str
    email: str
    idp: str
    container: str = ""
    datasource: str = ""
    index: str = ""
    indexer: str = ""
    indexerStatus: str = ""
    tokensAllotted:int = 5000
    tokensUsed:int = 0