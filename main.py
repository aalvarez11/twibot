import os 
from discord.ext.commands import Bot 
from discord import Intents
from dotenv import load_dotenv
import requests

# Load Token from env
load_dotenv()
DISCORD_TOKEN = os.getenv("BOT_TOKEN")

# Bot setup
intents = Intents.default()
intents.message_content = True
bot = Bot(command_prefix='!', intents=intents)

# Online indicator
@bot.event
async def on_ready():
    print(f'logged in as {bot.user.name}')

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

# Load token on startup
bot.run(token=DISCORD_TOKEN)