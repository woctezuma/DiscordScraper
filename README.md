# <p align=center> Discord Scraper of Guild Members

This repository contains Python code to scrape all the members in a specific guild's channel.

> [!Caution]
> Using selfbots is against Discord's Terms of Service, **use this project at your own risk**!

## Features

- Specify which guild (server) and which channel to scrape from in a `JSON` config file.
- Scrape nickname, handle, bio, picture for every member, then save the results to a `TXT` file.

## Installation

- Clone the repository from GitHub.
```sh
git clone https://github.com/woctezuma/DiscordScraper.git
```

- Install the Python dependencies.
```sh
pip install -r requirements.txt
```

- Rename `config.json.example` to `config.json` and edit the required settings.
> [!Note]
> Input `channel_id` if you wish to scrape members from a particular channel. Otherwise, leave it to `0`.

## Usage

```sh
python main.py 
```

## Screenshots

<img src='assets/console.png' style="width: 90%">
<img src='assets/datascraped_folder.png' style="width: 90%">
<img src='assets/guild_folder.png' style="width: 90%">
