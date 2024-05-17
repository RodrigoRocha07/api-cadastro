from pydantic import BaseModel

class User(BaseModel):
    id: str = None
    username: str
    password: str 
    email: str
    token:str = None



