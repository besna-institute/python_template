import json
import os

from flask import Flask, Response, jsonify, request

from src.example.solvers import SomeSolver
from src.models import Input, Output

app = Flask(__name__)


@app.route("/example", methods=["POST"])
def example_endpoint() -> Response:
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
    response_body = jsonify(output.to_dict())

    return response_body


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
