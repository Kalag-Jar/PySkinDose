import logging
from typing import Any, Dict, Optional, Tuple

import numpy as np
import pandas as pd
from pyskindose.calculate_dose.calculate_irradiation_event_result import calculate_irradiation_event_result

from pyskindose import constants as const
from pyskindose.corrections import (
    calculate_k_bs,
    calculate_k_tab
)
from pyskindose.geom_calc import (
    check_new_geometry,
    fetch_and_append_hvl,
    position_geometry)
from pyskindose.phantom_class import Phantom
from pyskindose.settings import PyskindoseSettings

logger = logging.getLogger(__name__)


def calculate_dose(normalized_data: pd.DataFrame, settings: PyskindoseSettings, table: Phantom,
                   pad: Phantom) -> Tuple[Phantom, Optional[Dict[str, Any]]]:
    if settings.mode != const.MODE_CALCULATE_DOSE:
        logger.debug("Mode not set to calculate dose. Returning without doing anything")
        return None

    logger.info("Start performing dose calculations")
    patient = Phantom(
        phantom_model=settings.phantom.model,
        phantom_dim=settings.phantom.dimension,
        human_mesh=settings.phantom.human_mesh)

    # position objects in starting position
    position_geometry(
        patient=patient, table=table, pad=pad,
        pad_thickness=settings.phantom.dimension.pad_thickness,
        patient_offset=[
            settings.phantom.patient_offset.d_lat,
            settings.phantom.patient_offset.d_ver,
            settings.phantom.patient_offset.d_lon])

    normalized_data = fetch_and_append_hvl(data_norm=normalized_data)

    # Check which irradiation events that contains updated
    # geometry parameters since the previous irradiation event
    new_geometry = check_new_geometry(normalized_data)

    # fetch of k_bs interpolation object (k_bs=f(field_size))for all events
    back_scatter_interpolation = calculate_k_bs(data_norm=normalized_data)

    k_tab = calculate_k_tab(data_norm=normalized_data,
                            estimate_k_tab=settings.estimate_k_tab,
                            k_tab_val=settings.k_tab_val)

    total_number_of_events = len(normalized_data)

    output_template = {
        const.OUTPUT_KEY_HITS: [[]] * total_number_of_events,
        const.OUTPUT_KEY_KERMA: [np.array] * total_number_of_events,
        const.OUTPUT_KEY_CORRECTION_INVERSE_SQUARE_LAW: [[]] * total_number_of_events,
        const.OUTPUT_KEY_CORRECTION_BACK_SCATTER: [[]] * total_number_of_events,
        const.OUTPUT_KEY_CORRECTION_MEDIUM: [[]] * total_number_of_events,
        const.OUTPUT_KEY_CORRECTION_TABLE: [[]] * total_number_of_events,
        const.OUTPUT_KEY_DOSE_MAP: np.zeros(len(patient.r))
    }

    output = calculate_irradiation_event_result(
        normalized_data=normalized_data, event=0, total_events=len(normalized_data), new_geometry=new_geometry,
        k_tab=k_tab, hits=[], patient=patient, table=table, pad=pad,
        back_scatter_interpolation=back_scatter_interpolation, output=output_template
    )

    return output

