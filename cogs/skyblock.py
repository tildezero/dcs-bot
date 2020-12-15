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
"""
    @commands.command()
    async def scammer(self, ctx, username):
        uuid_data = await http.get(url=f"https://api.mojang.com/users/profiles/minecraft/{username}",res_method="json")
        uuid = uuid_data["id"]
        # https://raw.githubusercontent.com/skyblockz/pricecheckbot/master/scammer.json
        try:
            scammer_data = await http.get(url="https://raw.githubusercontent.com/skyblockz/pricecheckbot/master/scammer.json", res_method="json")
        except aiohttp.ContentTypeError:
            await ctx.send("error pog")
        else:
            if uuid in scammer_data:
                await ctx.send("scammer")
            else:
                await ctx.send("not scammer")
"""
    @commands.command()
    async def scammer(self, ctx, username):
        uuid_data = await http.get(url=f"https://api.mojang.com/users/profiles/minecraft/{username}",res_method="json")
        uuid = uuid_data["id"]
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://raw.githubusercontent.com/skyblockz/pricecheckbot/master/scammer.json") as r:
                scammer_data = await res.json()
                if uuid in scammer_data:
                    await ctx.send("scammer")
                else:
                    await ctx.send("not scammer")




def setup(bot):
    bot.add_cog(Skyblock(bot))