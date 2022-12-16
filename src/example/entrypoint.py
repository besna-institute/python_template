from typing import Final

from fastapi import Body, FastAPI

from src.example.solvers import SomeSolver
from src.models import Input, Output

APP: Final[FastAPI] = FastAPI()


@APP.post("/", response_model=Output)
async def root(
    input: Input = Body(  # noqa: B008
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "value": {"api_name": "Solver", "name": "Taro"},
            }
        },
    )
) -> Output:
    return SomeSolver().process(input)
