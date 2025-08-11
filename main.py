import os 
from discord.ext.commands import Bot
from discord import Intents, Interaction, Object, app_commands
from dotenv import load_dotenv
from twitfix import fix_tweets
from twibot_consts import fun_facts
from datetime import datetime
from dice import roll_dice
from random import randint

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

    msg_lowered = msg.content.lower()

    if bot.user.mentioned_in(msg): 
        if 'hi' in msg_lowered or 'hello' in msg_lowered:
            await msg.channel.send(f'Hello {msg.author.display_name}!')

    await fix_tweets(msg)

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

@bot.tree.command(name='fun fact', description='provides a fun fact about someone in the server')
async def fun_fact(interaction: Interaction):
    rand_index = randint(0,len(fun_facts)-1)
    await interaction.response.send_message(fun_facts[rand_index])

# Load token on startup
bot.run(token=DISCORD_TOKEN)