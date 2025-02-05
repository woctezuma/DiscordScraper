import json
import shutil
import string
from functools import cache
from pathlib import Path
from typing import NamedTuple

from discord import Asset, Guild, Member, MemberFlags, PublicUserFlags
from rich import print as pprint

from internal.constants import (
    MEMBER_FOLDER_NAME,
    MEMBER_LIST_FNAME,
    OUTPUT_FOLDER_NAME,
    default_data,
    header,
    info,
)
from src.environment_utils import find_config_in_environment
from src.load_aggregate_from_disk import load_aggregate_from_disk

DUMMY_ROLE = "@everyone"
DATA_FOLDER_NAME = "data/"
MEMBER_ID_FNAME = f"{DATA_FOLDER_NAME}ids.txt"
SKIPPED_MEMBER_ID_FNAME = f"{DATA_FOLDER_NAME}ids_skipped.txt"


class DummyMember(NamedTuple):
    id: int
    guild: Guild
    bot: bool = False
    avatar: Asset | None = None


def filter_out_specific_ids(
    members: list[Member],
    specific_ids: set[int],
) -> list[Member]:
    skipped_member_ids = frozenset(specific_ids)
    return [e for e in members if e.id not in skipped_member_ids]


def build_known_ids(lst: list) -> frozenset[int]:
    return frozenset(int(i) for i in lst)


def load_ids_from_aggregate() -> list[int]:
    aggregate = load_aggregate_from_disk()
    return [e["id"] for e in aggregate.values()]


def list_individual_profiles() -> list:
    return list(Path(MEMBER_FOLDER_NAME).glob("*/*.json"))


def load_ids_from_individual_profiles() -> list[str]:
    return [s.stem for s in list_individual_profiles()]


def load_known_ids() -> frozenset[int]:
    return build_known_ids(
        load_ids_from_aggregate() + load_ids_from_individual_profiles(),
    )


@cache
def show_header() -> None:
    pprint(f"{header}{info}")


