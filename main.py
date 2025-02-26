import os 
from discord.ext.commands import Bot
from discord import Intents
from dotenv import load_dotenv
from twitfix import fix_tweets

# Load Token from env
load_dotenv()
DISCORD_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Bot setup
intents = Intents.default()
intents.message_content = True
bot = Bot(command_prefix='!', intents=intents)

# Online indicator
@bot.event
async def on_ready():
    print(f'logged in as {bot.user.name}')
    home_channel = bot.get_channel(CHANNEL_ID)
    await home_channel.send('Good morning everypony!')

# Message Functionality
@bot.event
async def on_message(msg):
    # ignore messages from the bot
    if msg.author == bot.user:
        return

    await fix_tweets(msg)

# Reaction Functionality
@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if(payload.user_id == payload.message_author_id and str(payload.emoji) == "\U0000274C"):
        await message.delete()
       
# Load token on startup
bot.run(token=DISCORD_TOKEN)