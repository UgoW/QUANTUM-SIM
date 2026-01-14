import numpy as np
from quantum_sim.waves import WaveFunction

class PlaneWave(WaveFunction):
    """Plane wave implementation: ψ(x,t) = A*exp(i(k(x - x0) - ωt + φ))

    Added parameters:
    - `position` (`x0`): initial spatial offset of the wave (shifts the phase locally by k*x0).
    - `phase` (`φ`): global initial phase (relevant for interference and relative phases).
    """
    
    def __init__(self, amplitude: complex, wavenumber: float, frequency: float,
                 position: float = 0.0, phase: float = 0.0, time: float = 0.0):
        """
        Initialize plane wave.
        
        Args:
            amplitude: Wave amplitude
            wavenumber: Wave number k
            frequency: Angular frequency ω
            time: Time parameter
            position: Initial spatial offset x0
            phase: Initial phase φ
        """
        self.amplitude = amplitude
        self.wavenumber = wavenumber
        self.frequency = frequency
        self.position = position
        self.phase = phase
        # store position as array for compatibility with base class
        super().__init__(np.array([position]), time)
    
    def evaluate(self, x: float | np.ndarray) -> np.ndarray:
        """Evaluate plane wave."""
        # TODO: Implement evaluation
        pass
    
    def probability_density(self, x: float | np.ndarray) -> np.ndarray:
        """Calculate probability density."""
        # TODO: Implement probability density
        pass
    
    def normalize(self) -> None:
        """Normalize the wave function."""
        # TODO: Implement normalization
        pass