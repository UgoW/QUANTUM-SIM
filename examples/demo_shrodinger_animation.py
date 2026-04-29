from quantum_sim import GaussianWavePacket, SchrodingerSolver
from quantum_sim.utils.constants import ELECTRON_MASS
from quantum_sim.potentials.StepPotential import StepPotential
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Paramètres de la simulation
x_min, x_max = -70.0, 70.0
n_points = 801

# Création d'un paquet d'ondes gaussien
packet = GaussianWavePacket(
    k_center=0.0,
    sigma_k=1,
    n_waves=200,
    position_center=0.0,
    time=0.0,
    mass=ELECTRON_MASS,
)

# Configuration du solveur de Schrödinger
solver = SchrodingerSolver(
    x_min=x_min,
    x_max=x_max,
    n_points=n_points,
    mass=ELECTRON_MASS,
    absorbing_boundaries=False,
    absorb_width=5.0,
    gamma_cap=8e13,
)

# Potentiel pour un potentiel en marche
step = StepPotential(x0=15.0, V0=5e-37)
V = step.evaluate(solver.x_grid)
solver.set_potential(V)
solver.init_from_packet(packet)

# Résolution de l'équation de Schrödinger pour faire évoluer le paquet d'ondes dans le temps
result = solver.solve(t_final=1_000_000, dt=500, method="RK45")

# Extraction des résultats pour l'affichage
x = result["x"]
t = result["t"]
prob = result["prob"]

# Animation de la densité de probabilité dans le temps
fig, ax = plt.subplots(figsize=(10, 4))
x_nm = x * 1e9
y_max = float(np.max(prob) * 1.15)

# Potentiel en marche (mis à l'échelle pour l'affichage)
potential_scaled = V / np.max(V) * np.max(prob)
ax.plot(x_nm, potential_scaled, color='k', lw=1.5, alpha=0.8, label='Step Potential')

(line_prob,) = ax.plot([], [], color='royalblue', lw=2.0, label=r'$|\psi(x,t)|^2$')
time_text = ax.text(0.02, 0.92, '', transform=ax.transAxes)

ax.set_xlim(x_nm.min(), x_nm.max())
ax.set_ylim(0.0, y_max)
ax.set_xlabel('x (nm)')
ax.set_ylabel(r'$|\psi(x,t)|^2$')
ax.set_title("Propagation d'un paquet gaussien dans un potentiel en marche")
ax.grid(True, alpha=0.3)
ax.legend(loc='upper right')

# Sous-échantillonnage des frames pour fluidifier l'animation
frame_step = max(1, len(t) // 300)
frame_indices = np.arange(0, len(t), frame_step)

def _init_anim():
    line_prob.set_data([], [])
    time_text.set_text('')
    return line_prob, time_text

def _update_anim(frame):
    idx = frame_indices[frame]
    line_prob.set_data(x_nm, prob[:, idx])
    time_text.set_text(f't = {t[idx]:.2e} s')
    return line_prob, time_text

anim = FuncAnimation(
    fig,
    _update_anim,
    init_func=_init_anim,
    frames=len(frame_indices),
    interval=40,
    blit=True,
    repeat=True,
)

plt.tight_layout()
plt.show()