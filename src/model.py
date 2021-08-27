# generated by datamodel-codegen:
#   filename:  schema.yaml
#   timestamp: 2021-08-27T11:50:28+00:00

from __future__ import annotations

from pydantic import BaseModel, Field


class ApiName(BaseModel):
    __root__: str = Field(..., description='API name', regex='^Solver$', title='API Name')


class ApiVersion(BaseModel):
    __root__: str = Field(
        ..., description='API version', regex='^[0-9]+\\.[0-9]+\\.[0-9]+((M|RC)-[0-9]+)*$', title='API Version'
    )


class Input(BaseModel):
    apiName: ApiName
    name: str = Field(..., description='name', title='Name')


class Output(BaseModel):
    apiName: ApiName
    apiVersion: ApiVersion
    text: str = Field(..., description='text', min_length=1, title='Text')


class Error(BaseModel):
    apiName: ApiName
    apiVersion: ApiVersion
    errorId: str = Field(..., description='error ID', regex='^error:.+$', title='Error ID')
    errorMessage: str = Field(..., description='error message', title='Error Message')
