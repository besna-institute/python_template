from src.model import input, output
from src.solver import some_solver

apiName = "Solver"
apiVersion = "1.0.0"


def process(input: input.SchemaOfSolverInput) -> output.SchemaOfSolverOutput:
    result = some_solver.analyze(input.name)
    response = output.SchemaOfSolverOutput(
        apiName=apiName,
        apiVersion=apiVersion,
        text=result.text,
    )

    return response
