import random

import discord
import openai
#from discord.ext import commands
#from discord.ext.commands import Bot

import constants
import rlrank
import scrape
import aichat

openai.api_key = constants.openai_key

intents = discord.Intents.all()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

steam_ids = {
    "window.95#0": "76561198037294606",
    "buckroe8208#8077": "76561198413196075",
    "rocky#9467": "76561198114679719",
    "RichardParker#2972": "76561198119027474"
}


@client.event
async def on_ready():
    print(f"{client.user} is ready!")

@client.event
async def on_message(message):
    print("worked")
    test = 0
    query = message.content.lower()

    if message.author == client.user:
        return

    if message.content.lower() == "/roll":
        num = random.randint(1, 6)
        await message.channel.send(f"{message.author.mention} rolled...", file=discord.File(f"d{num}.png"))
        test = 1

    if message.content.lower() == "/rank":
        heard = f"Let me check that for you, {message.author.mention}! Just a moment..."
        await message.channel.send(heard)
        rank = rlrank.scrape_rank(steam_ids[str(message.author)])
        response = f"{message.author.mention}, your Rocket League 3v3 rank is \n\n{rank}"

    if message.content.lower() == "/games":
        heard = f"Let me check that for you, {message.author.mention}! Just a moment..."
        await message.channel.send(heard)
        steam_ids_list = steam_ids.values()
        result = await scrape.get_owned_games(steam_ids_list)
        result_list = '\n'.join(result)
        response = f"{message.author.mention}, the Whiff City boys share the following multiplayer Steam games: \n\n{result_list} "

    
    if query[:4] == "/ai ":
        content = f"{constants.content} {message.content[3:]}"
        response = aichat.ai_chat(content)
        await message.channel.send(response)
        test = 1
        return test
    
    if query[:5] == "/img ":
        content = f"{message.content[5:]}"
        response = aichat.ai_img(content)
        await message.channel.send(response)
        test = 1
        return test
            
      
    if query[0] == "/" and test != 1:
        await message.channel.send(response)

client.run(constants.discord_token)
