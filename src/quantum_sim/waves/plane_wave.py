"""Plane wave implementation for quantum simulations.

This module provides the PlaneWave class, implementing a plane wave solution
to the Schrödinger equation: ψ(x,t) = A*exp(i(k(x - x0) - ωt + φ))
"""
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
    
    @property
    def momentum(self) -> float:
        """Calculate momentum p = ħk."""
        return REDUCED_PLANCK_CONSTANT * self.wave_number
    
    @property
    def energy(self) -> float:
        """Calculate energy E = p²/(2m)."""
        p = self.momentum
        return p**2 / (2 * self.masse)

    @property
    def phase_velocity(self) -> float:
        """Calculate phase velocity v_p = ω/k."""
        return self.angular_frequency / self.wave_number
    
    @property
    def period(self) -> float:
        """Calculate period T = 2π/ω."""
        return 2 * PI / self.angular_frequency

    def evaluate(self, x: float | np.ndarray) -> np.ndarray:
        """Evaluate plane wave."""
        return self.amplitude * np.exp(1j * (self.wave_number * (x - self.position) - self.angular_frequency * self.time + self.phase))
    
    def evaluate_at_time_zero(self, x: float | np.ndarray) -> np.ndarray:
        """Evaluate plane wave at time t = 0."""
        return self.amplitude * np.exp(1j * (self.wave_number * (x - self.position) + self.phase))
    
    def evaluate_at_position_zero(self, t: float | np.ndarray) -> np.ndarray:
        """Evaluate plane wave at position x = 0."""
        return self.amplitude * np.exp(1j * (-self.wave_number * self.position - self.angular_frequency * t + self.phase))