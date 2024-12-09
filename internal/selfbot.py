import random

from discord import Client, Guild
from discord.errors import HTTPException, InvalidData
from rich.progress import track
from src.aggregate_utils import save_aggregate_to_disk
from src.discord_utils import post_message_to_discord
from src.inspect_utils import find_trigger_warning
from src.load_aggregate_from_disk import load_aggregate_from_disk

from internal.utils import (
    DummyMember,
    Logger,
    create_guild_directory,
    create_member_file,
    filter_out_specific_ids,
    get_account_settings,
    get_guild_members_fname,
    load_known_ids,
    load_member_ids_from_disk,
    load_skipped_member_ids_from_disk,
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

    guild = client.get_guild(int(guild_id))
    try:
        members = await scrape(config, guild)
    except InvalidData:
        logger.scraper("The list of members could not be scraped from the guild.")
        members = []

    create_guild_directory(guild)

    if members:
        save_members_dict(members, get_guild_members_fname(guild))

    member_ids = set(load_member_ids_from_disk())

    if member_ids:
        logger.scraper("Focusing on member IDs found on the local disk.")
        member_ids.update([e.id for e in members])
        members = [DummyMember(i, guild) for i in member_ids]

    members = filter_out_specific_ids(
        members,
        set(load_skipped_member_ids_from_disk()).union(load_known_ids()),
    )

    counter = 0
    data = load_aggregate_from_disk()
    save_individual_profile_to_disk = False

    random.shuffle(members)
    for member in track(
        members,
        description="[bold white][Scraper] Scraping profiles...[/]",
    ):
        if config["download_bio"]:
            try:
                member_profile = await create_member_file(
                    member,
                    save_to_disk=save_individual_profile_to_disk,
                )
                if member_profile:
                    data[str(member.id)] = member_profile

                    if config["webhook_id"]:
                        trigger_warning = find_trigger_warning(member_profile)
                        if trigger_warning:
                            post_message_to_discord(
                                trigger_warning,
                                config["webhook_id"],
                            )
            except HTTPException:
                print(f"Error encountered for member ID = {member.id}.")

            counter += 1

            if counter >= config["max_num_requests"]:
                print(f"Stop after {counter} requests were made.")
                break

    save_aggregate_to_disk(data)

    logger.success("Finished scraping members profiles and data.\n")
    await client.close()
