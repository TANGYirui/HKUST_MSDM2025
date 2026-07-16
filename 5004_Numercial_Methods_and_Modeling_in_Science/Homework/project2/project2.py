import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy.stats import multivariate_normal

# 确保图片保存在当前脚本所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# =============================================================================
# Helper Functions (Shared across Part 2 & Part 3)
# =============================================================================
def log_likelihood(w, X, y):
    """Compute log-likelihood for logistic regression."""
    z = y * (X @ w)
    # Use log1p for numerical stability to avoid underflow
    log_sigma = -np.log1p(np.exp(-z))
    return np.sum(log_sigma)

def log_prior(w, alpha=1.0):
    """Zero-mean Gaussian prior."""
    d = len(w)
    return -0.5 * alpha * np.dot(w, w) - 0.5 * d * np.log(2 * np.pi / alpha)

def log_posterior(w, X, y, alpha=1.0):
    """
    Unnormalized log posterior: log_likelihood + log_prior.
    This exactly equals log[p(D|w)p(w)].
    """
    return log_likelihood(w, X, y) + log_prior(w, alpha)

def generate_synthetic_data(N=500):
    """Generate synthetic dataset with features and labels."""
    np.random.seed(42)
    w_true = np.array([-1.0, 1.0])
    x_features = np.random.normal(loc=1.0, scale=1.0, size=N)
    X = np.column_stack((np.ones(N), x_features))
    epsilon = np.random.normal(loc=0.0, scale=2.0, size=N)
    y = np.sign(X @ w_true + epsilon)
    y[y == 0] = 1 
    return X, y

# =============================================================================
# Part 1: 1D Rejection to Sample Normal Distributions
# =============================================================================
def sample_standard_normal_rejection(n_samples):
    lambda_val = 1.0
    A = np.sqrt(np.e / (2 * np.pi))
    samples = []
    total_trials = 0
    
    while len(samples) < n_samples:
        u = np.random.uniform(-0.5, 0.5)
        w_candidate = -np.sign(u) * np.log(1 - 2 * np.abs(u))
        v = np.random.uniform(0, 1)
        
        p_w = (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * w_candidate**2)
        f_w = A * np.exp(-lambda_val * np.abs(w_candidate))
        
        if v <= (p_w / f_w):
            samples.append(w_candidate)
        total_trials += 1
        
    return np.array(samples), (n_samples / total_trials)

def sample_general_normal(n_samples, mu, sigma_sq):
    sigma = np.sqrt(sigma_sq)
    z_samples, rate = sample_standard_normal_rejection(n_samples)
    w_samples = mu + sigma * z_samples
    return w_samples, rate

def run_part_1():
    print("="*50 + "\nPart 1: Rejection Sampling\n" + "="*50)
    n_points = 100000
    samples, emp_rate = sample_standard_normal_rejection(n_points)
    theoretical_rate = np.sqrt(np.pi / (2 * np.e))
    
    print(f"Theoretical Rate: {theoretical_rate:.4f} ({theoretical_rate*100:.2f}%)")
    print(f"Empirical Rate:   {emp_rate:.4f} ({emp_rate*100:.2f}%)")
    
    plt.figure(figsize=(10, 6))
    plt.hist(samples, bins=100, density=True, alpha=0.6, color='steelblue', label='Sampled Histogram')
    w_axis = np.linspace(-4, 4, 1000)
    pdf = (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * w_axis**2)
    plt.plot(w_axis, pdf, linewidth=2, color='darkred', label='Theoretical N(0,1) PDF')
    plt.title("Rejection Sampling Verification: N(0,1)")
    plt.xlabel("w")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('rejection_sampling_verification.png', dpi=300, bbox_inches='tight')
    print("[+] Plot saved as 'rejection_sampling_verification.png'")

# =============================================================================
# Part 2: Numerical Integration for Marginal Likelihood
# =============================================================================
def integrand_1d(w1, X, y, w0=-1.0):
    w = np.array([w0, w1])
    return np.exp(log_posterior(w, X, y))

