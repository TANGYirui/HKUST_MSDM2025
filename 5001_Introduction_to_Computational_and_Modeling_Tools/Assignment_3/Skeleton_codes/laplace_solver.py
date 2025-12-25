import numpy as np
import matplotlib.pyplot as plt
# you will need additional import statements here if you want to use your solver written in Cython

def initialize(phi_top=0, phi_bottom=0, phi_left=0, phi_right=0, n=100):
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
    # TO BE COMPLETED
    phi = np.zeros((n + 1, n + 1))
    phi[0, :] = phi_bottom  
    phi[-1, :] = phi_top  
    phi[:, 0] = phi_left   
    phi[:, -1] = phi_right  
    return phi

def update(phi_new, phi_old):
    '''
    Update phi_new in-place using values of phi_old

    Args:
        phi_new: the updated grid values
        phi_old: the previous grid values

    Returns:
        None
    '''
    # TO BE COMPLETED
    phi_new[1:-1, 1:-1] = 0.25 * (
        phi_old[2:, 1:-1] +
        phi_old[:-2, 1:-1] +   
        phi_old[1:-1, 2:] +    
        phi_old[1:-1, :-2]     
    )

##########################################
# DO NOT MODIFY ANYTHING BELOW THIS LINE #
##########################################

def solve_np(boundary_conditions, n=100, iter_max=10000, tol=1e-5):
    '''
    Solving the Laplace equation with Jacobi's iteration (using vectorized numpy operations)

    Args:
        boundary_conditions: a tuple of (phi_top, phi_bottom, phi_left, phi_right)
        n: size of grid (minus 1), default to 100
        iter_max: maximum number of iterations allowed, default to 10000
        tol: tolerance level, default to 1e-5

    Returns:
        A 2D numpy array corresponding to the solution to the Laplace equation with the specified boundary coniditions
    '''
    phi_old = initialize(*boundary_conditions, n)
    max_diff = np.inf
    iter = 0

    while (iter <= iter_max) and (max_diff >= tol):
        phi_new = initialize()
        update(phi_new, phi_old)
        
        max_diff = np.max(np.abs(phi_new - phi_old))
        phi_old = phi_new
        iter += 1

    return phi_new

def visualize(solution):
    '''
    Visualize the solution
    '''
    plt.figure(figsize=(8, 6))
    plt.imshow(solution, cmap='hot', interpolation='bilinear')
    plt.colorbar(label='Temperature')
    plt.title('Laplace Equation Solution')
    plt.xlabel('x')
    plt.ylabel('y')
    
    # Add contour lines
    X, Y = np.meshgrid(range(solution.shape[1]), range(solution.shape[0]))
    CS = plt.contour(X, Y, solution, levels=10, colors='black', alpha=0.3, linewidths=0.5)
    plt.clabel(CS, inline=True, fontsize=8)
    
    plt.tight_layout()
    plt.savefig('laplace_solution.png', dpi=100)

if __name__ == "__main__":
    boundary_conditions = (100, 100, 50, 50)

    solution = solve_np(boundary_conditions, n=100, iter_max=10000, tol=1e-5)
    visualize(solution) # for visualization