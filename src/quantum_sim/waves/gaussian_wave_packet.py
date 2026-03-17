import numpy as np
from quantum_sim.utils.constants import ELECTRON_MASS, PI
from quantum_sim.waves.wave_packet import WavePacket
from quantum_sim.waves.plane_wave import PlaneWave


class GaussianWavePacket(WavePacket):
    """Gaussian wave packet: superposition of plane waves with gaussian envelope."""

    """
    Gaussian wave packet: superposition of plane waves with a gaussian envelope.
    The amplitudes of the underlying plane waves are weighted by a Gaussian distribution
    in the momentum (k) space.
    """

    def __init__(
        self,
        k_center: float,
        sigma_k: float,
        n_waves: int = 100,
        position_center: float = 0.0,
        time: float = 0.0,
        mass: float = ELECTRON_MASS,
    ):
        """
        Initialize Gaussian Wave Packet.

        Args:
            k_center: Center wave number (k0)
            sigma_k: Width of the packet in momentum space
            n_waves: Number of plane waves to use for the superposition
            position_center: Initial spatial center of the packet (x0)
            time: Initial time parameter
            mass: Particle mass
        """
        if sigma_k <= 0:
            raise ValueError("sigma_k must be positive")
        if n_waves <= 0:
            raise ValueError("n_waves must be a positive integer")

        self.k0 = k_center
        self.sigma_k = sigma_k

        k_min = k_center - 4 * sigma_k
        k_max = k_center + 4 * sigma_k
        k_values = np.linspace(k_min, k_max, n_waves)

        amplitudes = np.exp(-((k_values - k_center) ** 2) / (2 * sigma_k**2))

        plane_waves = []
        for k, amp in zip(k_values, amplitudes):
            wavelength = 2 * PI / k if k != 0 else 1e15

            pw = PlaneWave(
                amplitude=amp,
                wavelength=wavelength,
                position=position_center,
                masse=mass,
            )
            plane_waves.append(pw)

        super().__init__(plane_waves=plane_waves, time=time)

    def _extract_wave_numbers(self, plane_waves) -> np.ndarray:
        """Extract wave numbers from list of plane waves.
        :param plane_waves: List of PlaneWave instances
        :return: Numpy array of wave numbers
        """
        return np.array([pw.wave_number for pw in plane_waves])

    def _compute_k0(self, k0, k_values) -> float:
        """Compute or retrieve center momentum.
        :param k0: Provided center momentum wave number
        :param k_values: Numpy array of wave numbers from plane waves
        :return: Center momentum wave number
        """
        if k0 is not None:
            return k0
        return float(np.mean(k_values))

    def _compute_sigma_k(self, sigma_k, k_values) -> float:
        """Compute or retrieve momentum width.
        :param sigma_k: Provided momentum width
        :param k_values: Numpy array of wave numbers from plane waves
        :return: Momentum width
        """
        if sigma_k is not None:
            if sigma_k <= 0:
                raise ValueError("sigma_k must be positive")
            return sigma_k

        sigma = float(np.std(k_values))
        if sigma <= 0:
            raise ValueError("Cannot infer sigma_k from plane waves (zero spread in k)")

        return sigma

    def _gaussian_envelope(self, k: float) -> complex:
        """Compute gaussian envelope for given wave number.
        :param k: wave number
        :type k: float
        :return: envelope value at wave number k
        :rtype: complex
        """
        return np.exp(-((k - self.k0) ** 2) / (2 * self.sigma_k**2))
