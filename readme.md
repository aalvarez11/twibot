# Twibot! The friendly discord bot

A discord bot that will hopefully evolve and grow, with new features for use in my discord servers.

## Dependencies

- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- [dot env](https://pypi.org/project/python-dotenv/)
- [vxtwitter API](https://github.com/dylanpdx/BetterTwitFix/blob/main/api.md)
- [pytest](https://docs.pytest.org/en/stable/)
- [pytest-asyncio](https://pypi.org/project/pytest-asyncio/)

## Features

1. Twitter Link Replacer

The bot detects whenever a user sends a twitter link in the chat and will either replace the message with an xcancel url, or extract any animated media at the source. The bot is also set up to parse batch link posting, though the upper limit has not been tested.

2. Delete User Messages with a Reaction

The bot detects when a user reacts to a message with a designated emoji, in our case ❌ (unicode value: U0000274C), and as long as the reactor is the initial author, the bot shall delete the message. There is potential for moderation in the future, expanding the criteria to a moderator role being able to delete a message.

3. Roll Dice

The bot has a slash command for rolling dice. The user inputs a message with the command that contains the amount of dice and what type of dice in the format of xdy. The user may also input multiple dice together and include a modifier value such as +x or -y. All the dice rolls input are summed up together and only modifiers may subtract from the pool.
Example roll input format: `3d6+4d10-5`

## Future Plans

- [x] Add dice rolling for xdy format
- [ ] Add sign checking for dice
- [ ] Add dice rolling using FFG's Fate Dice System
- [ ] Use the future [xcancel API](https://github.com/unixfox/nitter-fork) for video embedding
- [ ] Pray for in-house Discord video embedding (and in discord py)
- [ ] Separate twitter logic into functions
- [x] Add message deletion for user's own messages via emoji reaction
