from pathlib import Path

from internal.constants import AVATAR_URL_LIST_FNAME, OUTPUT_FOLDER_NAME
from src.member_utils import load_member_dictionaries


def load_avatar_urls() -> list[None | str]:
    d = load_member_dictionaries()
    return [v["avatar_url"] for v in d.values()]


def export_avatar_urls_to_txt(output_fname: str = "") -> None:
    if len(output_fname) == 0:
        output_fname = f"{OUTPUT_FOLDER_NAME}/{AVATAR_URL_LIST_FNAME}"

    urls = load_avatar_urls()
    filtered_urls = [url for url in urls if url]

    with Path(output_fname).open("w") as f:
        f.write("\n".join(filtered_urls))


if __name__ == "__main__":
    export_avatar_urls_to_txt()
