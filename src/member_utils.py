import json
from pathlib import Path

from internal.constants import MEMBER_LIST_FNAME, OUTPUT_FOLDER_NAME
from internal.utils import MEMBER_ID_FNAME


def load_member_dictionaries() -> dict:
    d = {}
    for fname in Path(OUTPUT_FOLDER_NAME).glob(f"*/{MEMBER_LIST_FNAME}"):
        with Path(fname).open() as f:
            d.update(json.load(f))
    return d


def parse_member_ids() -> list[str]:
    d = load_member_dictionaries()
    return list(d.keys())


def export_member_ids_to_txt(output_fname: str = "") -> None:
    if not output_fname:
        output_fname = MEMBER_ID_FNAME

    member_ids = sorted(parse_member_ids(), key=int)

    with Path(output_fname).open("w") as f:
        f.write("\n".join(member_ids))


if __name__ == "__main__":
    export_member_ids_to_txt()
