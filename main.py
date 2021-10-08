import discord
import os
from dotenv import load_dotenv
import json

client = discord.Client()
load_dotenv()

@client.event
async def on_ready():
    print("WE have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!build'):
        await message.channel.send('Hello! {0}'.format(message.author))
        all_data = get_data(message.content.split(' ')[1].lower())
        await message.channel.send(all_data)

def get_data(character):
    file = open('./data.json', 'r+')
    data = json.load(file)
    return data[character]['element']

client.run(os.getenv('TOKEN'))
