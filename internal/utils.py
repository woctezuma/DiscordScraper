import json
import shutil
import string
from collections.abc import Iterator
from functools import cache
from pathlib import Path
from typing import NamedTuple

from discord import Asset, Guild, Member, MemberFlags, PublicUserFlags
from rich import print

from internal.constants import (
    DUMMY_BIO,
    MEMBER_LIST_FNAME,
    OUTPUT_FOLDER_NAME,
    PATTERN_END,
    PATTERN_START,
    default_data,
    header,
    info,
)

DUMMY_ROLE = "@everyone"
MEMBER_ID_FNAME = "ids.txt"


class DummyMember(NamedTuple):
    id: int
    guild: Guild
    bot: bool = False
    avatar: Asset | None = None


def chunks(lst: list, n: int) -> Iterator[list]:
    """Yield successive n-sized chunks from l."""
    # Reference: https://stackoverflow.com/a/312464
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


@cache
def show_header() -> None:
    print(f"{header}{info}")


@cache
def check_config_file() -> None:
    """Creates a config file if it doesn"t exist.
    If it does, validates the config to required config.
    """
    if not Path(
        "config.json",
    ).is_file():
        with Path("config.json").open("w") as f:
            json.dump(default_data, f, indent=2)
        return

    with Path("config.json").open() as f:
        file_data = json.load(f)

    required_data = {}

    for key, value in file_data.items():
        if key in default_data:
            required_data[key] = value

    for default_key, default_value in default_data.items():
        if default_key not in required_data:
            required_data[default_key] = default_value

    with Path("config.json").open("w") as f:
        json.dump(required_data, f, indent=2)


class Logger:
    def __init__(self: "Logger") -> None: ...

    def scraper(self: "Logger", text: str) -> None:
        print(f"[bold white][Scraper] {text} [/]")

    def success(self: "Logger", text: str) -> None:
        print(f"[bold green][Success] {text} [/]")

    def error(self: "Logger", text: str) -> None:
        print(f"[bold red][Error] {text} [/]")

    def custom(
        self: "Logger",
        text: str,
        header: str | None = None,
        color: str = "white",
    ) -> None:
        print(f"[bold {color}][{header}] {text} [/]")


@cache
def get_account_settings() -> dict:
    with Path("config.json").open() as f:
        return json.load(f)


def get_guild_folder_name(guild: Guild) -> str:
    return f"{OUTPUT_FOLDER_NAME}/{guild.name}"


def strip_parameters(url: str) -> str:
    return url.split("?")[0]


def list_flag_names(flags: PublicUserFlags | MemberFlags) -> list[str]:
    return [f for f in flags.VALID_FLAGS if getattr(flags, f)]


def get_members_dict(members: list[Member]) -> dict:
    d = {}

    for e in members:
        public_flags = list_flag_names(e.public_flags)
        private_flags = list_flag_names(e.flags)

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
            "public_flags": sorted(public_flags),
            "private_flags": sorted(private_flags),
        }

    return d


def get_guild_members_fname(guild: Guild) -> str:
    return f"{get_guild_folder_name(guild)}/{MEMBER_LIST_FNAME}"


def load_member_ids_from_disk(fname: str = MEMBER_ID_FNAME) -> list[int]:
    try:
        with Path(fname).open() as f:
            member_ids = [int(i) for i in f]
    except FileNotFoundError:
        member_ids = []
    return member_ids


def save_members_dict(members: list[Member], fname: str) -> None:
    with Path(fname).open("w", encoding="utf8") as f:
        json.dump(get_members_dict(members), f, indent=2, sort_keys=True)


@cache
def create_guild_directory(guild: Guild) -> None:
    if get_account_settings()["purge_old_data"]:
        shutil.rmtree(f"data/{guild.id}", ignore_errors=True)
    Path(get_guild_folder_name(guild)).mkdir(parents=True, exist_ok=True)


@cache
def clean_string(string_to_clean: str) -> str:
    return "".join([char for char in string_to_clean if char in string.printable])


def get_bio_fname(member: Member) -> str:
    return f"{OUTPUT_FOLDER_NAME}/{member.guild.name}/{member.id}.txt"


@cache
async def create_member_file(member: Member) -> None:
    if member.bot:
        return

    profile = await member.guild.fetch_member_profile(
        member.id,
        with_mutual_friends=False,
    )
    bio = clean_string(profile.bio) if profile.bio else DUMMY_BIO
    pronouns = profile.metadata.pronouns
    connections = " / ".join(sorted([c.type.name for c in profile.connections]))
    banner_url = profile.banner.url if profile.banner else None
    metadata = (
        f"\nPronouns:{pronouns}\nConnections: {connections}\nBanner: {banner_url}"
    )
    Path(get_bio_fname(member)).write_text(
        f"Account ID: {member.id}{metadata}{PATTERN_START}{bio}{PATTERN_END}\n",
    )
