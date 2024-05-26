"""Flaskアプリとして開発する場合はこのファイルを利用する

※ Cloud Functionsで開発する場合はこのファイルは消してOK

開発用サーバーの起動
    python flask_server.py
本番用サーバーの起動（https://docs.gunicorn.org/en/latest/run.html）
    gunicorn flask_server:APP
"""
from flask import Flask, request
from flask.wrappers import Response

from src.example.entrypoint import example as example_

APP: Flask = Flask(__name__)


@APP.post("/")
def example() -> Response:
    return example_(request)  # type: ignore


if __name__ == "__main__":
    APP.run(port=8080)
