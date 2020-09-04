import logging
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import plotly.graph_objs as go

from ..constants import (
    IRRADIATION_EVENT_STEP_KEY_ARGUMENTS,
    IRRADIATION_EVENT_STEP_KEY_LABEL,
    IRRADIATION_EVENT_STEP_KEY_METHOD,
    MODE_PLOT_PROCEDURE,
    PLOT_SLIDER_BORDER_COLOR, PLOT_SLIDER_TICK_COLOR, PLOT_SLIDER_BACKGROUND_COLOR, PLOT_FONT_FAMILY, COLOR_PLOT_TEXT,
    PLOT_SLIDER_PADDING, PLOT_SLIDER_TRANSITION, PLOT_SLIDER_BORDER_WIDTH, PLOT_SLIDER_FONT_SIZE_CURRENT,
    PLOT_SLIDER_FONT_SIZE_GENERAL, COLOR_AZURE_DARK, PLOT_TITLE_FONT_FAMILY, PLOT_TITLE_FONT_SIZE
)
from .create_irradiation_event_procedure_plot_data import create_irradiation_event_procedure_plot_data
from .get_camera_view import get_camera_view
from ..phantom_class import Phantom

logger = logging.getLogger(__name__)


def plot_procedure(mode: str, data_norm: pd.DataFrame, include_patient: bool, patient: Optional[Phantom] = None):
    if mode != MODE_PLOT_PROCEDURE:
        return

    if include_patient and patient is None:
        logger.error("Plot procedure called with include patient but no patient input")
        raise IOError("Patient object must be given when include_patient set to True")

    logger.info(f"Plotting entire procedure with {len(data_norm)} irradiation events")
    title = f"<b>P</b>y<b>S</b>kin<b>D</b>ose [mode: {mode}]"

    meshes = [
        create_irradiation_event_procedure_plot_data(
            data_norm=data_norm,
            include_patient=include_patient,
            visible_status=(ind == 0),
            event=ind,
            patient=(patient if include_patient else None)
        )
        for ind in range(len(data_norm))
    ]

    layout = _create_procedure_layout(title=title, total_events=len(data_norm))


def _create_event_slider_step(total_events: int, event: int) -> Dict[str, Any]:
    step = {
        IRRADIATION_EVENT_STEP_KEY_METHOD: "restyle",
        IRRADIATION_EVENT_STEP_KEY_ARGUMENTS: ['visible', [False] * total_events],
        IRRADIATION_EVENT_STEP_KEY_LABEL: event + 1
    }
    step[IRRADIATION_EVENT_STEP_KEY_ARGUMENTS][1][event] = True

    return step


def _create_sliders(steps: List[Dict], total_events: int) -> List[Dict[str, Any]]:
    return [
        dict(
            active=0,
            transition=PLOT_SLIDER_TRANSITION,
            bordercolor=PLOT_SLIDER_BORDER_COLOR,
            borderwidth=PLOT_SLIDER_BORDER_WIDTH,
            tickcolor=PLOT_SLIDER_TICK_COLOR,
            bgcolor=PLOT_SLIDER_BACKGROUND_COLOR,
            currentvalue=dict(prefix="Active event: ",
                              suffix=f" of {total_events}",
                              font=dict(color=COLOR_PLOT_TEXT, size=PLOT_SLIDER_FONT_SIZE_CURRENT)),
            font=dict(family=PLOT_FONT_FAMILY, color=COLOR_PLOT_TEXT, size=PLOT_SLIDER_FONT_SIZE_GENERAL),
            pad=PLOT_SLIDER_PADDING,
            steps=steps
        )
    ]


def _create_procedure_layout(title: str, total_events: int) -> go.Layout:
    steps = [_create_event_slider_step(total_events=total_events, event=ind) for ind in range(total_events)]

    return go.Layout(
        sliders=_create_sliders(steps=steps, total_events=total_events),
        font=dict(family='Franklin Gothic', size=14),
        hoverlabel=dict(font=dict(family="Consolas, monospace", size=16)),
        showlegend=False,
        dragmode="orbit",
        title=title,
        titlefont=dict(family=PLOT_TITLE_FONT_FAMILY, size=PLOT_TITLE_FONT_SIZE,
                       color=COLOR_PLOT_TEXT),
        plot_bgcolor=COLOR_AZURE_DARK,
        paper_bgcolor=COLOR_AZURE_DARK,
        scene=dict(aspectmode="cube",
                   camera=get_camera_view(),
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
                              zerolinecolor="limegreen", zerolinewidth=3)
                   )
    )




