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
import praw
from modloader import modcheck

#
# MEME COMMANDS
#

mod = 'memes'

class MemesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @modcheck(mod)
    async def cheeto(self, ctx):
        await ctx.send(grab_cheeto())

    @commands.command()
    @modcheck(mod)
    async def newcheetopics(self, ctx):
        if(ctx.message.author.id == 372696487290863618): new_cheeto_pics()

reddit = praw.Reddit(
    client_id=open("tokens/redditid.token", "r").read(),
    client_secret=open("tokens/redditsecret.token", "r").read(),
    user_agent="linux:gunrockbot:1.5.3 (by u/BlatternMann)"
)

# initializes cheeto pickle if it doesn't already exist
def init_cheeto(): 
    try:
        try:
            with open("pickles/cheeto.pickle","rb") as cheeto:
                pickle.load(cheeto)
        except EOFError as error:
            with open("pickles/cheeto.pickle","wb") as file:
                pickle.dump({}, file)
    except FileNotFoundError as error:
        with open("pickles/cheeto.pickle","wb") as file:
            pickle.dump({}, file)

def grab_cheeto():
    with open("pickles/cheeto.pickle","rb") as cheeto:
        cheeto_dict = pickle.load(cheeto)
        return random.choice(list(cheeto_dict.keys()))

def new_cheeto_pics():
    cheeto_dict = {}
    with open("pickles/cheeto.pickle","rb") as cheeto:
        cheeto_dict = pickle.load(cheeto)
    with open("pickles/cheeto.pickle","wb") as file:
        for submission in reddit.subreddit("UCDavis").top("all", limit=900):
            if(not submission.is_self and "cheeto" in submission.title.lower() and not "gallery" in submission.url):
                if(not submission.url in cheeto_dict):
                    cheeto_dict[submission.url] = submission.title
        pickle.dump(cheeto_dict, file)

def setup(bot):
    bot.add_cog(MemesCog(bot))
    init_cheeto()