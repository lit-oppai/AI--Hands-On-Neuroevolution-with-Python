#!/bin/bash

# JetBrains 远程开发快速启动脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$SCRIPT_DIR"

echo "🚀 Starting Neuroevolution Development Environment for JetBrains IDEs..."

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# 停止现有容器
echo "🛑 Stopping existing container..."
docker-compose down --remove-orphans

# 构建并启动容器
echo "🏗️  Building and starting container..."
docker-compose up -d --build

echo "⏳ Waiting for container to initialize..."
sleep 15

# 检查容器状态
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Container failed to start. Check logs with: docker-compose logs"
    exit 1
fi

# 验证容器内环境
echo "🔍 Verifying container environment..."
docker-compose exec neuroevolution-dev python3.5 --version
docker-compose exec neuroevolution-dev python3.5 -c "import numpy; print('numpy:', numpy.__version__)" 2>/dev/null || echo "⚠️  numpy verification failed"

echo ""
echo "✅ Development environment is ready!"
echo ""
echo "🔗 JetBrains IDE Configuration:"
echo "  ┌─────────────────────────────────────────────────────────────┐"
echo "  │  SSH Configuration:                                        │"
echo "  │  Host: localhost                                           │"
echo "  │  Port: 2222                                                │"
echo "  │  Username: developer                                       │"
echo "  │  Password: developer                                       │"
echo "  │                                                             │"
echo "  │  Python Interpreter:                                       │"
echo "  │  Path: /usr/local/bin/python3.5                            │"
echo "  │                                                             │"
echo "  │  Project Path:                                             │"
echo "  │  Remote: /workspace                                        │"
echo "  │  Local: $PROJECT_DIR                                     │"
echo "  └─────────────────────────────────────────────────────────────┘"
echo ""
echo "🌐 Services:"
echo "  • Jupyter Notebook: http://localhost:8888"
echo "  • SSH: ssh developer@localhost -p 2222"
echo ""
echo "📋 Next Steps:"
echo "  1. Open your JetBrains IDE (PyCharm/IntelliJ IDEA)"
echo "  2. Configure SSH remote interpreter using the settings above"
echo "  3. Map project paths correctly"
echo "  4. Start coding!"
echo ""
echo "💡 Useful Commands:"
echo "  • View logs: docker-compose logs -f"
echo "  • Stop container: docker-compose down"
echo "  • SSH into container: ssh developer@localhost -p 2222"
echo "  • Restart container: docker-compose restart"
echo ""

# 可选：自动打开浏览器
if command -v xdg-open > /dev/null; then
    echo "🌐 Opening Jupyter in browser..."
    sleep 2
    xdg-open http://localhost:8888
elif command -v open > /dev/null; then
    echo "🌐 Opening Jupyter in browser..."
    sleep 2
    open http://localhost:8888
fi