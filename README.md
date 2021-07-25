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

## Docker によるアプリケーションの起動

```bash
docker build . -t python-template
docker run -p 80:80 -it python-template
```

## エディタ・IDEの設定

Pythonのコードの品質を確保するために `black`，`isort`，`flake8`，`mypy` を採用している．
また，`editorconfig`も採用している．
各種エディタ・IDE で設定が必要なので，以下に示す．

### VSCode

拡張機能は `.vscode/extensions.json`
設定は `.vscode/settings.json.default`

### IntelliJ IDEA

???

