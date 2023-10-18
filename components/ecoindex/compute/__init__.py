"""
Ecoindex basic compute engine
"""

from .ecoindex import (
    get_ecoindex,
    get_grade,
    get_greenhouse_gases_emmission,
    get_quantile,
    get_score,
    get_water_consumption,
)

__all__ = [
    "get_ecoindex",
    "get_grade",
    "get_greenhouse_gases_emmission",
    "get_quantile",
    "get_score",
    "get_water_consumption",
]