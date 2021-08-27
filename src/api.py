from abc import abstractmethod
from dataclasses import dataclass

from src.model import Input, Output


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

    def process(self, input: Input) -> Output:
        result = self.analyze(input.name)
        response = Output(
            apiName=self.apiName,
            apiVersion=self.apiVersion,
            text=result.text,
        )

        return response
