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
        await message.channel.send("Building for {}:".format(all_data['character'].replace('_', ' ').title()))
        for one_role in all_data['content']['roles']:
            await message.channel.send("For the role of {}:".format(one_role.title()))
            await message.channel.send("=====================================")
            await message.channel.send("Weapons: (Order is best to worst)")
            weapons = all_data["content"]["roles"][one_role]["weapons"]
            all_msg = str()
            for one_weapon in weapons:
                all_msg += "{} > ".format(one_weapon["id"].replace('_', ' ').title())
            await message.channel.send(all_msg)
            await message.channel.send("-------------------------------------")
            await message.channel.send("Artifacts: (Order is best to worst)")
            artifacts = all_data["content"]["roles"][one_role]["artifacts"]
            all_msg = str()
            for idx, one_artifact in enumerate(artifacts):
                all_msg += "{}: ".format(idx+1)
                for art_set in one_artifact:
                    all_msg += "{}, ".format(art_set.replace('_', ' ').title())
                all_msg += "\n"
            await message.channel.send(all_msg)
            await message.channel.send("-------------------------------------")
            await message.channel.send("Artifact Main Stat:")
            mainStats = all_data["content"]["roles"][one_role]["mainStats"]
            all_msg = str()
            for key in mainStats.keys():
                all_msg += "{} = {}, ".format(key.title(), mainStats[key])
            await message.channel.send(all_msg)
            await message.channel.send("-------------------------------------")
            await message.channel.send("Artifact Sub Stat:")
            subStats = all_data["content"]["roles"][one_role]["subStats"]
            all_msg = str()
            for subst in subStats:
                all_msg += "{} > ".format(subst)
            await message.channel.send(all_msg)
            await message.channel.send("-------------------------------------")
            await message.channel.send("Talent Priority:")
            talent = all_data["content"]["roles"][one_role]["talent"]
            all_msg = str()
            for each_talent in talent:
                all_msg += "{} > ".format(each_talent)
            await message.channel.send(all_msg)
            await message.channel.send("-------------------------------------")
            await message.channel.send("Tips:")
            tip = all_data["content"]["roles"][one_role]["tip"]
            tip = split_long_text(tip)
            for one_tip in tip:
                await message.channel.send(one_tip)
            await message.channel.send("-------------------------------------")
            await message.channel.send("Note:")
            note = all_data["content"]["roles"][one_role]["note"]
            note = split_long_text(note)
            for one_note in note:
                await message.channel.send(one_note)
            await message.channel.send("=====================================")
        await message.channel.send("Build request complete")
    
    if message.content.startswith('!gtalent'):
        await message.channel.send('Genshin Impact characters talent are being worked on. Stay Tuned :)')

    # Working on valorant agents
    if message.content.startswith('!vagent'):
        await message.channel.send('Valorant agents are being worked on. Please stay tuned {}. :)'.format(str(message.author).split('#')[0]))

def split_long_text(text):
    if len(text) == 0:
        return ["No data"]
    if len(text) < 2000:
        return [text]
    split_chunk = [text[begin:begin+2000] for begin in range(0, len(text), 2000)]    
    return split_chunk

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
