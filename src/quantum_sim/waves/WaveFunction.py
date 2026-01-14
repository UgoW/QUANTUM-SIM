from abc import ABC, abstractmethod
import numpy as np
from typing import Union, Callable 
# Union permet de typer une variable pouvant être de plusieurs types différents
#Il semble possible de remplacer Union par | dans les versions récentes de Python (3.10+)

#Callable permet de typer une fonction en spécifiant les types de ses arguments et de son retour

class WaveFunction(ABC):
    """Abstract base class for quantum wave functions."""
    
    def __init__(self, position: np.ndarray, time: float = 0.0):
        """
        Initialize the wave function.
        
        Args:
            position: Spatial coordinates
            time: Time parameter
        """
        self.position = position
        self.time = time
    
    @abstractmethod
    def evaluate(self, x: Union[float, np.ndarray]) -> np.ndarray:
        """
        Evaluate the wave function at given position(s).
        
        Args:
            x: Position(s) where to evaluate the wave function
            
        Returns:
            Complex amplitude(s)
        """
        pass
    
    @abstractmethod
    def probability_density(self, x: Union[float, np.ndarray]) -> np.ndarray:
        """
        Calculate probability density |ψ(x)|².
        
        Args:
            x: Position(s)
            
        Returns:
            Probability density values
        """
        pass
    
    @abstractmethod
    def normalize(self) -> None:
        """Normalize the wave function."""
        pass


class PlaneWave(WaveFunction):
    """Plane wave implementation: ψ(x,t) = A*exp(i(kx - ωt))"""
    
    def __init__(self, amplitude: complex, wavenumber: float, frequency: float, time: float = 0.0):
        """
        Initialize plane wave.
        
        Args:
            amplitude: Wave amplitude
            wavenumber: Wave number k
            frequency: Angular frequency ω
            time: Time parameter
        """
        self.amplitude = amplitude
        self.wavenumber = wavenumber
        self.frequency = frequency
        super().__init__(np.array([]), time)
    
    def evaluate(self, x: Union[float, np.ndarray]) -> np.ndarray:
        """Evaluate plane wave."""
        # TODO: Implement evaluation
        pass
    
    def probability_density(self, x: Union[float, np.ndarray]) -> np.ndarray:
        """Calculate probability density."""
        # TODO: Implement probability density
        pass
    
    def normalize(self) -> None:
        """Normalize the wave function."""
        # TODO: Implement normalization
        pass


class WavePacket(WaveFunction):
    """Wave packet: superposition of plane waves."""
    
    def __init__(self, momentum_distribution: Callable, position_center: float = 0.0, time: float = 0.0):
        """
        Initialize wave packet.
        
        Args:
            momentum_distribution: Function defining amplitude in momentum space
            position_center: Center position of the packet
            time: Time parameter
        """
        self.momentum_distribution = momentum_distribution
        self.position_center = position_center
        super().__init__(np.array([position_center]), time)
    
    def evaluate(self, x: Union[float, np.ndarray]) -> np.ndarray:
        """Evaluate wave packet."""
        # TODO: Implement Fourier transform of momentum distribution
        pass
    
    def probability_density(self, x: Union[float, np.ndarray]) -> np.ndarray:
        """Calculate probability density."""
        # TODO: Implement probability density
        pass
    
    def normalize(self) -> None:
        """Normalize the wave function."""
        # TODO: Implement normalization
        pass