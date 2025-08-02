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