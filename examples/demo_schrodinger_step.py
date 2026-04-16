"""
Demo : diffusion d'un paquet gaussien sur un potentiel en marche.

Ce script montre la réflexion et la transmission d'une fonction d'onde
incidente sur un potentiel de type StepPotential.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from quantum_sim.potentials.StepPotential import StepPotential
from quantum_sim.waves.schrodinger_solver import SchrodingerSolver

# ── Grille spatiale ──────────────────────────────────────────────────────────
X_MIN = -100.0
X_MAX = 100.0
N_POINTS = 1201

# ── Paquet gaussien incident ────────────────────────────────────────────────
X0 = -40.0            # centre initial du paquet
SIGMA_X = 8.0         # largeur spatiale
K0 = 8.0             # impulsion centrale positive

# ── Potentiel en marche ────────────────────────────────────────────────────
STEP_POSITION = 0.0
STEP_HEIGHT = 5.0e-38

# ── Paramètres temporels ───────────────────────────────────────────────────
T_FINAL = 2.0e5
DT = 1000.0
ANIM_STEP = 2
INTERVAL_MS = 40

# ── Initialisation ─────────────────────────────────────────────────────────
print("Construction de l'état initial …")
solver = SchrodingerSolver(
    x_min=X_MIN,
    x_max=X_MAX,
    n_points=N_POINTS,
    absorbing_boundaries=True,
)

x = solver.x_grid

psi_0 = np.exp(
    -((x - X0) ** 2) / (4.0 * SIGMA_X ** 2)
    + 1j * K0 * x
).astype(complex)
solver.init_from_array(psi_0, normalize=True)

step = StepPotential(x0=STEP_POSITION, V0=STEP_HEIGHT)
solver.set_potential(step.evaluate(x))

print(f"Potentiel : {step}")
print("Résolution du TDSE …")
result = solver.solve(t_final=T_FINAL, dt=DT)

x = result["x"]
t_arr = result["t"]
psi = result["psi"]
prob = result["prob"]

print(f"  → {len(t_arr)} snapshots calculés")

# ── Aperçu statique ─────────────────────────────────────────────────────────
fig_static, ax_static = plt.subplots(figsize=(10, 4))
checkpoints = np.linspace(0, len(t_arr) - 1, 5, dtype=int)
for idx in checkpoints:
    ax_static.plot(x, prob[:, idx], label=f"t = {t_arr[idx]:.0f}")

V_scaled = step.evaluate(x)
V_scaled = V_scaled / STEP_HEIGHT * np.max(prob) * 0.45
ax_static.plot(x, V_scaled, color="black", lw=1.5, label="Potentiel (échelle)")
ax_static.axvline(STEP_POSITION, color="gray", lw=1, ls="--")
ax_static.set_xlabel("x")
ax_static.set_ylabel("|ψ(x,t)|²")
ax_static.set_title("Réflexion et transmission sur un potentiel en marche")
ax_static.legend(loc="upper right")
ax_static.grid(True)
fig_static.tight_layout()

# ── Animation ──────────────────────────────────────────────────────────────
anim_indices = np.arange(0, len(t_arr), ANIM_STEP)

fig_anim, ax_anim = plt.subplots(figsize=(10, 4))

y_max = np.max(prob) * 1.2
ax_anim.set_xlim(X_MIN, X_MAX)
ax_anim.set_ylim(0, y_max)
ax_anim.set_xlabel("x")
ax_anim.set_ylabel("|ψ(x,t)|²")
ax_anim.set_title("Évolution temporelle du paquet sur la marche de potentiel")
ax_anim.grid(True)
ax_anim.plot(x, V_scaled, color="black", lw=1.0, label="Potentiel (échelle)")
ax_anim.axvline(STEP_POSITION, color="gray", lw=1, ls="--")

(line_prob,) = ax_anim.plot([], [], lw=2, color="royalblue", label="|ψ|²")
(line_re,) = ax_anim.plot([], [], lw=1, color="tomato", label="Re(ψ)", alpha=0.6)
(line_im,) = ax_anim.plot([], [], lw=1, color="seagreen", label="Im(ψ)", alpha=0.6)

time_text = ax_anim.text(0.02, 0.92, "", transform=ax_anim.transAxes, fontsize=10)
ax_anim.legend(loc="upper right")


def _init():
    line_prob.set_data([], [])
    line_re.set_data([], [])
    line_im.set_data([], [])
    time_text.set_text("")
    return line_prob, line_re, line_im, time_text


def _update(frame_idx):
    sol_idx = anim_indices[frame_idx]
    psi_frame = psi[:, sol_idx]
    line_prob.set_data(x, np.abs(psi_frame) ** 2)
    line_re.set_data(x, np.real(psi_frame))
    line_im.set_data(x, np.imag(psi_frame))
    time_text.set_text(f"t = {t_arr[sol_idx]:.0f}")
    return line_prob, line_re, line_im, time_text

anim = FuncAnimation(
    fig_anim,
    _update,
    frames=len(anim_indices),
    init_func=_init,
    interval=INTERVAL_MS,
    blit=True,
)

fig_anim.tight_layout()

print("Animation prête — ferme les fenêtres pour quitter.")
plt.show()
