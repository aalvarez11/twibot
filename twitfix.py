import requests
from typing import Optional

twit_urls = ['//twitter.com','//x.com','//fixupx.com','//fixvx.com','//vxtwitter.com','//fxtwitter.com','//girlcockx.com']

# Makes an API call 
# Returns the response object, if found
async def fetch_tweet_info(api_url):
    try:
        vx_api_response = requests.get(api_url)
        vx_api_response.raise_for_status()
        return vx_api_response.json()
    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)

# Checks if the tweet has media, particularly video or a gif
# Returns the url, if media is found
async def check_for_media(data) -> Optional[str]:
    if (data["hasMedia"] and (data["media_extended"][0]["type"] == 'video' or data["media_extended"][0]["type"] == 'gif')):
        return data["media_extended"][0]["url"]
    else:
        return None

# Checks if the tweet has text
# Returns tweet text with quote tweet links truncated
async def check_for_text(data) -> Optional[str]:
    if (data["text"]):
        response_text = data["text"]
        if('https://t.co/' in response_text): 
            response_text = response_text.split('https://t.co/')[0]
        # do not output empty strings
        if(response_text != ''):
            return (f'\"' + response_text + f'\"\n')
        else:
                return None
    else:
        return None

# Checks messages for twitter urls, 
# Returns equivalent xcancel url or rips media
async def fix_url(msg):
    sender_notice = f'Your friend, {msg.author.display_name}, wanted to share this with you!\n'

    msg_lowered = msg.content.lower()

    # handle multiple line inputs
    msg_split = msg_lowered.splitlines()

    for line in msg_split:
        for url in twit_urls:
            if url in line:
                api_url = line.replace(url, '//api.vxtwitter.com')
                response_data = fetch_tweet_info(api_url)

                # extract media if any
                media_url = check_for_media(response_data)
                tweet_text = check_for_text(response_data)

                if media_url: 
                    if tweet_text:
                        return (sender_notice + tweet_text + media_url)
                    else:
                        return (sender_notice + media_url)
                else:
                    cancel_url = line.replace(url, '//xcancel.com')
                    return (sender_notice + cancel_url)