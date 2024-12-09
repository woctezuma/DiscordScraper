from internal.utils import strip_parameters


def get_dict_values(d: dict, dict_key: str) -> list:
    return [v[dict_key] for v in d.values()]


def list_possible_dict_keys(keyword: str) -> list[str]:
    return [keyword, f"display_{keyword}", f"guild_{keyword}"]


def get_unique_dict_values(d: dict, keyword: str) -> list[str | None]:
    urls = []
    for dict_key in list_possible_dict_keys(keyword):
        urls += get_dict_values(d, dict_key)
    return list({strip_parameters(url) for url in urls})
