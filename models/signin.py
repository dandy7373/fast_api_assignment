from pydantic import BaseModel

class SigninModel(BaseModel):
    email:str
    password:str