import discord
from discord.ext import menus
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot
from discord.ext.commands import has_permissions
import operator
import random
import pickle
import datetime
import csv
import sys
import math

#
# DATA COMMANDS
#

class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def telltime(self, ctx):
        m = TimezoneTimes()
        await m.start(ctx)

class TimezoneTimes(menus.Menu):
    async def send_initial_message(self, ctx, channel):
        embed = discord.Embed(title="the time", description="1. Pacific Time\n2. Eastern Time\n3. Korean Time\n4. HK Time", color=0xffbf00)
        return await channel.send(embed = embed)

    @menus.button('1️⃣')
    async def on_one(self, payload):
        embed = discord.Embed(title="The Time on the West Coast", description=(datetime.datetime.utcnow() - datetime.timedelta(hours=7)).strftime("%b %d, %Y @ %I:%M %p"), color=0xffbf00)
        await self.message.edit(embed = embed)

    @menus.button('2️⃣')
    async def on_two(self, payload):
        embed = discord.Embed(title="The Time on the East Coast", description=(datetime.datetime.utcnow() - datetime.timedelta(hours=4)).strftime("%b %d, %Y @ %I:%M %p"), color=0xffbf00)
        await self.message.edit(embed = embed)

    @menus.button('3️⃣')
    async def on_three(self, payload):
        embed = discord.Embed(title="The Time on the Korean Coast", description=(datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%b %d, %Y @ %I:%M %p"), color=0xffbf00)
        await self.message.edit(embed = embed)

    @menus.button('4️⃣')
    async def on_four(self, payload):
        embed = discord.Embed(title="The Time on the HK Coast", description=(datetime.datetime.utcnow() + datetime.timedelta(hours=8)).strftime("%b %d, %Y @ %I:%M %p"), color=0xffbf00)
        await self.message.edit(embed = embed)

def setup(bot):
    bot.add_cog(MiscCog(bot))