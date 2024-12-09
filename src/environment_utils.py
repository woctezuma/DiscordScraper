import os

TARGET_PREFIX = "ACTION_"


def get_environment() -> dict:
    return os.environ.copy()


def filter_dict_by_key(d: dict, prefix: str) -> dict:
    return {
        k.removeprefix(prefix).lower(): v for k, v in d.items() if k.startswith(prefix)
    }


def find_config_in_environment() -> dict:
    return filter_dict_by_key(get_environment(), TARGET_PREFIX)
