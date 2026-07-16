"""
MSDM5004 Spring 2026 - Project 1 Part I
Heat Equation: u_t = a * u_xx,  a=2,  x in (-1,1)
Boundary: u(-1,t) = u(1,t) = 0
Initial:  u0(x) = (1/3)(x+1)  for x in [-1, 0.5]
                  1 - x        for x in (0.5,  1]

Part (1): Explicit (Forward Euler) scheme
Part (2): Crank-Nicolson scheme solved with Thomas algorithm
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')          # non-interactive backend — works everywhere
import matplotlib.pyplot as plt

# ── parameters ────────────────────────────────────────────────────────────────
a  = 2
J  = 20
dx = 0.1
x  = np.linspace(-1, 1, J + 1)   # 21 points including both boundaries
N  = J - 1                        # 19 interior points

plot_steps = [0, 1, 25, 50]      # time-step indices to record
dt_list    = [0.0025, 0.0026]


# ── helpers ───────────────────────────────────────────────────────────────────
def initial_condition(x):
    u = np.where(x <= 0.5, (x + 1) / 3, 1 - x)
    return u


def thomas_algorithm(sub, main, sup, rhs):
    """
    Solve a tridiagonal system with Thomas algorithm.
    sub  : sub-diagonal,   length n-1
    main : main diagonal,  length n
    sup  : super-diagonal, length n-1
    rhs  : right-hand side, length n
    Returns solution vector x of length n.
    """
    n = len(rhs)
    c = np.zeros(n - 1)
    d = np.zeros(n)
    sol = np.zeros(n)

    # forward sweep
    c[0] = sup[0] / main[0]
    d[0] = rhs[0] / main[0]
    for i in range(1, n):
        denom = main[i] - sub[i - 1] * c[i - 1]
        if i < n - 1:
            c[i] = sup[i] / denom
        d[i] = (rhs[i] - sub[i - 1] * d[i - 1]) / denom

    # back substitution
    sol[-1] = d[-1]
    for i in range(n - 2, -1, -1):
        sol[i] = d[i] - c[i] * sol[i + 1]
    return sol


def make_plot(x, snapshots, plot_steps, dt, title_str, fname):
    """Plot and save one figure."""
    colors = ['tab:blue', 'tab:red', 'tab:green', 'tab:purple']
    fig, ax = plt.subplots(figsize=(7, 5))
    for s, step in enumerate(plot_steps):
        t_val = step * dt
        ax.plot(x, snapshots[s], color=colors[s],
                marker='o', markersize=3, linewidth=1.4,
                label=f't = {t_val:.4f}')
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('u(x, t)', fontsize=12)
    ax.set_title(title_str, fontsize=12)
    ax.legend(loc='best')
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(fname, dpi=150)
    plt.close(fig)
    print(f'Saved: {fname}')


# ── initial condition (full grid and interior) ────────────────────────────────
u0_full = initial_condition(x)
u0      = u0_full[1:-1].copy()   # interior only, length N


# ══════════════════════════════════════════════════════════════════════════════
#  PART (1)  Explicit Scheme
# ══════════════════════════════════════════════════════════════════════════════
print('=== Part (1): Explicit Scheme ===')

for dt in dt_list:
    mu   = dt / dx**2
    amu  = a * mu
    print(f'  dt={dt}, mu={mu:.4f}, a*mu={amu:.4f}  '
          f'({"STABLE" if amu <= 0.5 else "UNSTABLE — a*mu > 0.5"})')

    max_step = max(plot_steps)
    U = u0.copy()

    # store only snapshots — do NOT save every time step
    snapshots = []
    snap_set  = set(plot_steps)

    # t = 0 snapshot
    full = np.concatenate(([0.0], U, [0.0]))
    snap_map = {0: full.copy()}

    for n in range(1, max_step + 1):
        # vectorised explicit update (boundary = 0 padded implicitly)
        U_left  = np.concatenate(([0.0], U[:-1]))
        U_right = np.concatenate((U[1:],  [0.0]))
        U = U + amu * (U_left - 2*U + U_right)

        if n in snap_set:
            snap_map[n] = np.concatenate(([0.0], U, [0.0]))

    ordered = [snap_map[s] for s in plot_steps]

    title = (f'Explicit Scheme,  $\\Delta t={dt}$,  '
             f'$a\\mu={amu:.2f}$')
    fname = f'explicit_dt{dt:.4f}.png'
    make_plot(x, ordered, plot_steps, dt, title, fname)

# ══════════════════════════════════════════════════════════════════════════════
#  PART (2)  Crank-Nicolson + Thomas Algorithm
# ══════════════════════════════════════════════════════════════════════════════
print('\n=== Part (2): Crank-Nicolson + Thomas Algorithm ===')

for dt in dt_list:
    mu = dt / dx**2
    r  = a * mu / 2          # CN parameter
    print(f'  dt={dt}, mu={mu:.4f}, r={r:.4f}  (unconditionally stable)')

    # tridiagonal diagonals of LHS matrix  A = I + r*L
    sub_d  = -r * np.ones(N - 1)
    main_d = (1 + 2*r) * np.ones(N)
    sup_d  = -r * np.ones(N - 1)

    max_step = max(plot_steps)
    U = u0.copy()

    snap_map = {0: np.concatenate(([0.0], U, [0.0]))}
    snap_set = set(plot_steps)

    for n in range(1, max_step + 1):
        # RHS:  b = (I - r*L) U^n   (boundary values = 0)
        rhs        = np.zeros(N)
        rhs[0]     = (1 - 2*r)*U[0]   + r*U[1]          # left:  U_{-1}=0
        rhs[1:-1]  = r*U[:-2] + (1 - 2*r)*U[1:-1] + r*U[2:]
        rhs[-1]    = r*U[-2]  + (1 - 2*r)*U[-1]          # right: U_{N}=0

        U = thomas_algorithm(sub_d, main_d, sup_d, rhs)

        if n in snap_set:
            snap_map[n] = np.concatenate(([0.0], U, [0.0]))

    ordered = [snap_map[s] for s in plot_steps]

    title = f'Crank-Nicolson Scheme,  $\\Delta t={dt}$'
    fname = f'cn_dt{dt:.4f}.png'
    make_plot(x, ordered, plot_steps, dt, title, fname)

print('\nDone! 4 PNG files saved in the current directory.')