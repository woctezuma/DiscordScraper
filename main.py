from internal.selfbot import client
from internal.utils import Logger, check_config_file, get_account_settings, show_header


def main() -> None:
    show_header()
    check_config_file()
    Logger()
    config = get_account_settings()

    client.run(config["token"])


if __name__ == "__main__":
    main()
