from src.check_raw_text_utils import check_word


def get_max_word_length(data: dict, fields: list[str]) -> int:
    word_lengths = [len(data[f]) for f in fields if data[f]]
    return max(word_lengths) if word_lengths else 0


def check_altered_word(
    word: str,
    data: dict,
    fields: list[str],
    separator: str = "",
) -> bool:
    # Ensure that a **replacement** of a character with the separator
    # does not disrupt the matching e.g. "hi/ler" or "hit/er".
    min_num_letters = 3
    max_num_letters = len(separator) + get_max_word_length(data, fields)
    if min_num_letters <= len(word) <= max_num_letters:
        for i in range(len(word)):
            altered_word = word[:i] + separator + word[(i + 1) :]
            if check_word(altered_word, data, fields):
                return True
    return False
