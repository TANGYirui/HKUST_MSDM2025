import numpy as np
from mpi4py import MPI
from check_percolate import check_percolate # make sure you have correctly compiled check_percolate.pyx with the given setup.py

def gen_grid(n, p):
    '''
    Generate an n-by-n binary grid with P(1) = p and P(0) = 1-p.

    Args:
        n: Size of the grid
        p: Probability the value of a lattice point is 1 (i.e. "Open")

    Returns:
        A two-dimensional binary numpy array with dtype=np.int32
    '''
    return (np.random.random((n, n)) < p).astype(np.int32)
    

def percolation_probability(n, p, N=10000):
    '''
    Estimate the probability of percolation for given n and p by running N simulations in parallel using MPI.
    The probability is given by K/N, where K is the number of simulations with percolating grids.

    Args:
        n: Size of the grid
        p: Probability the value of a lattice point is 1 (i.e. "Open")

    Returns:
        A floating-point number
    '''

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
# DO NOT MODIFY CODES BELOW THIS LINE

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    prob = percolation_probability(50, 0.6)

    if rank == 0:
        print(f"The percolation probability for n=50 and p=0.6 is {prob}")