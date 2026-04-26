
import numpy as np
from scipy import sparse
from scipy.integrate import solve_ivp

from quantum_sim.utils.constants import REDUCED_PLANCK_CONSTANT, ELECTRON_MASS
from quantum_sim.waves.wave_packet import WavePacket


class SchrodingerSolver:

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
        """
        Initialize the solver: builds the spatial grid, the finite-difference
        Laplacian, and the absorbing boundary potential (CAP).
        """
        if x_min >= x_max:
            raise ValueError(f"x_min ({x_min}) must be strictly less than x_max ({x_max})")
        if n_points < 3:
            raise ValueError(f"n_points must be >= 3, got {n_points}")
        if mass <= 0:
            raise ValueError(f"mass must be positive, got {mass}")

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


    def _build_laplacian(self) -> sparse.csr_matrix:
        """Build the Laplacian matrix."""

        return sparse.diags(
            [1.0, -2.0, 1.0],
            offsets=[-1, 0, 1],
            shape=(self.n_points, self.n_points),
            format="csr",
        ) / self.dx ** 2

    def _build_cap(self) -> np.ndarray:
        """Build the complex absorbing potential (CAP)."""

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

    def set_potential(self, V: np.ndarray) -> None:
        """Set the potential V(x)."""

        V = np.asarray(V, dtype=float)
        if V.shape != (self.n_points,):
            raise ValueError(
                f"V must have shape ({self.n_points},), got {V.shape}"
            )
        self._V = V

    def init_from_packet(self, packet: WavePacket) -> None:
        """
        Initialize the initial state ψ₀ from a WavePacket object:
        evaluates the packet on the grid and normalizes it.
        """
        # NEED TO BE FIX, WE CAN'T USE PRIVATE FUNCTION HERE
        psi_raw = packet.evaluate(self.x_grid).astype(complex)
        self.init_from_array(psi_raw, normalize=True)

    def init_from_array(self, psi_0: np.ndarray, normalize: bool = True) -> None:
        """
        Initialize the initial state ψ₀ directly from a complex array.
        If normalize=True, normalizes ψ₀ such that ∫|ψ|² dx = 1.
        """

        psi_0 = np.asarray(psi_0, dtype=complex)
        if psi_0.shape != (self.n_points,):
            raise ValueError(
                f"psi_0 must have shape ({self.n_points},), got {psi_0.shape}"
            )
        if normalize:
            norm = np.sqrt(np.trapezoid(np.abs(psi_0) ** 2) * self.dx)
            if norm <= 0 or not np.isfinite(norm):
                raise ValueError(f"Cannot normalise psi_0: norm = {norm}")
            psi_0 = psi_0 / norm
        self._psi_0 = psi_0

    def _rhs(self, t: float, psi: np.ndarray) -> np.ndarray:
        """
        Right-hand side of the time-dependent Schrödinger equation:
        dψ/dt = (-i/ℏ)(T + V)ψ − Γ(x)ψ  where Γ is the CAP absorption term.
        """
        hbar = REDUCED_PLANCK_CONSTANT
        kinetic = -(hbar ** 2 / (2.0 * self.mass)) * self._laplacian.dot(psi)
        potential_term = self._V * psi
        hamiltonian_psi = kinetic + potential_term
        absorption = self._cap * psi
        return (-1j / hbar) * hamiltonian_psi - absorption

    def solve(
        self,
        t_final: float,
        dt: float,
        method: str = "RK45",
    ) -> dict:
        """Integrate the Schrödinger equation from t=0 to t=t_final with step dt."""
 
        if self._psi_0 is None:
            raise RuntimeError(
                "Initial state not set"
            )
        if t_final <= 0:
            raise ValueError("t_final must be positive")
        if dt <= 0:
            raise ValueError("dt must be positive")
        
        if self.absorb_width >= (self.x_max - self.x_min) / 2:
            raise ValueError(
                f"absorb_width ({self.absorb_width}) must be less than half the domain width "
                f"({(self.x_max - self.x_min) / 2:.3f})"
            )

        n_steps = max(1, int(np.ceil(t_final / dt)))
        t_eval = np.linspace(0.0, t_final, n_steps + 1)

        solution = solve_ivp(
            self._rhs,
            t_span=(0.0, t_final),
            y0=self._psi_0.copy(),
            t_eval=t_eval,
            method=method,
        )

        if not solution.success:
            raise RuntimeError(f"Solver failed: {solution.message}")

        psi = solution.y  

        return {
            "x": self.x_grid,
            "t": solution.t,
            "psi": psi,
            "prob": np.abs(psi) ** 2,
        }
