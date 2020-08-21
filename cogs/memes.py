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
# MEME COMMANDS
#

class MemesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def boomer(self, ctx, member : discord.Member):
        member_id = member.id
        member_id = str(member_id)
        member_as_mention = "<@" + member_id + ">"
        await ctx.send(member_as_mention + " okay boomer")

    @commands.command()
    async def dab(self, ctx, member : discord.Member):
        member_id = member.id
        member_id = str(member_id)
        member_as_mention = "<@" + member_id + ">"
        await ctx.send(member_as_mention + " get dabbed on! <O/")

    @commands.command()
    async def cow(self, ctx, member : discord.Member):
        member_id = member.id
        member_id = str(member_id)
        member_as_mention = "<@" + member_id + ">"
        embed = discord.Embed(title="cow r8 machine", description=member_as_mention + " is " + str(random.randint(0,100)) + "% cow", color=0xffbf00)
        await ctx.send(embed = embed)

    @commands.command()
    async def bad(self, ctx, member : discord.Member):
        member_id = member.id
        member_id = str(member_id)
        member_as_mention = "<@" + member_id + ">"
        embed = discord.Embed(title="you're bad!", description="sorry " + member_as_mention + ", but you're bad", color=0xffbf00)
        await ctx.send(embed = embed)

    @commands.command()
    async def simp(self, ctx, member : discord.Member):
        member_id = member.id
        member_id = str(member_id)
        member_as_mention = "<@" + member_id + ">"
        embed = discord.Embed(title="simp r8 machine", description=member_as_mention + " is 100% simp", color=0xffbf00)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(MemesCog(bot))