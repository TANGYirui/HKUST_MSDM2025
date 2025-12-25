import threading
from concurrent.futures import ThreadPoolExecutor
import numpy as np # make sure you have install numpy version compatible with python 3.13t
import time

n_workers = 16
partial_sums = [None] * n_workers
final_answer = [0]

# prepare data
data = np.random.rand(n_workers * 1_000_000) # len(data) is divisible by n_workers for simplicity


def worker(thread_id):
    start = thread_id * len(data) // n_workers
    end = (thread_id + 1) * len(data) // n_workers
    partial_sums[thread_id] = np.sum(data[start:end])
    if thread_id == 0:
        final_answer[0] = sum(partial_sums)
    # TO-DO: FILL IN THE CODE


def main():
    threads = []
    for i in range(n_workers):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
    
    for i, t in enumerate(threads):
        t.join()
    
if __name__ == "__main__":
    start = time.time()
    main()
    elapsed_parallel = time.time() - start
    print(f"Time taken in parallel: {elapsed_parallel} seconds")

    start = time.time()
    np.sum(data)
    elapsed_serial = time.time() - start
    print(f"Time taken in serial: {elapsed_serial} seconds")

    print(f"Speed-up = {elapsed_serial/elapsed_parallel}")
    
