# src/quantum_sim/waves/result.py
import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Dict

@dataclass
class WaveResult:
    """
    Representation of the result of a quantum wave simulation.

    Attributes:
        x (np.ndarray): Positions where the wave is evaluated.
        psi (np.ndarray): Complex values of the wave function at positions x.
        t (Optional[np.ndarray]): Time associated with the result.
        metadata (Dict): Additional simulation parameters (amplitude, wavelength, mass, etc.).
        
    """
    x: np.ndarray
    psi: np.ndarray
    t: Optional[np.ndarray] = None
    metadata: Dict = field(default_factory=dict)

    def copy(self) -> 'WaveResult':
        """
        Create a deep copy of the WaveResult instance.

        Returns:
            WaveResult: A new instance with copied data.
        """
        return WaveResult(
            x=np.copy(self.x),
            psi=np.copy(self.psi),
            t=np.copy(self.t) if self.t is not None else None,
            metadata=self.metadata.copy()
        )

    


