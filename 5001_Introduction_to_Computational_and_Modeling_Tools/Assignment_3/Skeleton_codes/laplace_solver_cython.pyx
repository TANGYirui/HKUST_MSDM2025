# cython: language_level=3
import numpy as np
cimport numpy as np
cimport cython

cdef initialize(double phi_top, double phi_bottom, double phi_left, double phi_right, int n):
    '''
    Initialize the grid satisfying the boundary conditions with zero in the interior

    Args:
        phi_top: value of phi at the top edge
        phi_bottom: value of phi at the bottom edge
        phi_left: value of phi at the left edge
        phi_right: value of phi at the right edge
        n: size of grid (minus 1)

    Returns:
        A 2D numpy array
    '''
    cdef cnp.ndarray[cnp.double_t, ndim=2] phi = np.zeros((n + 1, n + 1), dtype=np.float64)
    cdef int i, j

    # 设置边界值
    for i in range(n + 1):
        phi[0, i] = phi_bottom   # Bottom row
        phi[n, i] = phi_top      # Top row
        phi[i, 0] = phi_left     # Left column
        phi[i, n] = phi_right    # Right column

    return phi

# TO DO: FILL IN THE APPROPRIATE ARGUMENTS IN update
@cython.boundscheck(False)  # Turn off bounds checking for speed
@cython.wraparound(False)   # Turn off negative indexing for speed
cdef update(double[:, :] phi_new, double[:, :] phi_old):
    '''
    Update phi_new in-place using values of phi_old

    Args:
        phi_new: the updated grid values (memory view)
        phi_old: the previous grid values (memory view)

    Returns:
        None
    '''
    cdef int m, n
    cdef int r, c
    m, n = phi_new.shape

    for r in range(1, m - 1):
        for c in range(1, n - 1):
            phi_new[r, c] = 0.25 * (
                phi_old[r + 1, c] +  # 下方邻居
                phi_old[r - 1, c] +  # 上方邻居
                phi_old[r, c + 1] +  # 右方邻居
                phi_old[r, c - 1]    # 左方邻居
            )

def solve_cython(boundary_conditions, n=100, iter_max=10000, tol=1e-5):
    '''
    Solving the Laplace equation with Jacobi's iteration (Cython version)

    Args:
        boundary_conditions: a tuple of (phi_top, phi_bottom, phi_left, phi_right)
        n: size of grid (minus 1), default to 100
        iter_max: maximum number of iterations allowed, default to 10000
        tol: tolerance level, default to 1e-5

    Returns:
        A 2D numpy array corresponding to the solution
    '''
    cdef double phi_top, phi_bottom, phi_left, phi_right
    cdef double[:, :] phi_old, phi_new
    cdef double max_diff
    cdef int iter = 0

    phi_top, phi_bottom, phi_left, phi_right = boundary_conditions

    phi_old = initialize(phi_top, phi_bottom, phi_left, phi_right, n)

    while iter <= iter_max:
        phi_new = initialize(phi_top, phi_bottom, phi_left, phi_right, n)
        update(phi_new, phi_old)

        max_diff = 0.0
        for r in range(n + 1):
            for c in range(n + 1):
                diff = fabs(phi_new[r, c] - phi_old[r, c])
                if diff > max_diff:
                    max_diff = diff

        if max_diff < tol:
            break

        phi_old, phi_new = phi_new, phi_old
        iter += 1

    return np.asarray(phi_old)
