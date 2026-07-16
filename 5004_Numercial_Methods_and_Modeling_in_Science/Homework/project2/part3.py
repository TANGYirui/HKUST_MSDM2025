import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ==========================================
# Helper Functions from Project Spec
# ==========================================
def log_likelihood(w, X, y):
    z = y * (X @ w)
    log_sigma = -np.log1p(np.exp(-z))
    return np.sum(log_sigma)

def log_prior(w, alpha=1.0):
    d = len(w)
    return -0.5 * alpha * np.dot(w, w) - 0.5 * d * np.log(2 * np.pi / alpha)

def log_posterior(w, X, y, alpha=1.0):
    return log_likelihood(w, X, y) + log_prior(w, alpha)

def generate_synthetic_data(N=500):
    np.random.seed(42)
    w_true = np.array([-1.0, 1.0])
    x_features = np.random.normal(loc=1.0, scale=1.0, size=N)
    X = np.column_stack((np.ones(N), x_features))
    epsilon = np.random.normal(loc=0.0, scale=2.0, size=N)
    y = np.sign(X @ w_true + epsilon)
    y[y == 0] = 1
    return X, y

# ==========================================
# (a) Metropolis Algorithm
# ==========================================
def run_metropolis(X, y, iters=10000, sigma_p=0.1):
    """Run a single Metropolis chain."""
    w = np.array([0.0, 0.0]) # Start at origin
    samples = np.zeros((iters, 2))
    accepted = 0
    
    log_post_current = log_posterior(w, X, y)
    
    for i in range(iters):
        # Symmetric Gaussian proposal
        delta = np.random.normal(0, sigma_p, size=2)
        w_prime = w + delta
        
        log_post_prime = log_posterior(w_prime, X, y)
        
        # Acceptance ratio in log space
        log_alpha = log_post_prime - log_post_current
        
        # Accept or reject
        if np.log(np.random.rand()) < log_alpha:
            w = w_prime
            log_post_current = log_post_prime
            accepted += 1
            
        samples[i] = w
        
    rate = accepted / iters
    # Discard burn-in (first 20%) for cleaner distribution
    burn_in = int(0.2 * iters)
    return samples[burn_in:], rate

def tune_and_sample_metropolis(X, y, target_rate=0.3, iters=10000):
    """Auto-tune proposal standard deviation to hit ~30% acceptance."""
    print("\n--- Tuning Metropolis Proposal Width ---")
    sigma_candidates = [0.01, 0.05, 0.08, 0.1, 0.12, 0.15, 0.2]
    best_sigma = 0.1
    best_diff = float('inf')
    
    for sig in sigma_candidates:
        _, rate = run_metropolis(X, y, iters=2000, sigma_p=sig)
        diff = abs(rate - target_rate)
        print(f"Sigma: {sig:.2f} -> Acceptance Rate: {rate:.2%}")
        if diff < best_diff:
            best_diff = diff
            best_sigma = sig
            
    print(f"[+] Selected optimal sigma_p: {best_sigma:.2f}")
    
    print("\n--- Running Final Metropolis Sampling ---")
    samples, final_rate = run_metropolis(X, y, iters=iters, sigma_p=best_sigma)
    print(f"[+] Final Acceptance Rate: {final_rate:.2%}")
    return samples

