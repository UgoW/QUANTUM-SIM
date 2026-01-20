# tests/quantum_sim/waves/test_plane_wave.py
from quantum_sim.waves import PlaneWave
from quantum_sim.utils.constants import ELECTRON_MASS, REDUCED_PLANCK_CONSTANT
import pytest
from pytest import fixture
import numpy as np

@fixture
def plane_wave_params():
    amplitude = 1.0 + 0.0j
    wavelength = 5.0
    position = 0.0
    phase = 0.0
    time = 0.0
    masse = 9.10938356e-31  # Electron mass
    return amplitude, wavelength, position, phase, time, masse

@pytest.mark.unit
def test_plane_wave_initialization(plane_wave_params):
    amplitude, wavelength, position, phase, time, masse = plane_wave_params
    wave = PlaneWave(amplitude, wavelength, position, phase, time, masse)
    
    assert wave.amplitude == amplitude
    assert wave.wavelength == wavelength
    assert wave.position == position
    assert wave.phase == phase
    assert wave.masse == masse
    assert wave.time == time
    