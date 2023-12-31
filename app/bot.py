import discord
import responses
import requests
from discord.ext import tasks
import os


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    print("STARTING")
    try:
        TOKEN = os.environ.get('TOKEN')
        APIKEY = os.environ.get('APIKEY')
        ChannelID = int(os.environ.get('ChannelID'))
    except Exception as e:
        print("ERROR: ", e)
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')
        checkCurrMap.start()

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        print(f'{username} said: {user_message} in {channel}')
        try:
            if user_message[0] == '?':
                user_message = user_message[1:]
                await send_message(message, user_message, is_private=True)
            else:
                await send_message(message, user_message, is_private=False)
        except Exception as e:
            print(e)

    @tasks.loop(minutes=0.5)
    async def checkCurrMap():
        channel = client.get_channel(ChannelID)
        response = requests.get(
            f"https://api.mozambiquehe.re/maprotation?auth={APIKEY}&version=2").json()
        map = response["ranked"]["current"]["map"]
        await channel.edit(name=map)

    client.run(TOKEN)