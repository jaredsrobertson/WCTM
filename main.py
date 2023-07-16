import asyncio
from pathlib import Path
import logging

import discord
from discord.ext import commands
from dotenv import dotenv_values

config = dotenv_values('.env')

logging.basicConfig(level=logging.INFO)
#discord.utils.setup_logging()

class Bot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.remove_command('help') 

    async def load_extensions(self):
        logging.info("Loading cogs...")
        for filename in Path("./cogs").glob("*.py"):
            if filename.is_file():
                try:
                    await self.load_extension(f"cogs.{filename.stem}")
                    logging.info(f"Loaded extension: {filename.stem}")
                except Exception as e:
                    logging.error(f"Failed to load extension: {filename.stem}. Error: {e}")

    async def on_ready(self):
        await self.load_extensions()
        logging.info(f"Bot is ready! Logged in as {self.user} (ID: {self.user.id})")

async def main():
    if not config.get("discord_token"):
        logging.error("Please set your discord token in .env")
        return
    
    intents = discord.Intents.all()
    intents.members = True
    intents.messages = True
    intents.message_content = True
    bot = Bot(command_prefix='.', intents=intents)

    try:
        await bot.start(config["discord_token"])
    except discord.LoginFailure:
        logging.error("Failed to log in with provided Discord token.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        await bot.close()

asyncio.run(main())