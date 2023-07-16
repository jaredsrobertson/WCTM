import random
import asyncio
#import os

import discord
from discord.ext import commands
import spotipy
from spotipy import SpotifyClientCredentials
from dotenv import dotenv_values

config = dotenv_values('.env')

class dmusic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("dmusic cog loaded!")
        self.voice_channel = None
        self.player = None
        self.queue = []

    def search_song(self, song_name):
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=config['SPOTIFY_CLIENT_ID'], client_secret=config["SPOTIFY_CLIENT_SECRET"]))
        results = sp.search(q=song_name, type="track", limit=1)

        if len(results["tracks"]["items"]) == 0:
            return None
        
        track = results["tracks"]["items"][0]
        track_name = track["name"]
        track_artist = track["artists"][0]["name"]
        track_url = track["external_urls"]["spotify"]
        return {
            "name": track_name,
            "artist": track_artist,
            "url": track_url
        }

    async def play_song(self, ctx, song):
        voice_channel = ctx.author.voice.channel
        if not self.voice_channel:
            self.voice_channel = voice_channel
            self.player = await self.voice_channel.connect()

        if not self.player.is_playing():
            source = discord.FFmpegPCMAudio(song["url"], options="-vn")
            
            self.player.play(source)
            embed = discord.Embed(
                title=f"Now playing: {song['name']} - {song['artist']}",
                url=song['url'],
                color=discord.Color.green()
            )
            #asyncio.run_coroutine_threadsafe(ctx.send(embed=embed), self.bot.loop)
            await ctx.send(embed=embed)



    @commands.command()
    async def play(self, ctx, *, query):
        song = self.search_song(query)
        if not song:
            await ctx.send("Song not found.")
            return

        self.queue.append(song)
        if not self.player or not self.player.is_playing():
            await self.play_song(ctx, song)

    @commands.command()
    async def skip(self, ctx):
        if not self.player or not self.player.is_playing():
            await ctx.send("No song is currently playing.")
            return

        self.player.stop()
        await ctx.send("Skipped the current song.")

    @commands.command()
    async def queue(self, ctx):
        if len(self.queue) == 0:
            await ctx.send("Queue is empty.")
            return

        queue_list = ""
        for i, song in enumerate(self.queue, start=1):
            queue_list += f"{i}. {song['name']} - {song['artist']}\n"
        embed = discord.Embed(
            title="Song Queue",
            description=queue_list,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        print("dmusic is ready!")

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
        await ctx.send("", file = discord.File(f"mj/{num}.gif"), delete_after=25)

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

async def setup(bot):
    await bot.add_cog(dmusic(bot))