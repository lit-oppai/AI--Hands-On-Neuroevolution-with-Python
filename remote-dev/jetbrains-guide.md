# JetBrains IDE 远程开发配置指南

## PyCharm Professional 远程开发

### 1. 启动 Docker 容器
```bash
cd /path/to/your/project/remote-dev
docker-compose up -d
```

### 2. 配置 PyCharm SSH 远程解释器

#### 方法一：使用 Docker 作为远程主机
1. 打开 PyCharm Professional
2. File → Settings → Project: neuroevolution → Python Interpreter
3. 点击 ⚙️ → Add...
4. 选择 "SSH Interpreter"
5. 配置 SSH 连接：
   - Host: localhost
   - Port: 2222
   - User name: developer
   - Password: developer
6. 点击 "Next" 
7. 选择解释器路径：`/usr/local/bin/python3.5`
8. 映射项目路径：
   - Local path: 你的本地项目路径
   - Remote path: /workspace
9. 点击 "Finish"

#### 方法二：使用 Docker Compose
1. File → Settings → Build, Execution, Deployment → Docker
2. 点击 + 添加 Docker 连接
3. 选择 Docker Compose
4. 设置：
   - Docker Compose service: neuroevolution-dev
   - Configuration files: 选择你的 docker-compose.yml
5. 应用设置
6. 然后配置 Python 解释器为 Docker Compose 服务

### 3. 配置远程部署
1. File → Settings → Build, Execution, Deployment → Deployment
2. 点击 + 添加新的服务器
3. 选择 SFTP
4. 配置连接：
   - Name: Neuroevolution Dev
   - Host: localhost
   - Port: 2222
   - User name: developer
   - Password: developer
   - Root path: /workspace
5. 在 Mappings 选项卡中：
   - Local path: 项目本地路径
   - Deployment path: /workspace
   - Web path: /

### 4. 运行配置
1. Run → Edit Configurations
2. 点击 + 添加 Python 配置
3. 设置：
   - Script path: 选择你的 Python 文件（如 Chapter3/xor_experiment.py）
   - Python interpreter: 选择远程 SSH 解释器
   - Working directory: /workspace/Chapter3

## IntelliJ IDEA 远程开发

### 1. 配置远程 SDK
1. File → Project Structure → SDKs
2. 点击 + 添加 Python SDK
3. 选择 SSH 远程 SDK
4. 配置 SSH 连接信息（同上）

### 2. 远程调试
1. Run → Edit Configurations
2. 添加 Python Debug 配置
3. 选择远程解释器
4. 设置断点并开始调试

## CLion 远程开发（C++ 扩展）

### 1. 配置工具链
1. File → Settings → Build, Execution, Deployment → Toolchains
2. 点击 + 添加 Remote Host
3. 配置 SSH 连接到容器

### 2. 配置 CMake
1. File → Settings → Build, Execution, Deployment → CMake
2. 选择远程工具链
3. 配置构建目录为远程路径

## 快速启动脚本

创建一个启动脚本来简化容器管理：

```bash
#!/bin/bash
# start-dev.sh

cd "$(dirname "$0")/remote-dev"

echo "🚀 Starting Neuroevolution Development Environment..."
docker-compose up -d

echo "⏳ Waiting for container to start..."
sleep 10

echo "✅ Container is ready!"
echo ""
echo "🔗 Connection Info:"
echo "  SSH: ssh developer@localhost -p 2222"
echo "  Jupyter: http://localhost:8888"
echo ""
echo "📝 Configure your JetBrains IDE to use:"
echo "  Host: localhost"
echo "  Port: 2222"
echo "  User: developer"
echo "  Python: /usr/local/bin/python3.5"
```

## 常见问题

### 1. SSH 连接失败
- 确保 Docker 容器正在运行：`docker ps`
- 检查端口映射：`docker port neuroevolution-remote-dev`
- 确认 SSH 服务在容器中运行

### 2. Python 解释器不可用
- 检查 Python 安装：`ssh developer@localhost -p 2222 "python3.5 --version"`
- 重新构建容器：`docker-compose build --no-cache`

### 3. 文件同步问题
- 确保 Docker volumes 正确挂载
- 检查文件权限
- 使用 PyCharm 的自动同步功能

### 4. 性能优化
- 在 PyCharm 中启用 "Upload changed files automatically" 
- 使用 SSH 密钥认证替代密码
- 调整 PyCharm 的远程连接超时设置