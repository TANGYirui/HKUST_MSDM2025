import numpy as np

cpdef int check_percolate(np.int32_t[:, ::1] grid):
    cdef Py_ssize_t n = grid.shape[0]
    cdef Py_ssize_t m = grid.shape[1]
    cdef Py_ssize_t i, j, ni, nj, top
    cdef int k
    cdef int di[4]
    cdef int dj[4]

    di[0] = -1
    dj[0] = 0
    di[1] = 1
    dj[1] = 0
    di[2] = 0
    dj[2] = -1
    di[3] = 0
    dj[3] = 1

    visited_arr = np.zeros((n, m), dtype=np.int8)
    cdef signed char[:, ::1] visited = visited_arr

    stack_arr = np.empty((n * m, 2), dtype=np.int64)
    cdef long[:, ::1] stack = stack_arr

    top = 0

    for j in range(m):
        if grid[0, j] == 1 and visited[0, j] == 0:
            visited[0, j] = 1
            stack[top, 0] = 0
            stack[top, 1] = j
            top += 1

            while top > 0:
                top -= 1
                i = stack[top, 0]
                j = stack[top, 1]

                if i == n - 1:
                    return 1

                for k in range(4):
                    ni = i + di[k]
                    nj = j + dj[k]
                    if 0 <= ni < n and 0 <= nj < m:
                        if grid[ni, nj] == 1 and visited[ni, nj] == 0:
                            visited[ni, nj] = 1
                            stack[top, 0] = ni
                            stack[top, 1] = nj
                            top += 1

    return 0