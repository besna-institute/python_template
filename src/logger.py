"""ロギング設定とログユーティリティモジュール

このモジュールはアプリケーション全体で使用されるロギング機能を提供します。
以下の機能が含まれています：
- ログフォーマッタ（カラー出力とGCP JSON形式）
- ロギング設定
- HTTPリクエスト/レスポンスのロギングミドルウェア
- 色付きログメッセージのユーティリティ関数

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
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"


def colorize(text: str, color: str) -> str:
    """テキストに色を付ける

    Args:
        text: 色を付けるテキスト
        color: Colors クラスで定義された色コード

    Returns:
        色付きテキスト（ターミナルがカラー対応の場合のみ）
    """
    # 本番環境では色付けしない
    if os.getenv("ENV", "local").lower() == "production":
        return text

    # ターミナルがカラー対応かチェック
    if hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
        return f"{color}{text}{Colors.RESET}"
    return text


def red(text: str) -> str:
    """テキストを赤色で表示する"""
    return colorize(text, Colors.RED)


def green(text: str) -> str:
    """テキストを緑色で表示する"""
    return colorize(text, Colors.GREEN)


def yellow(text: str) -> str:
    """テキストを黄色で表示する"""
    return colorize(text, Colors.YELLOW)


def blue(text: str) -> str:
    """テキストを青色で表示する"""
    return colorize(text, Colors.BLUE)


def magenta(text: str) -> str:
    """テキストを紫色で表示する"""
    return colorize(text, Colors.MAGENTA)


def cyan(text: str) -> str:
    """テキストを水色で表示する"""
    return colorize(text, Colors.CYAN)


def bold(text: str) -> str:
    """テキストを太字で表示する"""
    return colorize(text, Colors.BOLD)


def success(text: str) -> str:
    """成功メッセージを緑色で表示する"""
    return green(text)


def warning(text: str) -> str:
    """警告メッセージを黄色で表示する"""
    return yellow(text)


def error(text: str) -> str:
    """エラーメッセージを赤色で表示する"""
    return red(text)


def highlight(text: str) -> str:
    """テキストを目立たせる（太字+水色）"""
    return colorize(text, f"{Colors.BOLD}{Colors.CYAN}")


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
    if env == "production":
        root.setLevel(logging.INFO)
    else:
        # ローカル環境ではDEBUGレベル以上のログを出力
        root.setLevel(logging.DEBUG)
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
        # リクエストの処理
        response = await call_next(request)

        # /healthエンドポイントへのリクエストはログ記録をスキップ
        if request.url.path == "/health":
            return response

        logger.info(
            "%s %s",
            request.method,
            request.url.path,
            extra={
                "httpRequest": {
                    "requestMethod": request.method,
                    "requestUrl": str(request.url),
                    "requestSize": request.headers.get("content-length", ""),
                    "userAgent": request.headers.get("user-agent", ""),
                    "remoteIp": request.client.host if request.client else "",
                    "serverIp": request.headers.get("host", ""),
                    "protocol": request.scope.get("type", ""),
                },
            },
        )

        return response


if __name__ == "__main__":
    # NOTE:
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

    # 色付きログユーティリティの使用例
    logger.info("----- 色付きログユーティリティの使用例 -----")
    logger.info("通常テキスト + %s + 通常テキスト", red("赤色テキスト"))
    logger.info("ステータス: %s / %s / %s", success("成功"), warning("警告"), error("エラー"))
    logger.info("ユーザー %s がログインしました", highlight("admin"))
    logger.info("青色: %s / 緑色: %s", blue("これは青色のテキスト"), green("これは緑色のテキスト"))
    logger.info("紫色: %s / 水色: %s", magenta("これは紫色のテキスト"), cyan("これは水色のテキスト"))
    logger.info("太字: %s", bold("これは太字のテキスト"))
    logger.info("組み合わせ: %s", bold(red("赤色の太字テキスト")))
    logger.info("背景色: %s", colorize("警告メッセージ", Colors.BLACK + Colors.BG_YELLOW))
    logger.info("下線: %s", colorize("重要", Colors.UNDERLINE))

    # 追加の使用例
    logger.info("----- 実践的な使用例 -----")

    # 基本的な状態表示
    logger.info("■ 状態表示の例:")
    logger.info("  ✓ %s: ファイルのアップロードが完了しました", success("成功"))
    logger.warning("  ⚠ %s: ディスク容量が少なくなっています", warning("警告"))
    logger.error("  ✗ %s: 接続がタイムアウトしました", error("エラー"))

    # 強調表示
    logger.info("■ 強調表示の例:")
    logger.info("ユーザー %s が管理画面にログインしました", highlight("admin"))
    logger.info("重要な設定: %s", bold("DEBUG_MODE=True"))

    # 複雑な例
    logger.info("■ 複雑な例:")
    logger.info("ステータス: [%s] オンライン / [%s] オフライン", green("●"), red("●"))
    logger.info("進捗状況: %s□□□□□□□□□□ 60%%", colorize("██████████", Colors.GREEN))
    logger.info("実行時間: %s (前回: %s)", bold(green("152ms")), yellow("165ms"))

    # テーブル形式の例
    logger.info("■ テーブル形式の例:")
    logger.info("%s    | %s      | %s", bold("サーバー名"), bold("状態"), bold("レスポンス時間"))
    logger.info("--------------|-----------|---------------")
    logger.info("api-server-01 | %s     | %s", green("正常"), green("24ms"))
    logger.warning("api-server-02 | %s   | %s", yellow("不安定"), yellow("156ms"))
    logger.error("api-server-03 | %s    | %s", red("エラー"), red("タイムアウト"))

    logger.info("-----------------------------------------")