@cache
def check_config_file() -> None:
    """Creates a config file if it doesn"t exist.
    If it does, validates the config to required config.
    """
    if not Path(
        "config.json",
    ).is_file():
        with Path("config.json").open("w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=2)
        return

    with Path("config.json").open(encoding="utf-8") as f:
        file_data = json.load(f)

    required_data = {
        key: value for key, value in file_data.items() if key in default_data
    }

    for default_key, default_value in default_data.items():
        if default_key not in required_data:
            required_data[default_key] = default_value

    with Path("config.json").open("w", encoding="utf-8") as f:
        json.dump(required_data, f, indent=2)


class Logger:
    def __init__(self: "Logger") -> None: ...

    @staticmethod
    def scraper(text: str) -> None:
        pprint(f"[bold white][Scraper] {text} [/]")

    @staticmethod
    def success(text: str) -> None:
        pprint(f"[bold green][Success] {text} [/]")

    @staticmethod
    def error(text: str) -> None:
        pprint(f"[bold red][Error] {text} [/]")

    @staticmethod
    def custom(
        text: str,
        header: str | None = None,
        color: str = "white",
    ) -> None:
        pprint(f"[bold {color}][{header}] {text} [/]")


@cache
def get_account_settings() -> dict:
    with Path("config.json").open(encoding="utf-8") as f:
        config = json.load(f)
    config |= find_config_in_environment()
    return config


def get_guild_folder_name(guild: Guild) -> str:
    return f"{OUTPUT_FOLDER_NAME}/{guild.name}"


def strip_parameters(url: str | None) -> str | None:
    return url.split("?")[0] if url else url


def list_flag_names(flags: PublicUserFlags | MemberFlags) -> list[str]:
    return sorted([f for f in flags.VALID_FLAGS if getattr(flags, f)])


def get_members_dict(members: list[Member]) -> dict:
    d = {}

    for e in members:
        d[e.id] = {
            "id": e.id,
            "name": e.name,
            "nick": e.nick,
            "created_at": e.created_at.timestamp(),
            "joined_at": e.joined_at.timestamp(),
            "premium_since": e.premium_since.timestamp() if e.premium_since else None,
            "global_name": e.global_name,
            "display_name": e.display_name,
            "avatar": strip_parameters(e.avatar.url) if e.avatar else None,
            "avatar_decoration": strip_parameters(e.avatar_decoration.url)
            if e.avatar_decoration
            else None,
            "display_avatar": strip_parameters(e.display_avatar.url)
            if e.display_avatar
            else None,
            "guild_avatar": strip_parameters(e.guild_avatar.url)
            if e.guild_avatar
            else None,
            "top_role": e.top_role.name if e.top_role.name != DUMMY_ROLE else None,
            "roles": [f.name for f in e.roles if f.name != DUMMY_ROLE],
            "spammer": e.public_flags.spammer,
            "public_flags": list_flag_names(e.public_flags),
            "private_flags": list_flag_names(e.flags),
        }

    return d


def get_guild_members_fname(guild: Guild) -> str:
    return f"{get_guild_folder_name(guild)}/{MEMBER_LIST_FNAME}"


def load_member_ids_from_disk(fname: str = MEMBER_ID_FNAME) -> list[int]:
    try:
        with Path(fname).open(encoding="utf-8") as f:
            member_ids = [int(i) for i in f]
    except FileNotFoundError:
        member_ids = []
    return member_ids


def load_skipped_member_ids_from_disk() -> list[int]:
    return load_member_ids_from_disk(SKIPPED_MEMBER_ID_FNAME)


def save_members_dict(members: list[Member], fname: str) -> None:
    with Path(fname).open("w", encoding="utf8") as f:
        json.dump(get_members_dict(members), f, indent=2, sort_keys=True)


@cache
def create_guild_directory(guild: Guild) -> None:
    if get_account_settings()["purge_old_data"]:
        shutil.rmtree(f"data/{guild.id}", ignore_errors=True)
    Path(get_guild_folder_name(guild)).mkdir(parents=True, exist_ok=True)


@cache
def clean_string(string_to_clean: str) -> str | None:
    return (
        "".join([char for char in string_to_clean if char in string.printable])
        if string_to_clean
        else None
    )


def get_bio_fname(member: Member) -> str:
    num_digits = 2
    prefix = str(int(member.id))[:num_digits]
    folder_name = f"{MEMBER_FOLDER_NAME}/{prefix}"
    Path(folder_name).mkdir(exist_ok=True, parents=True)
    return f"{folder_name}/{member.id}.json"


@cache
async def create_member_file(member: Member, *, save_to_disk: bool = True) -> dict:
    if member.bot:
        return {}

    profile = await member.guild.fetch_member_profile(
        member.id,
        with_mutual_friends=False,
    )

    profile_summary = {
        "id": member.id,
        "name": clean_string(profile.name),
        "nick": clean_string(profile.nick),
        "display_name": clean_string(profile.display_name),
        "global_name": clean_string(profile.global_name),
        "pronouns": profile.metadata.pronouns,
        "guild_pronouns": profile.guild_metadata.pronouns,
        "bio": clean_string(profile.bio),
        "guild_bio": clean_string(profile.guild_bio),
        "display_bio": clean_string(profile.display_bio),
        "banner": profile.banner.url if profile.banner else None,
        "guild_banner": profile.guild_banner.url if profile.guild_banner else None,
        "display_banner": profile.display_banner.url
        if profile.display_banner
        else None,
        "badges": sorted([c.id for c in profile.badges]),
        "connections": {
            c.type.name: {"id": c.id, "name": c.name, "url": c.url}
            for c in profile.connections
        },
        "legacy_username": profile.legacy_username,
    }

    if save_to_disk:
        with Path(get_bio_fname(member)).open("w", encoding="utf8") as f:
            json.dump(profile_summary, f, indent=2, sort_keys=True)

    return profile_summary
