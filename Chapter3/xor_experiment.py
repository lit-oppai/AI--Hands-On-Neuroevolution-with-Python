#
# This file provides source code of XOR experiment using on NEAT-Python library
#

# The Python standard library import
import os
import shutil
# The NEAT-Python library imports
import neat
# The helper used to visualize experiment results
import visualize

# The current working directory
local_dir = os.path.dirname(__file__)
# The directory to store outputs
out_dir = os.path.join(local_dir, 'out')

# The XOR inputs and expected corresponding outputs for fitness evaluation
xor_inputs  = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
xor_outputs = [   (0.0,),     (1.0,),     (1.0,),     (0.0,)]

def eval_fitness(net):
    """
    Evaluates fitness of the genome that was used to generate 
    provided net
    评估 被用来提供生成网络基因的拟合度
    评估 给定网络生成的基因组的适应度
    Arguments:
        net: The feed-forward neural network generated from genome
        由基因组生成的 正反馈（前馈）进化网络
    Returns:
        The fitness score - the higher score the means the better 
        fit organism. Maximal score: 16.0
        拟合度分数 越高意味着更适合的个体，最大分数为16
    """
    error_sum = 0.0
    for xi, xo in zip(xor_inputs, xor_outputs):
        output = net.activate(xi)
        error_sum += abs(output[0] - xo[0])
    # Calculate amplified fitness
    # 计算放大拟合度
    fitness = (4 - error_sum) ** 2
    return fitness

def eval_genomes(genomes, config):
    """
    The function to evaluate the fitness of each genome in 
    the genomes list.
    评价基因组列表中每个基因组的拟合度
    The provided configuration is used to create feed-forward 
    neural network from each genome and after that created
    the neural network evaluated in its ability to solve
    XOR problem. As a result of this function execution,
    the fitness score of each genome updated to the newly
    evaluated one.
    提供的配置用来创建每个基因组的正向反馈网络，并且随后，创建评价他解决xor问题能力的进化网络。
    作为这个函数的执行结果，每个基因组适应度分数更新至最新的那个。
    每个基因组的拟合度评分，更新到最新的那个值
    Arguments:
        genomes: The list of genomes from population in the 
                current generation
                当前代种群中的基因组 list
        config: The configuration settings with algorithm
                hyper-parameters
                带有 算法超参 的配置
    """
    for genome_id, genome in genomes:
        genome.fitness = 4.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = eval_fitness(net)

def run_experiment(config_file):
    """
    The function to run XOR experiment against hyper-parameters 
    defined in the provided configuration file.
    针对配置文件中的超参数。 运行 XOR 实验
    The winner genome will be rendered as a graph as well as the
    important statistics of neuroevolution process execution.
    获胜的基因组将会被渲染成一个图谱，同时也很重要的神经进化执行过程的统计数据
    Arguments:
        config_file: the path to the file with experiment 
                    configuration
    """
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    # 添加  标准输出 报告器 用于 在控制台上显示 进度
    p.add_reporter(neat.StdOutReporter(True))
    # 统计 统计信息 收集器
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # 添加 检查点 收集器
    p.add_reporter(neat.Checkpointer(5, filename_prefix='out/neat-checkpoint-'))

    # Run for up to 300 generations.
    best_genome = p.run(eval_genomes, 300)

    # Display the best genome among generations.
    print('\nBest genome:\n{!s}'.format(best_genome))

    # Show output of the most fit genome against training data.
    # 针对训练数据，显示 适应度最强的基因组
    print('\nOutput:')
    net = neat.nn.FeedForwardNetwork.create(best_genome, config)
    for xi, xo in zip(xor_inputs, xor_outputs):
        output = net.activate(xi)
        print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    # Check if the best genome is an adequate XOR solver
    # 确认 如果最优基因组是一个 "足够的" XOR 求解器
    best_genome_fitness = eval_fitness(net)
    if best_genome_fitness > config.fitness_threshold:
        print("\n\nSUCCESS: The XOR problem solver found!!!")
    else:
        print("\n\nFAILURE: Failed to find XOR problem solver!!!")

    # Visualize the experiment results
    node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
    visualize.draw_net(config, best_genome, True, node_names=node_names, directory=out_dir)
    visualize.plot_stats(stats, ylog=False, view=True, filename=os.path.join(out_dir, 'avg_fitness.svg'))
    visualize.plot_species(stats, view=True, filename=os.path.join(out_dir, 'speciation.svg'))

def clean_output():
    if os.path.isdir(out_dir):
        # remove files from previous run
        import subprocess
        try:
            subprocess.run(['rm', '-rf', out_dir], check=False)
        except:
            pass
    
    # create the output directory
    os.makedirs(out_dir, exist_ok=True)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    config_path = os.path.join(local_dir, 'xor_config.ini')

    # Clean results of previous run if any or init the ouput directory
    clean_output()

    # Run the experiment
    run_experiment(config_path)