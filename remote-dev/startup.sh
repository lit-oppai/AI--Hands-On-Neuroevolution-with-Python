#!/bin/bash

set -e

echo "🚀 Starting Neuroevolution Remote Development Environment..."

# 启动 SSH 服务
echo "🔧 Starting SSH service..."
sudo service ssh start

# 验证 Python 环境
echo "📋 Verifying Python installation..."
python3.5 --version
python3.5 -m pip --version

# 验证关键依赖
echo "📋 Checking dependencies..."
python3.5 -c "import numpy; print(f'numpy: {numpy.__version__}')" || echo "⚠️  numpy not found"
python3.5 -c "import matplotlib; print(f'matplotlib: {matplotlib.__version__}')" || echo "⚠️  matplotlib not found"
python3.5 -c "import neat; print(f'neat-python: {neat.__version__}')" || echo "⚠️  neat-python not found"

# 构建 TensorFlow 扩展
echo "🔧 Building TensorFlow extensions..."
if [ -d "/workspace/Chapter10/gym_tensorflow" ]; then
    cd /workspace/Chapter10/gym_tensorflow
    if [ -f "Makefile" ]; then
        echo "Building gym_tensorflow extensions..."
        make clean || true
        make
        echo "✅ TensorFlow extensions built successfully"
    else
        echo "⚠️  Makefile not found in Chapter10/gym_tensorflow"
    fi
    cd /workspace
else
    echo "⚠️  Chapter10 directory not found"
fi

# 设置 Jupyter
echo "📓 Setting up Jupyter..."
jupyter notebook --generate-config || true
echo "c.NotebookApp.ip = '0.0.0.0'" >> ~/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.port = 8888" >> ~/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.open_browser = False" >> ~/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.allow_root = True" >> ~/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.token = ''" >> ~/.jupyter/jupyter_notebook_config.py
echo "c.NotebookApp.password = ''" >> ~/.jupyter/jupyter_notebook_config.py

# 显示连接信息
echo ""
echo "✅ Remote development environment is ready!"
echo ""
echo "🔗 Connection Information:"
echo "  SSH: ssh developer@localhost -p 2222"
echo "  Password: developer"
echo "  Jupyter: http://localhost:8888"
echo "  TensorBoard: http://localhost:6006"
echo ""
echo "📁 Project mounted at: /workspace"
echo "🐍 Python: $(python3.5 --version)"
echo ""
echo "💡 Quick commands:"
echo "  - SSH into container: ssh developer@localhost -p 2222"
echo "  - Start Jupyter: jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser"
echo "  - Run Chapter 3: cd /workspace/Chapter3 && python3.5 xor_experiment.py"
echo ""

# 保持容器运行
tail -f /dev/null