# This example requires the 'message_content' intent.
import discord
from Crawler.Crawling import crawl
import json
from Variables import USER_ID, TOKEN

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$reload'):
        res = crawl(USER_ID)
        print(res['notifs_note'])
        for i in range(len(res['notifs_note'])):
            res['notifs_note'][i] = " : ".join(res['notifs_note'][i])

        if res['notifs_note']:
            await message.channel.send("\n".join(res['notifs_note']))
        else:
            await message.channel.send("RAS")

client.run(TOKEN)