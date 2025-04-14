# Python template ![Python](https://img.shields.io/badge/python-3.12-blue.svg)

[VSCode](https://azure.microsoft.com/ja-jp/products/visual-studio-code/) による開発を**推奨**する．

## Python の依存パッケージの管理

### requirements.in の更新

- 必ず手動で更新すること
- 直接依存しているパッケージのみを書くこと
- [PyPI](https://pypi.org/)で利用可能なパッケージのみを書くこと

例) flake8 の バージョンを 1.2.X にしたい場合: `flake8~=1.2.3`
参考： https://www.python.org/dev/peps/pep-0440/#version-specifiers

以下のコマンドによる更新は禁止
```bash
pip freeze > requirements.in
pip freeze >> requirements.in
```

### requirement.txt の更新

以下のコマンドを実行
```bash
./scripts/generate_lockfile.sh
```

## 最新のテンプレートを適用する

作業ディレクトリをきれいにした状態で以下のコマンドを実行
```bash
./scripts/apply_template_updates.sh
```

`requirements.in` などに適用された変更が意図したものかを確認してからコミットする．

## 開発環境の構築

以下の手順を実行することで開発環境を構築できる．

### インストール

- [VSCode](https://azure.microsoft.com/ja-jp/products/visual-studio-code/)
- [Docker](https://docs.docker.com/get-docker/)

### VSCode の設定

VSCode を起動し，拡張機能の[Visual Studio Code Remote Containers](https://code.visualstudio.com/docs/remote/containers) をインストールする．

[コマンドパレット](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette)を開き，
```
Remote-Containers: Reopen in Container
```
を選択する．

### ローカルでのサーバーの起動

VSCode の Remote Container のターミナルで
```bash
functions-framework --target=example --debug
```

http://localhost:8080 に対してリクエストを送ることができるようになる．

JSON
```bash
curl -X POST -H "Content-Type: application/json" localhost:8080 -d '{"api_name": "Solver", "name": "Taro"}'
```

JSON Lines
```bash
DATA='
{"api_name": "Solver", "name": "Taro"}
{"api_name": "Solver", "name": "Jiro"}
{"api_name": "Solver", "name": "Siro"}
'
curl -X POST -H "Content-Type: application/jsonl" localhost:8080 -d "$DATA"
```

### ローカルでのテストの実行

VSCode の Remote Container のターミナルで
```bash
python -m unittest
```

## API の定義について

OpenAPI を用いて定義する．
[schema.yaml](schema.yaml) に OpenAPI を置く．

以下を実行することで Python の [dataclass](https://docs.python.org/ja/3.12/library/dataclasses.html#dataclasses.dataclass) を利用した表現に変換したものを [src/models/](src/models/) に置く．

```bash
./scripts/convert_open_api_to_dataclass.sh
```

ここで自動生成したコードを直接編集するのは避ける．
また，[scripts/convert_open_api_to_dataclass.sh](scripts/convert_open_api_to_dataclass.sh) は Docker コンテナ内で実行する想定であることに注意！

## リリース手順

1. mainブランチをチェックアウトし、コミットしていない変更がない状態にする。
```bash
git checkout main
```

2. リリース用の新しいブランチを作成する。`x.x.x`をリリースしたいバージョン番号に置き換える。
```bash
git checkout -b release/vx.x.x
```

3. 新しいブランチをリモートリポジトリにプッシュする。
```bash
git commit .
git push origin release/vx.x.x
```

4. プルリクエストを作成し、すべてのCIが通ることを確認する。

5. 新しいリリースを作成する。

https://github.com/besna-institute/python_template/releases/new から作成する。

以下のように設定し、"Generate release notes"を押す。

![スクリーンショット 2024-04-22 194831](https://github.com/besna-institute/python_template/assets/13166203/77fccdea-6e67-4a44-94bf-d2e829b9c3dd)

リリースノートを記入したら、"Publish release"を押す。

6. プルリクエストを main ブランチにマージする。
