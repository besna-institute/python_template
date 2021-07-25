from pydantic import BaseModel


class Input(BaseModel):
    apiName: str
    name: str


class Output(BaseModel):
    apiName: str
    apiVersion: str
    text: str
