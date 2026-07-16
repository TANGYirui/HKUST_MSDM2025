import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create a directory to store plots if you want to keep it organized (optional)
# os.makedirs('report_plots', exist_ok=True)
# If using a folder, change filename to 'report_plots/q1_1.png'

# Load data
data = np.loadtxt("sunspots.txt")
months = data[:, 0]
sunspots = data[:, 1]
N = len(sunspots)

# ---------------------------------------------------------
# Part (a): Plot original data
# ---------------------------------------------------------
plt.figure(figsize=(10, 4))
plt.plot(months, sunspots, color='black', linewidth=0.8)
plt.title("Sunspots vs. Time")
plt.xlabel("Months")
plt.ylabel("Number of Sunspots")
plt.grid(True, alpha=0.3)

# Save the first plot
plt.savefig('q1_1.png', dpi=300, bbox_inches='tight')
plt.show() 

# ---------------------------------------------------------
# Part (b): Fourier transform and power spectrum
# ---------------------------------------------------------
# Compute real FFT
c = np.fft.rfft(sunspots)
# Calculate power spectrum (magnitude squared)
power_spectrum = np.abs(c)**2
k_values = np.arange(len(power_spectrum))

plt.figure(figsize=(10, 4))
# We plot a subset (e.g., first 100 k values) to clearly see the peak
# We skip k=0 because it's the DC component (average value), which is usually huge
plt.plot(k_values[1:100], power_spectrum[1:100], color='blue') 
plt.title("Power Spectrum of Sunspot Data")
plt.xlabel("Wave number ($k$)")
plt.ylabel("Magnitude Squared ($|c_k|^2$)")
plt.grid(True, alpha=0.3)

# Save the second plot
plt.savefig('q1_2.png', dpi=300, bbox_inches='tight')
plt.show()

# ---------------------------------------------------------
# Part (c): Find periodicity
# ---------------------------------------------------------
# Find the k corresponding to the maximum power (excluding k=0)
k_peak = np.argmax(power_spectrum[1:]) + 1 
period = N / k_peak

print(f"--- Results for Report ---")
print(f"Total number of months (N): {N}")
print(f"Wave number of the peak (k): {k_peak}")
print(f"Estimated period (T = N/k): {period:.2f} months")
print(f"Estimated period in years: {period/12:.2f} years")