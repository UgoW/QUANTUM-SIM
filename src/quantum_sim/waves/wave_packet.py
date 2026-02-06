import numpy as np
from quantum_sim.waves.wave_function import WaveFunction
from quantum_sim.validators.wave_validators import validate_positive, validate_non_negative

class WavePacket(WaveFunction):
    """Wave packet: superposition of plane waves."""
    
    def __init__(self, plane_waves=None, time: float = 0.0):
        """
        Initialize wave packet.
        
        Args:
            plane_waves: Plane wave which form the 
            time: Time parameter
        """
        if plane_waves is not None:
            self.plane_waves = plane_waves
        else:
            raise ValueError("Either momentum_distribution or plane_waves must be provided")
        
        self._norm_factor = 1.0
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

    def _evaluate_raw(self, x: float | np.ndarray) -> np.ndarray:
        """Evaluate sum of plane waves.
            :param x: position(s) to evaluate the wave packet
            :type x: float | np.ndarray
        """
        result = np.zeros_like(x, dtype=complex)
        for pw in self.plane_waves:
            result += pw.evaluate(x)
        return result

    def evaluate(self, x: float | np.ndarray) -> np.ndarray:
        """Evaluate sum of plane waves with normalisation factor applied
            :param x: position(s) to evaluate the wave packet
            :type x: float | np.ndarray
        """
        return self._norm_factor * self._evaluate_raw(x)
    
    def normalize(self, x: np.ndarray) -> None:
        """Normalize the wave function."""

        psi = self._evaluate_raw(x)
        prob_raw = np.abs(psi) ** 2
        norm_val = np.trapz(prob_raw, x)
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