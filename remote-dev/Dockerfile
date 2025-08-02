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
    openssh-server \
    sudo \
    htop \
    tmux \
    vim \
    && rm -rf /var/lib/apt/lists/*

# 配置 SSH
RUN mkdir /var/run/sshd
RUN echo 'root:neurodev' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

# 创建开发用户
RUN useradd -m -s /bin/bash developer && \
    echo "developer:developer" | chpasswd && \
    echo "developer ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# 创建 .ssh 目录
RUN mkdir -p /home/developer/.ssh && \
    chown -R developer:developer /home/developer/.ssh && \
    chmod 700 /home/developer/.ssh

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
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# 暴露端口
EXPOSE 2222 8888 6006

# 启动脚本
COPY remote-dev/startup.sh /startup.sh
RUN chmod +x /startup.sh

# 启动 SSH 和其他服务
CMD ["/startup.sh"]