from src.banner_utils import export_banner_urls_to_txt


def main() -> None:
    export_banner_urls_to_txt(output_fname_for_aggregated_profiles="profiles.json")


if __name__ == "__main__":
    main()
