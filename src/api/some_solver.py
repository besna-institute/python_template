from src.api.model import Input, Output
from src.solver import some_sovler

apiName = "PythonTemplate"
apiVersion = "1.0.0"


def process(input: Input) -> Output:
    result = some_sovler.analyze(input.name)
    response = Output(
        apiName=apiName,
        apiVersion=apiVersion,
        text=result.text,
    )

    return response
