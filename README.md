# <p align=center> Discord Guild Members Scraper

> [!Caution]
> Using selfbots is against Discord's TOS, use this project at your own risk.

The goal of the project is to scrape all the users in a specific server's channel.

### Features
- Scrape nickname, handle, bio, picture for every user, then saved to a `txt` file.
- Specify which guild (server) and which channel to scrape from in a JSON config file.

### Installation

- Clone repo from git
```sh
git clone https://github.com/Sxvxgee/Discord-Scraper
```

- Install the dependencies.
```sh
pip install -r requirements.txt
```

- Rename `config.json.example` to `config.json` and edit required settings.

> [!Note]
> Input `channel_id` if you wish to scrape members from a particular channel; else leave 0


### Usage
```sh
python main.py 
```

### Project screenshots
<img src='assets/console.png' style="width: 90%">
<img src='assets/datascraped_folder.png' style="width: 90%">
<img src='assets/guild_folder.png' style="width: 90%">

