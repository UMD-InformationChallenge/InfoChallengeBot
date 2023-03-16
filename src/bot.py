import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

from common import logging
from models import init_db

load_dotenv()

IS_PROD = os.environ['IS_PROD'] == 'True'

EVENT_NAME = os.getenv('EVENT_NAME')

EVENT_GUILD_ID = int(os.getenv('EVENT_GUILD_ID'))
GUILD_OWNER_ID = int(os.getenv('GUILD_OWNER_ID'))

BOT_PREFIX = os.getenv('BOT_PREFIX')  # FIXME: Not in dotenv example
BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_CONN_URI = os.getenv('DB_CONN_URI')
LOGGING_STR = os.getenv('LOGGING_STR')

EVENT_BOT_ROLES = ['Planning Team']

# Extensions (cogs) to load
extensions = ["manager", "registrator", "teambuilder"]

# Configure intents
intents = discord.Intents.default()
intents.members = True
intents.typing = False

# Set up the bot
bot = commands.Bot(
    command_prefix=BOT_PREFIX,
    description=f"Registration Bot for {EVENT_NAME}",
    intents=intents)
bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.watching,
                                  name=EVENT_NAME)
    )
    log.info(f"Bot is ready for {EVENT_NAME}!")
    for guild in bot.guilds:
        log.info(f"Bot is connected to {guild.id} - {guild.name} - {guild.owner.name}")
    
        await guild.owner.send(f"I am awake! "
                               f"(https://github.com/UMD-InformationChallenge/InfoChallengeBot)")


if __name__ == '__main__':
    log = logging.get_module_logger(LOGGING_STR)
    log.info(f"Start automatic ground launch sequencer.")

    init_db()

    cog_count = 0
    for extension in extensions:
        try:
            bot.load_extension(f"cogs.{extension}")
            log.info(f"Loaded Cog: {extension}")
            cog_count += 1
        except Exception as error:
            log.warning(f"Cog Error: {extension} could not be loaded.\n\t[{error}]")

        log.info(f"Loaded {cog_count}/{len(extensions)} cogs.")

    log.info(f"Main engine start. Go for launch!")
    bot.run(BOT_TOKEN)
