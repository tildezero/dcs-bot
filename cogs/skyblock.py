import discord
from discord.ext import commands
from utils import default, http
import aiohttp

class Skyblock(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = default.config()
    
    @commands.command()
    async def sbprof(self, ctx, username, profile=None):
        """ Returns the sky.shiiyu.moe link for a given profile """
        if profile == None:
            await ctx.send(f"https://sky.shiiyu.moe/stats/{username}")
        else:
            await ctx.send(f'https://sky.shiiyu.moe/stats/{username}/{profile}')



def setup(bot):
    bot.add_cog(Skyblock(bot))