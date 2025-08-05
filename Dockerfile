# 优化的 Neuroevolution 开发环境 Dockerfile
# 基于 Python 3.5.10，支持神经进化算法开发

FROM ubuntu:18.04

# 元数据
LABEL maintainer="zhanghengxin" \
      description="Neuroevolution development environment with Python 3.5.10" \
      version="1.0"

# 环境变量
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PATH=/usr/local/bin:$PATH

# 清理 apt 缓存，减少镜像大小
RUN rm -rf /var/lib/apt/lists/*

# 安装系统构建依赖（合并 RUN 指令减少层数）
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
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# 创建构建目录
WORKDIR /usr/src

# 下载并构建 Python 3.5.10（使用多阶段构建优化）
RUN wget --no-check-certificate https://www.python.org/ftp/python/3.5.10/Python-3.5.10.tgz \
    && tar xzf Python-3.5.10.tgz \
    && cd Python-3.5.10 \
    && ./configure --enable-optimizations --with-ensurepip=install \
    && make -j$(nproc) \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.5.10 Python-3.5.10.tgz

# 升级 pip 并安装基础包
RUN python3.5 -m ensurepip \
    && python3.5 -m pip install --no-cache-dir --upgrade "pip==20.3.4" setuptools wheel

# 创建应用用户（安全最佳实践）
RUN groupadd -r developer && useradd -r -g developer developer \
    && mkdir -p /app \
    && chown -R developer:developer /app

# 切换到应用用户
USER developer

# 设置工作目录
WORKDIR /app

# 复制依赖文件（利用 Docker 缓存）
COPY --chown=developer:developer requirements.txt .

# 安装 Python 依赖（使用 --no-cache-dir 减少镜像大小）
RUN python3.5 -m pip install --no-cache-dir -r requirements.txt

# 创建符号链接方便使用
RUN ln -sf /usr/local/bin/python3.5 /usr/local/bin/python3

# 复制应用代码（最后复制，最大化缓存利用）
COPY --chown=developer:developer . .

# 验证安装
RUN python3.5 --version \
    && python3.5 -c "import numpy; print(f'numpy: {numpy.__version__}')" \
    && python3.5 -c "import matplotlib; print(f'matplotlib: {matplotlib.__version__}')" \
    && python3.5 -c "import neat; print(f'neat-python: {neat.__version__}')"

# 暴露端口（用于开发服务器）
EXPOSE 8888 6006

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python3.5 --version || exit 1

# 默认命令
CMD ["python3.5"]