from internal.selfbot import client
from internal.utils import Logger, check_config_file, get_account_settings, show_header

show_header()
check_config_file()
log = Logger()
config = get_account_settings()

client.run(config["token"])
