"""
Demo : évolution libre d'un paquet gaussien (sans potentiel).

L'état initial est construit directement en espace des k (superposition
de N_WAVES ondes planes gaussiennes) de sorte que les k négatifs soient
autorisés — ce qui reproduit fidèlement l'approche du notebook sprint_4.

Lance l'animation matplotlib en fenêtre interactive.

Usage
-----
    python examples/demo_schrodinger_free.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from quantum_sim.waves.schrodinger_solver import SchrodingerSolver

# ── Paramètres de la grille ────────────────────────────────────────────────
X_MIN = -70.0
X_MAX = 70.0
N_POINTS = 801        # impair → x = 0 exactement sur la grille

# ── Paramètres du paquet gaussien ─────────────────────────────────────────
K_CENTER = 0.0        # impulsion centrale nulle → paquet symétrique sur place
SIGMA_K = 1.0         # largeur en espace des k
N_WAVES = 200         # nombre d'ondes planes dans la superposition
X0 = 0.0              # centre spatial initial

# ── Paramètres temporels ──────────────────────────────────────────────────
T_FINAL = 1_000_000     # durée totale de la simulation
DT = 500              # pas de temps entre snapshots

# ── Paramètres de l'animation ─────────────────────────────────────────────
ANIM_STEP = 10        # on affiche 1 frame sur ANIM_STEP snapshots
INTERVAL_MS = 50      # durée d'une frame (ms)

# ══════════════════════════════════════════════════════════════════════════
# 1. État initial : superposition gaussienne en espace des k
#    (construit directement sur la grille pour accepter les k négatifs)
# ══════════════════════════════════════════════════════════════════════════

x_grid_pre = np.linspace(X_MIN, X_MAX, N_POINTS)
dx_pre = x_grid_pre[1] - x_grid_pre[0]

k_values = np.linspace(K_CENTER - 4 * SIGMA_K, K_CENTER + 4 * SIGMA_K, N_WAVES)
amplitudes = np.exp(-((k_values - K_CENTER) ** 2) / (2 * SIGMA_K ** 2))

print("Construction du paquet gaussien …")
psi_0_raw = np.sum(
    amplitudes[:, None] * np.exp(1j * k_values[:, None] * (x_grid_pre[None, :] - X0)),
    axis=0,
).astype(complex)

# ══════════════════════════════════════════════════════════════════════════
# 2. Solveur (sans potentiel)
# ══════════════════════════════════════════════════════════════════════════
print("Initialisation du solveur …")
solver = SchrodingerSolver(
    x_min=X_MIN,
    x_max=X_MAX,
    n_points=N_POINTS,
    absorbing_boundaries=True,
)
solver.init_from_array(psi_0_raw, normalize=True)   # V(x) = 0 par défaut

# ══════════════════════════════════════════════════════════════════════════
# 3. Résolution
# ══════════════════════════════════════════════════════════════════════════
print(f"Résolution TDSE jusqu'à t = {T_FINAL:.2e} …")
result = solver.solve(t_final=T_FINAL, dt=DT)

x       = result["x"]       # (N_POINTS,)
t_arr   = result["t"]       # (n_t,)
prob    = result["prob"]    # (N_POINTS, n_t)   |ψ|²

print(f"  → {len(t_arr)} snapshots calculés.")

# ══════════════════════════════════════════════════════════════════════════
# 4. Aperçu statique : densité à quelques instants
# ══════════════════════════════════════════════════════════════════════════
fig_static, ax_static = plt.subplots(figsize=(10, 4))
checkpoints = np.linspace(0, len(t_arr) - 1, 5, dtype=int)
for idx in checkpoints:
    ax_static.plot(x, prob[:, idx], label=f"t = {t_arr[idx]:.2e}")
ax_static.set_xlabel("x")
ax_static.set_ylabel("|ψ(x,t)|²")
ax_static.set_title("Étalement du paquet gaussien libre")
ax_static.legend()
ax_static.grid(True)
fig_static.tight_layout()

# ══════════════════════════════════════════════════════════════════════════
# 5. Animation
# ══════════════════════════════════════════════════════════════════════════
anim_indices = np.arange(0, len(t_arr), ANIM_STEP)

fig_anim, ax_anim = plt.subplots(figsize=(10, 4))

y_max = np.max(prob) * 1.15
ax_anim.set_xlim(X_MIN, X_MAX)
ax_anim.set_ylim(0, y_max)
ax_anim.set_xlabel("x")
ax_anim.set_ylabel("|ψ(x,t)|²")
ax_anim.set_title("Évolution du paquet gaussien sans potentiel")
ax_anim.grid(True)

(line_prob,) = ax_anim.plot([], [], lw=2, color="royalblue", label="|ψ|²")
(line_re,)   = ax_anim.plot([], [], lw=1, color="tomato",    label="Re(ψ)", alpha=0.6)
(line_im,)   = ax_anim.plot([], [], lw=1, color="seagreen",  label="Im(ψ)", alpha=0.6)
time_text    = ax_anim.text(0.02, 0.93, "", transform=ax_anim.transAxes, fontsize=10)
ax_anim.legend(loc="upper right")

psi_full = result["psi"]   # (N_POINTS, n_t)  complex


def _init():
    line_prob.set_data([], [])
    line_re.set_data([], [])
    line_im.set_data([], [])
    time_text.set_text("")
    return line_prob, line_re, line_im, time_text


def _update(frame_idx):
    sol_idx = anim_indices[frame_idx]
    psi = psi_full[:, sol_idx]
    line_prob.set_data(x, np.abs(psi) ** 2)
    line_re.set_data(x, np.real(psi))
    line_im.set_data(x, np.imag(psi))
    time_text.set_text(f"t = {t_arr[sol_idx]:.2e}")
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
