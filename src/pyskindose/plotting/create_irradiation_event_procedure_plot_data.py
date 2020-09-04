import logging
from typing import Dict, Optional, Union

import numpy as np
import pandas as pd
import plotly.graph_objs as go

from ..beam_class import Beam
from .create_mesh3d import create_mesh_3d_general
from .create_wireframes import create_wireframes
from ..constants import (
    COLOR_BEAM,
    COLOR_DETECTOR,
    COLOR_PAD,
    COLOR_PATIENT,
    COLOR_SOURCE,
    COLOR_TABLE,
    MESH_OPACITY_BEAM,
    IRRADIATION_EVENT_PROCEDURE_KEY_BEAM,
    IRRADIATION_EVENT_PROCEDURE_KEY_DETECTORS,
    IRRADIATION_EVENT_PROCEDURE_KEY_PAD,
    IRRADIATION_EVENT_PROCEDURE_KEY_PATIENT,
    IRRADIATION_EVENT_PROCEDURE_KEY_SOURCE,
    IRRADIATION_EVENT_PROCEDURE_KEY_TABLE,
    IRRADIATION_EVENT_PROCEDURE_KEY_WIRE_FRAME_BEAM,
    IRRADIATION_EVENT_PROCEDURE_KEY_WIRE_FRAME_DETECTORS,
    IRRADIATION_EVENT_PROCEDURE_KEY_WIRE_FRAME_PAD,
    IRRADIATION_EVENT_PROCEDURE_KEY_WIRE_FRAME_TABLE,
)
from ..phantom_class import Phantom

logger = logging.getLogger(__name__)


def create_irradiation_event_procedure_plot_data(data_norm: pd.DataFrame, include_patient: bool,
                                                 visible_status: bool, event: int, table: Phantom,
                                                 pad: Phantom, patient: Optional[Phantom] = None
                                                 ) -> Dict[str, Union[go.Scatter3d, go.Mesh3d]]:
    # Position geometry objects
    beam = Beam(data_norm, event=event, plot_setup=False)
    table.position(data_norm, event)
    pad.position(data_norm, event)

    # Define hoover texts and title
    source_text = [
        f"<b>X-ray source</b><br><br><b>LAT: </b>{np.around(beam.r[0, 2])} cm<br><b>LON: </b>{np.around(beam.r[0, 0])} cm<br><b>VER: </b>{np.around(beam.r[0, 1])} cm"]

    beam_text = [
        f"<b>X-ray beam vertex</b><br><br><b>LAT: </b>{np.around(beam.r[ind, 2])} cm<br><b>LON: </b>{np.around(beam.r[ind, 0])} cm<br><b>VER: </b>{np.around(beam.r[ind, 1])} cm"
        for ind in range(len(beam.r))]

    detectors_text = [
        f"<b>X-ray detector</b><br><br><b>LAT: </b>{np.around(beam.det_r[ind, 2])} cm<br><b>LON: </b>{np.around(beam.det_r[ind, 0])} cm<br><b>VER: </b>{np.around(beam.det_r[ind, 1])} cm"
        for ind in range(len(beam.det_r))]

    patient_text = [
        f"<b>Patient phantom</b><br><br><b>LAT: </b>{np.around(patient.r[ind, 2])} cm<br><b>LON: </b>{np.around(patient.r[ind, 0])} cm<br><b>VER: </b>{np.around(patient.r[ind, 1])} cm"
        for ind in range(len(patient.r))]

    table_text = [
        f"<b>Support table</b><br><br><b>LAT: </b>{np.around(table.r[ind, 2])} cm<br><b>LON: </b>{np.around(table.r[ind, 0])} cm<br><b>VER: </b>{np.around(table.r[ind, 1])} cm"
        for ind in range(len(table.r))]

    pad_text = [
        f"<b>Support pad</b><br><br><b>LAT: </b>{np.around(pad.r[ind, 2])} cm<br><b>LON: </b>{np.around(pad.r[ind, 0])} cm<br><b>VER: </b>{np.around(pad.r[ind, 1])} cm"
        for ind in range(len(pad.r))]

    output = {}

    if include_patient:
        patient.position(data_norm, event)

        # Create patient mesh
        output[IRRADIATION_EVENT_PROCEDURE_KEY_PATIENT] = create_mesh_3d_general(
            obj=patient, color=COLOR_PATIENT, mesh_text=patient_text,
            lighting=dict(diffuse=0.5, ambient=0.5))

    # Create X-ray source mesh
    output[IRRADIATION_EVENT_PROCEDURE_KEY_SOURCE] = go.Scatter3d(
            x=[beam.r[0, 0], beam.r[0, 0]],
            y=[beam.r[0, 1], beam.r[0, 1]],
            z=[beam.r[0, 2], beam.r[0, 2]],
            mode="markers", hoverinfo="text", visible=visible_status,
            marker=dict(size=8, color=COLOR_SOURCE),
            text=source_text)

    # Create support table mesh
    output[IRRADIATION_EVENT_PROCEDURE_KEY_TABLE] = create_mesh_3d_general(
        obj=table, color=COLOR_TABLE, mesh_text=table_text, visible_status=visible_status)

    # Create X-ray detector mesh
    output[IRRADIATION_EVENT_PROCEDURE_KEY_DETECTORS] = create_mesh_3d_general(
        obj=beam, color=COLOR_DETECTOR, mesh_text=detectors_text, visible_status=visible_status,
        detector_mesh=True
    )

    # Create support pad mesh
    output[IRRADIATION_EVENT_PROCEDURE_KEY_PAD] = create_mesh_3d_general(
        obj=pad, color=COLOR_PAD, mesh_text=pad_text, visible_status=visible_status
    )

    # Create X-ray beam mesh
    output[IRRADIATION_EVENT_PROCEDURE_KEY_BEAM] = create_mesh_3d_general(
        obj=beam, color=COLOR_BEAM, mesh_text=beam_text, visible_status=visible_status,
        opacity=MESH_OPACITY_BEAM
    )

    # Create wireframe meshes
    [
        output[IRRADIATION_EVENT_PROCEDURE_KEY_WIRE_FRAME_BEAM],
        output[IRRADIATION_EVENT_PROCEDURE_KEY_WIRE_FRAME_TABLE],
        output[IRRADIATION_EVENT_PROCEDURE_KEY_WIRE_FRAME_PAD],
        output[IRRADIATION_EVENT_PROCEDURE_KEY_WIRE_FRAME_DETECTORS],
    ] = create_wireframes(
        beam=beam, table=table, pad=pad, line_width=4, visible=visible_status)

    return output
