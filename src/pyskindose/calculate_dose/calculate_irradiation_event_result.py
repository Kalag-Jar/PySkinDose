from typing import List, Dict, Any

import numpy as np
import pandas as pd
from pyskindose import Phantom, constants as const
from pyskindose.calculate_dose.add_correction_and_event_dose_to_output import add_corrections_and_event_dose_to_output
# from pyskindose.calculate_dose.calculate_dose import logger
from pyskindose.calculate_dose.perform_calculations_for_new_geometries import perform_calculations_for_new_geometries
from scipy.interpolate import CubicSpline


def calculate_irradiation_event_result(normalized_data: pd.DataFrame, event: int, total_events: int,
                                       new_geometry: List[bool], k_tab: List[float], hits: List[bool],
                                       patient: Phantom, table: Phantom, pad: Phantom,
                                       back_scatter_interpolation: List[CubicSpline],
                                       output: Dict[str, Any], table_hits: List[bool] = None,
                                       field_area: List[float] = None, k_isq: np.array = None) -> Dict[str, Any]:
    #logger.debug(f"Calculating irradiation event {event + 1} out of {total_events}")

    hits, table_hits, field_area, k_isq = perform_calculations_for_new_geometries(
        normalized_data=normalized_data, event=event, new_geometry=new_geometry[event],
        patient=patient, table=table, pad=pad, hits=hits,
        table_hits=table_hits, field_area=field_area, k_isq=k_isq
    )

    #logger.debug("Saving event data")
    output[const.OUTPUT_KEY_HITS][event] = hits
    output[const.OUTPUT_KEY_KERMA][event] = normalized_data.K_IRP[event]
    output[const.OUTPUT_KEY_CORRECTION_INVERSE_SQUARE_LAW][event] = k_isq

    output = add_corrections_and_event_dose_to_output(normalized_data=normalized_data, event=event, hits=hits,
                                                      table_hits=table_hits, patient=patient,
                                                      back_scatter_interpolation=back_scatter_interpolation,
                                                      field_area=field_area, k_tab=k_tab, output=output)

    event += 1
    if event < total_events:
        output = calculate_irradiation_event_result(
            normalized_data=normalized_data, event=event, total_events=total_events,
            new_geometry=new_geometry, k_tab=k_tab, hits=hits, patient=patient, table=table, pad=pad,
            back_scatter_interpolation=back_scatter_interpolation, output=output
        )

    return output