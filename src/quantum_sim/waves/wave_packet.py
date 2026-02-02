import numpy as np
from collections.abc import Callable
from quantum_sim.waves.wave_function import WaveFunction

class WavePacket(WaveFunction):
    """Wave packet: superposition of plane waves."""
    
    def __init__(self, momentum_distribution=None, plane_waves=None, 
                 position_center: float = 0.0, time: float = 0.0):
        """
        Initialize wave packet.
        
        Args:
            momentum_distribution: Function defining amplitude in momentum space
            position_center: Center position of the packet
            time: Time parameter
        """
        if plane_waves is not None:
            self.plane_waves = plane_waves
            self.momentum_distribution = self._distribution_from_waves()
        elif momentum_distribution is not None:
            self.momentum_distribution = momentum_distribution
            self.plane_waves = []
        else:
            raise ValueError("Either momentum_distribution or plane_waves must be provided")
        
        self.position_center = position_center
        super().__init__(np.array([position_center]), time)
    
    def _distribution_from_waves(self) -> Callable:
        """Create momentum distribution from plane waves."""

        def dist(k: float) -> complex:
            """
            Momentum distribution from plane waves.
            
            :param k: wave number for which to evaluate the distribution
            :type k: float
            :return: amplitude at wave number k
            :rtype: complex
            """
            return sum(pw.amplitude for pw in self.plane_waves 
                      if abs(pw.wave_number - k) < 1e-10)
        return dist
    
    def evaluate_with_plane_waves(self, x: float | np.ndarray) -> np.ndarray:
        """Evaluate sum of plane waves.
            :param x: position(s) to evaluate the wave packet
            :type x: float | np.ndarray
        """
        result = np.zeros_like(x, dtype=complex)
        for pw in self.plane_waves:
            result += pw.evaluate(x)
        return result
    
    def evaluate_with_momentum_distribution(self, x: float | np.ndarray, k_max: float = 50.0, n_points: int = 1024) -> np.ndarray:
        """FFT inverse : φ(k) → ψ(x)
            :param x: position(s) to evaluate the wave packet
            :type x: float | np.ndarray
            :param k_max: maximum wave number for integration
            :type k_max: float
            :param n_points: number of points for FFT
            :type n_points: int
            :return: wave function evaluated at x
            :rtype: np.ndarray
        """
        k_values = np.linspace(-k_max, k_max, n_points)
        
        phi_k = np.array([self.momentum_distribution(k) for k in k_values])
        
        psi_x = np.fft.ifft(phi_k)
        
        x_fft = np.fft.fftfreq(n_points) * (2 * k_max)
        
        if isinstance(x, float):
            return np.array([np.interp(x, x_fft, psi_x)])
        else:
            return np.array(np.interp(x, x_fft, psi_x))
        
    
    def evaluate(self, x: float | np.ndarray) -> np.ndarray:
        """Evaluate wave packet."""
        if self.momentum_distribution is not None:
            return self.evaluate_with_momentum_distribution(x)
        else:
            return self.evaluate_with_plane_waves(x)
    
    def probability_density(self, x: float | np.ndarray) -> np.ndarray:
        """Calculate probability density."""
        return np.abs(self.evaluate(x))**2
    
    def normalize(self) -> None:
        """Normalize the wave function."""
        # TODO: Implement normalization
        pass