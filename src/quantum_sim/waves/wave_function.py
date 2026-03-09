from abc import ABC, abstractmethod
import numpy as np

from quantum_sim.validators.wave_validators import validate_positive, validate_range


class WaveFunction(ABC):
    """Abstract base class for quantum wave functions."""

    def __init__(self, position: float, time: float = 0.0):
        """
        Initialize the wave function.

        Args:
            position: Spatial reference position
            time: Time parameter
        """
        self.position = position
        self.time = time
        self.validate_parameters()

    @abstractmethod
    def validate_parameters(self) -> None:
        """Validate parameters of the wave function."""
        pass

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

    def evaluate_interval(
        self, start: float, end: float, points: int
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Evaluate the wave function on a generated spatial interval.

        Args:
            start: Start of interval
            end: End of interval
            points: Number of evaluation points

        Returns:
            Tuple containing:
                x: spatial coordinates
                ψ(x): wave function values
        """
        validate_range(start, end, "interval")
        validate_positive(points, "points")

        x = np.linspace(start, end, points)
        return x, self.evaluate(x)

    def probability_density(self, x: float | np.ndarray) -> np.ndarray:
        """
        Compute probability density |ψ(x)|².
        """
        psi = self.evaluate(x)
        return np.abs(psi) ** 2
