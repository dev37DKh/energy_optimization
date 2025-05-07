# battery_optimization/__init__.py
# -*- coding: utf-8 -*-
"""
battery_optimization subpackage of the energy optimization tool.

Provides:
  - BatteryModel: a class for modeling battery behavior
  - BatteryOptimizer: a class for running optimization routines on batteries
"""

import logging

# package-level logger
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# import key classes for easy access
from .battery_model_cont import BatteryModel_cont
from .battery_model_discr import BatteryModel_discr
from .battery_grid_optimization import BatteryOptimizer

# define what’s available at package level
__all__ = [
    "BatteryModelCont",
    "BatteryModelDiscr",
    "BatteryOptimizer",
]
