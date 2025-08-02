FROM ubuntu:18.04

# 安装系统构建依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    git \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    libsqlite3-dev \
    libbz2-dev \
    libpng-dev \
    libfreetype6-dev \
    pkg-config \
    graphviz \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# 构建 Python 3.5.10
WORKDIR /usr/src
RUN wget https://www.python.org/ftp/python/3.5.10/Python-3.5.10.tgz && \
    tar xzf Python-3.5.10.tgz && \
    cd Python-3.5.10 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall && \
    cd / && \
    rm -rf /usr/src/Python-3.5.10

# 确保使用 pip，升级到兼容版本
RUN /usr/local/bin/python3.5 -m ensurepip && \
    /usr/local/bin/python3.5 -m pip install --upgrade "pip==20.3.4" setuptools wheel

# 创建开发用户
RUN useradd -m -s /bin/bash developer && \
    echo "developer ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# 设置工作目录
WORKDIR /workspace
COPY requirements.txt .

# 切换到开发用户安装 Python 包
USER developer
RUN /usr/local/bin/python3.5 -m pip install -r requirements.txt

# 创建符号链接
USER root
RUN ln -s /usr/local/bin/python3.5 /usr/local/bin/python3

# 切换回开发用户
USER developer

# 设置环境变量
ENV PATH="/usr/local/bin:${PATH}"
ENV PYTHONPATH="/workspace:${PYTHONPATH}"

# 暴露端口（如果需要）
EXPOSE 8888

# 默认命令
CMD ["/bin/bash"]