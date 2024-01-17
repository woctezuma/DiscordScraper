from pathlib import Path

from internal.constants import DUMMY_BIO, PATTERN_END, PATTERN_START


def extract_bio(text: str) -> str:
    bio_start = text.find(PATTERN_START) + len(PATTERN_START)
    bio_end = text.find(PATTERN_END)

    bio = text[bio_start:bio_end].strip()

    if bio == DUMMY_BIO:
        bio = None

    return bio


def read_bios_from_text_files(folder_name: str) -> dict:
    d = {}

    for fname in Path(folder_name).glob("*.txt"):
        member_id = Path(fname).stem

        text = Path(fname).read_text(encoding="utf8")
        bio = extract_bio(text)

        if bio:
            d[member_id] = bio

    return d
