from src.member_utils import load_member_dictionaries

NUM_MEMBER_THRESHOLD = 150
NUM_CHARACTERS_DISPLAYED = 4
NUM_DIGITS_DISPLAYED = 4
NUM_MEMBERS_DISPLAYED = 3


def list_tags(member_dictionaries: dict) -> dict:
    tags = {}
    for member_id, member_data in member_dictionaries.items():
        tag_guild_id = member_data["tag_guild_id"]
        if tag_guild_id:
            if tag_guild_id not in tags:
                tags[tag_guild_id] = {
                    "members": [],
                    "tag_name": member_data["tag_name"],
                }

            tags[tag_guild_id]["members"].append(member_id)

    return tags


def format_tag_info(
    tag_name: str,
    guild_id: str,
    num_members: int,
    examples: str,
) -> str:
    return f"{tag_name:<{NUM_CHARACTERS_DISPLAYED}}\tguild: {guild_id}\t#members: {num_members:<{NUM_DIGITS_DISPLAYED}} e.g. members: {examples}"


def display_tags() -> None:
    d = load_member_dictionaries()

    tags = list_tags(d)

    for guild_id, tag_data in sorted(
        tags.items(),
        key=lambda x: len(x[1]["members"]),
        reverse=True,
    ):
        member_ids = sorted([int(i) for i in tag_data["members"]])
        num_members = len(member_ids)

        if num_members < NUM_MEMBER_THRESHOLD:
            break

        if tag_name := tag_data["tag_name"]:
            examples = "\t".join(str(i) for i in member_ids[:NUM_MEMBERS_DISPLAYED])
            print(format_tag_info(tag_name, guild_id, num_members, examples))
