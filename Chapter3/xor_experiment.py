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

def print_genome_summary(genome, genome_id):
    """打印基因组摘要信息"""
    print("--- Evaluating genome {} ---".format(genome_id))
    print("Initial fitness: {:.6f}".format(genome.fitness or 0.0))
    
def print_network_info(genome):
    """打印神经网络信息"""
    print("Neural network created - nodes: {}, connections: {}".format(
        len(genome.nodes), len(genome.connections)))

def print_xor_test_results(net, prefix="  "):
    """打印XOR测试结果"""
    total_error = 0.0
    print("Testing XOR cases:")
    
    for i, (xi, xo) in enumerate(zip(xor_inputs, xor_outputs)):
        output = net.activate(xi)
        error = abs(output[0] - xo[0])
        total_error += error
        print("{}Case {}: ({:.1f}, {:.1f}) -> Expected: {:.1f}, Actual: {:.6f}, Error: {:.6f}".format(
            prefix, i+1, xi[0], xi[1], xo[0], output[0], error))
    
    return total_error

def print_performance_analysis(fitness):
    """打印性能分析"""
    print("--- Genome test complete ---")
    print("Final fitness: {:.6f}".format(fitness))
    print("Fitness improvement: {:.6f}".format(fitness - 4.0))
    
    # 评估性能等级
    if fitness >= 15.0:
        print("Performance level: Excellent")
    elif fitness >= 10.0:
        print("Performance level: Good")
    elif fitness >= 5.0:
        print("Performance level: Average")
    else:
        print("Performance level: Poor")

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
    print("Evaluating {} genomes in current generation...".format(len(genomes)))
    
    for genome_id, genome in genomes:
        print_genome_summary(genome, genome_id)
        
        # 创建神经网络
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        print_network_info(genome)
        
        # 详细测试每个 XOR 测试用例
        total_error = print_xor_test_results(net)
        
        # 计算最终适应度
        fitness = (4 - total_error) ** 2
        genome.fitness = fitness
        
        print_performance_analysis(fitness)
        print("-" * 50)
    
    print("Current generation {} genomes evaluation complete!\n".format(len(genomes)))

def print_experiment_header():
    """打印实验头部信息"""
    print("=" * 60)
    try:
        print("Starting XOR Neural Evolution Experiment".encode('utf-8').decode('ascii', 'ignore'))
    except:
        print("Starting XOR Neural Evolution Experiment")
    print("=" * 60)

def print_config_info(config_file):
    """打印配置信息并返回配置对象"""
    print("Loading configuration file...")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    print("Configuration file loaded: {}".format(config_file))
    print("   - Population size: {}".format(config.pop_size))
    print("   - Fitness threshold: {}".format(config.fitness_threshold))
    print("   - Max generations: 300")
    return config

def print_setup_info(population, config):
    """打印设置信息并返回统计对象"""
    print("Creating initial population...")
    print("Population created with {} genomes".format(config.pop_size))

    print("Setting up experiment monitoring...")
    stats = neat.StatisticsReporter()
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(stats)
    # Disable checkpointing to avoid permission issues
    # population.add_reporter(neat.Checkpointer(5, filename_prefix='out/neat-checkpoint-'))
    print("Monitoring system setup complete")
    return stats

def print_final_header():
    """打印最终结果头部"""
    print("=" * 60)
    print("Evolution process complete!")
    print("=" * 60)

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
    print_experiment_header()
    
    # Load configuration.
    config = print_config_info(config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)
    stats = print_setup_info(p, config)

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
    
    print_final_header()
    
    # Display the best genome among generations.
    print_final_results(best_genome, config, stats, out_dir)