def trapezoidal_rule_adaptive(X, y, L=6.0, tol=1e-6):
    a, b = -L, L
    n = 1
    eval_count = 2
    h = (b - a) / n
    I_old = (h / 2.0) * (integrand_1d(a, X, y) + integrand_1d(b, X, y))
    
    for i in range(25):
        n *= 2
        h = (b - a) / n
        x_new = np.linspace(a + h, b - h, n // 2)
        f_new = np.array([integrand_1d(xi, X, y) for xi in x_new])
        eval_count += len(x_new)
        I_new = I_old / 2.0 + h * np.sum(f_new)
        
        error_est = np.abs(I_new - I_old) / 3.0
        rel_error = error_est / np.abs(I_new) if I_new != 0 else float('inf')
        if rel_error < tol and i > 2:
            return I_new, eval_count
        I_old = I_new
    return I_new, eval_count

def romberg_integration_1d(X, y, L=6.0, tol=1e-6):
    max_iter = 20
    R = np.zeros((max_iter, max_iter))
    a, b = -L, L
    h = b - a
    R[0, 0] = (h / 2.0) * (integrand_1d(a, X, y) + integrand_1d(b, X, y))
    eval_count = 2

    for k in range(1, max_iter):
        h = (b - a) / (2**k)
        x_new = [a + i * h for i in range(1, 2**k, 2)]
        sum_f = sum(integrand_1d(xi, X, y) for xi in x_new)
        eval_count += len(x_new)
        R[k, 0] = 0.5 * R[k-1, 0] + h * sum_f

        for j in range(1, k + 1):
            R[k, j] = R[k, j-1] + (R[k, j-1] - R[k-1, j-1]) / ((4**j) - 1)

        error_est = np.abs(R[k, k] - R[k, k-1])
        rel_error = error_est / np.abs(R[k, k]) if R[k, k] != 0 else float('inf')
        if rel_error < tol and k >= 3:
            return R[k, k], eval_count
    return R[max_iter-1, max_iter-1], eval_count

def integrand_2d(w0, w1, X, y):
    w = np.array([w0, w1])
    return np.exp(log_posterior(w, X, y))

def simpson_2d_adaptive(X, y, L=6.0, tol=1e-6):
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

    n = 11
    I_old, evals_old = compute_simpson_2d_grid(n)
    total_evals = evals_old
    
    for i in range(8):
        n = n * 2 - 1 
        I_new, evals_new = compute_simpson_2d_grid(n)
        total_evals += evals_new
        error_est = np.abs(I_new - I_old) / 15.0
        rel_error = error_est / np.abs(I_new) if I_new != 0 else float('inf')
        if rel_error < tol:
            return I_new, total_evals
        I_old = I_new
    return I_new, total_evals

def crude_monte_carlo_2d(X, y, num_samples=200000):
    np.random.seed(42)
    w_samples = np.random.normal(loc=0.0, scale=1.0, size=(num_samples, 2))
    likelihoods = np.zeros(num_samples)
    for i in range(num_samples):
        likelihoods[i] = np.exp(log_likelihood(w_samples[i], X, y))
    
    integral_estimate = np.mean(likelihoods)
    sample_std = np.std(likelihoods, ddof=1)
    error_est = sample_std / np.sqrt(num_samples)
    return integral_estimate, error_est

def run_part_2(X, y):
    print("\n" + "="*50 + "\nPart 2: Numerical Integration\n" + "="*50)
    I_trap, evals_trap = trapezoidal_rule_adaptive(X, y, L=6.0, tol=1e-6)
    print(f"(b) Trapezoidal 1D : {I_trap:.8e} (Evals: {evals_trap})")
    
    I_romb, evals_romb = romberg_integration_1d(X, y, L=6.0, tol=1e-6)
    print(f"(c) Romberg 1D     : {I_romb:.8e} (Evals: {evals_romb})")
    
    I_simp, evals_simp = simpson_2d_adaptive(X, y, L=6.0, tol=1e-6)
    print(f"(d) Simpson 2D     : {I_simp:.8e} (Evals: {evals_simp})")
    
    n_mc = 200000
    I_mc, err_mc = crude_monte_carlo_2d(X, y, num_samples=n_mc)
    print(f"(e) Crude MC 2D    : {I_mc:.8e} (Error: {err_mc:.8e}, Samples: {n_mc})")
    return I_mc # Return to be used in Part 3 plotting

# =============================================================================
# Part 3: MCMC, SA, and Importance Sampling
# =============================================================================
def run_metropolis(X, y, iters=10000, sigma_p=0.1):
    w = np.array([0.0, 0.0])
    samples = np.zeros((iters, 2))
    accepted = 0
    log_post_current = log_posterior(w, X, y)
    
    for i in range(iters):
        w_prime = w + np.random.normal(0, sigma_p, size=2)
        log_post_prime = log_posterior(w_prime, X, y)
        log_alpha = log_post_prime - log_post_current
        
        if np.log(np.random.rand()) < log_alpha:
            w = w_prime
            log_post_current = log_post_prime
            accepted += 1
            
        samples[i] = w
        
    rate = accepted / iters
    burn_in = int(0.2 * iters)
    return samples[burn_in:], rate

def tune_and_sample_metropolis(X, y, target_rate=0.3, iters=10000):
    print("\n--- Tuning Metropolis Proposal Width ---")
    sigma_candidates = [0.01, 0.05, 0.08, 0.1, 0.12, 0.15, 0.2]
    best_sigma = 0.1
    best_diff = float('inf')
    
    for sig in sigma_candidates:
        _, rate = run_metropolis(X, y, iters=2000, sigma_p=sig)
        print(f"Sigma: {sig:.2f} -> Acceptance Rate: {rate:.2%}")
        if abs(rate - target_rate) < best_diff:
            best_diff = abs(rate - target_rate)
            best_sigma = sig
            
    print(f"[+] Selected optimal sigma_p: {best_sigma:.2f}")
    samples, final_rate = run_metropolis(X, y, iters=iters, sigma_p=best_sigma)
    print(f"[+] Final Acceptance Rate: {final_rate:.2%}")
    return samples

def plot_posterior(samples, X, y, Z_estimated):
    plt.figure(figsize=(10, 8))
    plt.scatter(samples[:, 0], samples[:, 1], alpha=0.15, s=5, color='blue', label='MCMC Samples')
    
    w0_grid = np.linspace(-1.8, -0.2, 100)
    w1_grid = np.linspace(0.2, 1.8, 100)
    W0, W1 = np.meshgrid(w0_grid, w1_grid)
    Posterior_vals = np.zeros_like(W0)
    
    for i in range(100):
        for j in range(100):
            w = np.array([W0[i, j], W1[i, j]])
            log_unnorm = log_posterior(w, X, y)
            Posterior_vals[i, j] = np.exp(log_unnorm - np.log(Z_estimated))
            
    contours = plt.contour(W0, W1, Posterior_vals, levels=8, colors='red', linewidths=2)
    plt.clabel(contours, inline=True, fontsize=8, fmt='%.1e')
    plt.plot(-1, 1, 'g*', markersize=15, label='True Weights (-1, 1)')
    plt.title('Metropolis Samples vs True Posterior Contours')
    plt.xlabel('Bias (w0)')
    plt.ylabel('Feature Weight (w1)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('metropolis_posterior.png', dpi=300, bbox_inches='tight')
    print("[+] Plot saved as 'metropolis_posterior.png'")

def simulated_annealing_map(X, y):
    """
    Find MAP using Simulated Annealing.
    *UPDATED NOTE*: According to the prompt correction, E(w) = -log[p(D|w)p(w)].
    Because our log_posterior function computes exactly log_likelihood + log_prior,
    E(w) is exactly -log_posterior. No code change is needed!
    """
    print("\n--- Running Simulated Annealing for MAP ---")
    np.random.seed(42)
    w = np.array([0.0, 0.0])
    best_w = w.copy()
    
    log_post_current = log_posterior(w, X, y)
    best_log_post = log_post_current
    
    T = 10.0      
    T_min = 1e-6  
    alpha = 0.95  
    iters_per_temp = 50
    
    while T > T_min:
        for _ in range(iters_per_temp):
            w_prime = w + np.random.normal(0, max(0.01, T*0.1), 2)
            log_post_prime = log_posterior(w_prime, X, y)
            
            # delta_E = E(w_prime) - E(w) = -log_post_prime - (-log_post_current)
            delta_E = -(log_post_prime - log_post_current)
            
            if delta_E < 0 or np.log(np.random.rand()) < (-delta_E / T):
                w = w_prime
                log_post_current = log_post_prime
                if log_post_current > best_log_post:
                    best_log_post = log_post_current
                    best_w = w.copy()
        T *= alpha
        
    print(f"[+] MAP estimated by SA: w0={best_w[0]:.4f}, w1={best_w[1]:.4f}")
    return best_w

def importance_sampling(X, y, w_map, sample_cov, num_samples=200000):
    print("\n--- Running Importance Sampling ---")
    np.random.seed(42)
    w_samples = np.random.multivariate_normal(w_map, sample_cov, num_samples)
    
    log_weights = np.zeros(num_samples)
    mvn_dist = multivariate_normal(mean=w_map, cov=sample_cov)
    log_q_vals = mvn_dist.logpdf(w_samples)
    
    for k in range(num_samples):
        log_p_unnorm = log_posterior(w_samples[k], X, y)
        log_weights[k] = log_p_unnorm - log_q_vals[k]
        
    max_log_w = np.max(log_weights)
    scaled_weights = np.exp(log_weights - max_log_w)
    
    mean_scaled = np.mean(scaled_weights)
    marginal_likelihood = np.exp(max_log_w) * mean_scaled
    
    std_scaled = np.std(scaled_weights, ddof=1)
    error_est = np.exp(max_log_w) * std_scaled / np.sqrt(num_samples)
    
    print(f"[+] Importance Sampling Integral: {marginal_likelihood:.8e}")
    print(f"[+] Error Estimate              : {error_est:.8e}")

def run_part_3(X, y, Z_estimated):
    print("\n" + "="*50 + "\nPart 3: MCMC & Importance Sampling\n" + "="*50)
    metropolis_samples = tune_and_sample_metropolis(X, y, target_rate=0.3, iters=20000)
    plot_posterior(metropolis_samples, X, y, Z_estimated)
    w_map = simulated_annealing_map(X, y)
    
    sample_cov = np.cov(metropolis_samples.T)
    print("\n[+] Empirical Covariance Matrix from MCMC:")
    print(sample_cov)
    
    importance_sampling(X, y, w_map, sample_cov, num_samples=200000)

# =============================================================================
# Main Execution Flow
# =============================================================================
if __name__ == "__main__":
    # Execute Part 1
    run_part_1()
    
    # Generate Shared Data for Part 2 & 3
    X, y = generate_synthetic_data(N=500)
    
    # Execute Part 2
    Z_estimated = run_part_2(X, y)
    
    # Execute Part 3
    run_part_3(X, y, Z_estimated)