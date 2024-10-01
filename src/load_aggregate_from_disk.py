import json
from pathlib import Path

from internal.constants import AGGREGATED_PROFILES_FNAME, OUTPUT_FOLDER_NAME


def load_aggregate_from_disk(output_fname: str = AGGREGATED_PROFILES_FNAME) -> dict:
    try:
        with Path(f"{OUTPUT_FOLDER_NAME}/{output_fname}").open(
            encoding="utf8",
        ) as f:
            aggregate = json.load(f)
    except FileNotFoundError:
        aggregate = {}
    return aggregate
