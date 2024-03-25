import random
from pathlib import Path

from discord import Client, Guild
from discord.errors import HTTPException, InvalidData
from rich.progress import track

from internal.utils import (
    DummyMember,
    Logger,
    create_guild_directory,
    create_member_file,
    download_pfp,
    get_account_settings,
    get_bio_fname,
    get_guild_members_fname,
    get_pfp_fname,
    load_member_ids_from_disk,
    save_members_dict,
)

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
    try:
        members = await scrape(config, guild)
    except InvalidData:
        logger.scraper("The list of members could not be scraped from the guild.")
        members = []

    create_guild_directory(guild)

    if members:
        save_members_dict(members, get_guild_members_fname(guild))

    member_ids = load_member_ids_from_disk()

    if member_ids:
        logger.scraper("Focusing on member IDs found on the local disk.")
        members = [
            DummyMember(i, guild, False, None) for i in member_ids
        ]

    for member in track(
        members,
        description="[bold white][Scraper] Scraping profiles...[/]",
    ):
        if config["download_bio"] and not Path(get_bio_fname(member)).exists():
            try:
                await create_member_file(member)
            except HTTPException:
                break
        if (
            config["download_pfp"]
            and not Path(get_pfp_fname(member, pfp_format)).exists()
        ):
            await download_pfp(member, pfp_format)

    logger.success("Finished scraping members profiles and data.\n")
    await client.close()
