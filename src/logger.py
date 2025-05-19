"""ロギング設定とログユーティリティモジュール

このモジュールはアプリケーション全体で使用されるロギング機能を提供します。
以下の機能が含まれています：
- ログフォーマッタ（カラー出力とGCP JSON形式）
- ロギング設定
- HTTPリクエスト/レスポンスのロギングミドルウェア

環境変数 ENV によってログの出力形式が変わります：
- ENV=production: Google Cloud互換のJSON形式
- その他: カラー付きの人間が読みやすい形式
"""

import datetime
import json
import logging
import os
import sys
from collections.abc import Callable
from logging import LogRecord
from typing import Any

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


# ANSIエスケープシーケンスを使用した色定義
class Colors:
    """ANSIエスケープシーケンスを使用した色定義

    ターミナル出力の色付けに使用する定数を提供します。
    """

    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    BRIGHT_RED = "\033[91m"


class ColoredFormatter(logging.Formatter):
    """ANSIエスケープシーケンスを使用した色付きフォーマッタ"""

    LEVEL_COLORS = {
        "DEBUG": Colors.BLUE,
        "INFO": Colors.GREEN,
        "WARNING": Colors.YELLOW,
        "ERROR": Colors.RED,
        "CRITICAL": Colors.BRIGHT_RED,
    }

    def format(self, record: LogRecord) -> str:
        """ログレベルに応じて色を付ける"""
        message = super().format(record)

        # ターミナルがカラー対応かチェック
        if hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
            # 各ログレベルで行頭の部分を色付け
            for level, color in self.LEVEL_COLORS.items():
                if level in message:
                    # レベル名だけを色付け
                    return message.replace(f"{level}", f"{color}{level}{Colors.RESET}", 1)

        return message


class GoogleCloudJsonFormatter(logging.Formatter):
    def format(self, record: LogRecord) -> str:
        # 基本フィールド
        log_record: dict[str, Any] = {
            "timestamp": datetime.datetime.fromtimestamp(record.created).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            "severity": record.levelname,
            "message": record.getMessage(),
        }
        # ファイル名・行番号・関数名を sourceLocation にまとめる
        log_record["logging.googleapis.com/sourceLocation"] = {
            "file": record.filename,
            "line": record.lineno,
            "function": record.funcName,
        }
        # record.__dict__ からカスタム属性だけ抜き出す
        for key, val in record.__dict__.items():
            if (
                key not in log_record
                and not key.startswith("_")
                and key
                not in {
                    "name",
                    "msg",
                    "args",
                    "levelname",
                    "levelno",
                    "pathname",
                    "filename",
                    "module",
                    "exc_info",
                    "exc_text",
                    "stack_info",
                    "lineno",
                    "funcName",
                    "created",
                    "msecs",
                    "relativeCreated",
                    "thread",
                    "threadName",
                    "processName",
                    "process",
                }
            ):
                log_record[key] = val

        # 例外情報があれば別フィールドに
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record, ensure_ascii=False)


def configure_logging() -> None:
    """ロギングを設定する

    環境変数ENVに基づいてロギングを設定します：
    - production環境: GCP JSON形式
    - その他の環境: カラー付きの人間が読みやすい形式

    ロガーはINFOレベル以上のメッセージを標準出力に出力します。
    """
    env = os.getenv("ENV", "local").lower()
    handler = logging.StreamHandler(sys.stdout)

    if env == "production":
        handler.setFormatter(GoogleCloudJsonFormatter())
    else:
        fmt = "[%(asctime)s] %(levelname)-7s [%(filename)s:%(lineno)d] %(message)s"
        handler.setFormatter(ColoredFormatter(fmt=fmt, datefmt="%Y-%m-%dT%H:%M:%S"))

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()
    root.addHandler(handler)


configure_logging()
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """HTTPリクエストとレスポンスのロギングを行うミドルウェア

    このミドルウェアは以下の情報をログに記録します：
    - リクエストのメソッドとパス
    - リクエストヘッダー
    - レスポンスのステータスコード

    FastAPIアプリケーションに追加して使用します：
    ```python
    app = FastAPI()
    app.add_middleware(LoggingMiddleware)
    ```
    """

    async def dispatch(self, request: Request, call_next: Callable[[Request], Any]) -> Any:
        """HTTPリクエストを処理し、ログを記録する

        Args:
            request: 処理するHTTPリクエスト
            call_next: 次のミドルウェアまたはエンドポイントを呼び出す関数

        Returns:
            処理されたHTTPレスポンス
        """
        # リクエストのログ
        logger.info("Request: %s %s", request.method, request.url.path)
        logger.info("Request Headers: %s", dict(request.headers))

        # リクエストの処理
        response = await call_next(request)

        # レスポンスのログ
        logger.info("Response Status: %s", response.status_code)

        return response


if __name__ == "__main__":
    # 以下のコマンドを実行することでログの出力例が確認できます。
    # 環境別の実行方法と出力形式：
    # ローカル環境:
    #   実行方法: python src/logger.py
    #   出力形式: カラー付きの人間が読みやすい形式で表示されます
    # 本番環境:
    #   実行方法: ENV=production python src/logger.py
    #   出力形式: JSON形式で構造化されたログが出力されます
    logger.info("app_started", extra={"env": os.getenv("ENV", "local")})
    logger.warning("user_not_found", extra={"user_id": 42})
    try:
        1 / 0
    except ZeroDivisionError:
        logger.error("exception_occurred", exc_info=True)
