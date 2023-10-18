import pytest
from ecoindex.compute import (
    get_ecoindex,
    get_grade,
    get_greenhouse_gases_emmission,
    get_quantile,
    get_score,
    get_water_consumption,
)
from ecoindex.data import quantiles_dom, quantiles_req, quantiles_size
from ecoindex.models import Ecoindex


@pytest.mark.asyncio
class TestAsyncGroup:
    async def test_get_quantiles(self):
        assert await get_quantile(quantiles_size, 2500) == 14.086372025739513
        assert await get_quantile(quantiles_dom, 150) == 2.892857142857143
        assert await get_quantile(quantiles_req, 23) == 2.8
        assert await get_quantile(quantiles_size, 310182.902) == 20

    async def test_get_score(self):
        assert await get_score(dom=100, requests=100, size=100) == 72
        assert await get_score(dom=100, requests=100, size=1000) == 67
        assert await get_score(dom=100, requests=100, size=10000) == 58
        assert await get_score(dom=200, requests=200, size=10000) == 46
        assert await get_score(dom=2355, requests=267, size=2493) == 10
        assert await get_score(dom=240, requests=20, size=331) == 83

    async def test_get_ecoindex(self):
        assert await get_ecoindex(dom=100, requests=100, size=100) == Ecoindex(
            score=72,
            grade="B",
            ges=1.56,
            water=2.34,
        )

    async def test_get_grade(self):
        assert await get_grade(2) == "G"
        assert await get_grade(25) == "F"
        assert await get_grade(10) == "G"
        assert await get_grade(50.2) == "D"
        assert await get_grade(100) == "A"

    async def test_get_greenhouse_gases_emission(self):
        assert await get_greenhouse_gases_emmission(2) == 2.96
        assert await get_greenhouse_gases_emmission(10) == 2.8
        assert await get_greenhouse_gases_emmission(50) == 2
        assert await get_greenhouse_gases_emmission(70) == 1.6

    async def test_get_water_consumption(self):
        assert await get_water_consumption(2) == 4.44
        assert await get_water_consumption(10) == 4.2
        assert await get_water_consumption(50) == 3
        assert await get_water_consumption(70) == 2.4

    async def test_get_ecoindex_out_of_range(self):
        assert await get_ecoindex(dom=2240, requests=100, size=310182.902) == Ecoindex(
            score=16,
            grade="F",
            ges=2.68,
            water=4.02,
        )