def print_final_results(best_genome, config, stats, out_dir):
    """打印最终结果并生成可视化"""
    # Display the best genome among generations.
    print("\nFinal Results - Best Genome Details:")
    print("=" * 60)
    print('Genome ID: {}'.format(best_genome.key))
    print('Node count: {}'.format(len(best_genome.nodes)))
    print('Connection count: {}'.format(len(best_genome.connections)))
    print('Fitness: {:.6f}'.format(best_genome.fitness))
    print('\nGenome Structure Details:\n')
    print('{}'.format(best_genome))
    print("=" * 60)

    # Show output of the most fit genome against training data.
    print("\nFinal Test - Best Genome XOR Problem Solving Test:")
    print("=" * 60)
    net = neat.nn.FeedForwardNetwork.create(best_genome, config)
    
    total_error = 0.0
    print("XOR Truth Table Test Results:")
    for i, (xi, xo) in enumerate(zip(xor_inputs, xor_outputs)):
        output = net.activate(xi)
        error = abs(output[0] - xo[0])
        total_error += error
        
        print("  {}. ({:.1f}, {:.1f}) -> Expected: {:.1f}, Actual: {:.6f}, Error: {:.6f}".format(
            i+1, xi[0], xi[1], xo[0], output[0], error))
    
    print("\nPerformance Statistics:")
    print("   Total error: {:.6f}".format(total_error))
    print("   Average error: {:.6f}".format(total_error/4))
    
    best_genome_fitness = eval_fitness(net)
    print("   Final fitness: {:.6f}".format(best_genome_fitness))
    
    # Check if the best genome is an adequate XOR solver
    print("\nTarget fitness threshold: {}".format(config.fitness_threshold))
    
    if best_genome_fitness > config.fitness_threshold:
        print("\n" + "=" * 50)
        print("SUCCESS: Found XOR Problem Solver!")
        print("SUCCESS: Found XOR Problem Solver!")
        print("SUCCESS: Found XOR Problem Solver!")
        print("=" * 50)
        print("\nCongratulations! Final fitness ({:.6f}) successfully exceeded threshold ({})".format(
            best_genome_fitness, config.fitness_threshold))
        print("This neural network can now correctly solve the XOR problem!")
    else:
        print("\n" + "=" * 50)
        print("FAILURE: Could not find adequate XOR problem solver!")
        print("FAILURE: Could not find adequate XOR problem solver!")
        print("FAILURE: Could not find adequate XOR problem solver!")
        print("=" * 50)
        print("\nSorry! Final fitness ({:.6f}) is below threshold ({})".format(
            best_genome_fitness, config.fitness_threshold))
        print("Suggestion: Continue evolution or adjust algorithm parameters for better results")

    # Visualize the experiment results
    print("\nGenerating experiment visualization results...")
    node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
    
    # Draw neural network structure diagram
    print("Drawing neural network structure diagram...")
    visualize.draw_net(config, best_genome, True, node_names=node_names, directory=out_dir)
    print("Neural network structure diagram saved to: {}/network-{}.svg".format(out_dir, best_genome.key))
    
    # Draw fitness statistics chart
    print("Drawing fitness statistics chart...")
    visualize.plot_stats(stats, ylog=False, view=True, filename=os.path.join(out_dir, 'avg_fitness.svg'))
    print("Fitness statistics chart saved to: {}/avg_fitness.svg".format(out_dir))
    
    # Draw species evolution chart
    print("Drawing species evolution chart...")
    visualize.plot_species(stats, view=True, filename=os.path.join(out_dir, 'speciation.svg'))
    print("Species evolution chart saved to: {}/speciation.svg".format(out_dir))
    
    print("\nAll visualization results generated successfully!")
    print("Output directory: " + out_dir)
    
    print("\nExperiment Summary:")
    print("=" * 50)
    print("Best genome fitness: {:.6f}".format(best_genome.fitness))
    print("Genome nodes: {}".format(len(best_genome.nodes)))
    print("Genome connections: {}".format(len(best_genome.connections)))
    print("Evolution generations: {}".format(len(stats.most_fit_genomes)))
    print("Final result: {}".format("SUCCESS" if best_genome_fitness > config.fitness_threshold else "NOT MET"))
    print("=" * 50)

def clean_output():
    if os.path.isdir(out_dir):
        # remove files from previous run
        import subprocess
        try:
            subprocess.run(['rm', '-rf', os.path.join(out_dir, '*')], check=False)
        except:
            pass
    
    # create the output directory if it doesn't exist
    os.makedirs(out_dir, exist_ok=True)


if __name__ == '__main__':
    print("XOR Neural Evolution Experiment Program")
    print("=" * 80)
    
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    config_path = os.path.join(local_dir, 'xor_config.ini')
    print("Configuration file path: {}".format(config_path))
    print("Current working directory: {}".format(local_dir))
    print("Output directory: {}".format(out_dir))

    # Clean results of previous run if any or init the ouput directory
    print("\nCleaning previous experiment results...")
    clean_output()
    print("Output directory initialization complete")

    # Run the experiment
    print("\nStarting neural evolution experiment...")
    run_experiment(config_path)
    
    print("\n" + "=" * 80)
    print("Experiment execution complete! Thank you for using XOR Neural Evolution Experiment Program!")
    print("=" * 80)