import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from tqdm import tqdm

np.random.seed(3042)

def simulate_abp(dt, total_time, v, D_R):
    """
    Simulate an Active Brownian Particle using Euler-Maruyama method
    
    Parameters:
    dt: time step
    total_time: total simulation time
    v: active velocity
    D_R: rotational diffusion coefficient
    
    Returns:
    t: time array
    x, y: position coordinates
    phi: orientation angle
    """
    steps = int(total_time / dt)
    t = np.linspace(0, total_time, steps)
    
    x = np.zeros(steps)
    y = np.zeros(steps)
    phi = np.zeros(steps)
    
    noise_amp = np.sqrt(2 * D_R * dt)
    
    for i in range(1, steps):
        phi[i] = phi[i-1] + noise_amp * np.random.normal()
        x[i] = x[i-1] + v * np.cos(phi[i]) * dt
        y[i] = y[i-1] + v * np.sin(phi[i]) * dt
    
    return t, x, y, phi

def compute_directional_autocorrelation(phi, dt, max_lag_time=None):
    """
    Compute the directional autocorrelation function <n(t+s)·n(s)>
    
    Parameters:
    phi: orientation angles
    dt: time step
    max_lag_time: maximum lag time for correlation calculation
    
    Returns:
    lag_times: lag times
    autocorr: autocorrelation values
    """
    steps = len(phi)
    if max_lag_time is None:
        max_lag_time = steps // 10
    max_lag = int(max_lag_time / dt)
    
    n_x = np.cos(phi)
    n_y = np.sin(phi)
    
    autocorr = np.zeros(max_lag)
    lag_times = np.arange(max_lag) * dt
    
    for lag in range(max_lag):
        dot_products = n_x[lag:] * n_x[:-lag or None] + n_y[lag:] * n_y[:-lag or None]
        autocorr[lag] = np.mean(dot_products)
    
    return lag_times, autocorr

def exponential_decay(t, tau):
    """Exponential decay function for fitting"""
    return np.exp(-t / tau)

def analyze_autocorrelation_for_different_DR():
    dt = 0.01
    total_time = 200.0
    D_R_values = [0.01, 0.05, 0.1, 0.2, 0.5]
    tau_R_measured = []
    num_ensembles = 20
    
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    
    for D_R in D_R_values:
        all_autocorr = []
        theoretical_tau = 1/D_R
        
        for _ in tqdm(range(num_ensembles), desc=f"D_R={D_R}"):
            t, x, y, phi = simulate_abp(dt, total_time, 1.0, D_R)
            max_lag_time = min(5*theoretical_tau, total_time/2)
            lag_times, autocorr = compute_directional_autocorrelation(phi, dt, max_lag_time)
            all_autocorr.append(autocorr)
        
        avg_autocorr = np.mean(all_autocorr, axis=0)
        
        fit_range = (lag_times < 3*theoretical_tau) & (avg_autocorr > 0.05)
        if np.sum(fit_range) > 5:
            popt, pcov = curve_fit(exponential_decay, lag_times[fit_range], avg_autocorr[fit_range], p0=[theoretical_tau])
            tau_fit = popt[0]
            tau_R_measured.append(tau_fit)
            
            plt.plot(lag_times, avg_autocorr, 'o', markersize=2, alpha=0.7, 
                    label=f'D_R={D_R} (τ_R={tau_fit:.2f})')
            plt.plot(lag_times, exponential_decay(lag_times, tau_fit), '-', 
                    label=f'Fit: τ_R={tau_fit:.2f} (1/D_R={1/D_R:.2f})')
        else:
            tau_R_measured.append(np.nan)
    
    plt.xlabel('Lag time t')
    plt.ylabel('Directional autocorrelation <n(t+s)·n(s)>')
    plt.title('Directional Autocorrelation Function')
    plt.legend(fontsize=8)
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    theoretical_tau = 1/np.array(D_R_values)
    
    valid_indices = [i for i, tau in enumerate(tau_R_measured) if not np.isnan(tau)]
    if valid_indices:
        plt.plot(theoretical_tau[valid_indices], np.array(tau_R_measured)[valid_indices], 'o-', 
                label='Measured τ_R')
    
    plt.plot(theoretical_tau, theoretical_tau, 'r--', label='Theoretical τ_R = 1/D_R')
    plt.xlabel('Theoretical τ_R = 1/D_R')
    plt.ylabel('Measured τ_R')
    plt.title('Verification of τ_R = 1/D_R')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    
    plt.tight_layout()
    plt.savefig('autocorrelation_analysis.png', dpi=300)
    plt.show()
    
    return D_R_values, tau_R_measured

