import numpy as np
from quantum_sim.potentials.Potential import Potential
from typing import Dict, Any


class InfiniteWell(Potential):
    """Infinite square well: V(x) = 0 for a < x < b, V(x) = ∞ otherwise.

    Represents a particle confined between two infinite walls.
    This leads to discrete energy levels and standing waves.
    In practice, we use a very large finite value instead of infinity.
    """

    def __init__(self, a: float, b: float, V_wall: float = 1e10):
        """
        Initialize infinite well potential.

        Args:
            a: Left boundary of the well
            b: Right boundary of the well
            V_wall: Very large potential outside the well (default: 1e10)
        """
        super().__init__()
        if a >= b:
            raise ValueError("Left boundary 'a' must be less than right boundary 'b'")
        self.a = a
        self.b = b
        self.V_wall = V_wall

    def evaluate(self, x: float | np.ndarray) -> np.ndarray:
        """
        Evaluate the potential.

        Args:
            x: Position(s)

        Returns:
            0 inside [a, b], V_wall outside
        """
        x_arr = np.asarray(x)
        return np.where((x_arr >= self.a) & (x_arr <= self.b), 0.0, self.V_wall)

    @property
    def parameters(self) -> Dict[str, Any]:
        """Return parameters."""
        return {"a": self.a, "b": self.b, "V_wall": self.V_wall}

    def __str__(self) -> str:
        """String representation."""
        return f"InfiniteWell: V(x) = 0 for {self.a} < x < {self.b}, V(x) = {self.V_wall} otherwise"