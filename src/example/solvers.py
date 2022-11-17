from dataclasses import dataclass

from src.models import Input, Output, api_version


@dataclass
class Result:
    text: str


class SomeSolver:
    def __init__(self, api_name: str = "Solver") -> None:
        self.api_name = api_name

    def analyze(self, name: str) -> Result:
        text = f"Hello, {name}"
        return Result(text=text)

    def process(self, input: Input) -> Output:
        result = self.analyze(input.name)
        response = Output(
            apiName=self.api_name,
            apiVersion=api_version,
            text=result.text,
        )

        return response
