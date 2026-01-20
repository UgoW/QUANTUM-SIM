from abc import ABC, abstractmethod
import numpy as np
from typing import Callable

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
    def evaluate(self, x: float | np.ndarray) -> np.ndarray:
        """
        Evaluate the wave function at given position(s).
        
        Args:
            x: Position(s) where to evaluate the wave function
            
        Returns:
            Complex amplitude(s)
        """
        pass