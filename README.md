# Python template

[VSCode](https://azure.microsoft.com/ja-jp/products/visual-studio-code/) による開発を**推奨**する．

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

```bash
docker build -f Dockerfile -t python-template . && docker run -p 80:80 -it python-template
```

http://localhost:80 に対してリクエストを送ることができるようになる．

```bash
curl -X POST -H "Content-Type: application/json" localhost:80 -d '{"apiName": "Solver", "name": "Taro"}'
```

### ローカルでのテストの実行

```bash
docker build -f Dockerfile -t python-template . && docker run -p 80:80 -it python-template /usr/local/bin/python -m unittest
```

## API の定義について

OpenAPI を用いて定義する．
[src/schema.yaml](src/schema.yaml) に OpenAPI を置く．

以下を実行することで Python の [pydantic](https://pydantic-docs.helpmanual.io/) を利用した表現に変換したものを [src/model.py](src/model.py) を置く．

```bash
./scripts/convert_open_api_to_datamodel.sh
```

ここで自動生成したコードを直接編集するのは避ける．
また，[scripts/convert_open_api_to_datamodel.sh](scripts/convert_open_api_to_datamodel.sh) は Docker コンテナ内で実行する想定であることに注意！
