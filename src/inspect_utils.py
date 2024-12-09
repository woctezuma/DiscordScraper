from src.check_altered_text_utils import check_altered_word
from src.check_raw_text_utils import check_word
from src.load_aggregate_from_disk import load_monitored_content

NAME_FIELDS = ["name", "nick", "display_name", "global_name", "legacy_username"]
BIO_FIELDS = ["bio", "guild_bio", "display_bio"]
PRONOUNS_FIELDS = ["pronouns", "guild_pronouns"]
PRONOUN_SEPARATOR = "/"


def has_problematic_name(word: str, member_data: dict) -> bool:
    return check_word(word, member_data, NAME_FIELDS)


def has_problematic_bio(word: str, member_data: dict) -> bool:
    return check_word(word, member_data, BIO_FIELDS)


def has_problematic_pronouns(word: str, member_data: dict) -> bool:
    # Remove the separator from both the word and the text, so that **insertions**
    # do not disrupt the matching, e.g. "hi/tler", "hit/ler" or "hitl/er".
    return check_word(
        word,
        member_data,
        PRONOUNS_FIELDS,
        removed_characters=PRONOUN_SEPARATOR,
    ) or check_altered_word(
        word,
        member_data,
        PRONOUNS_FIELDS,
        separator=PRONOUN_SEPARATOR,
    )


def find_trigger_warning(
    member_profile: dict,
) -> str:
    member_id = member_profile["id"]
    for trigger_word in load_monitored_content():
        if has_problematic_name(trigger_word, member_profile):
            return f"[{member_id}] {trigger_word} in name"
        if has_problematic_bio(trigger_word, member_profile):
            return f"[{member_id}] {trigger_word} in bio"
        if has_problematic_pronouns(trigger_word, member_profile):
            return f"[{member_id}] {trigger_word} in pronouns"
    return ""
