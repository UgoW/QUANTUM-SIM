"""
Demo : évolution d'un paquet gaussien — FreePotential puis InfiniteWell.

Partie 1 : potentiel nul (FreePotential) — étalement libre.
Partie 2 : puits de potentiel infini (InfiniteWell) — rebonds sur les parois.

L'état initial est construit directement en espace des k (superposition
de N_WAVES ondes planes gaussiennes).

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from matplotlib.patches import Rectangle

from quantum_sim.potentials.FreePotential import FreePotential
from quantum_sim.potentials.InfiniteWell import InfiniteWell
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

# ── Paramètres du puits de potentiel infini ───────────────────────────────
WELL_A = -15.0          # bord gauche du puits
WELL_B = 15.0           # bord droit du puits
K_CENTER_WELL = 0.0     # impulsion centrale nulle → étalement symétrique sur place
SIGMA_K_WELL = 0.5      # largeur en espace des k (puits)
N_WAVES_WELL = 200      # nombre d'ondes planes (puits)
X0_WELL = 0.0           # centre spatial initial (milieu du puits)
T_FINAL_WELL = 1_000_000  # même durée que le cas libre → plusieurs rebonds
DT_WELL = 500           # même pas que le cas libre
ANIM_STEP_WELL = 10     # même cadence d'affichage que le cas libre

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
# 2. Solveur avec FreePotential (V(x) = 0 partout)
# ══════════════════════════════════════════════════════════════════════════
print("Initialisation du solveur …")
solver = SchrodingerSolver(
    x_min=X_MIN,
    x_max=X_MAX,
    n_points=N_POINTS,
    absorbing_boundaries=True,
)
solver.init_from_array(psi_0_raw, normalize=True)

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

# ══════════════════════════════════════════════════════════════════════════
# ██  PARTIE 2 — PUITS DE POTENTIEL INFINI (InfiniteWell)
# ══════════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════════
# 6. État initial : superposition gaussienne en espace des k (puits)
# ══════════════════════════════════════════════════════════════════════════

x_grid_well = np.linspace(X_MIN, X_MAX, N_POINTS)

k_values_w  = np.linspace(K_CENTER_WELL - 4 * SIGMA_K_WELL,
                           K_CENTER_WELL + 4 * SIGMA_K_WELL, N_WAVES_WELL)
amplitudes_w = np.exp(-((k_values_w - K_CENTER_WELL) ** 2) / (2 * SIGMA_K_WELL ** 2))

print("\nConstruction du paquet gaussien (puits) …")
psi_0_well = np.sum(
    amplitudes_w[:, None] * np.exp(1j * k_values_w[:, None] * (x_grid_well[None, :] - X0_WELL)),
    axis=0,
).astype(complex)

# Annuler le paquet en dehors du puits (conditions aux limites)
psi_0_well[x_grid_well < WELL_A] = 0.0
psi_0_well[x_grid_well > WELL_B] = 0.0

# ══════════════════════════════════════════════════════════════════════════
# 7. Solveur avec InfiniteWell
# ══════════════════════════════════════════════════════════════════════════
print("Initialisation du solveur (puits) …")
# V_wall doit être adapté aux constantes SI du solveur (hbar ≈ 1.055e-34) :
# V_wall < 5*hbar/DT pour la stabilité RK45, ET >> E_kin = hbar²k²/(2m) ≈ 6e-39
# V_wall = 5e-37 : 172× E_kin (confinement parfait) et stable avec DT=500
solver_w = SchrodingerSolver(
    x_min=X_MIN,
    x_max=X_MAX,
    n_points=N_POINTS,
    absorbing_boundaries=False,
)
solver_w.set_potential(InfiniteWell(a=WELL_A, b=WELL_B, V_wall=5e-37).evaluate(solver_w.x_grid))
solver_w.init_from_array(psi_0_well, normalize=True)

# ══════════════════════════════════════════════════════════════════════════
# 8. Résolution
# ══════════════════════════════════════════════════════════════════════════
print(f"Résolution TDSE jusqu'à t = {T_FINAL_WELL:.2e} (puits) …")
result_w = solver_w.solve(t_final=T_FINAL_WELL, dt=DT_WELL)

x_w        = result_w["x"]
t_arr_w    = result_w["t"]
prob_w     = result_w["prob"]
psi_full_w = result_w["psi"]

print(f"  → {len(t_arr_w)} snapshots calculés.")

# ══════════════════════════════════════════════════════════════════════════
# 9. Aperçu statique : densité à quelques instants (puits)
# ══════════════════════════════════════════════════════════════════════════
fig_static_w, ax_static_w = plt.subplots(figsize=(10, 4))
checkpoints_w = np.linspace(0, len(t_arr_w) - 1, 5, dtype=int)
for idx in checkpoints_w:
    ax_static_w.plot(x_w, prob_w[:, idx], label=f"t = {t_arr_w[idx]:.2e}")
for wall in (WELL_A, WELL_B):
    ax_static_w.axvline(wall, color="black", lw=2, ls="--", alpha=0.7)
ax_static_w.set_xlim(X_MIN, X_MAX)
ax_static_w.set_ylim(0, np.max(prob_w) * 1.15)
ax_static_w.set_xlabel("x")
ax_static_w.set_ylabel("|ψ(x,t)|²")
ax_static_w.set_title("Rebonds du paquet gaussien dans un puits infini")
ax_static_w.legend()
ax_static_w.grid(True)
fig_static_w.tight_layout()

# ══════════════════════════════════════════════════════════════════════════
# 10. Animation (puits)
# ══════════════════════════════════════════════════════════════════════════
anim_indices_w = np.arange(0, len(t_arr_w), ANIM_STEP_WELL)

fig_anim_w, ax_anim_w = plt.subplots(figsize=(10, 4))

y_max_w = np.max(prob_w) * 1.15
ax_anim_w.set_xlim(X_MIN, X_MAX)
ax_anim_w.set_ylim(0, y_max_w)
ax_anim_w.set_xlabel("x")
ax_anim_w.set_ylabel("|ψ(x,t)|²")
ax_anim_w.set_title("Évolution du paquet gaussien dans un puits de potentiel infini")
ax_anim_w.grid(True)

wall_color = "lightgray"
ax_anim_w.add_patch(Rectangle((X_MIN, 0), WELL_A - X_MIN, y_max_w, color=wall_color, zorder=0))
ax_anim_w.add_patch(Rectangle((WELL_B, 0), X_MAX - WELL_B, y_max_w, color=wall_color, zorder=0))
ax_anim_w.axvline(WELL_A, color="black", lw=2, ls="--", alpha=0.7, label="Parois")
ax_anim_w.axvline(WELL_B, color="black", lw=2, ls="--", alpha=0.7)

(line_prob_w,) = ax_anim_w.plot([], [], lw=2, color="royalblue", label="|ψ|²",   zorder=3)
(line_re_w,)   = ax_anim_w.plot([], [], lw=1, color="tomato",    label="Re(ψ)", alpha=0.6, zorder=2)
(line_im_w,)   = ax_anim_w.plot([], [], lw=1, color="seagreen",  label="Im(ψ)", alpha=0.6, zorder=2)
time_text_w    = ax_anim_w.text(0.02, 0.93, "", transform=ax_anim_w.transAxes, fontsize=10)
ax_anim_w.legend(loc="upper right")


def _init_w():
    line_prob_w.set_data([], [])
    line_re_w.set_data([], [])
    line_im_w.set_data([], [])
    time_text_w.set_text("")
    return line_prob_w, line_re_w, line_im_w, time_text_w


def _update_w(frame_idx):
    sol_idx = anim_indices_w[frame_idx]
    psi = psi_full_w[:, sol_idx]
    line_prob_w.set_data(x_w, np.abs(psi) ** 2)
    line_re_w.set_data(x_w, np.real(psi))
    line_im_w.set_data(x_w, np.imag(psi))
    time_text_w.set_text(f"t = {t_arr_w[sol_idx]:.2e}")
    return line_prob_w, line_re_w, line_im_w, time_text_w


anim_w = FuncAnimation(
    fig_anim_w,
    _update_w,
    frames=len(anim_indices_w),
    init_func=_init_w,
    interval=INTERVAL_MS,
    blit=False,
)

fig_anim_w.tight_layout()

# ══════════════════════════════════════════════════════════════════════════
# 11. Animation 3D (puits) — hélice complexe  x / Re(ψ) / Im(ψ)
#     Axe x  : position
#     Axe y  : Re(ψ)  (partie réelle)
#     Axe z  : Im(ψ)  (partie imaginaire)
#     Ombre  : |ψ|² projetée sur le plan z=z_min  (densité de probabilité)
# ══════════════════════════════════════════════════════════════════════════
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

fig_3d  = plt.figure(figsize=(11, 6))
ax_3d   = fig_3d.add_subplot(111, projection="3d")

# Limites fixes pour toute l'animation
amp_max  = np.max(np.abs(psi_full_w)) * 1.1
prob_max = np.max(prob_w) * 1.1
z_floor  = -amp_max * 1.1   # plancher pour l'ombre |ψ|²

ax_3d.set_xlim(WELL_A, WELL_B)
ax_3d.set_ylim(-amp_max, amp_max)
ax_3d.set_zlim(z_floor, amp_max)
ax_3d.set_xlabel("x")
ax_3d.set_ylabel("Re(ψ)")
ax_3d.set_zlabel("Im(ψ)")
ax_3d.set_title("Vue 3D — fonction d'onde dans le puits infini")

# Parois verticales (plans x = WELL_A et x = WELL_B)
for wall_x in (WELL_A, WELL_B):
    yy, zz = np.meshgrid([-amp_max, amp_max], [z_floor, amp_max])
    ax_3d.plot_surface(
        np.full_like(yy, wall_x), yy, zz,
        alpha=0.08, color="gray", zorder=0,
    )

# Lignes de référence (axes Re=0, Im=0)
ax_3d.plot([WELL_A, WELL_B], [0, 0], [0, 0],
           color="black", lw=0.8, ls="--", alpha=0.4)

# Objets dynamiques (initialisés vides)
(helix_line,)  = ax_3d.plot([], [], [], lw=2,   color="royalblue",  label="ψ(x,t)")
(shadow_line,) = ax_3d.plot([], [], [], lw=1.5, color="royalblue",  alpha=0.25,
                             linestyle="-", label="|ψ|² (ombre)")
(re_proj,)     = ax_3d.plot([], [], [], lw=1,   color="tomato",     alpha=0.5,
                             label="Re(ψ) proj.")
(im_proj,)     = ax_3d.plot([], [], [], lw=1,   color="seagreen",   alpha=0.5,
                             label="Im(ψ) proj.")
tt_3d = ax_3d.text2D(0.02, 0.95, "", transform=ax_3d.transAxes, fontsize=10)
ax_3d.legend(loc="upper right", fontsize=8)

# Sous-échantillonnage spatial pour fluidité (tous les 2 pts)
stride = 2
x_w_s  = x_w[::stride]
mask_w = (x_w_s >= WELL_A) & (x_w_s <= WELL_B)
x_w_in = x_w_s[mask_w]


def _init_3d():
    for ln in (helix_line, shadow_line, re_proj, im_proj):
        ln.set_data([], [])
        ln.set_3d_properties([])
    tt_3d.set_text("")
    return helix_line, shadow_line, re_proj, im_proj, tt_3d


def _update_3d(frame_idx):
    si  = anim_indices_w[frame_idx]
    psi = psi_full_w[::stride, si][mask_w]

    re  = np.real(psi)
    im  = np.imag(psi)
    amp = np.abs(psi) ** 2

    # Hélice 3D  (x, Re, Im)
    helix_line.set_data(x_w_in, re)
    helix_line.set_3d_properties(im)

    # Ombre |ψ|² sur le plancher  (x, amp, z_floor)
    shadow_line.set_data(x_w_in, amp)
    shadow_line.set_3d_properties(np.full_like(amp, z_floor))

    # Projections latérales Re(ψ) sur plan Im=0  →  (x, Re, 0)
    re_proj.set_data(x_w_in, re)
    re_proj.set_3d_properties(np.zeros_like(re))

    # Projections Im(ψ) sur plan Re=0  →  (x, 0, Im)
    im_proj.set_data(x_w_in, np.zeros_like(im))
    im_proj.set_3d_properties(im)

    tt_3d.set_text(f"t = {t_arr_w[si]:.2e}")
    return helix_line, shadow_line, re_proj, im_proj, tt_3d


anim_3d = FuncAnimation(
    fig_3d,
    _update_3d,
    frames=len(anim_indices_w),
    init_func=_init_3d,
    interval=INTERVAL_MS,
    blit=False,
)

fig_3d.tight_layout()
print("Animation prête — ferme les fenêtres pour quitter.")
plt.show()


