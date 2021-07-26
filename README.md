# Python template

## 開発環境の構築

ここでは Docker を用いた構築方法について紹介する．

### Docker のインストール

https://docs.docker.com/get-docker/

### Docker イメージのビルド

```bash
docker build -f Dockerfile.development -t python-template .
```

### Docker コンテナの実行

```bash
docker run -p 8000:8000 -it python-template
```

http://localhost:8000 に対してリクエストを送ることができるようになる．

### ローカルでのテストの実行

```bash
docker run -p 8000:8000 -it python-template /usr/local/bin/python -m unittest discover
```

## API の定義について

JSON Schema を用いて定義する．
[src/model/schema/](src/model/schema) に JSON Schema を置く．

以下を実行することで Python の [pydantic](https://pydantic-docs.helpmanual.io/) を利用した表現に変換したものを [src/model/](src/model) を置く．

```bash
./scripts/convert_jsonschema_to_pydantic.sh
```

ここで自動生成したコードを直接編集するのは避ける．
また，[scripts/convert_jsonschema_to_pydantic.sh](scripts/convert_jsonschema_to_pydantic.sh) は Docker コンテナ内で実行する想定であることに注意！

## Docker によるアプリケーションの起動

```bash
docker build . -t python-template
docker run -p 80:80 -it python-template
```

## エディタ・IDE の設定

Python のコードの品質を確保するために `black`，`isort`，`flake8`，`mypy` を採用している．
また，`editorconfig`も採用している．
各種エディタ・IDE で設定が必要なので，以下に示す．

### VSCode

[Visual Studio Code Remote Containers](https://code.visualstudio.com/docs/remote/containers) の設定は [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json) にある．

拡張機能は [.vscode/extensions.json](.vscode/extensions.json) にある．

設定は [.vscode/settings.json.default](.vscode/settings.json.default) にある．これをベースに `.vscode/settings.json` を作成する．
