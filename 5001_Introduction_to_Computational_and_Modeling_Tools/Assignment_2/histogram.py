import threading
import time
import numpy as np

lock = threading.Lock()

def worker(thread_id, data, results, low, high, n_bins, n_threads):
    """
    Worker function for each thread.
    Each thread should work on a chunk of data and modify the results array in-place
    """
    # 计算数据分块
    n = len(data)
    chunk_size = n // n_threads
    start = thread_id * chunk_size
    end = start + chunk_size if thread_id != n_threads - 1 else n

    # 计算 bin 宽度
    bin_width = (high - low) / n_bins

    # 线程局部计数器，减少锁争用
    local_counts = [0] * n_bins

    # 处理自己的数据段
    for i in range(start, end):
        x = data[i]
        if x < low or x >= high:
            continue  # 超出范围，跳过
        bin_index = min(int((x - low) / bin_width), n_bins - 1)
        local_counts[bin_index] += 1

    # 合并局部计数到全局结果
    with lock:
        for j in range(n_bins):
            results[j] += local_counts[j]

def serial_histogram(data, low, high, n_bins):
    """
    A serial function to compute histogram

    Args:
        data: an array of numbers from which the histogram is built
        low: the lower range of the bins
        high: the upper range of the bins
        n_bins: number of bins used

    Returns:
        An array that contains counts of elements in each bin
    """

    results = [0] * n_bins
    bin_width = (high - low) / n_bins

    for x in data:
        if x < low or x >= high:
            continue
        bin_index = min(int((x - low) / bin_width), n_bins - 1)
        results[bin_index] += 1

    return results

def parallel_histogram(data, low, high, n_bins, n_threads):
    """
    Compute histogram using multiple threads.
    
    Args:
        data: an array of numbers from which the histogram is built
        low: the lower range of the bins
        high: the upper range of the bins
        n_bins: number of bins used
        n_threads: number of threads to use
    
    Returns:
        An array that contains counts of elements in each bin
    """
    # YOU ARE FREE TO CHANGE THE IMPLEMENTATION IF YOU WISH

    results = [0] * n_bins

    threads = []

    for i in range(n_threads):
        t = threading.Thread(target=worker, args=(i, data, results, low, high, n_bins, n_threads))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return results


def main():
    """
    Measure the speed-up of parallel vs serial histogram functions
    """
    import sys
    print("GIL enabled:", sys._is_gil_enabled())
    test_data = np.random.rand(100000)
    n_threads = 8
    low = 0.0
    high = 1.0
    n_bins = 50

    start = time.time()
    serial_hist = serial_histogram(test_data, low, high, n_bins)
    elapsed_serial = time.time() - start

    start = time.time()
    parallel_hist = parallel_histogram(test_data, low, high, n_bins, n_threads)
    elapsed_parallel = time.time() - start

    print(f"Serial time: {elapsed_serial:.4f}s")
    print(f"Parallel time: {elapsed_parallel:.4f}s")
    print(f"Speed up: {elapsed_serial / elapsed_parallel:.2f}x")

if __name__ == "__main__":
    main()
