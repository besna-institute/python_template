# pylint: disable=duplicate-code
import json
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from src.another_example.solvers import SomeSolver
from src.logger import LoggingMiddleware
from src.models import Input, Output

app = FastAPI()

app.add_middleware(LoggingMiddleware)


@app.get("/health")
async def health() -> dict[str, str]:
    """ヘルスチェックエンドポイント
    DBやAPIの疎通確認もここで行う。
    """
    return {"status": "ok"}


@app.post("/")
async def another_example(request: Request) -> Response:
    """サンプル

    JSON Lines を入力とする場合
      Content-Type: application/jsonl

    JSON を入力とする場合
      Content-Type: application/json
    """
    match request.headers.get("content-type", ""):
        case "application/jsonl":
            jsonl_request_body: bytes = await request.body()
            result: list[str] = []
            for json_str in jsonl_request_body.decode().splitlines():
                if not json_str:
                    continue
                request_json = json.loads(json_str)
                input_: Input = Input(api_name=request_json["api_name"], name=request_json["name"])
                output_: Output = SomeSolver().process(input=input_)
                result.append(json.dumps(output_.to_dict()))
            response_content = "\n".join(result)
            return Response(content=response_content, media_type="application/jsonl")
        case _:
            request_json = await request.json()
            input__: Input = Input(api_name=request_json["api_name"], name=request_json["name"])
            output__: Output = SomeSolver().process(input=input__)
            response_dict = output__.to_dict()
            return JSONResponse(content=response_dict)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("PORT", 8081)))
