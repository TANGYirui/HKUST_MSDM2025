import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def sample_standard_normal_rejection(n_samples):
    """
    (d) Sample N(0,1) using Rejection Method with Laplace envelope.
    Returns the accepted samples and the empirical acceptance rate.
    """
    # Optimal parameters from (c)
    lambda_val = 1.0
    A = np.sqrt(np.e / (2 * np.pi))
    
    samples = []
    total_trials = 0
    
    while len(samples) < n_samples:
        # Step 1: Sample from Laplace distribution proportional to exp(-|w|)
        # Inverse transform sampling for Laplace: 
        # generate u in (-0.5, 0.5), w = -sign(u) * ln(1 - 2|u|)
        u = np.random.uniform(-0.5, 0.5)
        w_candidate = -np.sign(u) * np.log(1 - 2 * np.abs(u))
        
        # Step 2: Generate uniform variable for rejection check
        v = np.random.uniform(0, 1)
        
        # Step 3: Check acceptance criterion
        # We accept if v <= p(w) / f(w)
        p_w = (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * w_candidate**2)
        f_w = A * np.exp(-lambda_val * np.abs(w_candidate))
        
        if v <= (p_w / f_w):
            samples.append(w_candidate)
            
        total_trials += 1
        
    empirical_rate = n_samples / total_trials
    return np.array(samples), empirical_rate

def sample_general_normal(n_samples, mu, sigma_sq):
    """
    (f) Sample from general normal N(mu, sigma^2) using standard samples.
    """
    sigma = np.sqrt(sigma_sq)
    z_samples, rate = sample_standard_normal_rejection(n_samples)
    w_samples = mu + sigma * z_samples
    return w_samples, rate

# ==========================================
# (e) Execution and Verification
# ==========================================
if __name__ == "__main__":
    n_points = 100000
    print(f"Generating {n_points} samples...")
    
    # Run the standard normal sampler
    samples, emp_rate = sample_standard_normal_rejection(n_points)
    
    # Calculate Theoretical Rate
    theoretical_rate = np.sqrt(np.pi / (2 * np.e))
    
    print(f"--- Acceptance Rate Check ---")
    print(f"Theoretical Rate: {theoretical_rate:.4f} ({theoretical_rate*100:.2f}%)")
    print(f"Empirical Rate:   {emp_rate:.4f} ({emp_rate*100:.2f}%)")
    
    # Plotting to verify distribution visually
    plt.figure(figsize=(10, 6))
    
    # Empirical histogram
    count, bins, ignored = plt.hist(samples, bins=100, density=True, alpha=0.6, 
                                    color='steelblue', label='Sampled Histogram')
    
    # Theoretical PDF curve
    w_axis = np.linspace(-4, 4, 1000)
    pdf = (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * w_axis**2)
    plt.plot(w_axis, pdf, linewidth=2, color='darkred', label='Theoretical N(0,1) PDF')
    
    plt.title("Rejection Sampling Verification: N(0,1)")
    plt.xlabel("w")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('rejection_sampling_verification.png', dpi=300, bbox_inches='tight')

    plt.show()
    
    # Quick test for General Normal N(mu, sigma^2)
    mu_test = 5.0
    sigma_sq_test = 4.0 # standard deviation = 2.0
    gen_samples, _ = sample_general_normal(10000, mu=mu_test, sigma_sq=sigma_sq_test)
    print(f"\n--- General Normal N({mu_test}, {sigma_sq_test}) Check ---")
    print(f"Sample Mean (Expected {mu_test}): {np.mean(gen_samples):.4f}")
    print(f"Sample Variance (Expected {sigma_sq_test}): {np.var(gen_samples):.4f}")