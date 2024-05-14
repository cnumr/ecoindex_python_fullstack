import asyncio
from pprint import pprint

from ecoindex.compute import compute_ecoindex

ecoindex = asyncio.run(compute_ecoindex(nodes=100, size=100, requests=100))
pprint(ecoindex)
