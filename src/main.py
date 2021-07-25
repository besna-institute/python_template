from fastapi import Body, FastAPI

from src.api import model, some_resolver

app = FastAPI()


@app.post("/", response_model=model.Output)
async def root(
    input: model.Input = Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "value": {"apiName": "PythonTemplate", "name": "Taro"},
            }
        },
    )
):
    return some_resolver.process(input)
