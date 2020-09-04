import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as ply
from typing import Dict

from pyskindose.phantom_class import Phantom
from pyskindose.beam_class import Beam
from .plot_event import plot_event
from .plot_procedure import plot_procedure
from .plot_setup import plot_setup


def plot_geometry(patient: Phantom, table: Phantom, pad: Phantom,
                  data_norm: pd.DataFrame, mode: str, event: int = 0,
                  include_patient: bool = False) -> None:
    """Visualize the geometry from the irradiation events.

    This function plots the phantom, table, pad, beam and detector. The type of
    plot is specified in the parameter mode.

    Parameters
    ----------
    patient : Phantom
        Patient phantom from instance of class Phantom. Can be of
        phantom_model "plane", "cylinder" or "human"
    table : Phantom
        Table phantom from instance of class Phantom. phantom_model must be
        "table"
    pad : Phantom
        Pad phantom from instance of class Phantom. phantom_model must be
        "pad"
    data_norm : pd.DataFrame
        Table containing dicom RDSR information from each irradiation event
        See parse_data.py for more information.
    mode : str
        Choose between "plot_setup", "plot_event" and "plot_procedure".

         "plot_setup" plots the patient, table and pad in reference position
         together with the X-ray system with zero angulation. This is a
         debugging feature

        "plot_event" plots a specific irradiation event, in which the patient,
        table, pad, and beam are positioned according to the irradiation event
        specified by the parameter event

        "plot_procedure" plots out the X-ray system, table and pad for all
        irradiation events in the procedure The visible event are chosen by a
        event slider

    event : int, optional
        choose specific irradiation event if mode "plot_event" are used
        Default is 0, in which the first irradiation event is considered.

    include_patient : bool, optional
        Choose if the patient phantom should be included in the plot_procedure
        function. WARNING, very heavy on memory. Default is False.

    """
    # Define colors
    source_color = '#D3D3D3'
    table_color = '#D3D3D3'
    detector_color = '#D3D3D3'
    pad_color = 'slateblue'
    beam_color = 'red'
    patient_color = '#CE967C'
    azure_dark = '#201f1e'

    # Visual offset to show plane phantom correctly
    if patient.phantom_model == "plane":
        visual_offset = -0.01
    else:
        visual_offset = 0

    # Camera view settings
    camera = dict(up=dict(x=0, y=-1, z=0),
                  center=dict(x=0, y=0, z=0),
                  eye=dict(x=-1.3, y=-1.3, z=0.7))

    plot_setup(mode=mode, data_norm=data_norm, patient=patient, table=table, pad=pad)
    plot_event(mode=mode, data_norm=data_norm, event=event, patient=patient, table=table, pad=pad)
    plot_procedure(mode=mode, data_norm=data_norm, include_patient=include_patient)

    if mode == "plot_procedure":
        print(f'plotting entire procedure with {len(data_norm)}'
              ' irradiation events...')

        title = f"<b>P</b>y<b>S</b>kin<b>D</b>ose [mode: {mode}]"
        source_mesh = [0] * len(data_norm)
        table_mesh = [0] * len(data_norm)
        patient_mesh = [0] * len(data_norm)
        detector_mesh = [0] * len(data_norm)
        pad_mesh = [0] * len(data_norm)
        beam_mesh = [0] * len(data_norm)
        wf_beam = [0] * len(data_norm)
        wf_table = [0] * len(data_norm)
        wf_pad = [0] * len(data_norm)
        wf_detector = [0] * len(data_norm)

        # For each irradiation event
        for i in range(len(data_norm)):

            # Position geometry objects
            beam = Beam(data_norm, event=i, plot_setup=False)
            table.position(data_norm, i)
            pad.position(data_norm, i)

            # Define hoover texts and title
            source_text = [f"<b>X-ray source</b><br><br><b>LAT: </b>{np.around(beam.r[0, 2])} cm<br><b>LON: </b>{np.around(beam.r[0, 0])} cm<br><b>VER: </b>{np.around(beam.r[0, 1])} cm"]

            beam_text = [f"<b>X-ray beam vertex</b><br><br><b>LAT: </b>{np.around(beam.r[ind, 2])} cm<br><b>LON: </b>{np.around(beam.r[ind, 0])} cm<br><b>VER: </b>{np.around(beam.r[ind, 1])} cm"
                for ind in range(len(beam.r))]

            detectors_text = [f"<b>X-ray detector</b><br><br><b>LAT: </b>{np.around(beam.det_r[ind, 2])} cm<br><b>LON: </b>{np.around(beam.det_r[ind, 0])} cm<br><b>VER: </b>{np.around(beam.det_r[ind, 1])} cm"
                for ind in range(len(beam.det_r))]

            patient_text = [f"<b>Patient phantom</b><br><br><b>LAT: </b>{np.around(patient.r[ind, 2])} cm<br><b>LON: </b>{np.around(patient.r[ind, 0])} cm<br><b>VER: </b>{np.around(patient.r[ind, 1])} cm"
                for ind in range(len(patient.r))]

            table_text = [f"<b>Support table</b><br><br><b>LAT: </b>{np.around(table.r[ind, 2])} cm<br><b>LON: </b>{np.around(table.r[ind, 0])} cm<br><b>VER: </b>{np.around(table.r[ind, 1])} cm"
                for ind in range(len(table.r))]


            pad_text = [f"<b>Support pad</b><br><br><b>LAT: </b>{np.around(pad.r[ind, 2])} cm<br><b>LON: </b>{np.around(pad.r[ind, 0])} cm<br><b>VER: </b>{np.around(pad.r[ind, 1])} cm"
                for ind in range(len(pad.r))]


            if include_patient:
                patient.position(data_norm, i)

                # Create patient mesh
                patient_mesh[i] = go.Mesh3d(
                    x=patient.r[:, 0], y=patient.r[:, 1] + visual_offset,
                    z=patient.r[:, 2], i=patient.ijk[:, 0],
                    j=patient.ijk[:, 1], k=patient.ijk[:, 2],
                    color=patient_color, hoverinfo="text",
                    visible=False, text=patient_text,
                    lighting=dict(diffuse=0.5, ambient=0.5))

            # Create X-ray source mesh
            source_mesh[i] = go.Scatter3d(
                x=[beam.r[0, 0], beam.r[0, 0]],
                y=[beam.r[0, 1], beam.r[0, 1]],
                z=[beam.r[0, 2], beam.r[0, 2]],
                mode="markers", hoverinfo="text", visible=False,
                marker=dict(size=8, color=source_color),
                text=source_text)

            # Create support table mesh
            table_mesh[i] = go.Mesh3d(
                x=table.r[:, 0], y=table.r[:, 1], z=table.r[:, 2],
                i=table.ijk[:, 0], j=table.ijk[:, 1], k=table.ijk[:, 2],
                color=table_color, hoverinfo="text", visible=False,
                text=table_text)

            # Create X-ray detector mesh
            detector_mesh[i] = go.Mesh3d(
                x=beam.det_r[:, 0], y=beam.det_r[:, 1], z=beam.det_r[:, 2],
                i=beam.det_ijk[:, 0],
                j=beam.det_ijk[:, 1],
                k=beam.det_ijk[:, 2],
                color=detector_color, hoverinfo="text", visible=False,
                text=detectors_text)

            # Create support pad mesh
            pad_mesh[i] = go.Mesh3d(
                x=pad.r[:, 0], y=pad.r[:, 1], z=pad.r[:, 2],
                i=pad.ijk[:, 0], j=pad.ijk[:, 1], k=pad.ijk[:, 2],
                color=pad_color, hoverinfo="text", visible=False,
                text=pad_text)

            # Create X-ray beam mesh
            beam_mesh[i] = go.Mesh3d(
                x=beam.r[:, 0], y=beam.r[:, 1], z=beam.r[:, 2],
                i=beam.ijk[:, 0], j=beam.ijk[:, 1], k=beam.ijk[:, 2],
                color=beam_color, hoverinfo="text", visible=False, opacity=0.3,
                text=beam_text)

            # Add wireframes to mesh objects
            wf_beam[i], wf_table[i], wf_pad[i], wf_detector[i] = \
                create_wireframes(beam, table, pad,
                                  line_width=4, visible=False)

        # Set first irradiation event initally visible
        source_mesh[0].visible = table_mesh[0].visible = pad_mesh[0].visible \
            = detector_mesh[0].visible = beam_mesh[0].visible = \
            wf_beam[0].visible = wf_table[0].visible = wf_pad[0].visible = \
            wf_detector[0].visible = True

        if include_patient:
            patient_mesh[0].visible = True

        steps = []

        # Event slider settings
        for i in range(len(data_norm)):
            step: Dict = dict(method='restyle',
                              args=['visible', [False] * len(data_norm)],
                              label=i + 1)
            step['args'][1][i] = True  # Toggle i'th trace to "visible"
            steps.append(step)

        sliders = [dict(active=0,
                        transition=dict(duration=300, easing="quad-in-out"),
                        bordercolor="rgb(45,45,45)",
                        borderwidth=3,
                        tickcolor="white",
                        bgcolor="red",
                        currentvalue=dict(prefix="Active event: ",
                                          suffix=f" of {len(data_norm)}",
                                          font=dict(color="white", size=30)),
                        font=dict(family="Franklin Gothic", color="white", size=16),
                        pad=dict(b=10, t=10, l=250, r=250),
                        steps=steps)]

        # Layout settings
        layout = go.Layout(
            sliders=sliders,
            font=dict(family='Franklin Gothic', size=14),
            hoverlabel=dict(font=dict(family="Consolas, monospace", size=16)),
            showlegend=False,
            dragmode="orbit",
            title=title,
            titlefont=dict(family='Franklin Gothic', size=35,
                           color='white'),
            plot_bgcolor=azure_dark,
            paper_bgcolor=azure_dark,

            scene=dict(aspectmode="cube", camera=camera,

                       xaxis=dict(title='X - LON [cm]',
                                  range=[-150, 150],
                                  color="white",
                                  zerolinecolor="limegreen", zerolinewidth=3),

                       yaxis=dict(title="Y - VER [cm]",
                                  range=[-150, 150],
                                  color="white",
                                  zerolinecolor="limegreen", zerolinewidth=3),

                       zaxis=dict(title='Z - LAT [cm]',
                                  range=[-150, 150],
                                  color="white",
                                  zerolinecolor="limegreen", zerolinewidth=3)))
        if include_patient:
            data = source_mesh + table_mesh + pad_mesh + patient_mesh + \
                beam_mesh + detector_mesh + wf_table + wf_pad + wf_beam + \
                wf_detector

        else:
            data = source_mesh + table_mesh + pad_mesh + beam_mesh + \
                detector_mesh + wf_table + wf_pad + wf_beam + wf_detector

        fig = go.Figure(data=data, layout=layout)
        # Execute plot
        ply.plot(fig, filename=f'{mode}.html')


