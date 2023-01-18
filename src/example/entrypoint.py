import json

import functions_framework  # type: ignore
from flask import jsonify
from flask.wrappers import Request, Response

from src.example.solvers import SomeSolver
from src.models import Input, Output


@functions_framework.http  # type: ignore
def example(request: Request) -> Response:
    """サンプル

    JSON Lines を入力とする場合
      Content-Type: application/jsonl

    JSON を入力とする場合
      Content-Type: application/json
    """
    if request.content_type == "application/jsonl":
        jsonl_request_body: str = request.get_data(as_text=True)
        result: list[str] = []
        for json_str in jsonl_request_body.splitlines():
            if not json_str:
                continue
            request_json = json.loads(json_str)
            input_: Input = Input(api_name=request_json["api_name"], name=request_json["name"])
            output_: Output = SomeSolver().process(input=input_)
            result.append(json.dumps(output_.to_dict()))
        return Response("\n".join(result), headers={"Content-Type": "application/jsonl"})
    if (request_body := request.get_json()) is None:
        raise ValueError("Invalid JSON.")
    input: Input = Input(api_name=request_body["api_name"], name=request_body["name"])
    output: Output = SomeSolver().process(input=input)
    response_body: Response = jsonify(output)

    return response_body