def compute_msd(x, y, dt, max_lag_time=None):
    """
    Compute the mean square displacement (MSD)
    
    Parameters:
    x, y: position coordinates
    dt: time step
    max_lag_time: maximum lag time for MSD calculation
    
    Returns:
    lag_times: lag times
    msd: MSD values
    """
    steps = len(x)
    if max_lag_time is None:
        max_lag_time = 20.0
    max_lag = int(min(max_lag_time / dt, steps // 5))
    
    msd = np.zeros(max_lag)
    lag_times = np.arange(max_lag) * dt
    
    for lag in range(1, max_lag):
        if steps - lag < 10:
            break
            
        dx = x[lag:] - x[:-lag]
        dy = y[lag:] - y[:-lag]
        msd[lag] = np.mean(dx*dx + dy*dy)
    
    return lag_times, msd

def analyze_msd_for_different_parameters():
    dt = 0.01
    total_time = 50.0
    num_ensembles = 20
    
    parameter_sets = [
        (0.5, 0.1),
        (1.0, 0.1),
        (1.0, 0.2),
        (2.0, 0.1)
    ]
    
    plt.figure(figsize=(14, 6))
    
    plt.subplot(1, 2, 1)
    
    for v, D_R in parameter_sets:
        tau_R = 1.0 / D_R
        max_lag_time = 20.0
        
        all_msd = []
        for _ in tqdm(range(num_ensembles), desc=f"MSD ensemble (v={v}, D_R={D_R})"):
            t, x, y, phi = simulate_abp(dt, total_time, v, D_R)
            lag_times, msd = compute_msd(x, y, dt, max_lag_time)
            all_msd.append(msd)
        
        avg_msd = np.mean(all_msd, axis=0)
        
        plt.plot(lag_times[1:], avg_msd[1:], 'o', markersize=3, 
                label=f'v={v}, D_R={D_R} (τ_R={tau_R:.1f})')
        
        ballistic_mask = lag_times < 0.1 * tau_R
        if np.any(ballistic_mask):
            plt.plot(lag_times[ballistic_mask], v**2 * lag_times[ballistic_mask]**2, '--', 
                    label=f'Theory (ballistic): v²t² (v={v})')
        
        diffusive_mask = lag_times > 3 * tau_R
        if np.any(diffusive_mask) and np.max(lag_times) > 3 * tau_R:
            plt.plot(lag_times[diffusive_mask], 2 * v**2 * tau_R * lag_times[diffusive_mask], '-', 
                    label=f'Theory (diffusive): 2v²τ_Rt (v={v}, τ_R={tau_R:.1f})')
    
    plt.xlabel('Time lag t')
    plt.ylabel('MSD(t)')
    plt.title('MSD in Linear Scale (Ballistic to Diffusive Transition)')
    plt.legend(fontsize=8)
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    
    for v, D_R in parameter_sets:
        tau_R = 1.0 / D_R
        max_lag_time = 100.0
        
        all_msd = []
        for _ in range(num_ensembles):
            t, x, y, phi = simulate_abp(dt, total_time, v, D_R)
            lag_times, msd = compute_msd(x, y, dt, max_lag_time)
            all_msd.append(msd)
        
        avg_msd = np.mean(all_msd, axis=0)
        
        plt.loglog(lag_times[1:], avg_msd[1:], 'o', markersize=3, 
                  label=f'v={v}, D_R={D_R} (τ_R={tau_R:.1f})')
        
        diffusive_mask = lag_times > 3 * tau_R
        if np.any(diffusive_mask) and np.max(lag_times) > 3 * tau_R:
            plt.loglog(lag_times[diffusive_mask], 2 * v**2 * tau_R * lag_times[diffusive_mask], '-', 
                      label=f'Theory: 2v²τ_Rt (v={v}, τ_R={tau_R:.1f})')
        
        if v == parameter_sets[0][0] and D_R == parameter_sets[0][1]:
            ref_t = np.logspace(-2, 2, 100)
            ballistic_ref = v**2 * ref_t**2
            plt.loglog(ref_t, ballistic_ref, 'k--', alpha=0.5, label='Reference: ~t²')
            v0, D_R0 = parameter_sets[0]
            tau_R0 = 1/D_R0
            diffusive_ref = 2 * v0**2 * tau_R0 * ref_t
            plt.loglog(ref_t, diffusive_ref, 'k-.', alpha=0.5, label='Reference: ~t')

    
    plt.xlabel('Time lag t')
    plt.ylabel('MSD(t)')
    plt.title('MSD in Log-Log Scale')
    plt.legend(fontsize=8)
    plt.grid(True, which="both", ls="-")
    
    plt.tight_layout()
    plt.savefig('msd_analysis_complete.png', dpi=300)
    plt.draw()
    plt.pause(0.001)
    plt.show()
    
    return parameter_sets

def main():
    print("Starting Active Brownian Particle simulation analysis...")
    
    print("\n1. Analyzing directional autocorrelation function...")
    D_R_values, tau_R_measured = analyze_autocorrelation_for_different_DR()
    
    print("\nMeasured τ_R values:")
    for D_R, tau_R in zip(D_R_values, tau_R_measured):
        print(f"D_R = {D_R:.3f}, Measured τ_R = {tau_R:.3f}, Theoretical τ_R = {1/D_R:.3f}")
    
    print("\n2. Analyzing mean square displacement (MSD)...")
    parameter_sets = analyze_msd_for_different_parameters()
    
    print("\nAnalysis complete. Figures have been saved.")

if __name__ == "__main__":
    main()