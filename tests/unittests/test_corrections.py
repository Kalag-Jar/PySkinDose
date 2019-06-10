from pathlib import Path
import numpy as np
import pandas as pd
import sys

from pyskindose.corrections import calculate_k_bs
from pyskindose.corrections import calculate_k_med
from pyskindose.corrections import calculate_k_isq

p = Path(__file__).parent.parent.parent
sys.path.insert(1, str(p.absolute()))


def test_calculate_k_isq_unchanged_fluence():
    # Tests if the X-ray fluence is left unscaled if cell is located at the
    # distance source to IRP
    expected = 1
    test = calculate_k_isq(source=np.array([0, 0, 0]),
                           cells=np.array([0, 100, 0]),
                           dref=100)
    assert expected == test


def test_calculate_k_isq_increased_fluence():
    # Tests if the fluence is correctly increased at a smaller distance then
    # distance source to IRP
    expected = 4
    test = calculate_k_isq(source=np.array([0, 0, 0]),
                           cells=np.array([0, 50, 0]),
                           dref=100)
    assert expected == test


def test_calculate_k_isq_decreased_fluence():
    # Tests if the fluence is correctly decreased at a larger distance then
    # distance source to IRP
    expected = 0.25
    test = calculate_k_isq(source=np.array([0, 0, 0]),
                           cells=np.array([0, 200, 0]),
                           dref=100)
    assert expected == test


def test_calculate_k_bs():
    # Tests if the interpolated backscatter factor lies within 1% of the
    # tabulated value, for all tabulated field sizes at a specific kVp/HVL
    # combination.

    expected = 5 * [True]

    # Tabulated backscatter factor for param in data_norm
    tabulated_k_bs = [1.3, 1.458, 1.589, 1.617, 1.639]

    data_norm = pd.DataFrame({'kVp': 5 * [80], 'HVL': 5 * [7.88], 
                              'FSL': [5, 10, 20, 25, 35]})

    # create interpolation object
    bs_interp = calculate_k_bs(data_norm)

    # interpolate at tabulated filed sizes
    k_bs = bs_interp[0](data_norm.FSL)

    diff = [100 * (abs(k_bs[i] - tabulated_k_bs[i])) / tabulated_k_bs[i]
            for i in range(len(tabulated_k_bs))]

    test = [percent_difference <= 1 for percent_difference in diff]

    assert expected == test


def test_calculate_k_med():

    # Expected k_med factors for kVp = 80 kV and HVL = 4.99 mmAl
    expected = [1.027, 1.026, 1.025, 1.025, 1.025]

    data = {'kVp': [80], 'HVL': [4.99]}
    data_norm = pd.DataFrame(data)

    # Tests if we get a value in expected, for cells with different field
    # sizes with filed side length in [5 to 35] cm.
    test = calculate_k_med(data_norm, np.square([6, 10, 20, 22, 32]), 0)

    assert test in expected