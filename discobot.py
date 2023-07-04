import asyncio
import random

import discord
from discord.ext import commands

import aichat
import constants
import rlrank
import scrape

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)
bot.remove_command('help')

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def mj(self, ctx):

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('mj/song.mp3'))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        num = random.randint(1, 9)
        await ctx.send("", file = discord.File(f"mj/{num}.gif"), delete_after=10)

    @commands.command()
    async def stop(self, ctx):
 
        await ctx.voice_client.disconnect()

    @mj.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


class DBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def help(self, ctx):
        await ctx.send(constants.help)

    @commands.command()
    async def roll(self, ctx):
        num = random.randint(1, 6)
        await ctx.send(f"{ctx.author.mention} rolled...", file=discord.File(f"dice/d{num}.png"), delete_after=150)

    @commands.command()
    async def rank(self, ctx):
        message = await ctx.send(f"Let me check that for you, {ctx.author.mention}! Just a moment...")
        rank, rankimg = rlrank.scrape_rank(constants.steam_ids[str(ctx.author)])
        #rankimg = imgrank.rank_check(rank)
        await ctx.send(f"{ctx.author.mention}, your Rocket League 3v3 rank is \n\n{rank}", file=discord.File(f"rank/{rankimg}.png"), delete_after=150)
        await message.delete()

    @commands.command()
    async def games(self, ctx):
        message = await ctx.send(f"Let me check that for you, {ctx.author.mention}! Just a moment...")
        result = await scrape.get_owned_games(constants.steam_ids.values())
        result_list = '\n'.join(result)
        await ctx.send(f"{ctx.author.mention}, the Whiff City boys share the following multiplayer Steam games: \n\n{result_list} ", delete_after=150)
        await message.delete()

    @commands.command()
    async def ai(self, ctx, *, query):
        content = f"{constants.content} {query}"
        response = aichat.ai_chat(content)
        await ctx.send(response)

    @commands.command()
    async def img(self, ctx, *, query):
        response = aichat.ai_img(query)
        await ctx.send(response)

    @commands.command()
    async def secret(self, ctx):
        await ctx.send('Message will be deleted in 5 seconds...', delete_after=5)
        await asyncio.sleep(5)
        await ctx.message.delete()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

async def main():
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.add_cog(DBot(bot))
        await bot.start(constants.discord_token)

asyncio.run(main())