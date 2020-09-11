import discord
from discord.ext import menus
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot
from discord.ext.commands import has_permissions
import asyncio

# Cog for nuking text channels
class NukeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True) # Must do pass_context = True for code to work
    @commands.has_permissions(manage_guild=True)
    async def nuke(self, ctx):
        channel = ctx.message.channel
        messages = []

        # Gets messages and adds them to list
        async for message in channel.history(limit = 100):
            messages.append(message)

        # Doomsday countdown message
        for count in range(0,6):
            embed = discord.Embed(title="DOOMSDAY COUNTDOWN", description=str("Nuking commences in " + str(5 - count) + "..."), color=0xd11313)
            await ctx.send(embed = embed)
            await asyncio.sleep(1)

        embed = discord.Embed(title="GOODBYE", description=str("IT'S BEEN FUN"), color=0xd11313)
        await ctx.send(embed = embed)
        await channel.delete_messages(messages) # Deletes all messages in list

    @commands.command(pass_context = True) # Must do pass_context = True for code to work
    @commands.has_permissions(manage_guild=True)
    # Deletes EVERY SINGLE message in a channel one by one and sets the channel to read only while doing so
    async def halo(self, ctx):
        # ctx.guild.default_role gets the @everyone role that all members have by default
        '''
        await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=True, end_messages=False)

        await asyncio.sleep(3)
        await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=True, send_messages=False)
        '''
       # await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = True)




def setup(bot):
    bot.add_cog(NukeCog(bot))

