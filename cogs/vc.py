import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class VC(commands.Cog, description="Voice channel related commands!"):
    def __init__(self, bot):
        self.bot = bot
    
    # commands: 


def setup(bot):
    bot.add_cog(VC(bot))