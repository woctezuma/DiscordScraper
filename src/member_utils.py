import json
from pathlib import Path

from internal.constants import MEMBER_LIST_FNAME, OUTPUT_FOLDER_NAME


def load_member_dictionaries() -> dict:
    d = {}
    for fname in Path(OUTPUT_FOLDER_NAME).glob(f"*/{MEMBER_LIST_FNAME}"):
        with Path(fname).open() as f:
            d.update(json.load(f))
    return d
