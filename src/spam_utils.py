import json
from pathlib import Path

from internal.utils import MEMBER_LIST_FNAME, OUTPUT_FOLDER_NAME


def display_spammers() -> dict:
    d = {}
    for fname in Path(OUTPUT_FOLDER_NAME).glob(f"*/{MEMBER_LIST_FNAME}"):
        with Path(fname).open() as f:
            d.update(json.load(f))

    # Check if there is any spammer
    for k, v in d.items():
        if v["spammer"]:
            print(f"{k} -> {v}")

    return d
