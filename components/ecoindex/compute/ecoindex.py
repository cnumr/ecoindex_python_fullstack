from ecoindex.data import (  # noqa: F401
    A,
    B,
    C,
    D,
    E,
    F,
    G,
    quantiles_dom,
    quantiles_req,
    quantiles_size,
)
from ecoindex.models import Ecoindex
from ecoindex.models.enums import Grade
from typing_extensions import deprecated


async def get_quantile(quantiles: list[int | float], value: int | float) -> float:
    for i in range(1, len(quantiles)):
        if value < quantiles[i]:
            return (
                i - 1 + (value - quantiles[i - 1]) / (quantiles[i] - quantiles[i - 1])
            )

    return len(quantiles) - 1


async def get_score(dom: int, size: float, requests: int) -> float:
    q_dom = await get_quantile(quantiles_dom, dom)  # type: ignore
    q_size = await get_quantile(quantiles_size, size)
    q_req = await get_quantile(quantiles_req, requests)  # type: ignore

    return round(100 - 5 * (3 * q_dom + 2 * q_req + q_size) / 6)


@deprecated("Use compute_ecoindex instead")
async def get_ecoindex(dom: int, size: float, requests: int) -> Ecoindex:
    score = await get_score(dom=dom, size=size, requests=requests)

    return Ecoindex(
        score=score,
        grade=Grade(await get_grade(score)),
        ges=await get_greenhouse_gases_emmission(score),
        water=await get_water_consumption(score),
    )


async def compute_ecoindex(nodes: int, size: float, requests: int) -> Ecoindex:
    return await get_ecoindex(
        dom=nodes,
        size=size,
        requests=requests,
    )


async def get_grade(ecoindex: float) -> str:
    for grade in "ABCDEF":
        if ecoindex > globals()[grade]:
            return grade

    return "G"


async def get_greenhouse_gases_emmission(ecoindex: float) -> float:
    return round(100 * (2 + 2 * (50 - ecoindex) / 100)) / 100


async def get_water_consumption(ecoindex: float) -> float:
    return round(100 * (3 + 3 * (50 - ecoindex) / 100)) / 100
