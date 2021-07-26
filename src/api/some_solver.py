from src.api.model import input, output
from src.solver import some_sovler

apiName = "Solver"
apiVersion = "1.0.0"


def process(input: input.SchemaOfSolverInput) -> output.SchemaOfSolverOutput:
    result = some_sovler.analyze(input.name)
    response = output.SchemaOfSolverOutput(
        apiName=apiName,
        apiVersion=apiVersion,
        text=result.text,
    )

    return response
