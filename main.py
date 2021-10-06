import discord
import os
from dotenv import load_dotenv

client = discord.Client()
load_dotenv()

@client.event
async def on_ready():
    print("WE have logged in as (0.user)".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!build %s'):
        await message.channel.send('Hello! %s')

client.run(os.getenv('TOKEN'))
