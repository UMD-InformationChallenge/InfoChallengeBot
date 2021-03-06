import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

from common import logging
from models import init_db

load_dotenv()

IS_PROD = os.environ['is_production'] == 'True'
DB_CONN = os.getenv('db_conn_uri')
EVENT_NAME = os.getenv('event_name')
EVENT_GUILD_ID = int(os.getenv('event_guild_id'))
DATA_DIR = os.getenv('data_dir')
LOGGING_STR = os.getenv('logging_str')
BOT_KEY = os.getenv('bot_prefix')
BOT_TOKEN = os.getenv('bot_token')
GUILD_OWNER_ID = int(os.getenv('guild_owner_id'))

EVENT_BOT_ROLES = ['Planning Team']
current_dir = Path('..')
data_path = current_dir / DATA_DIR

# Extensions (cogs) to load
extensions = ["manager", "registrator", "teambuilder"]

# Configure intents
intents = discord.Intents.default()
intents.members = True
intents.typing = False

# Set up the bot
bot = commands.Bot(
    command_prefix=BOT_KEY,
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
