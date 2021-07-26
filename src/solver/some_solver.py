from dataclasses import dataclass


@dataclass
class Result:
    text: str


def analyze(name: str) -> Result:
    text = f"Hello, {name}"
    return Result(text=text)
