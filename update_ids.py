import json
from pathlib import Path

from internal.constants import OUTPUT_FOLDER_NAME
from internal.utils import DATA_FOLDER_NAME

FNAME_MEMBERS = f"{OUTPUT_FOLDER_NAME}/SteamDB/members.json"
FNAME_PROFILES = f"{OUTPUT_FOLDER_NAME}/profiles.json"
FNAME_IDS_SKIPPED = f"{DATA_FOLDER_NAME}ids_skipped.txt"
FNAME_IDS = f"{DATA_FOLDER_NAME}ids.txt"


def to_int_list(iterable: list[str] | dict) -> list[int]:
    return [int(i.strip()) for i in iterable]


def to_str(iterable: list[int]) -> str:
    return "\n".join([str(i) for i in iterable])


def main() -> None:
    with Path(FNAME_MEMBERS).open(encoding="utf8") as f:
        d = to_int_list(json.load(f))

    with Path(FNAME_PROFILES).open(encoding="utf8") as f:
        dp = to_int_list(json.load(f))

    with Path(FNAME_IDS_SKIPPED).open() as f:
        ls = to_int_list(f.readlines())

    s = sorted(set(d).difference(dp).difference(ls))

    with Path(FNAME_IDS).open("w") as f:
        f.write(to_str(s))


if __name__ == "__main__":
    main()
