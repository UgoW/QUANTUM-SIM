from quantum_sim import GaussianWavePacket, SchrodingerSolver
from quantum_sim.utils.constants import ELECTRON_MASS
import matplotlib.pyplot as plt
import numpy as np

# Paramètres de la simulation
x_min, x_max = -40e-9, 40e-9
n_points = 1201

# Création d'un paquet d'ondes gaussien
packet = GaussianWavePacket(
    k_center=8e9,
    sigma_k=8e8,
    n_waves=121,
    position_center=-20e-9,
    time=0.0,
    mass=ELECTRON_MASS,
)

# Configuration du solveur de Schrödinger
solver = SchrodingerSolver(
    x_min=x_min,
    x_max=x_max,
    n_points=n_points,
    mass=ELECTRON_MASS,
    absorbing_boundaries=True,
    absorb_width=8e-9,
    gamma_cap=8e13,
)

# Potentiel nul pour une particule libre
solver.set_potential(np.zeros(n_points))
solver.init_from_packet(packet)

# Résolution de l'équation de Schrödinger pour faire évoluer le paquet d'ondes dans le temps
result = solver.solve(t_final=6e-15, dt=2e-17, method="RK45")

# Extraction des résultats pour l'affichage
x = result["x"]
t = result["t"]
prob = result["prob"]

# Affichage de la densité de probabilité à différents instants
fig, ax = plt.subplots(figsize=(10, 4))
indices = np.linspace(0, len(t) - 1, 5, dtype=int)
colors = plt.cm.plasma(np.linspace(0, 1, len(indices)))

# Affichage de la densité de probabilité à différents instants
for idx, c in zip(indices, colors):
    ax.plot(x * 1e9, prob[:, idx], color=c, lw=1.8, label=f't = {t[idx]:.2e} s')

# Configuration de l'affichage
ax.set_xlabel('x (nm)')
ax.set_ylabel(r'$|\psi(x,t)|^2$')
ax.set_title("Propagation d'un paquet gaussien")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
