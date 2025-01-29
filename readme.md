# Twibot! The friendly discord bot

A discord bot that will hopefully evolve and grow, with new features for use in my discord servers.

## Dependencies

- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- [dot env](https://pypi.org/project/python-dotenv/)
- [vxtwitter API](https://github.com/dylanpdx/BetterTwitFix/blob/main/api.md)

## Features

1. Twitter link replacer

The bot detects whenever a user sends a twitter link in the chat and will either replace the message with an xcancel url, or extract any animated media at the source. The bot is also set up to parse batch link posting, though the upper limit has not been tested.
