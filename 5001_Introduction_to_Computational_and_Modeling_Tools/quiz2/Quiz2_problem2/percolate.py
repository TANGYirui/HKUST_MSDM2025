import numpy as np
from mpi4py import MPI
 
from check_percolate import check_percolate

def gen_grid(n, p):
    return (np.random.random((n, n)) < p).astype(np.int32)

def percolation_probability(n, p, N=10000):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    base_seed = 3042  
    np.random.seed(base_seed + rank)

    base = N // size
    remainder = N % size
    if rank < remainder:
        local_N = base + 1
    else:
        local_N = base

    local_count = 0
    for _ in range(local_N):
        if check_percolate(gen_grid(n, p)):
            local_count += 1

    total_count = comm.allreduce(local_count, op=MPI.SUM)
    return total_count / float(N)

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    prob = percolation_probability(50, 0.6)

    if rank == 0:
        print(f"The percolation probability for n=50 and p=0.6 is {prob}")
