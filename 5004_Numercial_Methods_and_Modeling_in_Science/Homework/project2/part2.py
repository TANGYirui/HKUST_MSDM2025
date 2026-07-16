import numpy as np
import scipy.integrate as integrate

# ==========================================
# Helper Functions
# ==========================================
def log_likelihood(w, X, y):
    """Compute log-likelihood for logistic regression."""
    z = y * (X @ w)
    # Use log1p for numerical stability to avoid underflow
    log_sigma = -np.log1p(np.exp(-z))
    return np.sum(log_sigma)

# ==========================================
# (a) Generating Synthetic Classification Data
# ==========================================
def generate_synthetic_data(N=500):
    """Generate synthetic dataset with features and labels."""
    np.random.seed(42)  # For reproducibility
    w_true = np.array([-1.0, 1.0])
    
    # Sample x_i ~ N(1, 1), since -w0/w1 = -(-1)/1 = 1
    x_features = np.random.normal(loc=1.0, scale=1.0, size=N)
    
    # Construct design matrix X (bias column first)
    X = np.column_stack((np.ones(N), x_features))
    
    # Simulate noise epsilon ~ N(0, 4) -> standard deviation = 2
    epsilon = np.random.normal(loc=0.0, scale=2.0, size=N)
    
    # Generate labels y_i = sign(w_true^T x_i + epsilon_i)
    y = np.sign(X @ w_true + epsilon)
    y[y == 0] = 1 # Handle edge case
    
    return X, y

# ==========================================
# (b) Trapezoidal Rule for 1D Integration
# ==========================================
def integrand_1d(w1, X, y, w0=-1.0):
    """1D integrand: p(D|w_0, w_1) * p(w_1) with fixed w0."""
    w = np.array([w0, w1])
    ll = log_likelihood(w, X, y)
    # p(w1) = 1/sqrt(2pi) * exp(-w1^2 / 2)
    log_prior_w1 = -0.5 * np.log(2 * np.pi) - 0.5 * (w1 ** 2)
    return np.exp(ll + log_prior_w1)

