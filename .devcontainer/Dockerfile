FROM mcr.microsoft.com/vscode/devcontainers/python:3.10
RUN su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install 16 2>&1"
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
  && apt-get -y install --no-install-recommends \
    build-essential \
    openjdk-17-jre
RUN wget --progress=dot:giga -O /usr/local/bin/shfmt https://github.com/mvdan/sh/releases/download/v3.6.0/shfmt_v3.6.0_linux_amd64 \
    && chmod 755 /usr/local/bin/shfmt
