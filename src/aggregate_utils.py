import json
from pathlib import Path

from internal.constants import MEMBER_FOLDER_NAME, OUTPUT_FOLDER_NAME


def aggregate_profiles(output_fname: str = "") -> dict:
    d = {}
    for fname in Path(MEMBER_FOLDER_NAME).glob("*/*.json"):
        with Path(fname).open() as f:
            data = json.load(f)
            d[data["id"]] = data

    if output_fname:
        with Path(f"{OUTPUT_FOLDER_NAME}/{output_fname}").open(
            "w",
            encoding="utf8",
        ) as f:
            json.dump(d, f, indent=2)

    return d
