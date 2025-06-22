#FROM continuumio/miniconda3
#LABEL authors="zhanghengxin"
#
#WORKDIR /app
#
#RUN  conda create -n py35  python=3.5 -y
##    && conda activate py35 \
##    && pip install --upgrade pip \
##    && pip install -r requirements.txt
#
#RUN /bin/bash -c "source activate py35 && \
#    pip install neat-python==0.92 matplotlib=3.0.3"
#
#COPY . /app
#
#CMD ["/bin/bash"]
##ENTRYPOINT ["top", "-b"]



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
    graphviz

# 构建 Python 3.5.10
WORKDIR /usr/src
RUN wget https://www.python.org/ftp/python/3.5.10/Python-3.5.10.tgz && \
    tar xzf Python-3.5.10.tgz && \
    cd Python-3.5.10 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall

# 确保使用 pip，升级到兼容版本
RUN /usr/local/bin/python3.5 -m ensurepip && \
    /usr/local/bin/python3.5 -m pip install --upgrade "pip==20.3.4" setuptools wheel

## 安装 numpy **单独提前装**
#RUN /usr/local/bin/python3.5 -m pip install "numpy==1.17.0"
#
## 再装 matplotlib
#RUN /usr/local/bin/python3.5 -m pip install matplotlib==3.0.3 graphviz==0.8.4
#
## 安装 neat-python
#RUN /usr/local/bin/python3.5 -m pip install "neat-python==0.92"

COPY requirements.txt .

RUN /usr/local/bin/python3.5 -m pip install -r requirements.txt

RUN ln -s /usr/local/bin/python3.5 /usr/local/bin/python3

# 项目代码目录
WORKDIR /app
COPY . /app

# 启动交互
CMD ["/usr/local/bin/python3.5"]