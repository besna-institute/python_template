from fastapi import Body, FastAPI

from src.model import input, output
from src.solver.some_solver import SomeSolver

app = FastAPI()


@app.post("/", response_model=output.SchemaOfSolverOutput)
async def root(
    input: input.SchemaOfSolverInput = Body(
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
