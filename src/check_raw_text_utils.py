def standardize_text(text: str, removed_characters: str) -> str:
    return text.lower().strip(removed_characters)


def check_word(
    word: str,
    data: dict,
    fields: list[str],
    removed_characters: str = "",
) -> bool:
    # Specified characters are removed from both the word and the text.
    standardized_word = standardize_text(word, removed_characters)
    return any(
        data[f] and standardized_word in standardize_text(data[f], removed_characters)
        for f in fields
    )
