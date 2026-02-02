import numpy as np
from collections.abc import Callable
from quantum_sim.waves.wave_packet import WavePacket
from quantum_sim.waves.plane_wave import PlaneWave


class GaussianWavePacket(WavePacket):
    """Gaussian wave packet: superposition of plane waves with gaussian envelope."""
    
    def __init__(self, plane_waves: list[PlaneWave], k0=None, sigma_k=None, time=0.0):
        """
        Initialize Gaussian wave packet from plane waves.
        
        Args:
            plane_waves: List of PlaneWave instances
            k0: Center momentum wave number (auto-computed if None)
            sigma_k: Momentum width (auto-computed if None)
            position_center: Center position of the packet
            time: Time parameter
        """
        if not plane_waves:
            raise ValueError("plane_waves list cannot be empty")
        
        k_values = self._extract_wave_numbers(plane_waves)
        self.k0 = self._compute_k0(k0, k_values)
        self.sigma_k = self._compute_sigma_k(sigma_k, k_values)
        
        super().__init__(plane_waves=plane_waves, time=time)
    
    def _extract_wave_numbers(self, plane_waves) -> np.ndarray:
        """Extract wave numbers from list of plane waves.
            :param plane_waves: List of PlaneWave instances
            :return: Numpy array of wave numbers
        """
        return np.array([pw.wave_number for pw in plane_waves])
    
    def _compute_k0(self, k0, k_values) -> float:
        """Compute or retrieve center momentum.
            :param k0: Provided center momentum wave number
            :param k_values: Numpy array of wave numbers from plane waves
            :return: Center momentum wave number
        """
        if k0 is not None:
            return k0
        return float(np.mean(k_values))
    
    def _compute_sigma_k(self, sigma_k, k_values) -> float:
        """Compute or retrieve momentum width.
            :param sigma_k: Provided momentum width
            :param k_values: Numpy array of wave numbers from plane waves
            :return: Momentum width
        """
        if sigma_k is not None:
            if sigma_k <= 0:
                raise ValueError("sigma_k must be positive")
            return sigma_k
        
        sigma = float(np.std(k_values))
        if sigma <= 0:
            raise ValueError("Cannot infer sigma_k from plane waves (zero spread in k)")

        return sigma
    
    def _evaluate_raw(self, x: float | np.ndarray) -> np.ndarray:
        """Evaluate wave packet with gaussian envelope applied to plane waves.
            :param x: position(s) to evaluate the wave packet
            :type x: float | np.ndarray
            :return: Evaluated wave packet at positions x
            :rtype: np.ndarray
        """
        x = np.asarray(x)
        result = np.zeros_like(x, dtype=complex)
        
        for pw in self.plane_waves:
            envelope = self._gaussian_envelope(pw.wave_number)
            result += envelope * pw.evaluate(x)
        
        return result
    
    def _gaussian_envelope(self, k: float) -> complex:
        """Compute gaussian envelope for given wave number.
            :param k: wave number
            :type k: float
            :return: envelope value at wave number k
            :rtype: complex
        """
        return np.exp(-(k - self.k0)**2 / (2 * self.sigma_k**2))

    def evaluate(self, x: float | np.ndarray) -> np.ndarray:
        return self._norm_factor * self._evaluate_raw(x)