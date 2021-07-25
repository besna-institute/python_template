from dataclasses import dataclass

from src.api import model


@dataclass
class Result:
    text: str


def analyze(input: model.Input.name) -> Result:
    text = f"Hello, {input.name}"
    return Result(text=text)
