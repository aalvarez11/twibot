import os 
from discord.ext.commands import Bot
from discord import Intents, Interaction, Object, app_commands
from dotenv import load_dotenv
from datetime import datetime
import requests
from dice import roll_dice

# Load Token from env
load_dotenv()
DISCORD_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
GUILD_ID = int(os.getenv("SERVER_ID"))

# Bot setup
intents = Intents.default()
intents.message_content = True
bot = Bot(command_prefix='!', intents=intents)
curr_time = datetime.now()

# Online indicator
@bot.event
async def on_ready():
    print(f'logged in as {bot.user.name}')
    try:
        command_count = await bot.tree.sync()
        print(f'Synced {len(command_count)} command(s)')
    except Exception as e:
        print(f'An error with syncing occurred: {e}')
    
    home_channel = bot.get_channel(CHANNEL_ID)
    time_of_day = ''
    if curr_time.hour >= 17:
        time_of_day = 'evening'
    elif curr_time.hour >= 12:
        time_of_day = 'afternoon'
    else:
        time_of_day = 'morning'
    await home_channel.send(f'Good {time_of_day} everypony!')

# Message Functionality
@bot.event
async def on_message(msg):
    # ignore messages from the bot
    if msg.author == bot.user:
        return

    botResponse = f'Your friend, {msg.author.display_name}, wanted to share this with you!\n'
    
    msgLowered = msg.content.lower()

    # handle multiple line inputs
    msgContent = msgLowered.splitlines()

    # check if the message is a twitter link
    twitUrls = ['//twitter.com','//x.com','//fixupx.com','//fixvx.com','//vxtwitter.com','//fxtwitter.com','//girlcockx.com']

    for msgLine in msgContent:
        for url in twitUrls:
            if url in msgLine:
                # check if the tweet has media, then if it is video
                checkUrl = msgLine.replace(url, '//api.vxtwitter.com')
                try:
                    vxApiResponse = requests.get(checkUrl)
                    vxApiResponse.raise_for_status()
                    responseData = vxApiResponse.json()

                    if (responseData["hasMedia"] and (responseData["media_extended"][0]["type"] == 'video' or responseData["media_extended"][0]["type"] == 'gif')):
                        await msg.channel.send(botResponse + responseData["media_extended"][0]["url"])
                        
                        # check for text in media tweet
                        if (responseData["text"]):
                            responseText = responseData["text"]
                            # remove quote tweet links
                            if('https://t.co/' in responseText): responseText = responseText.split('https://t.co/')[0]
                            # do not send empty strings    
                            if(responseText != ''): await msg.channel.send(f'\n\"' + responseText + f'\"')
                    else:
                        # replace the url with the cancel url
                        newUrl = msgLine.replace(url, '//xcancel.com')

                        # output a message
                        await msg.channel.send(botResponse + newUrl)

                except requests.exceptions.HTTPError as e:
                    raise SystemExit(e)

                # don't delete original until all lines have been parsed
                if (msgLine == msgContent[len(msgContent)-1]):
                    await msg.delete()

# Reaction Functionality
@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if(payload.user_id == payload.message_author_id and str(payload.emoji) == "\U0000274C"):
        await message.delete()

# Command Functionality
@bot.tree.command(name='roll', description='rolls and sums up dice and a modifier')
@app_commands.describe(msg="roll format: xdy+...+modifier")
async def roll(interaction: Interaction, msg: str):
    try: 
        result = await roll_dice(msg)
        await interaction.response.send_message(f'You rolled {msg} and your result is: {result}!')
    except TypeError as e:
        await interaction.response.send_message(e)

# Load token on startup
bot.run(token=DISCORD_TOKEN)