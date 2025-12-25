import numpy as np
from laplace_solver import solve_np

def main():
    boundary_conditions = (100, 100, 50, 50)  # (top, bottom, left, right)

    solution = solve_np(boundary_conditions, n=100, iter_max=10000, tol=1e-5)

    np.save('laplace_solution.npy', solution)
    print("Solution saved to 'laplace_solution.npy'")

if __name__ == "__main__":
    main()