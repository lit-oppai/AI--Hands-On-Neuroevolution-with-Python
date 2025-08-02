# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains the code for "Hands-On Neuroevolution with Python" book. It implements various neuroevolution algorithms including NEAT, HyperNEAT, and ES-HyperNEAT for solving reinforcement learning problems like maze navigation, cart-pole balancing, and Atari games.

## Development Environment

### Python Version
- The project uses Python 3.5.10 (see Dockerfile for setup)
- Dependencies are specified in `requirements.txt`

### Key Dependencies
- `matplotlib==3.0.3` - for visualization
- `graphviz==0.8.4` - for neural network visualization
- `neat-python==0.92` - NEAT algorithm implementation
- `numpy==1.17.0` - numerical computations

### DevContainer Environment (Recommended)
The project includes a complete DevContainer configuration for VS Code or GitHub Codespaces. This is the recommended way to develop on systems that don't natively support Python 3.5.10.

**Using VS Code:**
1. Install the Dev Containers extension
2. Open the project folder
3. Press F1 and select "Dev Containers: Reopen in Container"
4. The container will automatically build with Python 3.5.10 and all dependencies

**Using GitHub Codespaces:**
1. Click "Code" → "Codespaces" → "New codespace"
2. The environment will be automatically configured

The DevContainer will:
- Build Python 3.5.10 from source
- Install all project dependencies
- Build TensorFlow extensions for Chapter10
- Set up VS Code with Python extensions
- Configure the development environment

### Remote Development Environment
For JetBrains IDEs (PyCharm, IntelliJ IDEA, CLion) and other remote development scenarios:

**Quick Start with Docker Compose:**
```bash
cd remote-dev
./start-jetbrains.sh
```

**Manual Setup:**
```bash
cd remote-dev
docker-compose up -d
```

**JetBrains IDE Configuration:**
- SSH Host: localhost
- Port: 2222
- Username: developer
- Password: developer
- Python Interpreter: /usr/local/bin/python3.5
- Project Path: /workspace

See `remote-dev/jetbrains-guide.md` for detailed IDE-specific instructions.

### Docker Environment
The project includes a Dockerfile that sets up a complete environment with Python 3.5.10 and all dependencies. To build and run:

```bash
docker build -t neuroevolution-python .
docker run -it neuroevolution-python
```

## Project Structure

The code is organized by chapters, each containing different neuroevolution experiments:

- **Chapter3**: Basic NEAT algorithm with XOR problem
- **Chapter4**: Cart-pole balancing experiments
- **Chapter5**: Maze navigation with geometric primitives
- **Chapter6**: Novelty search and multi-objective optimization
- **Chapter7**: Vehicle driver with MultiNEAT
- **Chapter8**: Retina processing and visual systems
- **Chapter9**: Safe exploration in maze navigation
- **Chapter10**: Advanced deep neuroevolution with TensorFlow

### Key Components

#### Chapter10 - Advanced Architecture
- `neuroevolution/`: Core neuroevolution framework
  - `models/`: Neural network architectures (DQN, batch normalization, etc.)
  - `helper.py`: Shared noise table and scheduling utilities
  - `optimizers.py`: Evolution strategies implementations
- `gym_tensorflow/`: TensorFlow integration with OpenAI Gym
  - `atari/`: Atari game environments
  - `maze/`: Maze environments
  - `ops/`: Custom TensorFlow operations
- `configurations/`: JSON configuration files for different experiments

## Running Experiments

### Basic NEAT Experiment (Chapter3)
```bash
cd Chapter3
python xor_experiment.py
```

### Chapter10 Deep Neuroevolution
```bash
cd Chapter10
# Build TensorFlow extensions first
cd gym_tensorflow
make
cd ..
# Run evolution strategies
python es.py --config configurations/es_atari_config.json
```

### Configuration Files
- Chapter3-6 use `.ini` files for NEAT configuration
- Chapter10 uses `.json` files for experiment configuration

## Architecture Overview

### Neuroevolution Framework (Chapter10)
The advanced framework in Chapter10 implements:
- **BaseModel**: Abstract base class for neural network models
- **SharedNoiseTable**: Efficient noise generation for evolution strategies
- **Scheduling**: Linear and exponential scheduling for hyperparameters
- **TensorFlow Integration**: Custom ops for indexed matrix operations

### Environment Integration
- **Maze Environments**: Grid-based navigation problems
- **Atari Integration**: Classic arcade games via ALE
- **Custom TensorFlow Ops**: Performance-critical operations in C++

## Development Notes

### Building TensorFlow Extensions
The Chapter10 code requires building custom TensorFlow operations:
```bash
cd Chapter10/gym_tensorflow
make
```

### Common Patterns
- Each chapter has a consistent structure: experiment file, environment, agent, and utilities
- Visualization components are provided for most experiments
- Configuration-driven approach allows easy parameter tuning

### Testing
The project doesn't include formal test suites. Experiments serve as validation:
- Run individual chapter experiments to verify functionality
- Check output directories for generated visualizations and results