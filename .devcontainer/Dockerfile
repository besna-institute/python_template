# https://github.com/devcontainers/images/tree/main/src/python
FROM mcr.microsoft.com/vscode/devcontainers/python:3.10
RUN su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install 16 2>&1"

# See https://github.com/hadolint/hadolint/releases
ARG HADOLINT_VERSION="v2.12.0"
RUN wget --progress=dot:giga -O /usr/local/bin/hadolint https://github.com/hadolint/hadolint/releases/download/${HADOLINT_VERSION}/hadolint-Linux-x86_64 \
  && chmod 755 /usr/local/bin/hadolint
