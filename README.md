# Python template ![Python](https://img.shields.io/badge/python-3.12-blue.svg)

## 概要

このリポジトリは、Pythonを使用したAPIサーバー開発の効率化を目的としたテンプレートリポジトリです。以下の特徴を持っています：

- FastAPIによる高速なAPIサーバー実装
- [OpenAPI Generator](https://openapi-generator.tech/)によるコード生成
- [DevContainer](https://containers.dev/)による開発環境のDockerコンテナ化
- 依存パッケージの厳密なバージョン管理
- Python標準ライブラリの`unittest`ですぐにテストを始められる環境
- `flake8`、`black`、`isort`によるコード品質の自動チェックと整形
- CSpellによるスペルチェック
- GitHub Actionsによる継続的インテグレーション（CI）の整備
- Cloud Runへのデプロイ対応

このテンプレートを使用することで、各案件に向けたAPIサーバー開発を迅速に開始し、一貫した開発スタイルを維持することができます。

## 開発の始め方

### 必要な環境

> [!IMPORTANT]
> [VSCode](https://azure.microsoft.com/ja-jp/products/visual-studio-code/) による開発を**推奨**します。

- [VSCode](https://azure.microsoft.com/ja-jp/products/visual-studio-code/)
- [Docker](https://docs.docker.com/get-docker/)

### 開発環境のセットアップ

1. VSCodeの拡張機能[Visual Studio Code Remote Containers](https://code.visualstudio.com/docs/remote/containers)をインストールします。
2. コマンドパレットを開き、`Remote-Containers: Reopen in Container`を選択します。

### ローカルでの開発

#### サーバーの起動
```bash
# exampleを実行する場合
python -m src.example.entrypoint

# another_exampleを実行する場合
python -m src.another_example.entrypoint

# save_resultを実行する場合
python -m src.save_result.entrypoint
```

http://localhost:8080 に対してリクエストを送ることができるようになります。

#### テストの実行
```bash
python -m unittest
```

#### APIのテスト
JSONリクエスト
```bash
curl -X POST -H "Content-Type: application/json" localhost:8080/ -d '{"api_name": "Solver", "name": "Taro"}'
```

JSON Linesリクエスト
```bash
DATA='
{"api_name": "Solver", "name": "Taro"}
{"api_name": "Solver", "name": "Jiro"}
{"api_name": "Solver", "name": "Siro"}
'
curl -X POST -H "Content-Type: application/jsonl" localhost:8080/ -d "$DATA"
```

## APIの定義

OpenAPI仕様でAPIを定義し、[OpenAPI Generator](https://openapi-generator.tech/)を使用してPythonコードを自動生成します。`schema.yaml`にOpenAPIの定義を記述し、以下のコマンドでPythonのデータモデルに変換します：

```bash
./scripts/convert_open_api_to_dataclass.sh
```

生成されたコードは [src/models/](src/models/) に配置されます。自動生成されたコードは直接編集せず、`schema.yaml`を更新して再生成してください。

## Python の依存パッケージの管理

### requirements.in の更新

- 必ず手動で更新すること
- 直接依存しているパッケージのみを書くこと
- [PyPI](https://pypi.org/)で利用可能なパッケージのみを書くこと

例) flake8 の バージョンを 1.2.X にしたい場合: `flake8~=1.2.3`
参考： https://www.python.org/dev/peps/pep-0440/#version-specifiers

以下のコマンドによる更新は禁止します。
```bash
pip freeze > requirements.in
pip freeze >> requirements.in
```

### requirements.txt の更新

以下のコマンドを実行します。
```bash
./scripts/generate_lockfile.sh
```

## トラブルシューティング

### よくある問題

1. **コンテナが起動しない**
   - Dockerが正しくインストールされているか確認します。
   - VSCodeのRemote Containers拡張機能が最新版か確認します。

2. **依存パッケージのインストールに失敗**
   - `requirements.in`のバージョン指定が正しいか確認します。
   - インターネット接続を確認します。

3. **APIの自動生成が失敗**
   - `schema.yaml`の構文が正しいか確認します。
   - Dockerコンテナ内で実行しているか確認します。

## ログの書き方

### 基本的なログ出力

このプロジェクトでは、標準的なPythonの`logging`モジュールを拡張した独自のロギング機能を提供しています。`src.logger`モジュールを使用することで、統一されたフォーマットでログを出力できます。

```python
from src.logger import logger

# 基本的なログ出力
logger.debug("デバッグ情報")
logger.info("通常の情報")
logger.warning("警告メッセージ")
logger.error("エラーメッセージ")
logger.critical("致命的なエラー")

# 追加情報を含むログ
logger.info("ユーザー情報", extra={"user_id": 123, "username": "test_user"})

# 例外情報を含むログ
try:
    1 / 0
except ZeroDivisionError:
    logger.error("計算エラーが発生しました", exc_info=True)
```

### 色付きログメッセージ

開発環境では視認性を高めるため、色付きログメッセージを使用できます。以下のユーティリティ関数を使用して、ログメッセージに色や強調を追加できます。

```python
from src.logger import logger, red, green, yellow, blue, bold, success, warning, error, highlight

# 色付きメッセージの例
logger.info("ステータス: %s", success("成功"))
logger.warning("注意: %s", warning("ディスク容量が少なくなっています"))
logger.error("エラー: %s", error("データベース接続に失敗しました"))

# 強調表示の例
logger.info("ユーザー %s が管理画面にログインしました", highlight("admin"))
logger.info("重要な設定: %s", bold("DEBUG_MODE=True"))

# 複合的な使用例
logger.info("実行時間: %s (前回: %s)", bold(green("152ms")), yellow("165ms"))
```

> [!NOTE]
> 本番環境（`ENV=production`）では、色付けは自動的に無効になり、代わりにGoogle Cloud互換のJSON形式でログが出力されます。これにより、ログ解析システムとの互換性が確保されます。

### 環境別のログ出力

環境変数 `ENV` によってログの出力形式が変わります：

- **開発環境（デフォルト）**: カラー付きの人間が読みやすい形式
  ```
  [2025-05-26T07:04:17] INFO    [logger.py:304] app_started
  ```

- **本番環境（`ENV=production`）**: Google Cloud互換のJSON形式
  ```json
  {"timestamp": "2025-05-26T07:03:43.566Z", "severity": "INFO", "message": "app_started", "logging.googleapis.com/sourceLocation": {"file": "logger.py", "line": 304, "function": "<module>"}, "env": "production"}
  ```

### HTTPリクエストのロギング

FastAPIアプリケーションでHTTPリクエストを自動的にログに記録するには、`LoggingMiddleware`を使用します：

```python
from fastapi import FastAPI
from src.logger import LoggingMiddleware

app = FastAPI()
app.add_middleware(LoggingMiddleware)
```

これにより、各HTTPリクエストの情報（メソッド、パス、レスポンスコードなど）が自動的にログに記録されます。ヘルスチェックリクエスト（`/health`エンドポイント）はログから除外されます。

### 生成AIを活用したログ作成

ログメッセージの作成には、生成AIを活用することも推奨されます。特に以下のような場合にAIの支援が有効です：

- 一貫性のあるログメッセージフォーマットの作成
- 適切なログレベル（INFO/WARNING/ERROR）の選択
- 色付きログの効果的な使用例の生成
- エラーメッセージの明確で詳細な記述

生成AIを使用する際は、以下のポイントに注意してください：

1. 機密情報や個人情報をAIに送信しないこと
2. 生成されたコードを必ず確認し、プロジェクトの規約に合致していることを確認すること
3. 自動生成されたログメッセージの文言が適切かどうかをレビューすること

例えば、以下のようなプロンプトでAIにログメッセージの作成を依頼できます：
```
「src.logger モジュールを使って、ユーザー認証に失敗した場合のエラーログを作成してください。logger.error と error() 関数を使用し、ユーザーID、IPアドレス、失敗理由を含めること。extra パラメータを使用して構造化ログも実装し、適切な色付けも提案してください。」
```

これにより開発者は、効率的かつ一貫性のあるログ実装が可能になります。

## スペルチェック

このプロジェクトでは、[CSpell](https://cspell.org/)を使用してコード内のスペルミスをチェックしています。これにより、コードベース全体で一貫した命名規則を保ちやすくなります。

### スペルチェックの実行

全ファイルのスペルチェックを実行するには、以下のコマンドを使用します：

```bash
npx cspell --config cspell.json "**" --dot
```

このコマンドは、プロジェクト内のすべてのファイル（ドット始まりのファイルも含む）に対してスペルチェックを実行します。

### 辞書の追加

プロジェクト固有の用語や技術用語は、`.cspell/project-words.txt`に追加することができます。このファイルに追加された単語は、スペルチェックで「正しい」と認識されます。

例えば、`myapi`という用語を追加する場合：

1. `.cspell/project-words.txt`ファイルを開きます。
2. 適切なセクションに`myapi`を追加します。
3. 変更を保存します。

次回のスペルチェック実行時に、その単語はエラーとして報告されなくなります。

### GitHub Actionsでのスペルチェック

このプロジェクトではGitHub Actionsを使用して、すべてのブランチへのプッシュ時に自動的にスペルチェックが実行されます。ワークフローは`.github/workflows/spellcheck.yml`で定義されています。

## Dockerfileの構文チェック

このプロジェクトでは、[Hadolint](https://github.com/hadolint/hadolint)を使用してDockerfileの構文チェックを行っています。Hadolintは、Dockerfileのベストプラクティスに基づいたリンターで、潜在的な問題や改善点を自動的に検出します。

### チェック対象のDockerfile

以下のDockerfileが自動チェックの対象となっています：

1. **ルートのDockerfile** - アプリケーションのコンテナ化用
2. **DevContainer用Dockerfile** - 開発環境用（`.devcontainer/Dockerfile`）
3. **GPU対応DevContainer用Dockerfile** - GPU開発環境用（`.devcontainer/nvidia-gpu.Dockerfile`）

### GitHub Actionsでの自動チェック

Dockerfileが変更された場合、GitHub Actionsによって自動的にHadolintが実行されます。ワークフローの設定は`.github/workflows/check-dockerfile.yml`で定義されています。

このワークフローには以下の特徴があります：

- Dockerfileが存在しない場合は自動的にチェックをスキップ
- 各Dockerfileに対して専用のジョブが実行される
- プッシュおよびプルリクエスト時に自動実行

## 保守運用

このテンプレートリポジトリの保守運用に関する詳細は[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。リリース手順についても同ファイルに記載されています。