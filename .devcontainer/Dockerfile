FROM mcr.microsoft.com/vscode/devcontainers/python:3.9
RUN su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install 16 2>&1"
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
  && apt-get -y install --no-install-recommends \
    build-essential \
    openjdk-17-jre