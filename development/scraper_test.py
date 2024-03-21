import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
from ecoindex.scraper import EcoindexScraper
from haralyzer import HarParser
from slugify import slugify


async def get_page_analysis(url: str):
    scraper = EcoindexScraper(url=url)
    return (
        await scraper.get_page_analysis(),
        await scraper.get_all_requests(),
        await scraper.get_requests_by_category(),
        scraper.har_temp_file_path,
    )


def run_page_analysis(url: str, index: int):
    analysis, requests, aggregation, har_file_path = asyncio.run(get_page_analysis(url))

    return index, analysis, requests, aggregation, har_file_path


with ThreadPoolExecutor(max_workers=8) as executor:
    future_to_analysis = {}

    urls = ["https://www.graphic-sud.com/", "https://federiconavarrete.com/"]
    i = 0

    for url in urls:
        print(f"Starting ecoindex {i} analysis")
        future_to_analysis[
            executor.submit(
                run_page_analysis,
                url,
                i,
            )
        ] = url
        i += 1

    for future in as_completed(future_to_analysis):
        try:
            index, analysis, requests, aggregation, har_file_path = future.result()

            har_parser = HarParser.from_file(har_file_path)
            for page in har_parser.pages:
                haralyzer_data = [
                    {
                        "type": "audio",
                        "count": len(page.audio_files),
                        "size": page.audio_size_trans,
                    },
                    {
                        "type": "css",
                        "count": len(page.css_files),
                        "size": page.css_size_trans,
                    },
                    {
                        "type": "javascript",
                        "count": len(page.js_files),
                        "size": page.js_size_trans,
                    },
                    {"type": "page", "count": 1, "size": page.page_size_trans},
                    {
                        "type": "image",
                        "count": len(page.image_files),
                        "size": page.image_size_trans,
                    },
                    {
                        "type": "video",
                        "count": len(page.video_files),
                        "size": page.video_size_trans,
                    },
                    {
                        "type": "other",
                        "count": len(page.text_files),
                        "size": page.text_size_trans,
                    },
                    {"type": "html", "count": len(page.html_files), "size": None},
                    {
                        "type": "total",
                        "count": len(page.entries),
                        "size": page.page_size_trans,
                    },
                ]

                df_haralyzer = pd.DataFrame(
                    haralyzer_data, columns=["type", "count", "size"]
                )

            flatten_aggregation = [
                {
                    "type": type,
                    "count": item["total_count"],
                    "size": item["total_size"],
                }
                for type, item in aggregation.model_dump().items()
            ]
            flatten_aggregation.append(
                {
                    "type": "total",
                    "count": analysis.requests,
                    "size": analysis.size * 1000,
                }
            )

            df = pd.DataFrame(flatten_aggregation, columns=["type", "count", "size"])
            df.to_csv(f"ecoindex_{index}.csv", index=False)

            joinned_df = pd.merge(
                df,
                df_haralyzer,
                on="type",
                how="left",
                suffixes=("_ecoindex", "_haralyzer"),
            )

            joinned_df["size_ecoindex"] = joinned_df["size_ecoindex"] / 1000
            joinned_df["size_haralyzer"] = joinned_df["size_haralyzer"] / 1000

            print()
            print(page.url)
            print(joinned_df)
            print()

            joinned_df.to_csv(f"joinned_ecoindex_{slugify(page.url)}.csv", index=False)

        except Exception as e:
            print(e)
