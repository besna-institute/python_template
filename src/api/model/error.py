# generated by datamodel-codegen:
#   filename:  error.json
#   timestamp: 2021-07-26T08:39:10+00:00

from __future__ import annotations

from pydantic import BaseModel, Field


class ApiName(BaseModel):
    __root__: str = Field(..., description='API name', regex='^Solver$', title='API Name')


class ApiVersion(BaseModel):
    __root__: str = Field(
        ..., description='API version', regex='^[0-9]+\\.[0-9]+\\.[0-9]+((M|RC)-[0-9]+)*$', title='API Version'
    )


class SchemaOfSolverError(BaseModel):
    apiName: ApiName
    apiVersion: ApiVersion
    errorId: str = Field(..., description='error ID', regex='^error:.+$', title='Error ID')
    errorMessage: str = Field(..., description='error message', title='Error Message')
