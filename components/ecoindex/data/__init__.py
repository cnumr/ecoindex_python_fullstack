import os

from ecoindex.data.colors import A as A_color
from ecoindex.data.colors import B as B_color
from ecoindex.data.colors import C as C_color
from ecoindex.data.colors import D as D_color
from ecoindex.data.colors import E as E_color
from ecoindex.data.colors import F as F_color
from ecoindex.data.colors import G as G_color
from ecoindex.data.grades import A, B, C, D, E, F, G
from ecoindex.data.medians import (
    median_dom,
    median_req,
    median_size,
)
from ecoindex.data.quantiles import (
    quantiles_dom,
    quantiles_req,
    quantiles_size,
)
from ecoindex.data.targets import (
    target_dom,
    target_req,
    target_size,
)
from ecoindex.utils.sync_version import read_version_from_file

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

current_directory = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(current_directory, "..", "compute", "VERSION")

ecoindex_compute_version = read_version_from_file(filename)
