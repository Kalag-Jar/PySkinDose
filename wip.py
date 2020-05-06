from src.pyskindose.parse_data import rdsr_normalizer
from src.pyskindose.analyze_data import analyze_data
from src.pyskindose.dev_data import DEVELOPMENT_PARAMETERS
from src.pyskindose.settings import PyskindoseSettings
from src.pyskindose import constants as const
import pandas as pd 
import numpy as np
settings = DEVELOPMENT_PARAMETERS
settings = PyskindoseSettings(settings=settings)

file_name = 'PTC.json'
data_parsed = pd.read_json(file_name)


# tmp manual parsing
data_parsed['model'] = ["AXIOMArtis"] * len(data_parsed)

data_parsed = data_parsed.rename(columns={'IrradiationEventTypeId': 'IrradiationEventType',
                                          'AcquisitionPlaneId': 'AcquisitionPlane',
                                          'CollimatedFieldArea': 'CollimatedFieldArea_m2',
                                          'DistanceSourceToDetector': 'DistanceSourcetoDetector_mm',
                                          'DistanceSourceToIsocenter': 'DistanceSourcetoIsocenter_mm',
                                          'DoseRP': 'DoseRP_Gy',
                                          'kVp': 'KVP_kV',
                                          'PositionerPrimaryAngle': 'PositionerPrimaryAngle_deg',
                                          'PositionerSecondaryAngle': 'PositionerSecondaryAngle_deg',
                                          'TableLateralPosition': 'TableLateralPosition_mm',
                                          'TableLongitudinalPosition': 'TableLongitudinalPosition_mm',
                                          'TableHeightPosition': 'TableHeightPosition_mm',
                                          'XrayFilterThicknessMaximum': 'XRayFilterThicknessMaximum_mm',
                                          'XrayFilterType': 'XRayFilterType'})



data_norm = rdsr_normalizer(data_parsed=data_parsed)

data_norm['acquisition_plane'] = ['Single Plane'] * len(data_parsed)


_ = analyze_data(normalized_data=data_norm,
                 settings=settings,
                 plot_dose_map=settings.mode == const.MODE_CALCULATE_DOSE)

