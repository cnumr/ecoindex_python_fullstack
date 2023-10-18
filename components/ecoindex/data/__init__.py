"""
Ecoindex reference data
"""

from .colors import A as A_color
from .colors import B as B_color
from .colors import C as C_color
from .colors import D as D_color
from .colors import E as E_color
from .colors import F as F_color
from .colors import G as G_color
from .grades import A, B, C, D, E, F, G
from .medians import (
    median_dom,
    median_req,
    median_size,
)
from .quantiles import (
    quantiles_dom,
    quantiles_req,
    quantiles_size,
)
from .targets import (
    target_dom,
    target_req,
    target_size,
)

__all__ = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "A_color",
    "B_color",
    "C_color",
    "D_color",
    "E_color",
    "F_color",
    "G_color",
    "median_dom",
    "median_req",
    "median_size",
    "quantiles_dom",
    "quantiles_req",
    "quantiles_size",
    "target_dom",
    "target_req",
    "target_size",
]
