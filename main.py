import discord
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import json
import genimp.gtalent as get
import val.agents as vaa

URL_GENSHIN_CHARS = "https://library.keqingmains.com/characters"
client = discord.Client()
load_dotenv()

def process_url(character):
    json_data = open('./genimp/gdata.json', 'r+')
    json_data = json.load(json_data)
    if character == 'hutao':
        character = 'hu-tao'
    if not character in json_data.keys():
        return {'error': "No character with such a name found. Please put the actual name of the character"}
    elif json_data[character]["released"] == 'false':
        return {'error': "Character is not released or not computed on. No data to show"}
    return {
        'character_name': character, 
        'element': json_data[character]["element"], 
        'artifacts': json_data[character]["artifacts"],
        'substat': json_data[character]["substat"],
        'weapons': json_data[character]["weapons"],
        'error': "None"
    }

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
        
        if all_data['message'] != None:
            await message.channel.send(all_data["message"])
            return
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
    
    if message.content.startswith('!gtalent'):
        
        await message.channel.send('Genshin Impact characters talent are being worked on. Stay Tuned :)')

    # Working on valorant agents
    if message.content.startswith('!vagent'):
        await message.channel.send('Valorant agents are being worked on. Please stay tuned {}. :)'.format(str(message.author).split('#')[0]))

def get_data(character):

    data = process_url(character)

    if data['error'] != "None":
        return {"message": data['error']}

    artifacts = data['artifacts']
    weapons = data['weapons']
    substat = data['substat']

    response = requests.get(url = "{}/{}/{}".format(URL_GENSHIN_CHARS, data['element'], data['character_name'].lower()))
    soup = BeautifulSoup(response.content, 'html.parser')
    actual_name = [r.strip() for r in soup.select_one('div > span:nth-child(3) > span')]

    if character.lower() == 'kokomi' or character.lower() == 'thoma':
        ascension_stat = [r.strip() for r in soup.select_one('#root > div > div > div > div.css-1dbjc4n.r-14lw9ot.r-13awgt0 > div > div > div > div.css-1dbjc4n.r-1ro0kt6.r-18u37iz.r-16y2uox.r-1wbh5a2.r-1777fci > div > div:nth-child(2) > div.css-1dbjc4n.r-bnwqim > div:nth-child(2) > div:nth-child(4) > div > div > div > div > div.css-1dbjc4n.r-150rngu.r-156hn8l.r-z2wwpe.r-rs99b7.r-18u37iz.r-16y2uox.r-1wbh5a2.r-lltvgl.r-buy8e9.r-1sncvnh > div > div:nth-child(1) > div:nth-child(5) > div')]
    else:
        ascension_stat = [r.strip() for r in soup.select_one('div > div:nth-child(1) > div:nth-child(5) > div > div > div > span > span')]
    
    base_hp = [r.strip() for r in soup.select_one('div > div:nth-child(8) > div:nth-child(2) > div > div > div > span > span')]
    base_atk = [r.strip() for r in soup.select_one('div > div:nth-child(8) > div:nth-child(3) > div > div > div > span > span')]
    base_def = [r.strip() for r in soup.select_one('div > div:nth-child(8) > div:nth-child(4) > div > div > div > span > span')]
    ascension_stat_num = [r.strip() for r in soup.select_one('div > div:nth-child(8) > div:nth-child(5) > div > div > div > span > span')]
    
    returning = [actual_name[0], data['element'], ascension_stat[0], base_hp[0], base_atk[0], base_def[0], ascension_stat_num[0], artifacts, weapons, substat]
    return_data = {key: value for key, value in enumerate(returning)}
    return_data["message"] = None
    return return_data

client.run(os.getenv('TOKEN'))
