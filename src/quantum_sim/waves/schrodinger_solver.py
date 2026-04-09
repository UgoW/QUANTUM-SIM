
import numpy as np
from scipy import sparse
from scipy.integrate import solve_ivp

from quantum_sim.utils.constants import REDUCED_PLANCK_CONSTANT, ELECTRON_MASS
from quantum_sim.waves.wave_packet import WavePacket


class SchrodingerSolver:

    # Initialise le solveur : construit la grille spatiale, le laplacien
    # aux différences finies et le potentiel absorbant (CAP) aux bords.
    def __init__(
        self,
        x_min: float,
        x_max: float,
        n_points: int = 801,
        mass: float = ELECTRON_MASS,
        absorbing_boundaries: bool = True,
        absorb_width: float = 5.0,
        gamma_cap: float = 5e-4,
    ) -> None:
        if x_min >= x_max:
            raise ValueError("error 1")
        if n_points < 3:
            raise ValueError("error 2")
        if mass <= 0:
            raise ValueError("error 3")

        self.x_min = x_min
        self.x_max = x_max
        self.n_points = n_points
        self.mass = mass
        self.absorbing_boundaries = absorbing_boundaries
        self.absorb_width = absorb_width
        self.gamma_cap = gamma_cap

        self.x_grid: np.ndarray = np.linspace(x_min, x_max, n_points)
        self.dx: float = float(self.x_grid[1] - self.x_grid[0])


        self._V: np.ndarray = np.zeros(n_points, dtype=float)

        self._psi_0: np.ndarray | None = None

        self._laplacian: sparse.csr_matrix = self._build_laplacian()
        self._cap: np.ndarray = self._build_cap() if absorbing_boundaries else np.zeros(n_points)


    # Construit la matrice laplacienne 
    def _build_laplacian(self) -> sparse.csr_matrix:

        return sparse.diags(
            [1.0, -2.0, 1.0],
            offsets=[-1, 0, 1],
            shape=(self.n_points, self.n_points),
            format="csr",
        ) / self.dx ** 2

    # Construit le potentiel absorbant complexe (CAP) 
    def _build_cap(self) -> np.ndarray:

        V_cap = np.zeros(self.n_points, dtype=float)
        for i, xi in enumerate(self.x_grid):
            if xi < self.x_min + self.absorb_width:
                V_cap[i] = self.gamma_cap * (
                    (self.x_min + self.absorb_width - xi) / self.absorb_width
                ) ** 2
            elif xi > self.x_max - self.absorb_width:
                V_cap[i] = self.gamma_cap * (
                    (xi - (self.x_max - self.absorb_width)) / self.absorb_width
                ) ** 2
        return V_cap

    # Définit le potentiel V(x) 
    def set_potential(self, V: np.ndarray) -> None:

        V = np.asarray(V, dtype=float)
        if V.shape != (self.n_points,):
            raise ValueError(
                f"V must have shape ({self.n_points},), got {V.shape}"
            )
        self._V = V

    # Initialise l'état initial ψ₀ à partir d'un objet WavePacket :
    # évalue le paquet sur la grille puis normalise.
    def init_from_packet(self, packet: WavePacket) -> None:

        psi_raw = packet._evaluate_raw(self.x_grid).astype(complex)
        self.init_from_array(psi_raw, normalize=True)

    # Initialise l'état initial ψ₀ directement depuis un tableau complexe.
    # Si normalize=True, normalise ψ₀ de sorte que ∫|ψ|² dx = 1.
    def init_from_array(self, psi_0: np.ndarray, normalize: bool = True) -> None:

        psi_0 = np.asarray(psi_0, dtype=complex)
        if psi_0.shape != (self.n_points,):
            raise ValueError(
                f"psi_0 must have shape ({self.n_points},), got {psi_0.shape}"
            )
        if normalize:
            norm = np.sqrt(np.sum(np.abs(psi_0) ** 2) * self.dx)
            if norm <= 0 or not np.isfinite(norm):
                raise ValueError(f"Cannot normalise psi_0: norm = {norm}")
            psi_0 = psi_0 / norm
        self._psi_0 = psi_0



    # Second membre de l'équation de Schrödinger dépendante du temps :
    # dψ/dt = (-i/ℏ)(T + V)ψ − Γ(x)ψ  où Γ est le terme d'absorption CAP.
    def _rhs(self, t: float, psi: np.ndarray) -> np.ndarray:

        hbar = REDUCED_PLANCK_CONSTANT
        kinetic = -(hbar ** 2 / (2.0 * self.mass)) * self._laplacian.dot(psi)
        potential_term = self._V * psi
        hamiltonian_psi = kinetic + potential_term
        absorption = self._cap * psi
        return (-1j / hbar) * hamiltonian_psi - absorption

    # Intègre l'équation de Schrödinger de t=0 à t=t_final avec le pas
    def solve(
        self,
        t_final: float,
        dt: float,
        method: str = "RK45",
    ) -> dict:
 
        if self._psi_0 is None:
            raise RuntimeError(
                "Initial state not set"
            )
        if t_final <= 0:
            raise ValueError("t_final must be positive")
        if dt <= 0:
            raise ValueError("dt must be positive")

        t_eval = np.arange(0.0, t_final + dt, dt)

        solution = solve_ivp(
            self._rhs,
            t_span=(0.0, t_final),
            y0=self._psi_0.copy(),
            t_eval=t_eval,
            method=method,
        )

        psi = solution.y  

        return {
            "x": self.x_grid,
            "t": solution.t,
            "psi": psi,
            "prob": np.abs(psi) ** 2,
            "solution": solution,
        }