def trapezoidal_rule_adaptive(X, y, L=6.0, tol=1e-6):
    """Adaptive trapezoidal rule for 1D marginal likelihood."""
    a, b = -L, L
    n = 1
    
    f_a = integrand_1d(a, X, y)
    f_b = integrand_1d(b, X, y)
    eval_count = 2
    
    h = (b - a) / n
    I_old = (h / 2.0) * (f_a + f_b)
    
    for i in range(25): # Max iterations
        n *= 2
        h = (b - a) / n
        x_new = np.linspace(a + h, b - h, n // 2)
        
        f_new = np.array([integrand_1d(xi, X, y) for xi in x_new])
        eval_count += len(x_new)
        
        I_new = I_old / 2.0 + h * np.sum(f_new)
        
        # Richardson error estimation
        error_est = np.abs(I_new - I_old) / 3.0
        rel_error = error_est / np.abs(I_new) if I_new != 0 else float('inf')
        
        if rel_error < tol and i > 2:
            return I_new, eval_count
            
        I_old = I_new

    return I_new, eval_count

# ==========================================
# (c) Romberg Integration for 1D Integration (Custom Implementation)
# ==========================================
def romberg_integration_1d(X, y, L=6.0, tol=1e-6):
    """1D marginal likelihood using custom Romberg integration."""
    max_iter = 20
    R = np.zeros((max_iter, max_iter))
    eval_count = 0
    a, b = -L, L

    f_a = integrand_1d(a, X, y, w0=-1.0)
    f_b = integrand_1d(b, X, y, w0=-1.0)
    eval_count += 2
    
    h = b - a
    R[0, 0] = (h / 2.0) * (f_a + f_b)

    for k in range(1, max_iter):
        h = (b - a) / (2**k)
        
        x_new = [a + i * h for i in range(1, 2**k, 2)]
        sum_f = sum(integrand_1d(xi, X, y, w0=-1.0) for xi in x_new)
        eval_count += len(x_new)
        R[k, 0] = 0.5 * R[k-1, 0] + h * sum_f

        for j in range(1, k + 1):
            R[k, j] = R[k, j-1] + (R[k, j-1] - R[k-1, j-1]) / ((4**j) - 1)

        error_est = np.abs(R[k, k] - R[k, k-1])
        rel_error = error_est / np.abs(R[k, k]) if R[k, k] != 0 else float('inf')

        if rel_error < tol and k >= 3:
            return R[k, k], eval_count

    print("Warning: Romberg did not strictly converge.")
    return R[max_iter-1, max_iter-1], eval_count

# ==========================================
# (d) Simpson's Rule for 2D Integration
# ==========================================
def integrand_2d(w0, w1, X, y):
    """2D integrand: p(D|w_0, w_1) * p(w_0, w1)."""
    w = np.array([w0, w1])
    ll = log_likelihood(w, X, y)
    # p(w0, w1) = 1/(2pi) * exp(-(w0^2 + w1^2) / 2)
    log_prior = -np.log(2 * np.pi) - 0.5 * (w0**2 + w1**2)
    return np.exp(ll + log_prior)

def simpson_2d_adaptive(X, y, L=6.0, tol=1e-6):
    """Adaptive 2D Simpson's integration on a grid."""
    def compute_simpson_2d_grid(n):
        w0_vals = np.linspace(-L, L, n)
        w1_vals = np.linspace(-L, L, n)
        W0, W1 = np.meshgrid(w0_vals, w1_vals)
        Z = np.zeros_like(W0)
        
        eval_count = 0
        for i in range(n):
            for j in range(n):
                Z[i, j] = integrand_2d(W0[i, j], W1[i, j], X, y)
                eval_count += 1
                
        int_w1 = integrate.simpson(Z, x=w1_vals, axis=0)
        result = integrate.simpson(int_w1, x=w0_vals)
        return result, eval_count

    n = 11 # Grid size must be odd for Simpson's rule
    I_old, evals_old = compute_simpson_2d_grid(n)
    total_evals = evals_old
    
    for i in range(8): # Max iterations
        n = n * 2 - 1 
        I_new, evals_new = compute_simpson_2d_grid(n)
        total_evals += evals_new
        
        # 2D Simpson error estimation: |I_2n - I_n| / 15
        error_est = np.abs(I_new - I_old) / 15.0
        rel_error = error_est / np.abs(I_new) if I_new != 0 else float('inf')
        
        if rel_error < tol:
            return I_new, total_evals
        
        I_old = I_new
        
    return I_new, total_evals

# ==========================================
# (e) Crude Monte Carlo Integration (2D)
# ==========================================
def crude_monte_carlo_2d(X, y, num_samples=200000):
    """2D marginal likelihood using Crude Monte Carlo integration."""
    np.random.seed(42)
    # Sample from prior p(w) = N(0, I)
    w_samples = np.random.normal(loc=0.0, scale=1.0, size=(num_samples, 2))
    
    likelihoods = np.zeros(num_samples)
    for i in range(num_samples):
        ll = log_likelihood(w_samples[i], X, y)
        likelihoods[i] = np.exp(ll)
        
    integral_estimate = np.mean(likelihoods)
    
    # Error estimation: sample standard deviation / sqrt(N)
    sample_std = np.std(likelihoods, ddof=1)
    error_est = sample_std / np.sqrt(num_samples)
    
    return integral_estimate, error_est

# ==========================================
# Execution Block
# ==========================================
if __name__ == "__main__":
    print("--- Part 2: Numerical Integration Results ---")
    
    X, y = generate_synthetic_data(N=500)
    
    I_trap, evals_trap = trapezoidal_rule_adaptive(X, y, L=6.0, tol=1e-6)
    print(f"(b) Trapezoidal 1D : {I_trap:.8e} (Evals: {evals_trap})")
    
    I_romb, evals_romb = romberg_integration_1d(X, y, L=6.0, tol=1e-6)
    print(f"(c) Romberg 1D     : {I_romb:.8e} (Evals: {evals_romb})")
    
    I_simp, evals_simp = simpson_2d_adaptive(X, y, L=6.0, tol=1e-6)
    print(f"(d) Simpson 2D     : {I_simp:.8e} (Evals: {evals_simp})")
    
    n_mc = 200000
    I_mc, err_mc = crude_monte_carlo_2d(X, y, num_samples=n_mc)
    print(f"(e) Crude MC 2D    : {I_mc:.8e} (Error: {err_mc:.8e}, Samples: {n_mc})")