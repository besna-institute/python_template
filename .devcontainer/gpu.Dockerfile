# https://github.com/devcontainers/images/tree/main/src/base-ubuntu
FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# Install cuDNN
# https://docs.nvidia.com/deeplearning/cudnn/install-guide/index.html#package-manager-ubuntu-install
ENV OS ubuntu2204
# OS is debian11, ubuntu1804, ubuntu2004, or ubuntu2204
RUN apt-get update \
  && apt-get install --no-install-recommends -yq software-properties-common \
  && wget --progress=dot:giga https://developer.download.nvidia.com/compute/cuda/repos/${OS}/x86_64/cuda-${OS}.pin \
  && mv cuda-${OS}.pin /etc/apt/preferences.d/cuda-repository-pin-600 \
  && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/${OS}/x86_64/3bf863cc.pub \
  && add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/${OS}/x86_64/ /" \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/12.1.1/ubuntu2204/devel/cudnn8/Dockerfile
ENV NV_CUDNN_VERSION 8.9.0.131
ENV NV_CUDNN_PACKAGE_NAME "libcudnn8"
ENV NV_CUDNN_PACKAGE "libcudnn8=$NV_CUDNN_VERSION-1+cuda12.1"
ENV NV_CUDNN_PACKAGE_DEV "libcudnn8-dev=$NV_CUDNN_VERSION-1+cuda12.1"

RUN apt-get update && apt-get install -y --no-install-recommends \
  ${NV_CUDNN_PACKAGE} \
  ${NV_CUDNN_PACKAGE_DEV} \
  && apt-mark hold ${NV_CUDNN_PACKAGE_NAME} \
  && rm -rf /var/lib/apt/lists/*

# https://github.com/devcontainers/images/tree/main/src/python#optional-allowing-the-non-root-vscode-user-to-pip-install-globally-without-sudo
ENV PYTHON_VERSION 3.10
RUN apt-get update && apt-get install --no-install-recommends -yq software-properties-common \
  && add-apt-repository ppa:deadsnakes/ppa && apt-get update \
  && apt-get install -yq --no-install-recommends python3 python3-pip python${PYTHON_VERSION} \
  && update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_VERSION} 1 \
  && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 1 \
  && pip3 install --no-cache-dir --upgrade pip setuptools wheel \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
