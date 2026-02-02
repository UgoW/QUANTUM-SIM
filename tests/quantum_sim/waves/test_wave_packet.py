from quantum_sim.waves.wave_packet import WavePacket
from quantum_sim.waves.plane_wave import PlaneWave
import pytest
from pytest import fixture
import numpy as np

@pytest.fixture
def plane_waves():
    return [
        PlaneWave(amplitude=1.0, wavelength=1.0),
        PlaneWave(amplitude=1.0, wavelength=2.0),
    ]

@pytest.fixture
def x_grid():
    return np.linspace(-10, 10, 1000)

@pytest.fixture
def wave_packet(plane_waves):
    return WavePacket(plane_waves=plane_waves)

@pytest.mark.unit
def test_wave_packet_creation(wave_packet):
    assert isinstance(wave_packet, WavePacket)
    assert len(wave_packet.plane_waves) == 2

@pytest.mark.unit
def test_wave_packet_is_sum_of_plane_waves(wave_packet, plane_waves, x_grid):
    psi_packet = wave_packet.evaluate(x_grid)
    psi_sum = sum(pw.evaluate(x_grid) for pw in plane_waves)

    assert np.allclose(psi_packet, psi_sum)

@pytest.mark.unit
def test_probability_density_positive(wave_packet, x_grid):
    prob = wave_packet.probability_density(x_grid)

    assert np.all(prob >= 0)


