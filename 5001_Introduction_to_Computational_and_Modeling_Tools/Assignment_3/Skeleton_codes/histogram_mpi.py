from mpi4py import MPI
import numpy as np

def parallel_histogram(data, low, high, n_bins):
    """
    Compute histogram using MPI processes.
    
    Args:
        data: an array of numbers (only on rank 0)
        low: the lower range of the bins
        high: the upper range of the bins
        n_bins: number of bins used
    
    Returns:
        An array that contains counts of elements in each bin (only on rank 0)
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        total_len = len(data)
        chunk_size = total_len // size
        remainder = total_len % size
        counts = [chunk_size + (1 if i < remainder else 0) for i in range(size)]
        displacements = [sum(counts[:i]) for i in range(size)]
        local_n = counts[rank]
    else:
        data = None
        counts = None
        displacements = None
        local_n = None

    local_n = comm.scatter([counts[i] if rank == 0 else None for i in range(size)], root=0)
    local_data = np.empty(local_n, dtype='d')
    comm.Scatterv([data, counts, displacements, MPI.DOUBLE] if rank == 0 else None, local_data, root=0)

    local_hist, _ = np.histogram(local_data, bins=n_bins, range=(low, high))

    global_hist = None
    if rank == 0:
        # 修改：将 dtype 改为 np.int64，与 local_hist 的类型一致
        global_hist = np.empty(n_bins, dtype=np.int64)
    comm.Reduce(local_hist, global_hist, op=MPI.SUM, root=0)

    return global_hist 
    # # TO BE COMPLETED
    # # Hint: Scatter data to all processes, compute local histogram, reduce results
    
    # pass

# DO NOT MODIFY ANYTHING BELOW THIS POINT IN YOUR SUBMITTED CODE
def main():
    """
    Compute histogram using MPI
    Run with: mpiexec -n <num_processes> python histogram_mpi.py
    """
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    
    if rank == 0:
        test_data = np.random.rand(100000)
        low = 0.0
        high = 1.0
        n_bins = 50

        hist = parallel_histogram(test_data, low, high, n_bins)
        print(f"Histogram: {hist}")

if __name__ == "__main__":
    main()