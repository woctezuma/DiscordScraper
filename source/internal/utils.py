import json
import os
import shutil
import string
from functools import cache

from discord import Guild, Member  # type: ignore
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
[bold yellow]🚀 Star the repo: https://github.com/Sxvxgee/Discord-Scraper
[bold green]✅ Follow me: https://github.com/Sxvxgee/
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
def show_header():
    print(f"{header}{info}")


@cache
def check_config_file():
    """
    Creates a config file if it doesn"t exist.
    If it does, validates the config to required config.
    """
    if not os.path.isfile(
        "config.json",
    ):  # Create a config file with default values if it doesn't exist
        json.dump(default_data, open("config.json", "w"), indent=2)
        return

    # Validating the JSON file, adding keys if they don"t exist in it
    with open("config.json") as file:
        file_data = json.loads(file.read())

    required_data = {}

    # TODO: The complexity of this part is more than requierd; could be shortened possibly.
    for key, value in file_data.items():
        if key in default_data:
            required_data[key] = value

    for default_key, default_value in default_data.items():
        if default_key not in required_data:
            required_data[default_key] = default_value

    json.dump(required_data, open("config.json", "w"), indent=2)


class Logger:
    def __init__(self) -> None:
        ...

    def scraper(self, text: str) -> None:
        print(f"[bold white][Scraper] {text} [/]")

    def success(self, text: str) -> None:
        print(f"[bold green][Success] {text} [/]")

    def error(self, text: str) -> None:
        print(f"[bold red][Error] {text} [/]")

    def custom(
        self,
        text: str,
        header: str | None = None,
        color: str = "white",
    ) -> None:
        print(f"[bold {color}][{header}] {text} [/]")


@cache
def get_account_settings():
    return json.load(open("config.json"))


@cache
def create_guild_directory(guild: Guild):
    if get_account_settings()["purge_old_data"]:
        shutil.rmtree(f"data/{guild.id}", ignore_errors=True)
    os.makedirs(f"DataScraped/{guild.name}", exist_ok=True)


@cache
def clean_string(string_to_clean: str) -> str:
    return "".join([char for char in string_to_clean if char in string.printable])


def get_bio_fname(member):
    return f"DataScraped/{member.guild.name}/{member.id}.txt"


@cache
async def create_member_file(member: Member):
    if member.bot:
        return

    try:
        username = clean_string(member.display_name)
        profile = await member.guild.fetch_member_profile(member.id)
        bio = clean_string(profile.bio) if profile.bio else "User doesn't have a bio."
        with open(get_bio_fname(member), "w+") as file:
            file.write(
                f"Username: {username}\nAccount ID: {member.id}\nBio: {bio}\nDiscriminator: #{member.discriminator}\n\n\nScraped by Discord-Scraper: https://github.com/Sxvxgee/Discord-Scraper/ \nFollow Sxvxge: https://github.com/Sxvxgee/",
            )
    except Exception as e:
        print(
            f'[bold red][Error] Failed to write the data of the account "{member}": {e} [/]',
        )


def get_pfp_fname(member, pfp_format=".png"):
    return f"DataScraped/{member.guild.name}/{member.id}.{pfp_format}"


@cache
async def download_pfp(member: Member):
    if member.bot or member.avatar is None:
        return
    try:
        data = get_account_settings()
        await member.avatar.save(get_pfp_fname(member, data["pfp_format"]))
    except Exception as e:
        print(
            f'[bold red][Error] Failed to save the profile picture of the account "{member}": {e} [/]',
        )
