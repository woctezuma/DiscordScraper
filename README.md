# Discord: Scraper of Guild Members' Metadata

This repository contains Python code to scrape metadata of all the members in a specific guild's channel on Discord.

## Features

- Specify which guild (server) and which channel to scrape from in a `JSON` config file.
- Scrape nickname, handle, bio, picture for every member, then save the results to a `TXT` file.

> [!Important]
> Bios are [heavily rate-limited][discord-api-docs].

## Requirements

-   Install the latest version of [Python 3.X][python-download].
-   Install the required packages:

```bash
pip install -r requirements.txt
```

> [!Tip]
> You may want to download some packages from [a third-party website][python-libs].
> Typically:
> - `frozenlist‑1.3.0‑py3‑none‑any.whl`
> - `multidict‑6.0.2‑py3‑none‑any.whl`

- Rename `config.json.example` to `config.json` and edit the required settings.

> [!Note]
> The `token` is the value of [`Authorization`][discord-token] as found in the `Headers` of your browser requests.

> [!Note]
> Input `channel_id` if you wish to scrape members from a particular channel. Otherwise, leave it to `0`.

> [!Important]
> For pictures, the image format is always `PNG`, no matter the file extension which you ask for via the JSON config.

## Usage

- Run the following script:

```bash
python main.py 
```

> [!Warning]
> About 300 bios can be downloaded before reaching the rate-limit and getting error `429 Too Many Requests` for an hour.

> [!Caution]
> Using selfbots is against Discord's Terms of Service, **use this project at your own risk**!

- To display a list of spammers identified by Discord, run the following script:

```bash
python display_spammers.py 
```

> [!Tip]
> If this is your sole objective, set `download_bio` and `download_pfp` to `false` to speed the process up.

## Screenshots

<img src='assets/console.png' style="width: 90%">
<img src='assets/guild_folder.png' style="width: 90%">

<!-- Definitions -->

[python-download]: <https://www.python.org/downloads/>
[python-libs]: <https://www.lfd.uci.edu/~gohlke/pythonlibs/>
[discord-token]: <https://developer.mozilla.org/docs/Web/HTTP/Headers/Authorization>
[discord-api-docs]: <https://github.com/discord/discord-api-docs/issues/3095>