def plot_posterior(samples, X, y, Z_estimated):
    """Plot Metropolis samples vs theoretical scaled posterior contours."""
    plt.figure(figsize=(10, 8))
    
    # 1. Plot MCMC Samples (2D Histogram / Scatter)
    plt.scatter(samples[:, 0], samples[:, 1], alpha=0.15, s=5, color='blue', label='MCMC Samples')
    
    # 2. Create Grid for Contours
    w0_grid = np.linspace(-1.8, -0.2, 100)
    w1_grid = np.linspace(0.2, 1.8, 100)
    W0, W1 = np.meshgrid(w0_grid, w1_grid)
    Posterior_vals = np.zeros_like(W0)
    
    for i in range(100):
        for j in range(100):
            w = np.array([W0[i, j], W1[i, j]])
            # p(w|D) = p(D|w)p(w) / p(D)
            log_unnorm = log_posterior(w, X, y)
            # Safe exponentiation using the Z_estimated from Part 2
            # Value is tiny, so we scale it up purely for contour visualization
            Posterior_vals[i, j] = np.exp(log_unnorm - np.log(Z_estimated))
            
    # 3. Plot Contours
    contours = plt.contour(W0, W1, Posterior_vals, levels=8, colors='red', linewidths=2)
    plt.clabel(contours, inline=True, fontsize=8, fmt='%.1e')
    
    # Plot true weights
    plt.plot(-1, 1, 'g*', markersize=15, label='True Weights (-1, 1)')
    
    plt.title('Metropolis Samples vs True Posterior Contours')
    plt.xlabel('Bias (w0)')
    plt.ylabel('Feature Weight (w1)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig('metropolis_posterior.png', dpi=300, bbox_inches='tight')
    print("[+] Plot saved as 'metropolis_posterior.png'")

# ==========================================
# (b) Simulated Annealing for MAP
# ==========================================
def simulated_annealing_map(X, y):
    """Find Maximum A Posteriori (MAP) using Simulated Annealing."""
    print("\n--- Running Simulated Annealing for MAP ---")
    np.random.seed(42)
    w = np.array([0.0, 0.0])
    best_w = w.copy()
    
    log_post_current = log_posterior(w, X, y)
    best_log_post = log_post_current
    
    T = 10.0      # Initial Temperature
    T_min = 1e-6  # Final Temperature
    alpha = 0.95  # Cooling rate
    
    iters_per_temp = 50
    
    while T > T_min:
        for _ in range(iters_per_temp):
            # Proposal depends slightly on T for finer search as it cools
            w_prime = w + np.random.normal(0, max(0.01, T*0.1), 2)
            log_post_prime = log_posterior(w_prime, X, y)
            
            # E(w) = -log_posterior. We want to MINIMIZE Energy.
            delta_E = -(log_post_prime - log_post_current)
            
            # Accept if Energy decreases, or with probability exp(-delta_E / T)
            if delta_E < 0 or np.log(np.random.rand()) < (-delta_E / T):
                w = w_prime
                log_post_current = log_post_prime
                
                # Track global best
                if log_post_current > best_log_post:
                    best_log_post = log_post_current
                    best_w = w.copy()
        T *= alpha
        
    print(f"[+] MAP estimated by SA: w0={best_w[0]:.4f}, w1={best_w[1]:.4f}")
    return best_w

# ==========================================
# (c) Importance Sampling
# ==========================================
def importance_sampling(X, y, w_map, sample_cov, num_samples=200000):
    """Calculate Marginal Likelihood using Importance Sampling."""
    print("\n--- Running Importance Sampling ---")
    np.random.seed(42)
    
    # 1. Define Proposal q(w) = N(w_map, sample_cov)
    w_samples = np.random.multivariate_normal(w_map, sample_cov, num_samples)
    
    # 2. Compute Weights: W_k = p(D|w)p(w) / q(w)
    # We do this entirely in log-space to prevent catastrophic underflow
    log_weights = np.zeros(num_samples)
    
    # We use scipy's multivariate_normal to get log q(w)
    mvn_dist = multivariate_normal(mean=w_map, cov=sample_cov)
    log_q_vals = mvn_dist.logpdf(w_samples)
    
    for k in range(num_samples):
        log_p_unnorm = log_posterior(w_samples[k], X, y)
        log_weights[k] = log_p_unnorm - log_q_vals[k]
        
    # 3. Log-Sum-Exp Trick for Stable Mean
    # Mean(exp(log_weights)) = exp(max) * Mean(exp(log_weights - max))
    max_log_w = np.max(log_weights)
    scaled_weights = np.exp(log_weights - max_log_w)
    
    mean_scaled = np.mean(scaled_weights)
    marginal_likelihood = np.exp(max_log_w) * mean_scaled
    
    # 4. Error Estimation
    std_scaled = np.std(scaled_weights, ddof=1)
    error_est = np.exp(max_log_w) * std_scaled / np.sqrt(num_samples)
    
    print(f"[+] Importance Sampling Integral: {marginal_likelihood:.8e}")
    print(f"[+] Error Estimate              : {error_est:.8e}")
    
    return marginal_likelihood, error_est

# ==========================================
# Execution Block
# ==========================================
if __name__ == "__main__":
    X, y = generate_synthetic_data()
    
    # (a) Metropolis
    metropolis_samples = tune_and_sample_metropolis(X, y, target_rate=0.3, iters=20000)
    
    # For plotting, we use the Marginal Likelihood obtained from Part 2 (Crude MC)
    Z_estimated = 1.47537193e-143 
    plot_posterior(metropolis_samples, X, y, Z_estimated)
    
    # (b) Simulated Annealing for MAP
    w_map = simulated_annealing_map(X, y)
    
    # (c) Importance Sampling
    # Width (covariance) estimated using the sample variance from (a)
    sample_cov = np.cov(metropolis_samples.T)
    print("\n[+] Empirical Covariance Matrix from MCMC:")
    print(sample_cov)
    
    importance_sampling(X, y, w_map, sample_cov, num_samples=200000)
    