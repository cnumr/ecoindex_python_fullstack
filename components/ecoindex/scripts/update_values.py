from asyncio import run
from json import dumps
from os import getcwd

from aiofile import async_open
from requests import get


async def update_values_async() -> None:
    response = get(
        "https://cdn.jsdelivr.net/gh/cnumr/ecoindex_reference@1/ecoindex_reference.json",
    )

    data = response.json()
    data_folder = f"{getcwd()}/components/ecoindex/data/"

    async with async_open(f"{data_folder}quantiles.py", "w") as quantile_file:
        quantiles = f"quantiles_dom = {dumps(data['quantiles']['dom_size'])}\n"
        quantiles += f"quantiles_req = {dumps(data['quantiles']['nb_request'])}\n"
        quantiles += f"quantiles_size = {dumps(data['quantiles']['response_size'])}\n"

        await quantile_file.write(quantiles)

    async with async_open(f"{data_folder}targets.py", "w") as target_file:
        targets = f"target_dom = {dumps(data['targets']['dom_size'])}\n"
        targets += f"target_req = {dumps(data['targets']['nb_request'])}\n"
        targets += f"target_size = {dumps(data['targets']['response_size'])}\n"

        await target_file.write(targets)

    async with async_open(f"{data_folder}medians.py", "w") as median_file:
        medians = f"median_dom = {dumps(data['medians']['dom_size'])}\n"
        medians += f"median_req = {dumps(data['medians']['nb_request'])}\n"
        medians += f"median_size = {dumps(data['medians']['response_size'])}\n"

        await median_file.write(medians)

    async with async_open(f"{data_folder}grades.py", "w") as grades_file:
        grades = ""

        for grade in data["grades"]:
            grades += f"{grade['grade']} = {grade['value']}\n"

        await grades_file.write(grades)

    print("Values updated")


def update_values() -> None:
    run(update_values_async())
