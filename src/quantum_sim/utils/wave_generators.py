import numpy as np
from quantum_sim.waves.plane_wave import PlaneWave


def random_waves(n, amp_range=(0.1, 1.0), wavenumber_range=(0.5, 5.0), seed=None):
    """
    Generate n random PlaneWave instances.

    :param n: Number of plane waves to generate
    :type n: int
    :param amp_range: Range for random amplitudes (min, max)
    :type amp_range: tuple[float, float]
    :param wavenumber_range: Range for random wavenumber (min, max)
    :type wavenumber_range: tuple[float, float]
    :param seed: Random seed for reproducibility
    :type seed: int or None
    """
    if seed is not None:
        np.random.seed(seed)

    waves = []

    for _ in range(n):
        amplitude = np.random.uniform(*amp_range)
        wave_number = np.random.uniform(*wavenumber_range)
        waves.append((PlaneWave(amplitude, wave_number)))

    return waves


def waves_from_tuples(params):
    """
    Create PlaneWave instances from list of (amplitude, wave_number) tuples.

    :param params: list of tuples (amplitude, wave_number)
    :type params: list[tuple[float, float]]
    :returns: list of PlaneWave instances
    """
    waves = []
    for amplitude, wave_number in params:
        waves.append(PlaneWave(amplitude, wave_number))
    return waves


def waves_harmonics(n, first_wave_number):
    """
    Generate first n harmonics of a fundamental PlaneWave.

    :param n: Number of harmonics to generate
    :type n: int
    :param first_wave_number: Wavenumber of the fundamental wave
    :type first_wave_number: float
    :return: List of PlaneWave instances representing the harmonics
    """
    waves = []
    for i in range(1, n + 1):
        waves.append(PlaneWave(i / 10, first_wave_number / i))
    return waves
