# Discord: Scraper of Guild Members' Metadata

This repository contains Python code to scrape metadata of all the members in a specific guild's channel on Discord.

## Features

- Specify which guild (server) and which channel to scrape from in a `JSON` config file.
- Scrape nickname, handle, bio, picture for every member, then save the results to a `TXT` file.

## Requirements

-   Install the latest version of [Python 3.X][python-download].
-   Install the required packages:

```bash
pip install -r requirements.txt
```

- Rename `config.json.example` to `config.json` and edit the required settings.

> [!Note]
> Input `channel_id` if you wish to scrape members from a particular channel. Otherwise, leave it to `0`.

## Usage

- Run the following script:

```bash
python main.py 
```

> [!Caution]
> Using selfbots is against Discord's Terms of Service, **use this project at your own risk**!

## Screenshots

<img src='assets/console.png' style="width: 90%">
<img src='assets/guild_folder.png' style="width: 90%">

<!-- Definitions -->

[python-download]: <https://www.python.org/downloads/>
