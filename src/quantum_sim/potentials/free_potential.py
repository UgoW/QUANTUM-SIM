import numpy as np
from quantum_sim.potentials.Potential import Potential
from typing import Dict, Any


class FreePotential(Potential):
    """Free particle potential: V(x) = 0 everywhere.

    Represents a particle moving in free space with no potential energy.
    This is the simplest case, often used as a reference or for comparison.
    """

    def __init__(self):
        """Initialize free potential (no parameters needed)."""
        super().__init__()

    def evaluate(self, x: float | np.ndarray) -> np.ndarray:
        """
        Evaluate the potential: always returns 0.

        Args:
            x: Position(s) (ignored for free potential)

        Returns:
            Array of zeros with the same shape as x
        """
        x_arr = np.asarray(x)
        return np.zeros_like(x_arr)

    @property
    def parameters(self) -> Dict[str, Any]:
        """Return parameters: none for free potential."""
        return {}

    def __str__(self) -> str:
        """String representation."""
        return "FreePotential: V(x) = 0"