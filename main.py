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

# Message Functionality
@bot.event
async def on_ready():
    print(f'logged in as {bot.user.name}')

@bot.event
async def on_message(msg):
    # ignore messages from the bot
    if msg.author == bot.user:
        return

    # try:
    #     vxApiResponseImg = requests.get('https://api.vxtwitter.com/twipiebongrip/status/1883670764639174788?t=8G7EkwbsUEapejLU5U24zA&s=19')
    #     vxApiResponseImg.raise_for_status()
    #     imgData = vxApiResponseImg.json()
    #     print(imgData["media_extended"][0]["type"])
    # except requests.exceptions.HTTPError as e:
    #     raise SystemExit(e)
    
    # print('========================================================')
    # try:
    #     vxApiResponseVid = requests.get('https://api.vxtwitter.com/PokemonGems/status/1688174828308590592?t=qvnfMnjMZWK-RQXuxE9t8w&s=19')
    #     vxApiResponseVid.raise_for_status()
    #     vidData = vxApiResponseVid.json()
    #     print(vidData["media_extended"][0]["type"])
    #     print(vidData["media_extended"][0]["url"])
    # except requests.exceptions.HTTPError as e:
    #     raise SystemExit(e)

    # print('========================================================')
    # try:
    #     vxApiResponseVid = requests.get('https://api.vxtwitter.com/xsheyou58g/status/1767121503752208670?t=cG6LtKb-3kgMUr44GqZEJQ&s=19')
    #     vxApiResponseVid.raise_for_status()
    #     vidData = vxApiResponseVid.json()
    #     print(vidData["media_extended"][0]["type"])
    #     print('========================================================')
    #     print(vidData)
    # except requests.exceptions.HTTPError as e:
    #     raise SystemExit(e)
    
    # print('========================================================')
    # try:
    #     vxApiResponseText = requests.get('https://api.vxtwitter.com/LyonsRoar15/status/1884361255881740687')
    #     vxApiResponseText.raise_for_status()
    #     textData = vxApiResponseText.json()
    #     print(textData)
    # except requests.exceptions.HTTPError as e:
    #     raise SystemExit(e)
    
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
                        await msg.channel.send('That one\'s supposed to move!\n' + responseData["media_extended"][0]["url"])
                    else:
                        # replace the url with the cancel url
                        newUrl = msgLine.replace(url, '//xcancel.com')

                        # output a message
                        await msg.channel.send('Fixed it for you!\n' + newUrl)

                except requests.exceptions.HTTPError as e:
                    raise SystemExit(e)

                # don't delete original until all lines have been parsed
                if (msgLine == msgContent[len(msgContent)-1]):
                    await msg.delete()

# Load token on startup
bot.run(token=DISCORD_TOKEN)