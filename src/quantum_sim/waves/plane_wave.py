import numpy as np
from quantum_sim.waves import WaveFunction
from quantum_sim.utils.constants import ELECTRON_MASS, REDUCED_PLANCK_CONSTANT, PI
from quantum_sim.validators.wave_validators import validate_positive, validate_non_negative, validate_range

class PlaneWave(WaveFunction):
    """
    Plane wave implementation: ψ(x,t) = A*exp(i(k(x - x0) - ωt + φ))
    """
    
    def __init__(self, amplitude: complex, wavelength: float,
                 position: float = 0.0, phase: float = 0.0, time: float = 0.0, masse: float = ELECTRON_MASS):
        """
        Initialize plane wave.
        
        Args:
            amplitude: Wave amplitude
            wavelength: Wavelength λ
            time: Time parameter t
            position: Initial spatial offset x0
            phase: Initial phase φ
            masse: Particle mass
        """
        self.amplitude = amplitude  
        self.wavelength = wavelength
        self.position = position
        self.phase = phase
        self.masse = masse
        super().__init__(np.array([position]), time)
    
    def validate_parameters(self) -> None:
        """Validate parameters of the plane wave."""
        validate_positive(self.wavelength, "wavelength")
        validate_non_negative(self.masse, "masse")
    
    @property
    def wave_number(self) -> float:
        """Calculate wave number k = 2π/λ."""
        return 2 * PI / self.wavelength

    @property
    def angular_frequency(self) -> float:
        """Calculate angular frequency ω = ħk²/(2m)."""
        k = self.wave_number
        return (REDUCED_PLANCK_CONSTANT * k**2) / (2 * self.masse)
        
    def evaluate(self, x: float | np.ndarray) -> np.ndarray:
        """Evaluate plane wave."""
        return self.amplitude * np.exp(1j * (self.wave_number * (x - self.position) - self.angular_frequency * self.time + self.phase))