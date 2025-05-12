# Python template ![Python](https://img.shields.io/badge/python-3.12-blue.svg)

## 概要

このリポジトリは、Pythonを使用したAPIサーバー開発の効率化を目的としたテンプレートリポジトリです。以下の特徴を持っています：

- OpenAPIによるAPI定義の自動生成
- [DevContainer](https://containers.dev/)による開発環境のDockerコンテナ化
- 依存パッケージの厳密なバージョン管理
- Python標準ライブラリの`unittest`ですぐにテストを始められる環境
- `flake8`、`black`、`isort`によるコード品質の自動チェックと整形
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
python app.py
```

http://localhost:8080 に対してリクエストを送ることができるようになります。

#### テストの実行
```bash
python -m unittest
```

#### APIのテスト
JSONリクエスト
```bash
curl -X POST -H "Content-Type: application/json" localhost:8080/example -d '{"api_name": "Solver", "name": "Taro"}'
```

JSON Linesリクエスト
```bash
DATA='
{"api_name": "Solver", "name": "Taro"}
{"api_name": "Solver", "name": "Jiro"}
{"api_name": "Solver", "name": "Siro"}
'
curl -X POST -H "Content-Type: application/jsonl" localhost:8080/example -d "$DATA"
```

## APIの定義

OpenAPIを使用してAPIを定義します。`schema.yaml`にOpenAPIの定義を記述し、以下のコマンドでPythonの [dataclass](https://docs.python.org/ja/3.12/library/dataclasses.html#dataclasses.dataclass) に変換します：

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

## 保守運用

このテンプレートリポジトリの保守運用に関する詳細は[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。リリース手順についても同ファイルに記載されています。