#!/bin/bash

set -e

echo "🚀 Setting up Neuroevolution development environment..."

# 验证 Python 版本
echo "📋 Verifying Python installation..."
python3.5 --version

# 验证 pip 安装
echo "📋 Verifying pip installation..."
python3.5 -m pip --version

# 验证关键依赖包
echo "📋 Checking key dependencies..."
python3.5 -c "import numpy; print(f'numpy: {numpy.__version__}')"
python3.5 -c "import matplotlib; print(f'matplotlib: {matplotlib.__version__}')"
python3.5 -c "import neat; print(f'neat-python: {neat.__version__}')"

# 构建 Chapter10 的 TensorFlow 扩展
echo "🔧 Building TensorFlow extensions for Chapter10..."
if [ -d "Chapter10/gym_tensorflow" ]; then
    cd Chapter10/gym_tensorflow
    if [ -f "Makefile" ]; then
        echo "Building gym_tensorflow extensions..."
        make clean || true
        make
        echo "✅ TensorFlow extensions built successfully"
    else
        echo "⚠️  Makefile not found in Chapter10/gym_tensorflow"
    fi
    cd ../..
else
    echo "⚠️  Chapter10 directory not found"
fi

# 设置 Jupyter kernel (可选)
echo "📓 Setting up Jupyter kernel..."
python3.5 -m pip install ipykernel || true
python3.5 -m ipykernel install --user --name=python3.5 --display-name="Python 3.5.10" || true

echo "✅ Development environment setup complete!"
echo ""
echo "🎯 Quick start commands:"
echo "  - Run Chapter 3 XOR experiment: cd Chapter3 && python3.5 xor_experiment.py"
echo "  - Run Chapter 10 ES: cd Chapter10 && python3.5 es.py --config configurations/es_atari_config.json"
echo "  - Start Jupyter: jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser"