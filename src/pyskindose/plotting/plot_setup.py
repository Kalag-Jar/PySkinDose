import logging

import numpy as np
import pandas as pd

from ..beam_class import Beam
from ..constants import MODE_PLOT_SETUP
from .create_setup_and_event_plot import create_setup_and_event_plot
from ..phantom_class import Phantom

logger = logging.getLogger(__name__)


def plot_setup(mode: str, data_norm: pd.DataFrame, patient: Phantom, table: Phantom, pad: Phantom):
    """Debugging feature for visualizing the geometry setup from the irradiation events.

    This function plots the patient, table and pad in reference position
    together with the X-ray system with zero angulation.

    Parameters
    ----------
    mode : str
        The function will only run if this is set to "plot_setup".
    data_norm : pd.DataFrame
        Table containing dicom RDSR information from each irradiation event
        See parse_data.py for more information.
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
    if mode != MODE_PLOT_SETUP:
        return

    logger.info("plotting geometry setup...")

    logger.debug("Creating beam")
    beam = Beam(data_norm, event=0, plot_setup=True)

    logger.debug("Creating hover texts")
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
        f"<b>X-ray detector</b><br><br><b>LAT: </b>{np.around(beam.det_r[ind, 2])} cm<br><b>LON: </b>{np.around(beam.det_r[ind, 0])} cm<br><b>VER: </b> {np.around(beam.det_r[ind, 1])} cm"
        for ind in range(len(beam.det_r))]

    # Define plot title
    title = f"<b>P</b>y<b>S</b>kin<b>D</b>ose [mode: {mode}]"

    create_setup_and_event_plot(mode=mode, title=title,
                                patient=patient, patient_text=patient_text,
                                table=table, table_text=table_text,
                                pad=pad, pad_text=pad_text,
                                beam=beam, beam_text=beam_text,
                                source_text=source_text, detectors_text=detectors_text)