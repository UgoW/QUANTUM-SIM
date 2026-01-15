import numpy as np
from quantum_sim.potentials.Potential import Potential
from typing import Dict, Any


class StepPotential(Potential):
    """Step potential: V(x) = 0 for x < x0, V(x) = V0 for x >= x0.

    Represents a sudden change in potential energy at position x0.
    This is a classic pedagogical example for studying quantum tunneling
    and reflection at potential barriers.
    """

    def __init__(self, x0: float, V0: float):
        """
        Initialize step potential.

        Args:
            x0: Position of the step
            V0: Height of the potential step (energy units)
        """
        super().__init__()
        self.x0 = x0
        self.V0 = V0

    def evaluate(self, x: float | np.ndarray) -> np.ndarray:
        """
        Evaluate the potential.

        Args:
            x: Position(s)

        Returns:
            V0 where x >= x0, 0 otherwise
        """
        x_arr = np.asarray(x)
        return np.where(x_arr >= self.x0, self.V0, 0.0)

    @property
    def parameters(self) -> Dict[str, Any]:
        """Return parameters."""
        return {"x0": self.x0, "V0": self.V0}

    def __str__(self) -> str:
        """String representation."""
        return f"StepPotential: V(x) = 0 for x < {self.x0}, V(x) = {self.V0} for x >= {self.x0}"