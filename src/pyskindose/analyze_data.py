from typing import Any, Dict, Optional

import pandas as pd

from pyskindose import constants as const
from pyskindose.calculate_dose.calculate_dose import calculate_dose
from pyskindose.phantom_class import Phantom
from pyskindose.plotting.create_dose_map_plot import create_dose_map_plot
from pyskindose.plotting.plot_without_dose_map import plot_without_dose_map
from pyskindose.settings import PyskindoseSettings


def analyze_data(normalized_data: pd.DataFrame, settings: PyskindoseSettings, plot_dose_map: Optional[bool] = False) -> Dict[str, Any]:
    # create table, pad and patient phantoms.
    table = Phantom(phantom_model=const.PHANTOM_MODEL_TABLE, phantom_dim=settings.phantom.dimension)
    pad = Phantom(phantom_model=const.PHANTOM_MODEL_PAD, phantom_dim=settings.phantom.dimension)

    # TODO rename function
    plot_without_dose_map(normalized_data=normalized_data, table=table, pad=pad, settings=settings)

    patient, output = calculate_dose(normalized_data=normalized_data, settings=settings, table=table, pad=pad)

    if not plot_dose_map:
        return output

    create_dose_map_plot(patient=patient, settings=settings, dose_map=output[const.OUTPUT_KEY_DOSE_MAP])
    return output
