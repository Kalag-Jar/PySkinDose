import logging

import numpy as np
import pandas as pd

from ..beam_class import Beam
from ..constants import MODE_PLOT_EVENT
from .create_setup_and_event_plot import create_setup_and_event_plot
from ..phantom_class import Phantom

logger = logging.getLogger(__name__)


def plot_event(mode: str, data_norm: pd.DataFrame, event: int, patient: Phantom, table: Phantom, pad: Phantom):
    """Visualize the geometry from a specific irradiation event.

    This function plots an irradiation event with the patient,
    table, pad, and beam positioned according to the irradiation event
    specified by the parameter event

    Parameters
    ----------
    mode : str
        The function will only run if this is set to "plot_event".
    data_norm : pd.DataFrame
        Table containing dicom RDSR information from each irradiation event
        See parse_data.py for more information.
    event : int, optional
        choose specific irradiation event if mode "plot_event" are used
        Default is 0, in which the first irradiation event is considered.
    patient : Phantom
        Patient phantom from instance of class Phantom. Can be of
        phantom_model "plane", "cylinder" or "human"
    table : Phantom
        Table phantom from instance of class Phantom. phantom_model must be
        "table"
    pad : Phantom
        Pad phantom from instance of class Phantom. phantom_model must be
        "pad"
    """
    if mode != MODE_PLOT_EVENT:
        return

    logger.info(f"Plotting event {event + 1} of {len(data_norm)}")

    # Create beam
    beam = Beam(data_norm, event=event, plot_setup=False)

    # Position geometry
    patient.position(data_norm, event)
    table.position(data_norm, event)
    pad.position(data_norm, event)

    # Define hoover texts
    patient_text = [
        f"<b>Patient phantom</b><br><br><b>LAT: </b>{np.around(patient.r[ind, 2])} cm<br><b>LON: </b>{np.around(patient.r[ind, 0])} cm<br><b>VER: </b>{np.around(patient.r[ind, 1])} cm"
        for ind in range(len(patient.r))]

    table_text = [
        f"<b>Support table</b><br><br><b>LAT: </b>{np.around(table.r[ind, 2])} cm<br><b>LON: </b>{np.around(table.r[ind, 0])} cm<br><b>VER: </b>{np.around(table.r[ind, 1])} cm"
        for ind in range(len(table.r))]

    pad_text = [
        f"<b>Support pad</b><br><br><b>LAT: </b>{np.around(pad.r[ind, 2])} cm<br><b>LON: </b>{np.around(pad.r[ind, 0])} cm<br><b>VER: </b>{np.around(pad.r[ind, 1])} cm"
        for ind in range(len(pad.r))]

    source_text = [
        f"<b>X-ray source</b><br><br><b>LAT: </b>{np.around(beam.r[0, 2])} cm<br><b>LON: </b>{np.around(beam.r[0, 0])} cm<br><b>VER: </b>{np.around(beam.r[0, 1])} cm"]

    beam_text = [
        f"<b>X-ray beam vertex</b><br><br><b>LAT: </b>{np.around(beam.r[ind, 2])} cm<br><b>LON: </b>{np.around(beam.r[ind, 0])} cm<br><b>VER: </b>{np.around(beam.r[ind, 1])} cm"
        for ind in range(len(beam.r))]

    detectors_text = [
        f"<b>X-ray detector</b><br><br><b>LAT: </b>{np.around(beam.det_r[ind, 2])} cm<br><b>LON: </b>{np.around(beam.det_r[ind, 0])} cm<br><b>VER: </b>{np.around(beam.det_r[ind, 1])} cm"
        for ind in range(len(beam.det_r))]

    # Define plot title
    title = f"<b>P</b>y<b>S</b>kin<b>D</b>ose [mode: {mode}]"

    create_setup_and_event_plot(mode=mode, title=title,
                                patient=patient, patient_text=patient_text,
                                table=table, table_text=table_text,
                                pad=pad, pad_text=pad_text,
                                beam=beam, beam_text=beam_text,
                                source_text=source_text, detectors_text=detectors_text)
