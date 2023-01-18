from dataclasses import dataclass

from src.models import API_VERSION, Input, Output


@dataclass
class Result:
    text: str


class SomeSolver:
    def __init__(self, api_name: str = "Solver") -> None:
        self.api_name = api_name

    def analyze(self, name: str) -> Result:  # pylint: disable=no-self-use
        text: str = f"Hello, {name}"
        return Result(text=text)

    def process(self, input: Input) -> Output:
        result: Result = self.analyze(input.name)
        response: Output = Output(
            api_name=self.api_name,
            api_version=API_VERSION,
            text=result.text,
        )

        return response
