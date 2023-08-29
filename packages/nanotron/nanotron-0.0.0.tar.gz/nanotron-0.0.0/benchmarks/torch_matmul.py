import torch
import time
from torch.autograd import profiler

# Define the sizes of matrices for benchmarking
matrix_sizes = [2**15]

# Number of warm-up and benchmark runs for averaging
num_warmup_runs = 1
num_benchmark_runs = 3

# Initialize the GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Perform matrix multiplication and measure time
def benchmark_matmul(matrix_size, num_runs):
    global num_warmup_runs
    torch.cuda.empty_cache()  # Clear GPU cache before each run
    total_time = 0
    for _ in range(num_warmup_runs + num_runs):
        a = torch.rand(matrix_size, matrix_size, device=device)
        b = torch.rand(matrix_size, matrix_size, device=device)

        with profiler.profile(record_shapes=True, use_cuda=True) as prof:
            start_time = time.time()
            c = torch.matmul(a, b)
            torch.cuda.synchronize()  # Wait for the computation to finish
            end_time = time.time()

        if num_warmup_runs > 0:
            num_warmup_runs -= 1
        else:
            total_time += end_time - start_time
    
    return total_time / num_runs, prof

# Calculate TFLOPs for a given matrix size and execution time
def calculate_tflops(matrix_size, execution_time):
    flops = 2 * matrix_size ** 3  # Matmul has 2N^3 floating point operations
    tflops = flops / (execution_time * 1e12)  # Convert time to seconds and TFLOPs to tera scale
    return tflops

# Print summary table with profiling information
def print_summary_table(matrix_sizes, execution_times, tflops_list, profiling_results):
    print("Matrix Size\tAverage Time (s)\tTFLOPs\t\tProfiler Stats")
    print("-" * 80)
    for i, size in enumerate(matrix_sizes):
        average_execution_time = execution_times[i]
        tflops = tflops_list[i]
        prof = profiling_results[i]
        print(f"{size}\t\t{average_execution_time:.6f} s\t\t{tflops:.6f} TFLOPs\t{prof}")

# Benchmark matmul for different matrix sizes
execution_times = []
tflops_list = []
profiling_results = []

for size in matrix_sizes:
    average_execution_time, prof = benchmark_matmul(size, num_benchmark_runs)
    execution_times.append(average_execution_time)
    
    tflops = calculate_tflops(size, average_execution_time)
    tflops_list.append(tflops)
    
    profiling_results.append(prof)

print_summary_table(matrix_sizes, execution_times, tflops_list, profiling_results)
