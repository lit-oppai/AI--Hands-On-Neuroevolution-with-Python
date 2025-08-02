  🎯 远程开发解决方案

  📁 创建的文件结构：

  remote-dev/
  ├── Dockerfile              # 专用远程开发 Docker 镜像
  ├── docker-compose.yml      # Docker Compose 配置
  ├── startup.sh             # 容器启动脚本
  ├── ssh_config             # SSH 配置模板
  ├── jetbrains-guide.md     # JetBrains IDE 详细指南
  └── start-jetbrains.sh     # 一键启动脚本

  🚀 在 JetBrains IDE 中使用的步骤：

  1. 快速启动

  cd /path/to/project/remote-dev
  ./start-jetbrains.sh

  2. PyCharm Professional 配置

  1. File → Settings → Project → Python Interpreter
  2. 点击 ⚙️ → Add → SSH Interpreter
  3. 配置连接：
    - Host: localhost
    - Port: 2222
    - Username: developer
    - Password: developer
  4. 解释器路径：/usr/local/bin/python3.5
  5. 项目路径映射：
    - Local: 你的本地项目路径
    - Remote: /workspace

  3. IntelliJ IDEA 配置

  - 类似 PyCharm，但需要添加 Python 插件
  - 配置远程 SDK 和解释器

  4. CLion 配置（用于 C++ 扩展）

  - 配置远程工具链
  - 设置 CMake 远程构建

  ✨ 远程开发环境特性：

  🔧 完整的环境配置

  - Python 3.5.10 从源码构建
  - 所有项目依赖预安装
  - TensorFlow 扩展自动构建
  - SSH 服务器配置
  - Jupyter Notebook 预配置

  🌐 服务端口

  - SSH: localhost:2222
  - Jupyter: localhost:8888
  - TensorBoard: localhost:6006

  📁 文件系统

  - 项目代码通过 Docker volume 挂载到 /workspace
  - 实时文件同步
  - 完整的开发工具集（vim, tmux, htop）

  🔐 用户账户

  - 开发用户：developer
  - 密码：developer
  - sudo 权限无密码

  💡 使用优势：

  1. 环境隔离：不影响本地系统
  2. 版本一致性：确保 Python 3.5.10 环境
  3. IDE 集成：完整的 JetBrains IDE 支持
  4. 性能优化：容器化环境，启动快速
  5. 跨平台：在任何支持 Docker 的系统上运行
