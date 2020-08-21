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
# QUOTEBOOK COMMANDS
#

class QuotebookCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addquote(self, ctx, member : discord.Member, *, message):
        member_id = member.id
        save_quote(member_id, message)

        member_as_mention = "<@" + str(member_id) + ">"
        embed = discord.Embed(title="Quote Added!", description="Okie, added to " + member_as_mention + f"'s quotebook: {message}", color=0xffbf00)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed = embed)

    @commands.command()
    async def quote(self, ctx, member: discord.Member):
        member_id = member.id

        embed = discord.Embed(title=get_random_quote(member_id), color=0xffbf00)
        await ctx.send(embed = embed)

    @commands.command()
    async def listquotes(self, ctx, member: discord.Member):
        member_id = member.id
        await ctx.send(embed = list_quotes(member_id, member.display_name))

    @commands.command()
    async def removequote(self, ctx, member: discord.Member, num):
        member_id = member.id

        embed = discord.Embed(title=remove_quote(member_id, num), color=0xffbf00)
        await ctx.send(embed = embed)

    @commands.command()
    async def editquote(self, ctx, member: discord.Member, num, *, new_quote):
        member_id = member.id

        embed = discord.Embed(title="Editing Quote...", description=edit_quote(member_id, num, new_quote), color=0xffbf00)
        await ctx.send(embed = embed)

def save_quote(member_id, quote):
    try:
        pickle_in = open("pickles/quotebook.pickle", "rb")

    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_out = open("pickles/quotebook.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("pickles/quotebook.pickle", "rb")
    dict = pickle.load(pickle_in)

    quote = datetime.datetime.now().strftime("%b %d, %Y @ %I:%M %p") + " - \"" + quote + "\"" # <-- typical freedom format
    member_string = str(member_id)
    if member_string not in dict:
        dict[member_string] = []
        dict[member_string].append(quote)
    elif member_string in dict:
        dict[member_string].append(quote)

    # Save to pickle
    pickle_out = open("pickles/quotebook.pickle", "wb")
    pickle.dump(dict, pickle_out)
    pickle_out.close()

def list_quotes(member_id, member_display_name):
    try:
        pickle_in = open("pickles/quotebook.pickle", "rb")

    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_out = open("pickles/quotebook.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("pickles/quotebook.pickle", "rb")
    dict = pickle.load(pickle_in)

    member_string = str(member_id)
    if member_string not in dict:
        all_quotes = "That user ain't got no quotes to quote bruh."
        quote_list = {}
    elif member_string in dict:
        quote_list = dict[member_string]

    all_quotes = ""
    place_count = 0
    # Loop through the user's quotes and print them out in one message
    for i in quote_list:
        place_count += 1
        place_count_str = str(place_count)
        all_quotes += place_count_str + ": " + i  + "\n"

    if place_count == 0:
        all_quotes = "That user ain't got no quotes to quote bruh."

    embed = discord.Embed(title=member_display_name + "\'s Quotes:", description=all_quotes, color=0xffbf00)

    return embed

def get_random_quote(member_id):
    try:
        pickle_in = open("pickles/quotebook.pickle", "rb")

    except FileNotFoundError:
        pickle_out = open("pickles/quotebook.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("pickles/quotebook.pickle", "rb")
    dict = pickle.load(pickle_in)

    member_string = str(member_id)
    if member_string not in dict:
        # Say that that user doesn't exist
        return("That user doesn't have any quotes, you absolute boomer.")
    elif member_string in dict:
        quote_list = dict[member_string]
        random_quote = random.choice(quote_list)
        return(random_quote)

def remove_quote(member_id, num):
    num = int(num)

    try:
        pickle_in = open("pickles/quotebook.pickle", "rb")

    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_out = open("pickles/quotebook.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("pickles/quotebook.pickle", "rb")
    dict = pickle.load(pickle_in)

    member_string = str(member_id)
    if member_string not in dict:
        # Say that that user doesn't exist
        return("That user doesn't have any quotes, you absolute boomer.")
    elif member_string in dict:
        quote_list = dict[member_string]
        if num <= len(quote_list):
            del dict[member_string][num-1]
        else:
            return("The index you gave does not exist. :(")

    # Save dic to pickle
    pickle_out = open("pickles/quotebook.pickle", "wb")
    pickle.dump(dict, pickle_out)
    pickle_out.close()

    return("Removed quote!")

def edit_quote(member_id, num, new_quote):
    num = int(num)

    try:
        pickle_in = open("pickles/quotebook.pickle", "rb")

    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_out = open("pickles/quotebook.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("pickles/quotebook.pickle", "rb")
    dict = pickle.load(pickle_in)

    member_string = str(member_id)
    if member_string not in dict:
        # Say that that user doesn't exist
        return("That user doesn't have any quotes, you absolute boomer.")
    elif member_string in dict:
        quote_list = dict[member_string]
        if num <= len(quote_list):
            dict[member_string][num-1] = new_quote
        else:
            return("The index you gave does not exist. :(")

    # Save dic to pickle
    pickle_out = open("pickles/quotebook.pickle", "wb")
    pickle.dump(dict, pickle_out)
    pickle_out.close()

    return("Edited quote!")
    
def setup(bot):
    bot.add_cog(QuotebookCog(bot))