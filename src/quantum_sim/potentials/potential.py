from abc import ABC, abstractmethod
import numpy as np
from typing import Dict, Any


class Potential(ABC):
    """Abstract base class for quantum potentials.

    A potential defines the energy landscape in which quantum particles evolve.
    """

    def __init__(self):
        """Initialize the potential."""
        pass

    @abstractmethod
    def evaluate(self, x: float | np.ndarray) -> np.ndarray:
        """
        Evaluate the potential at given position(s).

        Args:
            x: Position(s) where to evaluate the potential

        Returns:
            Potential energy value(s) at x
        """
        pass

    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """
        Return the parameters defining this potential.

        Returns:
            Dictionary of parameter names and values
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """String representation of the potential."""
        pass