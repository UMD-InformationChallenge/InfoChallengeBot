import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
BOT_MANAGER_ROLE_ID = int(os.getenv('BOT_MANAGER_ROLE_ID'))
GUILD_OWNER_ID = int(os.getenv('GUILD_OWNER_ID'))
EVENT_BOT_CHANNEL_ID = int(os.getenv('EVENT_BOT_CHANNEL_ID'))

# This is a mixin to make sure that these commands only work in the channel specified.
def is_in_bot_channel():
    async def channel_predicate(ctx):
        return ctx.channel and ctx.channel.id == EVENT_BOT_CHANNEL_ID

    return commands.check(channel_predicate)

def is_owner_or_botmgr():
    async def predicate(ctx):
        role = discord.utils.get(ctx.guild.roles, id=BOT_MANAGER_ROLE_ID)
        return (role in ctx.author.roles) or ctx.author.id == GUILD_OWNER_ID
    return commands.check(predicate)