import numpy as np
from scipy.fft import dstn, idstn
import matplotlib.pyplot as plt
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ── 1. 网格设置 ──────────────────────────────────────────────────────
Lx, Ly = 1.0, 2.0
dx = dy = 0.01   # delta <= 0.01

# 内部节点数
Nx = int(Lx / dx) - 1   # 99
Ny = int(Ly / dy) - 1   # 199

# 内部节点坐标
x = np.linspace(dx, Lx - dx, Nx)
y = np.linspace(dy, Ly - dy, Ny)
X, Y = np.meshgrid(x, y, indexing='ij')   # shape: (Nx, Ny)

# ── 2. 边界条件齐次化 ─────────────────────────────────────────────────
# 令 phi = u + g，其中 g(x,y) = (y/2) * sqrt(1-x^2)
# g 满足所有边界条件，u 四边全为 0，可以用 DST

g = (Y / 2.0) * np.sqrt(1.0 - X**2)

# g 的拉普拉斯（解析求导）
lap_g = -(Y / 2.0) / (1.0 - X**2)**1.5

# ── 3. 源项 rho ───────────────────────────────────────────────────────
rho = np.zeros((Nx, Ny))
rho[(X >= 0.25) & (X < 0.5) & (Y >= 1.25) & (Y < 1.5)] = 16 * np.pi

# ── 4. 修正后的右端项 ─────────────────────────────────────────────────
rho_tilde = rho - lap_g

# ── 5. 谱方法求解（DST-I）────────────────────────────────────────────
# 对 rho_tilde 做二维 DST
rho_hat = dstn(rho_tilde, type=1)

# 计算本征值 lambda_m + mu_n
m = np.arange(1, Nx + 1)
n = np.arange(1, Ny + 1)
lam = (2 / dx**2) * (np.cos(m * np.pi / (Nx + 1)) - 1)   # shape (Nx,)
mu  = (2 / dy**2) * (np.cos(n * np.pi / (Ny + 1)) - 1)   # shape (Ny,)
LAM, MU = np.meshgrid(lam, mu, indexing='ij')

# 谱空间除以本征值
u_hat = rho_hat / (LAM + MU)

# 逆 DST 得到 u
u = idstn(u_hat, type=1)

# ── 6. 还原 phi = u + g ───────────────────────────────────────────────
phi_interior = u + g

# ── 7. 拼上边界，组成完整网格 ─────────────────────────────────────────
x_full = np.linspace(0, Lx, Nx + 2)
y_full = np.linspace(0, Ly, Ny + 2)
X_full, Y_full = np.meshgrid(x_full, y_full, indexing='ij')

phi = np.zeros((Nx + 2, Ny + 2))
phi[1:-1, 1:-1] = phi_interior
phi[:, -1] = np.sqrt(np.maximum(1.0 - x_full**2, 0.0))  # y=2 边界

# ── 8. 画图 ───────────────────────────────────────────────────────────
plt.figure(figsize=(6, 5))
plt.contourf(X_full, Y_full, phi, levels=50, cmap='jet')
plt.colorbar(label='φ(x, y)')
plt.contour(X_full, Y_full, phi, levels=15, colors='k', linewidths=0.5)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Poisson Equation - Spectral Method')
plt.tight_layout()
plt.savefig('q4_1.png', dpi=150)
plt.show()
print("Image saved as q4_1.png")