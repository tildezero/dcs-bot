import discord
from discord.ext import commands
import asyncio
from utils import permissions, default

class DCS(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.config = default.config()
    

def setup(bot):
    bot.add_cog(DCS(bot))

