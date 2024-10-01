import json
from pathlib import Path

from internal.constants import (
    AGGREGATED_PROFILES_FNAME,
    OUTPUT_FOLDER_NAME,
)
from internal.utils import list_individual_profiles


def load_aggregate_from_disk(output_fname: str = AGGREGATED_PROFILES_FNAME) -> dict:
    try:
        with Path(f"{OUTPUT_FOLDER_NAME}/{output_fname}").open(
            encoding="utf8",
        ) as f:
            aggregate = json.load(f)
    except FileNotFoundError:
        aggregate = {}
    return aggregate


def save_aggregate_to_disk(
    aggregate: dict,
    output_fname: str = AGGREGATED_PROFILES_FNAME,
) -> None:
    with Path(f"{OUTPUT_FOLDER_NAME}/{output_fname}").open(
        "w",
        encoding="utf8",
    ) as f:
        json.dump(aggregate, f, indent=2)


def aggregate_profiles(output_fname: str = "") -> dict:
    d = {}
    for fname in list_individual_profiles():
        with Path(fname).open(encoding="utf-8") as f:
            data = json.load(f)
            d[data["id"]] = data

    if output_fname:
        save_aggregate_to_disk(d, output_fname)

    return d
