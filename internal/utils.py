import json
import shutil
import string
from functools import cache
from pathlib import Path

from discord import Guild, Member
from rich import print

header = """[bold white]
██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗     ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗
██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║    ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║    ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝    ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝     ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
[/]"""
info = """[bold black]
🏴 Made by Sxvxge.
[/]"""

default_data = {
    "token": "",
    "guild_id": 0,
    "pfp_format": "png",
    "purge_old_data": True,
    "download_bio": True,
    "download_pfp": True,
    "channel_id": 0,
}


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
    def __init__(self: "Logger") -> None:
        ...

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


@cache
def create_guild_directory(guild: Guild) -> None:
    if get_account_settings()["purge_old_data"]:
        shutil.rmtree(f"data/{guild.id}", ignore_errors=True)
    Path(f"DataScraped/{guild.name}").mkdir(parents=True, exist_ok=True)


@cache
def clean_string(string_to_clean: str) -> str:
    return "".join([char for char in string_to_clean if char in string.printable])


def get_bio_fname(member: Member) -> str:
    return f"DataScraped/{member.guild.name}/{member.id}.txt"


@cache
async def create_member_file(member: Member) -> None:
    if member.bot:
        return

    try:
        username = clean_string(member.display_name)
        profile = await member.guild.fetch_member_profile(
            member.id,
            with_mutual_friends=False,
        )
        bio = clean_string(profile.bio) if profile.bio else "User doesn't have a bio."
        Path(get_bio_fname(member)).write_text(
            f"Username: {username}\nAccount ID: {member.id}\nBio: {bio}\nDiscriminator: #{member.discriminator}\n",
        )
    except Exception as e:
        print(
            f'[bold red][Error] Failed to write the data of the account "{member}": {e} [/]',
        )


def get_pfp_fname(member: Member, pfp_format: str = ".png") -> str:
    return f"DataScraped/{member.guild.name}/{member.id}.{pfp_format}"


@cache
async def download_pfp(member: Member, pfp_format: str = ".png") -> None:
    if member.bot or member.avatar is None:
        return
    try:
        await member.avatar.save(get_pfp_fname(member, pfp_format))
    except Exception as e:
        print(
            f'[bold red][Error] Failed to save the profile picture of the account "{member}": {e} [/]',
        )
