import numpy as np
from quantum_sim.waves.plane_wave import PlaneWave

def random_waves(n, amp_range=(0.1, 1.0), wavelength_range=(0.5, 5.0), seed=None):
    """
    Generate n random PlaneWave instances.
    
    :param n: Number of plane waves to generate
    :type n: int
    :param amp_range: Range for random amplitudes (min, max)
    :type amp_range: tuple[float, float]
    :param wavelength_range: Range for random wavelengths (min, max)
    :type wavelength_range: tuple[float, float]
    :param seed: Random seed for reproducibility
    :type seed: int or None
    """
    if seed is not None:
        np.random.seed(seed)

    waves = []

    for _ in range(n):
        amplitude = np.random.uniform(*amp_range)
        wavelength = np.random.uniform(*wavelength_range)
        waves.append((PlaneWave(amplitude, wavelength)))

    return waves

def waves_from_tuples(params):
    """
    Create PlaneWave instances from list of (amplitude, wavelength) tuples.

    :param params: list of tuples (amplitude, wavelength)
    :type params: list[tuple[float, float]]
    :returns: list of PlaneWave instances
    """
    waves = []
    for amplitude, wavelength in params:
        waves.append(PlaneWave(amplitude, wavelength))
    return waves

def waves_harmonics(n, first_wave_length):
  """
    Generate first n harmonics of a fundamental PlaneWave.

    :param n: Number of harmonics to generate
    :type n: int
    :param first_wave_length: Wavelength of the fundamental wave
    :type first_wave_length: float
    :return: List of PlaneWave instances representing the harmonics
  """
  waves = []
  for i in range(1, n+1):
    waves.append(PlaneWave(i/10, first_wave_length/i))
  return waves