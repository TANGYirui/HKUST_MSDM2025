import threading
from concurrent.futures import ThreadPoolExecutor
import time

n_workers = 8
N = n_workers * 1_000_000
count = 0 # counter for number of primes

def is_prime(n):
    
    # FILL IN YOUR CODE HERE
    pass

def worker(thread_id):
    # FILL IN YOUR CODE HERE
    pass

def serial():
    count = 0

    for i in range(N):
        if is_prime(i):
            count += 1

    return count

def manual_threading():
    threads = []
    for i in range(n_workers):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

def thread_pool():
    # FILL IN YOUR CODE HERE
    pass

def main():
    start = time.time()
    manual_threading()
    manual_time = time.time() - start

    start = time.time()
    thread_pool()
    thread_pool_time = time.time() - start

    start = time.time()
    serial()
    serial_time = time.time() - start

    print(f"Time taken with manual threading: {manual_time} seconds")
    print(f"Time taken with using thread pool: {thread_pool_time} seconds")
    print(f"Serial time taken: {serial_time} seconds")

if __name__ == "__main__":
    main()