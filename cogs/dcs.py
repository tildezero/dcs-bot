import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import aiohttp
from utils import default, ticket_utils, http
from replit import db
import json
import importlib

class DCS(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.config = default.config()
        self.session = aiohttp.ClientSession()
    
    @commands.command()
    async def scammer(self, ctx, ign: str):
      uuid_data = await self.session.get(f"https://api.mojang.com/users/profiles/minecraft/{ign}")
      if uuid_data.status == 204:
        return await ctx.send("Ign Invalid!")
      uuid_json = await uuid_data.json()
      uuid = uuid_json['id']
      scammer_data = await http.get("https://raw.githubusercontent.com/skyblockz/pricecheckbot/master/scammer.json", res_method = "text")
      scammer_json = json.loads(scammer_data)
      if uuid in scammer_json:
        await ctx.send("scammer")
      else:
        await ctx.send("not scammer")

    @commands.has_any_role(800794819009052672,784452088691294208,783019756520472577,782256668733734933)
    @commands.command(name="updateprice", aliases=['update','setprice'])
    async def update_price(self, ctx, floor: str, score: str, amount: str):
      if not score.lower() in ["completion", "s", "s+"]:
        return await ctx.send("Invalid score! Valid scores are: Completion, S, and S+")
      if not floor.lower() in ["1", "2", "3", "4", "5", "6", "7"]:
        return await ctx.send("Invalid floor! Valid floors are 1, 2, 3, 4, 5, 6, and 7 (NUMBER ONLY)")
      db[f"price-{floor.lower()}-{score.lower()}"] = amount
      await ctx.send("sucessfully updated price!")
      module_name = importlib.import_module("utils.ticket_utils")
      importlib.reload(module_name)
    
    @commands.has_any_role(800794819009052672,784452088691294208,783019756520472577,782256668733734933)
    @commands.command(name="setbulkprice", aliases=['sbp'])
    async def set_bulk_price(self, ctx, floor: str, score: str, amount: str):
      if not score.lower() in ["completion", "s", "s+"]:
        return await ctx.send("Invalid score! Valid scores are: Completion, S, and S+")
      if not floor.lower() in ["1", "2", "3", "4", "5", "6", "7"]:
        return await ctx.send("Invalid floor! Valid floors are 1, 2, 3, 4, 5, 6, and 7 (NUMBER ONLY)")
      db[f"bulk-price-{floor.lower()}-{score.lower()}"] = amount
      await ctx.send("sucessfully updated price!")
      module_name = importlib.import_module("utils.ticket_utils")
      importlib.reload(module_name)

    @commands.command()
    async def price(self, ctx, floor: str, score: str):
      if not score.lower() in ["completion", "s", "s+"]:
        return await ctx.send("Invalid score! Valid scores are: Completion, S, and S+")
      if not floor.lower() in ["1", "2", "3", "4", "5", "6", "7"]:
        return await ctx.send("Invalid floor! Valid floors are 1, 2, 3, 4, 5, 6, and 7 (NUMBER ONLY)")
      
      price = await ticket_utils.give_price(floor, score)
      await ctx.send(f"Price for that carry would be about {price} coins")
    
    @commands.cooldown(1, 3600, BucketType.user)
    @commands.command(cooldown_after_parsing=True)
    async def rep(self, ctx, user: discord.Member):
      if user == ctx.author:
        return await ctx.send("You can't rep yourself!")
      if user.bot:
        return await ctx.send("you can't give rep to bots!")
      try:
        curr_rep = db[str(user.id)]
      except KeyError:
        db[str(user.id)] = 1
        await ctx.send(f"sucessfully gave {user.name}#{user.discriminator} 1 reputation!")
      else:
        new_rep = curr_rep + 1
        db[str(user.id)] = new_rep
        await ctx.send(f"sucessfully gave {user.name}#{user.discriminator} 1 reputation!")
    
    @commands.command()
    async def checkrep(self, ctx, user: discord.Member = None):
      member = user or ctx.author
      try:
        rep = db[str(member.id)]
      except KeyError:
        await ctx.send(f"{member.name}#{member.discriminator} has 0 reputation!")
      else:
        await ctx.send(f"{member.name}#{member.discriminator} has {rep} reputation!")
    
    @commands.cooldown(1, 3600, BucketType.user)
    @commands.command()
    async def takerep(self, ctx, user: discord.Member):
      if user == ctx.author:
        return await ctx.send("You can't -rep yourself!")
      if user.bot:
        return await ctx.send("you can't -rep bots!")
      try:
        curr_rep = db[str(user.id)]
      except KeyError:
        await ctx.send("This user doesn't have any reputation you can take away!")
      else:
        if curr_rep <= 0 :
          return await ctx.send("This use doesn't have any reputation you can take away!")
        new_rep = curr_rep - 1
        db[str(user.id)] = new_rep
        await ctx.send(f"sucessfully took 1 reputation away from {user.name}#{user.discriminator}!")
      


def setup(bot):
    bot.add_cog(DCS(bot))

