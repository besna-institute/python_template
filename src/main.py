from fastapi import Body, FastAPI

from src.api import some_solver
from src.api.model import input, output

app = FastAPI()


@app.post("/", response_model=output.SchemaOfSolverOutput)
async def root(
    input: input.SchemaOfSolverInput = Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "value": {"apiName": "PythonTemplate", "name": "Taro"},
            }
        },
    )
):
    return some_solver.process(input)
