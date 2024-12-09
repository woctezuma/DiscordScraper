import requests

DISCORD_API_URL = "https://discord.com/api/webhooks/"
TIMEOUT_IN_SECONDS = 5


def get_webhook_url(webhook_id: str) -> str:
    return f"{DISCORD_API_URL}{webhook_id}"


def post_message_to_discord(message: str, webhook_id: str) -> requests.Response | None:
    if webhook_id is None or len(message) == 0:
        response = None
    else:
        json_data = {"content": message}
        response = requests.post(
            url=get_webhook_url(webhook_id),
            json=json_data,
            timeout=TIMEOUT_IN_SECONDS,
        )

    return response
