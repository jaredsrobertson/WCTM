import asyncio
import random
import sys

import discord
from discord.ext import commands
from selenium.common.exceptions import WebDriverException

import ai
import constants
import steam
import web


class dbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}
        print("dbot cog loaded!")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        print("dbot is ready!")

    @commands.command()
    async def steam(self, ctx):
        discord_id = ctx.author.id
        message = await ctx.send(f"Let me check that for you, {ctx.author.mention}! Just a moment...")
        steam_id = await steam.get_steam_id(str(discord_id))
        if steam_id == False:
            msg_connect_steam(ctx, discord_id)
        else:
            await ctx.send(f"{ctx.author.mention}, your Steam ID is {steam_id}!")
        await message.delete() 

    @commands.command()
    async def help(self, ctx):
        await ctx.send(constants.help, delete_after=150)

    @commands.command()
    async def roll(self, ctx):
        num = random.randint(1, 6)
        await ctx.send(f"{ctx.author.mention} rolled...", file=discord.File(f"dice/d{num}.png"), delete_after=150)

    @commands.command()
    async def rank(self, ctx):
        discord_id = ctx.author.id
        message = await ctx.send(f"Let me check that for you, {ctx.author.mention}! Just a moment...")
        steam_id = await steam.get_steam_id(str(discord_id))
        if steam_id == False:
            msg_connect_steam(discord_id)
        else:
            rank, rankimg = await web.get_rank(steam_id)
        await ctx.send(f"{ctx.author.mention}, your Rocket League 3v3 rank is \n\n{rank}", file=discord.File(f"rank/{rankimg}.png"), delete_after=150)
        await message.delete()

    @commands.command()
    async def games(self, ctx):
        message = await ctx.send(f"Let me check that for you, {ctx.author.mention}! Just a moment...")
        channel = self.bot.get_channel(ctx.author.voice.channel.id)
        discord_ids = list(channel.voice_states.keys())
        steam_ids = []
        if len(discord_ids) < 2:
            await ctx.send(f"{ctx.author.mention} This command gets a list of multiplayer steam games that all users in the current voice channel own. There needs to be at least two users present, and you're the only one here...")
            return
        else: 
            for discord_id in discord_ids:
                print(f"For discord_id in discord_ids: {discord_id}")
                steam_id = await steam.get_steam_id(str(discord_id))
                steam_ids.append(steam_id)
        if len(steam_ids) < 2:
            await ctx.send(f"{ctx.author.mention} This command gets a list of multiplayer steam games that all users in the current voice channel own, but it seems only one user here has a connected Steam account...")
            return
        else:
            result = await steam.get_owned_games(steam_ids)
        await message.delete()
        return result

    @commands.command()
    async def ai(self, ctx, *, query):
        content = f"{constants.content} {query}"
        response = ai.ai_chat(content)
        await ctx.send(response)

    @commands.command()
    async def img(self, ctx, *, query):
        response = ai.ai_img(query)
        await ctx.send(response)

    @commands.command()
    async def secret(self, ctx):
        await ctx.send('Message will be deleted in 5 seconds...', delete_after=5)
        await asyncio.sleep(5)
        await ctx.message.delete()

    @commands.command()
    async def x(self, ctx):
        await ctx.send("Exiting program...")
        try:
            web.exit()
        except WebDriverException as e:
            await ctx.send(f"Error while closing Selenium: {e}")
        try:
            await self.bot.close()
        except Exception as e:
            await ctx.send(f"Error while closing Discord bot: {e}")
        sys.exit()


async def msg_connect_steam(self, ctx, discord_id):
        user = await self.bot.fetch_user(discord_id)
        await ctx.send(f"{user.mention} Your Steam account is not connected to Discord! Go to Settings > Connections and connect your Steam account.", delete_after=60)

async def setup(bot):
    await bot.add_cog(dbot(bot))