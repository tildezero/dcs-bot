import discord
from discord.ext import commands
import asyncio
from utils import permissions, default, ticket_utils
import aiohttp
from replit import db

class Tickets(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.config = default.config()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        if payload.message_id == 788271918717468673 and str(payload.emoji) == "✉️":
            g = self.bot.get_guild(payload.guild_id)
            t = g.get_channel(788158807770791936)
            
            carry_role = g.get_role(782256235259887616)
            overwrites = {
                g.default_role: discord.PermissionOverwrite(read_messages=False),
                g.me:discord.PermissionOverwrite(read_messages=True),
                payload.member: discord.PermissionOverwrite(read_messages=True,send_messages=True,attach_files=True,embed_links=True),
                # carry_role: discord.PermissionOverwrite(read_messages=True,send_messages=True,attach_files=True,embed_links=True),
                
            }
            c = await t.create_text_channel(name=f"ticket-{payload.member.id}", overwrites= overwrites)
            await c.send(f"Hello <@{payload.member.id}>! Please answer these questions in order to recieve your carry. You may close the ticket at anytime with `d!close`")
            await c.send("Please enter the floor you need a carry for (1,2,3,4,5,6, or 7)! You have 60 seconds to response or else this ticket will be closed.")
            db[str(c.id)] = {"user": payload.member.id}
            def checkfloor(m):
                return m.author == payload.member and m.channel.id == c.id and m.content in ["1","2","3","4","5","6","7"]
            try:
                msg = await self.bot.wait_for('message', check = checkfloor, timeout = 120.0)
            except asyncio.TimeoutError:
                await c.send("you didn't send any message in this channel for 60 seconds... closing this ticket in 5 seconds")
                await asyncio.sleep(5)
                await c.delete()
                
        
            else:
                await c.send(f"Ok, a floor {msg.content} carry it is. On to the next question!")
                floor = msg.content
                
                
                pings = {
                    "1": 782258133581430784,
                    "2": 782258239457722410,
                    "3": 782258242331738144,
                    "4": 782258245045452800,
                    "5": 782258263949180940,
                    "6": 782258268369584179,
                    "7": 782258271968690186
                }
                g = self.bot.get_guild(payload.guild_id)
                t = g.get_channel(788158807770791936)
            
                # carry_role = g.get_role(782256235259887616)
             
                carry_role = g.get_role(pings[msg.content])
                # overwrites = {
                #     g.default_role: discord.PermissionOverwrite(read_messages=False),
                #     g.me:discord.PermissionOverwrite(read_messages=True),
                #     payload.member: discord.PermissionOverwrite(read_messages=True,send_messages=True,attach_files=True,embed_links=True),
                #     carry_role: discord.PermissionOverwrite(read_messages=True,send_messages=True,attach_files=True,embed_links=True),
                #     helper_role: discord.PermissionOverwrite(read_messages=True,send_messages=True,attach_files=True,embed_links=True),
                #     mod_role: discord.PermissionOverwrite(read_messages=True,send_messages=True,attach_files=True,embed_links=True) 
                # }
                
                # await c.edit(overwrites=overwrites)
                await c.edit(name=f"f{msg.content}-carry")
                await c.send("What score of carry do you want? (S, S+, Completion)\nNote: F1-4 only has completion. You have 60 seconds to respond.")
            def checkscore(m):
                return m.author == payload.member and m.channel.id == c.id and m.content.lower() in ["s","s+","completion"]
            try:
                scoremsg = await self.bot.wait_for('message', check = checkscore, timeout = 300.0)
            except asyncio.TimeoutError:
                await c.send("you didn't send any message in this channel for 60 seconds... closing this ticket in 5 seconds")
                await asyncio.sleep(5)
                await c.delete()
                
            else:
                await c.send(f"Ok! {scoremsg.content.title()} it is. Last question, then a carrier will be on their way")
                await c.send("What is your minecraft IGN? You have 60 seconds to respond.")
                score = scoremsg.content.lower()
            def checkign(m):
                return m.author == payload.member and m.channel.id == c.id
            try:
                ignmsg = await self.bot.wait_for('message', check = checkign, timeout = 300.0)
            except asyncio.TimeoutError:
                await c.send("you didn't send any message in this channel for 60 seconds... closing this ticket in 5 seconds")
                await asyncio.sleep(5)
                await c.delete()
                
        
            else:
                pings = {
                    "1": 782258133581430784,
                    "2": 782258239457722410,
                    "3": 782258242331738144,
                    "4": 782258245045452800,
                    "5": 782258263949180940,
                    "6": 782258268369584179,
                    "7": 782258271968690186
                }
                carry_role = g.get_role(pings[msg.content])
                overwrites = {
                    g.default_role: discord.PermissionOverwrite(read_messages=False),
                    g.me:discord.PermissionOverwrite(read_messages=True),
                    payload.member: discord.PermissionOverwrite(read_messages=True,send_messages=True,attach_files=True,embed_links=True),
                    carry_role: discord.PermissionOverwrite(read_messages=True,send_messages=True,attach_files=True,embed_links=True)
                }
                await c.edit(overwrites=overwrites)
                await c.send(f"""Thanks! A carrier will be coming shortly <@&{pings[msg.content]}>
                
Info for carrier:
Floor - {msg.content}
Requested score - {scoremsg.content.title()}
IGN - {ignmsg.content}
Price - {await ticket_utils.give_price(floor, score)}""")
        #add: ping floor carriers

        @commands.Cog.listener()
        async def on_raw_reaction_add(self, payload):
            if payload.member.id == self.bot.user.id:
                return
            carry_channels = ["f1-carry","f2-carry","f3-carry","f4-carry","f5-carry","f6-carry","f7-carry"]
            c = self.bot.get_channel(payload.channel_id)
            if str(payload.emoji) == "🔒" and c.name in carry_channels:
                await c.send('Please confirm this action by saying "yes" within the next 60 seconds, and your ticket will close')
            def checkyes(m):
                return m.author == payload.member and m.channel.id == c.id and m.content == "yes"
            try:
                msg = await self.bot.wait_for('message', check = checkyes, timeout = 60)
            except asyncio.TimeoutError:
                await c.send("you didn't confirm this action... this ticket will not close")
                
            else:
                
                await c.send("ok, closing the ticket in 5 seconds since you said " + msg.content)
                await asyncio.sleep(5)
                await c.delete()
        
    
    @commands.has_any_role(800794819009052672, 782256235259887616)
    @commands.command()
    @commands.guild_only()
    async def claim(self, ctx): 
        carry_channels = ["f1-carry","f2-carry","f3-carry","f4-carry","f5-carry","f6-carry","f7-carry"]
        if ctx.channel.name not in carry_channels:
            await ctx.send("not a ticket channel!")
            return
        else:
            await ctx.send('soon')
    
    @commands.command()
    @commands.guild_only()
    async def close(self, ctx):
        """Close a completed ticket"""
        carry_channels = ["f1-carry","f2-carry","f3-carry","f4-carry","f5-carry","f6-carry","f7-carry"]
        if ctx.channel.name not in carry_channels:
            await ctx.send("not a ticket channel!")
            return
        else:
            await ctx.send('Please confirm this action by saying "yes" within the next 60 seconds')
        def check(m):
            return m.author == ctx.author and m.channel.id == ctx.channel.id and m.content.lower() == "yes"
    
        try:
            msg = await self.bot.wait_for('message', check = check, timeout = 60.0)
        except asyncio.TimeoutError:
            await ctx.send("Oh no! You did not confirm, so this ticket will stay open")
            return
        
        else:
          messages = await ctx.channel.history(limit=None, oldest_first=True).flatten()
          ticketContent = " ".join([f"{message.content} | {message.author.name}\n" for message in messages])
        async with aiohttp.ClientSession() as cs:
          async with cs.post("https://hst.sh/documents", data=ticketContent) as r:
            resp = await r.json()
            ch = ctx.guild.get_channel(814902983392886804)
            await ch.send(f"Transcript for <#{ctx.channel.id}>\n https://hst.sh/{resp['key']}")
            await ctx.send(f"Closing the ticket in 5 seconds, <@{msg.author.id}>!")
        
            await asyncio.sleep(5)
            await ctx.channel.delete()

def setup(bot):
    bot.add_cog(Tickets(bot))

