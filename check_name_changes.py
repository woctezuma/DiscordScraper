import json
from pathlib import Path

from internal.constants import OUTPUT_FOLDER_NAME
from internal.utils import clean_string
from src.check_raw_text_utils import standardize_text
from src.inspect_utils import NAME_FIELDS
from update_ids import FNAME_MEMBERS, FNAME_PROFILES

ARROW_STR = " -> "
OUTPUT_FNAME = f"{OUTPUT_FOLDER_NAME}/name_changes.json"


def load_json(file_path: str) -> dict:
    with Path(file_path).open(encoding="utf8") as file:
        return json.load(file)


def save_json(file_path: str, data: dict) -> None:
    with Path(file_path).open("w", encoding="utf8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def sanitize_name(name: str) -> str:
    return standardize_text(clean_string(name) if name else "", "")


def create_comparison_string(old: str, new: str) -> str:
    return f"{old}{ARROW_STR}{new}"


def compare_names(
    members: dict,
    profiles: dict,
    ids: set,
    *,
    verbose: bool = True,
) -> dict:
    data = {}
    for k in ids:
        for field in NAME_FIELDS:
            if field not in members:
                continue
            p = sanitize_name(profiles[k][field])
            m = sanitize_name(members[k][field])
            if m != p:
                if k not in data:
                    data[k] = {}
                data[k][field] = create_comparison_string(p, m)
    if verbose:
        print(f"Found {len(data)} members with name changes.")
    return data


def main() -> None:
    profiles = load_json(FNAME_PROFILES)
    members = load_json(FNAME_MEMBERS)
    ids = set(profiles).intersection(members)
    data = compare_names(members, profiles, ids)
    save_json(OUTPUT_FNAME, data)


if __name__ == "__main__":
    main()
