from src.member_utils import load_member_dictionaries


def display_spammers() -> dict:
    d = load_member_dictionaries()

    # Check if there is any spammer
    for k, v in d.items():
        if v["spammer"]:
            print(f"{k} -> {v}")

    return d
