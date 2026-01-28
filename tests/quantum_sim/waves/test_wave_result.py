# tests/quantum_sim/waves/test_wave_result.py
from quantum_sim.waves import WaveResult
import pytest
from pytest import fixture
import numpy as np

@fixture
def wave_result_data():
    x: np.ndarray = np.array([0.0, 1.0, 2.0])
    psi: np.ndarray = np.array([1+0j, 0+1j, 1-1j])
    t: np.ndarray = np.array([0.0])
    metadata: dict = {'amplitude': 1.0, 'wavelength': 2.0, 'mass': 1.0}
    return x, psi, t, metadata

@pytest.mark.unit
def test_wave_result_creation(wave_result_data):

    x, psi, t, metadata = wave_result_data
    result = WaveResult(x=x, psi=psi, t=t, metadata=metadata)

    assert (result.x == x).all()
    assert (result.psi == psi).all()
    assert (result.t == t).all()
    assert result.metadata == metadata

@pytest.mark.unit
def test_default_metadata_is_separate_instances():
    a = WaveResult(x=np.array([0.0]), psi=np.array([1+0j]))
    b = WaveResult(x=np.array([1.0]), psi=np.array([1+0j]))
    a.metadata['k'] = 1
    assert 'k' not in b.metadata

@pytest.mark.unit
def test_wave_result_copy(wave_result_data):

    x, psi, t, metadata = wave_result_data
    result = WaveResult(x=x, psi=psi, t=t, metadata=metadata)

    result_copy = result.copy()

    assert (result_copy.x == result.x).all()
    assert (result_copy.psi == result.psi).all()
    assert (result_copy.t == result.t).all()
    assert result_copy.metadata == result.metadata
    assert result_copy is not result

@pytest.mark.unit
def test_copy_arrays_and_metadata_independence(wave_result_data):
    x, psi, t, metadata = wave_result_data
    result = WaveResult(x=x, psi=psi, t=t, metadata=metadata.copy())

    result_copy = result.copy()
    result_copy.x[0] = 99.0
    result_copy.psi[1] = 2 + 2j
    result_copy.metadata['new_key'] = 'value'

    assert result.x[0] == 0.0
    assert result.psi[1] == 0 + 1j
    assert 'new_key' not in result.metadata

@pytest.mark.unit
def test_copy_with_none_t():
    result = WaveResult(x=np.array([0.0]), psi=np.array([1+0j]), t=None)
    copy = result.copy()
    assert copy.t is None
    assert copy is not result
