from quantum_sim import GaussianWavePacket, SchrodingerSolver
from quantum_sim.utils.constants import ELECTRON_MASS
from quantum_sim.potentials.StepPotential import StepPotential
import matplotlib.pyplot as plt
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

# Affichage de la densité de probabilité à différents instants
fig, ax = plt.subplots(figsize=(10, 4))
indices = np.linspace(0, len(t) - 1, 5, dtype=int)
colors = plt.cm.plasma(np.linspace(0, 1, len(indices)))

# Affichage de la densité de probabilité à différents instants
for idx, c in zip(indices, colors):
    ax.plot(x * 1e9, prob[:, idx], color=c, lw=1.8, label=f't = {t[idx]:.2e} s')

# Affichage du potentiel en marche
ax.plot(x * 1e9, V / np.max(V) * np.max(prob), color='k', lw=1.5, label='Step Potential')

# Configuration de l'affichage
ax.set_xlabel('x (nm)')
ax.set_ylabel(r'$|\psi(x,t)|^2$')
ax.set_title("Propagation d'un paquet gaussien dans un potentiel en marche")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
