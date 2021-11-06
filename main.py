import discord
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import re
import json
import genimp.genbase as geb
import val.agents as vaa

URL_GENSHIN_CHARS = "https://paimon.moe/client/build.fc5db9a5.js"
ALTERED_NAMES = {
    'kokomi': 'sangonomiya_kokomi',
    'hutao': 'hu_tao',
    'sara': 'kujou_sara',
    'raiden': 'raiden_shogun',
    'shogun': 'raiden_shogun',
    'baal': 'raiden_shogun',
    'childe': 'tartaglia',
    'ayaka': 'kamisato_ayaka',
    'kazuha': 'kaedehara_kazuha'
}
client = discord.Client()

load_dotenv()

@client.event
async def on_ready():
    print("WE have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!cloudshelp'):
        await message.channel.send('You are viewing all the commands of Clouds Bot')
    
    if message.content.startswith('!gbuild'):
        # await message.channel.send('Hello! {0}'.format(message.author))
        print("Request accepted from {}".format(message.author))
        response = requests.get(url = URL_GENSHIN_CHARS)
        response = response.text
        response = response.replace('const e=', '')
        response = response.replace('!0', '0')
        response = response.replace('!1', '1')
        response = response.replace(';export{e as b};', '')
        response = response.replace('\n//# sourceMappingURL=build.fc5db9a5.js.map', '')
        reg = re.findall(r'(\{|\,)([A-z]+)\:', response)
        list_all = list(set(reg))
        repeat_check = list()
        for _, name in list_all:
            if name not in repeat_check:
                response = response.replace('{}:\\n'.format(name), '{} \\n'.format(name))
                response = re.sub(r'(%s)\:'% name, '"{}":'.format(name), response)
                repeat_check.append(name)
        as_json = json.loads(response)
        all_data = parse_data(message.content.split(' ')[1].lower(), as_json)
        if all_data['message'] != "null":
            await message.channel.send(all_data["message"])
            return
        await message.channel.send("Building for {}:".format(all_data['character'].replace('_', ' ')))
        for one_role in all_data['content']['roles']:
            await message.channel.send("For the role of {}:".format(one_role))
            await message.channel.send("=====================================")
            await message.channel.send("Weapons: (Order is best to worst)")
            weapons = all_data["content"]["roles"][one_role]["weapons"]
            for one_weapon in weapons:
                await message.channel.send(one_weapon["id"].replace('_', ' '))
            await message.channel.send("-------------------------------------")
            await message.channel.send("Artifacts: (Order is best to worst)")
            artifacts = all_data["content"]["roles"][one_role]["artifacts"]
            for one_artifact in artifacts:
                await message.channel.send(one_artifact)
            await message.channel.send("-------------------------------------")
            await message.channel.send("Artifact Main Stat:")
            mainStats = all_data["content"]["roles"][one_role]["mainStats"]
            await message.channel.send(mainStats)
            await message.channel.send("-------------------------------------")
            await message.channel.send("Artifact Sub Stat:")
            subStats = all_data["content"]["roles"][one_role]["subStats"]
            await message.channel.send(subStats)
            await message.channel.send("-------------------------------------")
            await message.channel.send("Talent Priority:")
            talent = all_data["content"]["roles"][one_role]["talent"]
            await message.channel.send(talent)
            # await message.channel.send("-------------------------------------")
            # await message.channel.send("Tips:")
            # tip = all_data["content"]["roles"][one_role]["tip"]
            # await message.channel.send(tip)
            # await message.channel.send("-------------------------------------")
            # await message.channel.send("Note:")
            # note = all_data["content"]["roles"][one_role]["note"]
            # await message.channel.send(note)
            await message.channel.send("=====================================")
    
    if message.content.startswith('!gtalent'):
        await message.channel.send('Genshin Impact characters talent are being worked on. Stay Tuned :)')

    # Working on valorant agents
    if message.content.startswith('!vagent'):
        await message.channel.send('Valorant agents are being worked on. Please stay tuned {}. :)'.format(str(message.author).split('#')[0]))

def parse_data(character, all_data):
    if character in ALTERED_NAMES.keys():
        character = ALTERED_NAMES[character]
    if character not in all_data.keys():
        return {
            "message": "No Character with such a name found.",
            "content": "null"
        }
    return {
        "message": "null",
        "content": all_data[character],
        "character": character 
    }

client.run(os.getenv('TOKEN'))
