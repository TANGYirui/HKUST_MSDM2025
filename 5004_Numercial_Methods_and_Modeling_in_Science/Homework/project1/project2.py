"""
MSDM5004 Spring 2026 - Project 1 Part II
Advection equation: u_t + 1.8*u_x = 0,  x in (-2, 2)
Initial:   u0(x) = 1 if x<=0, 0 if x>0
Boundary:  u(-2,t)=1,  u(2,t)=0
nu = dt/dx = 0.25  =>  dx = 4*dt

Methods: (1) Upwind  (2) Lax-Wendroff
Plot solution at t = 0.5 for dt = 0.01 and dt = 0.0025
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── parameters ────────────────────────────────────────────────────────────────
c      = 1.8          # wave speed
nu     = 0.25         # CFL-like ratio: nu = dt/dx  (given)
t_end  = 0.5
dt_list = [0.01, 0.0025]


# ── helpers ───────────────────────────────────────────────────────────────────
def make_grid(dt):
    dx = dt / nu                        # dx = 4*dt
    x  = np.arange(-2, 2 + dx/2, dx)   # includes both endpoints
    return x, dx

def initial_condition(x):
    return np.where(x <= 0, 1.0, 0.0)

def exact_solution(x, t):
    # right-travelling wave: shift x by c*t
    return np.where(x - c*t <= 0, 1.0, 0.0)

def upwind(u, c, dt, dx):
    """First-order upwind scheme (c > 0: left-biased)."""
    r = c * dt / dx                     # Courant number = c*nu
    # U_j^{n+1} = U_j^n - r*(U_j^n - U_{j-1}^n)
    u_new = u.copy()
    u_new[1:] = u[1:] - r * (u[1:] - u[:-1])
    u_new[0]  = 1.0   # left BC
    return u_new

def lax_wendroff(u, c, dt, dx):
    """Lax-Wendroff scheme."""
    r = c * dt / dx
    u_new = u.copy()
    # interior: j = 1, ..., N-2  (keep boundaries fixed)
    u_new[1:-1] = (u[1:-1]
                   - 0.5*r  * (u[2:] - u[:-2])
                   + 0.5*r**2 * (u[2:] - 2*u[1:-1] + u[:-2]))
    u_new[0]  = 1.0   # left BC
    u_new[-1] = 0.0   # right BC
    return u_new

def run_scheme(scheme_fn, dt):
    x, dx = make_grid(dt)
    u = initial_condition(x)
    n_steps = round(t_end / dt)
    # do NOT store every time step — just march forward
    for _ in range(n_steps):
        u = scheme_fn(u, c, dt, dx)
    return x, u

def make_plot(x_num, u_num, dt, method_name, fname):
    x_ex = np.linspace(-2, 2, 2000)
    u_ex = exact_solution(x_ex, t_end)
    r    = c * dt / (dt / nu)           # Courant number = c*nu
    dx   = dt / nu

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(x_ex, u_ex, 'k-',  linewidth=1.5, label='Exact solution')
    ax.plot(x_num, u_num, 'b-o', markersize=3, linewidth=1.2,
            label=f'{method_name}  ($\\Delta t={dt}$, $\\Delta x={dx:.4f}$)')
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('u(x, 0.5)', fontsize=12)
    ax.set_title(f'{method_name},  $\\Delta t={dt}$,  '
                 f'Courant $= c\\nu = {r:.3f}$', fontsize=12)
    ax.legend(loc='center right')
    ax.set_xlim(-2, 2); ax.set_ylim(-0.2, 1.3)
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(fname, dpi=150)
    plt.close(fig)
    print(f'Saved: {fname}')


# ── main ──────────────────────────────────────────────────────────────────────
print('=== Part (1): Upwind Method ===')
for dt in dt_list:
    x, u = run_scheme(upwind, dt)
    make_plot(x, u, dt, 'Upwind Method', f'upwind_dt{dt:.4f}.png')

print('\n=== Part (2): Lax-Wendroff Method ===')
for dt in dt_list:
    x, u = run_scheme(lax_wendroff, dt)
    make_plot(x, u, dt, 'Lax-Wendroff Method', f'lw_dt{dt:.4f}.png')

print('\nDone! 4 PNG files saved.')
