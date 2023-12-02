import random
import time
from pathlib import Path
from urllib.error import HTTPError

from discord import Client, Guild
from rich.progress import track

from internal.utils import (
    Logger,
    create_guild_directory,
    create_member_file,
    download_pfp,
    get_account_settings,
    get_bio_fname,
    get_guild_members_fname,
    get_pfp_fname,
    save_members_dict,
)

COOLDOWN_IN_SECONDS = 1

client = Client(chunk_guilds_at_startup=False)
logger = Logger()


async def scrape(conf: dict, guild: Guild) -> list:
    logger.scraper("Starting...")
    members = await guild.fetch_members(
        [random.choice(guild.channels)]
        if conf["channel_id"] != 0
        else conf["channel_id"],
    )
    members = [member for member in members if not member.bot]
    logger.success("Fetched members successfully")
    return members


@client.event
async def on_ready() -> None:
    logger.scraper(f"Logged in as {client.user}")

    config = get_account_settings()
    guild_id = config["guild_id"]
    pfp_format = config["pfp_format"]

    guild = client.get_guild(int(guild_id))
    members = await scrape(config, guild)

    create_guild_directory(guild)

    save_members_dict(members, get_guild_members_fname(guild))

    for member in track(
        members,
        description="[bold white][Scraper] Scraping profiles...[/]",
    ):
        if config["download_bio"] and not Path(get_bio_fname(member)).exists():
            time.sleep(1)
            try:
                await create_member_file(member)
            except HTTPError:
                break
        if (
            config["download_pfp"]
            and not Path(get_pfp_fname(member, pfp_format)).exists()
        ):
            await download_pfp(member, pfp_format)

    logger.success("Finished scraping members profiles and data.\n")
