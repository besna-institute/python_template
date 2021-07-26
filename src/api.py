from abc import abstractmethod
from dataclasses import dataclass

from src.model import input, output


@dataclass
class Result:
    text: str


class BaseSolverAPI:
    def __init__(self, apiName: str, apiVersion: str):
        self.apiName = apiName
        self.apiVersion = apiVersion

    @abstractmethod
    def analyze(self, name: str) -> Result:
        pass

    def process(self, input: input.SchemaOfSolverInput) -> output.SchemaOfSolverOutput:
        result = self.analyze(input.name)
        response = output.SchemaOfSolverOutput(
            apiName=self.apiName,
            apiVersion=self.apiVersion,
            text=result.text,
        )

        return response
