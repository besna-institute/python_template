from fastapi import Body, FastAPI

from src.model import Input, Output
from src.solvers import SomeSolver

app = FastAPI()


@app.post("/", response_model=Output)
async def root(
    input: Input = Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "value": {"apiName": "Solver", "name": "Taro"},
            }
        },
    )
):
    return SomeSolver().process(input)
