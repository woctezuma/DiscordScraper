from pathlib import Path

from internal.constants import AVATAR_URL_LIST_FNAME, OUTPUT_FOLDER_NAME

from src.member_utils import load_member_dictionaries
from src.utils import get_unique_dict_values


def load_avatar_urls() -> list[None | str]:
    d = load_member_dictionaries()
    return get_unique_dict_values(d, "avatar")


def export_avatar_urls_to_txt(output_fname: str = "") -> None:
    if not output_fname:
        output_fname = f"{OUTPUT_FOLDER_NAME}/{AVATAR_URL_LIST_FNAME}"

    urls = load_avatar_urls()
    filtered_urls = sorted([url for url in urls if url])

    with Path(output_fname).open("w", encoding="utf-8") as f:
        f.write("\n".join(filtered_urls))


if __name__ == "__main__":
    export_avatar_urls_to_txt()
