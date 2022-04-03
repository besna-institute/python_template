from dataclasses import dataclass

from src.models import Input, Output


@dataclass
class Result:
    text: str


class SomeSolver:
    def __init__(self):
        self.apiName = "Solver"
        self.apiVersion = "1.0.0"

    def analyze(self, name: str) -> Result:
        text = f"Hello, {name}"
        return Result(text=text)

    def process(self, input: Input) -> Output:
        result = self.analyze(input.name)
        response = Output(
            apiName=self.apiName,
            apiVersion=self.apiVersion,
            text=result.text,
        )

        return response
