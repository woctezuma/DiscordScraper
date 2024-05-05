import json
from pathlib import Path

from internal.constants import (
    AGGREGATED_PROFILES_FNAME,
    MEMBER_FOLDER_NAME,
    OUTPUT_FOLDER_NAME,
)


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
    for fname in Path(MEMBER_FOLDER_NAME).glob("*/*.json"):
        with Path(fname).open() as f:
            data = json.load(f)
            d[data["id"]] = data

    if output_fname:
        save_aggregate_to_disk(d, output_fname)

    return d
