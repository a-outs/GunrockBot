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
        async for message in channel.history(limit = 5):
            messages.append(message)

        # Doomsday countdown message
        for count in range(0,6):
            embed = discord.Embed(title="DOOMSDAY COUNTDOWN", description=str("Nuking commences in " + str(5 - count) + "..."), color=0xd11313)
            await ctx.send(embed = embed)
            await asyncio.sleep(1)

        embed = discord.Embed(title="GOODBYE", description=str("IT'S BEEN FUN"), color=0xd11313)
        await ctx.send(embed = embed)
        await channel.delete_messages(messages) # Deletes all messages in list

def setup(bot):
    bot.add_cog(NukeCog(bot))

