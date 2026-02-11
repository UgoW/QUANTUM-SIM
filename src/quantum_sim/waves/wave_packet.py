import numpy as np
from quantum_sim.waves.plane_wave import PlaneWave
from quantum_sim.waves.wave_function import WaveFunction
from quantum_sim.validators.wave_validators import validate_positive, validate_non_negative


class WavePacket(WaveFunction):
    """Wave packet: superposition of plane waves."""

    def __init__(self, plane_waves: list[PlaneWave], time: float = 0.0):
        """
        Initialize a WavePacket instance by vectorizing multiple PlaneWave objects.

        This constructor extracts physical parameters from a list of PlaneWave instances 
        and stores them as NumPy arrays. This transition from a list of objects to 
        vectorized arrays is essential for high-performance matrix operations during 
        wave function evaluation, avoiding slow Python loops.

        Args:
            plane_waves (list[PlaneWave]): A list of PlaneWave objects that constitute 
                the wave packet. Each wave carries its own amplitude, wave number (k), 
                and frequency (omega).
            time (float): Initial time parameter (t) for the simulation. 
                Defaults to 0.0.

        Raises:
            ValueError: If the plane_waves list is empty, as a wave packet 
                requires at least one constituent wave.
        """

        if not plane_waves:
            raise ValueError("plane_waves list cannot be empty")
            
        self.plane_waves = plane_waves
        self._norm_factor = 1.0
        
        self._amplitudes = np.array([pw.amplitude for pw in plane_waves], dtype=complex).ravel()
        
        self._k_vectors = np.array([pw.wave_number for pw in plane_waves], dtype=float).ravel()
        
        self._omegas = np.array([pw.angular_frequency for pw in plane_waves], dtype=float).ravel()
        
        self._phases = np.array([pw.phase for pw in plane_waves], dtype=float).ravel()
        
        self._positions = np.array([pw.position for pw in plane_waves], dtype=float).ravel()

        super().__init__(np.array([]), time)
    
    def validate_parameters(self) -> None:
        """Validate parameters of the plane wave."""
        validate_positive(self._norm_factor, "norm factor")

    def momentum_components(self) -> list[tuple[float, complex]]:
        """
        Discrete momentum representation (k, amplitude).
        """
        return [(pw.wave_number, pw.amplitude) for pw in self.plane_waves]
    
    def probability_density(self, x: float | np.ndarray) -> np.ndarray:
        """Calculate probability density."""
        return np.abs(self.evaluate(x))**2

    def _evaluate_raw(self, x: float | np.ndarray, t: float | None = None) -> np.ndarray:
        """
        Evaluate the wave packet using vectorized matrix operations for high performance.

        Instead of iterating through each plane wave in a Python loop, this method 
        leverages NumPy broadcasting to compute the superposition of all constituent 
        waves across all input positions simultaneously.

        The computation follows these steps:
        1. Reshape the input positions 'x' into a column vector (M x 1).
        2. Reshape the wave parameters (k, omega, phase, etc.) into row vectors (1 x N).
        3. Create a phase matrix (M x N) where each element (i, j) represents the 
           phase of the j-th wave at the i-th position.
        4. Compute the complex exponential for the entire matrix and weight it by amplitudes.
        5. Sum along the wave axis (axis=1) to obtain the total wave function value.

        Args:
            x (float | np.ndarray): Spatial position(s) where the wave packet is evaluated.

        Returns:
            np.ndarray: The complex value(s) of the wave function at position(s) x.
                        Returns a scalar if the input x was a scalar.
        """

        x_array = np.atleast_1d(x)

        X = x_array[:, np.newaxis]
        
        K = self._k_vectors[np.newaxis, :]
        W = self._omegas[np.newaxis, :]
        P = self._phases[np.newaxis, :]
        X0 = self._positions[np.newaxis, :]
        A = self._amplitudes[np.newaxis, :]
        
        # Changement: rajout d'un parametre t pour evaluer a un instant t
        time_value = self.time if t is None else t
        
        total_phase = K * (X - X0) - (W * time_value) + P
        
        waves_matrix = A * np.exp(1j * total_phase)
        
        psi_sum = np.sum(waves_matrix, axis=1)
        
        if np.ndim(x) == 0:
            return psi_sum[0]
        return psi_sum

    def evaluate(self, x: float | np.ndarray, t: float | None = None) -> np.ndarray:
        """Evaluate sum of plane waves with normalisation factor applied
            :param x: position(s) to evaluate the wave packet
            :type x: float | np.ndarray
        """
        # Changement: rajout d'un parametre t pour evaluer a un instant t
        return self._norm_factor * self._evaluate_raw(x, t=t)
        
    def normalize(self, x: np.ndarray) -> None:
        """Normalize the wave function."""

        psi = self._evaluate_raw(x)
        prob_raw = np.abs(psi) ** 2
        norm_val = np.trapezoid(prob_raw, x)
        if norm_val <= 0 or not np.isfinite(norm_val):
            # TODO : Revoir pour utiliser des exceptions personnalisés
            raise ValueError(f"Invalid norm computed: {norm_val}")

        self._norm_factor = 1.0 / np.sqrt(norm_val)
            

    @property
    def energy(self) -> float:
        """
        Expectation value of energy for the wave packet.
        
        Computed as weighted sum of individual plane wave energies.
        
        Returns:
            Energy in Joules
            
        Raises:
            ValueError: if wave packet has no plane_waves
        """
        if not self.plane_waves:
            raise ValueError("Wave packet must contain plane_waves to compute energy")
        
        return self.energy_expectation()

    def energy_expectation(self) -> float:
        """
        Compute expectation value ⟨E⟩ of energy for the wave packet.
        
        For plane waves: ⟨E⟩ = Σ w_n * E_n
            where w_n = |A_n|² / Σ|A_m|² (normalized weights)
            and E_n is the energy of plane wave n
        
        Each plane wave contributes proportionally to |amplitude|².
        
        Returns:
            float: Expectation value of energy in Joules
            
        Raises:
            ValueError: if all amplitudes are zero
        """
        amps = np.array([pw.amplitude for pw in self.plane_waves], dtype=complex)
        weights = np.abs(amps) ** 2
        
        if np.sum(weights) <= 0:
            raise ValueError("All component amplitudes are zero; cannot compute energy")
        
        weights = weights / np.sum(weights)
        energies = np.array([pw.energy for pw in self.plane_waves], dtype=float)
        
        return float(np.sum(weights * energies))