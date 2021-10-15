import discord
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import json

URL_GENSHIN_CHARS = "https://library.keqingmains.com/characters"
client = discord.Client()
load_dotenv()

@client.event
async def on_ready():
    print("WE have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!help'):
        await message.channel.send('You are viewing all the commands of Clouds Bot')
    
    if message.content.startswith('!gbuild'):
        # await message.channel.send('Hello! {0}'.format(message.author))
        print("Request accepted from {}".format(message.author))
        all_data = get_data(message.content.split(' ')[1].lower())
        display_data = [
            "Name: {}, Element: {}".format(all_data[0], all_data[1][0].upper()+all_data[1][1:]),
            "At Level 90",
            "============",
            "Base HP: {}, Base ATK: {}, Base DEF:{}, {}:{}".format(all_data[3], all_data[4], all_data[5], all_data[2], all_data[6]),
            "Recommended Artifacts: {}".format(all_data[7]),
            "Recommended Mainstat: {}".format(all_data[9]),
            "Recommended Weapons: {}".format(all_data[8])
        ]
        for one_data in display_data:
            await message.channel.send(one_data)

    # Working on valorant agents
    if message.content.startswith('!vagent'):
        await message.channel.send('Valorant agents are being worked on. Please stay tuned {}. :)'.format(str(message.author).split('#')[0]))

def get_data(character):

    json_data = open('./gdata.json', 'r+')
    json_data = json.load(json_data)
    if character == 'hutao':
        character = 'hu-tao'
    if not character in json_data.keys():
        return "No character with such a name found"
    element = json_data[character]['element']
    released = json_data[character]['released']
    artifacts = json_data[character]['artifacts']
    weapons = json_data[character]['weapons']
    substat = json_data[character]['substat']

    if released == 'false':
        return "Character is not released or not computed on. No data to show"

    response = requests.get(url = "{}/{}/{}".format(URL_GENSHIN_CHARS, element, character.lower()))
    soup = BeautifulSoup(response.content, 'html.parser')
    actual_name = [r.strip() for r in soup.select_one('div > span:nth-child(3) > span')]
    ascension_stat = [r.strip() for r in soup.select_one('div > div:nth-child(5) > div > div > div > div > div > div > div > span > span')]
    base_hp = [r.strip() for r in soup.select_one('div > div:nth-child(8) > div > div:nth-child(2) > div > div > div > div > div > div > div > span > span')]
    base_atk = [r.strip() for r in soup.select_one('div > div:nth-child(8) > div > div:nth-child(3) > div > div > div > div > div > div > div > span > span')]
    base_def = [r.strip() for r in soup.select_one('div > div:nth-child(8) > div > div:nth-child(4) > div > div > div > div > div > div > div > span > span')]
    ascension_stat_num = [r.strip() for r in soup.select_one('div > div:nth-child(8) > div > div:nth-child(5) > div > div > div > div > div > div > div > span > span')]
    if character.lower() == 'kokomi':
        ascension_stat = ['Hydro DMG%']
    return [actual_name[0], element, ascension_stat[0], base_hp[0], base_atk[0], base_def[0], ascension_stat_num[0], artifacts, weapons, substat]

client.run(os.getenv('TOKEN'))
