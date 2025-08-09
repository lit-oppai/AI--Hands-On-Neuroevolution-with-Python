构建和使用命令

  1. 构建所有版本的镜像

  # 原始版本
  docker build -t neuroevolution-python:original -f
  Dockerfile .

  # 优化版本
  docker build -t neuroevolution-python:optimized -f
  Dockerfile.new .

  # 快速版本（带缓存）
  docker build -t neuroevolution-python:fast -f
  Dockerfile.fast-cached .

  2. 使用缓存优化构建

  # 第一次构建（完整构建）
  docker build -t neuroevolution-python:fast -f
  Dockerfile.fast-cached .

  # 后续构建（使用缓存，速度更快）
  docker build -t neuroevolution-python:fast -f
  Dockerfile.fast-cached .

  3. 运行容器

  # 运行快速版本
  docker run -it --name neuro-fast
  neuroevolution-python:fast

  # 运行优化版本
  docker run -it --name neuro-optimized
  neuroevolution-python:optimized

  # 运行原始版本
  docker run -it --name neuro-original
  neuroevolution-python:original

  缓存优化策略

  Dockerfile.fast-cached版本的缓存优化：
  1. 基础层缓存：系统依赖和Python编译层很少变化
  2. 依赖层缓存：requirements.txt变化时才重建依赖层
  3. 代码层缓存：只有代码变化时才重建最后一层

# 配置 PyCharm 使用容器内 Python 3.5 解释器的步骤：

  1. 在 PyCharm 中配置 Docker 解释器：
    - File → Settings → Project: [项目名] → Python Interpreter
    - 点击齿轮图标 → Add
    - 选择 Docker Compose
    - 选择 docker-compose.yml 文件
    - 选择服务名称（通常是 app 或容器名）
    - PyCharm 会自动识别容器内的 Python 3.5
  2. 或者使用 SSH 解释器：
    - File → Settings → Project: [项目名] → Python Interpreter
    - 点击齿轮图标 → Add
    - 选择 SSH Interpreter
    - Host: localhost
    - Port: 2222（如果使用远程开发配置）
    - Username: developer
    - Password: developer
    - PyCharm 会自动发现 /usr/local/bin/python3.5
  3. 验证配置：
    - 在 PyCharm 终端运行 python --version
    - 应该显示 Python 3.5.10