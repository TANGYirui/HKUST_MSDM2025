import numpy as np

# for part (a)
def distance_pure_python(data):
    n = data.shape[0]
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            diff = data[i] - data[j]
            D[i, j] = np.sqrt(np.sum(diff ** 2))
    return D

# for part (b)
def distance_numpy(data):
    sum_sq = np.sum(data ** 2, axis=1, keepdims=True)
    dot = data @ data.T
    D_sq = sum_sq + sum_sq.T - 2 * dot
    D_sq = np.clip(D_sq, 0, None)
    return np.sqrt(D_sq)

# DO NOT MODIFY ANYTHING BELOW THIS POINT IN YOUR SUBMITTED CODE
def main():
    rng = np.random.default_rng()
    n, d = 500, 500

    data = rng.random((n, d))

    dist_mat_pure_python = distance_pure_python(data)
    dist_mat_numpy = distance_numpy(data)

    print(f"Are the two results the same?: {np.max(np.abs(dist_mat_pure_python - dist_mat_numpy)) < 1e-5}")

if __name__ == "__main__":
    main()