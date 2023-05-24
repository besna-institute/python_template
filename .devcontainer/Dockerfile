# https://github.com/devcontainers/images/tree/main/src/python
FROM mcr.microsoft.com/vscode/devcontainers/python:3.10
RUN su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install 16 2>&1"
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
  build-essential \
  openjdk-17-jre