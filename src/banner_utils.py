from pathlib import Path

from internal.constants import (
    AGGREGATED_PROFILES_FNAME,
    BANNER_URL_LIST_FNAME,
    OUTPUT_FOLDER_NAME,
)

from src.aggregate_utils import aggregate_profiles, load_aggregate_from_disk
from src.utils import get_unique_dict_values


def load_banner_urls(
    output_fname_for_aggregated_profiles: str = "",
) -> list[None | str]:
    d = load_aggregate_from_disk()
    if not d:
        d = aggregate_profiles(output_fname_for_aggregated_profiles)
    return get_unique_dict_values(d, "banner")


def export_banner_urls_to_txt(
    output_fname: str = "",
    output_fname_for_aggregated_profiles: str = "",
) -> None:
    if not output_fname:
        output_fname = f"{OUTPUT_FOLDER_NAME}/{BANNER_URL_LIST_FNAME}"

    urls = load_banner_urls(output_fname_for_aggregated_profiles)
    filtered_urls = sorted([url for url in urls if url])

    with Path(output_fname).open("w", encoding="utf-8") as f:
        f.write("\n".join(filtered_urls))


if __name__ == "__main__":
    export_banner_urls_to_txt(
        output_fname_for_aggregated_profiles=AGGREGATED_PROFILES_FNAME,
    )
