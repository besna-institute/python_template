from typing import Any

import functions_framework
from flask import jsonify
from flask.wrappers import Request, Response

from src.example.solvers import SomeSolver
from src.models import Input, Output


@functions_framework.http  # type: ignore
def example(request: Request) -> Response:
    request_body: Any | None = request.get_json()
    if request_body is None:
        raise ValueError("Invalid JSON.")
    input: Input = Input(api_name=request_body["api_name"], name=request_body["name"])
    output: Output = SomeSolver().process(input=input)
    response_body: Response = jsonify(output)

    return response_body
