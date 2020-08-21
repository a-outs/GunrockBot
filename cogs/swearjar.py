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
# SWEARJAR
#

class SwearjarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def add(self, ctx, member : discord.Member, num):
        member_id = member.id
        num_int = int(num)

        # Save to pickle
        current_score = save_score(member_id, num_int, ctx.message.guild.id)

        member_as_mention = "<@" + str(member.id) + ">"
        embed = discord.Embed(title="Points Added!", description=f"Gotcha, added {num} points to " + member_as_mention + "'s swear jar! Current score: " + str(current_score), color=0xffbf00)
        await ctx.send(embed = embed)

    @commands.command()
    async def remove(self, ctx, member : discord.Member, num):
        member_id = member.id
        num_int = int(num)

        # Save to pickle
        current_score = save_score(member_id, -num_int, ctx.message.guild.id)

        member_as_mention = "<@" + str(member_id) + ">"
        embed = discord.Embed(title="Points Removed!", description=f"Gotcha, removed {num} points from " + member_as_mention + "'s swear jar! Current score: " + str(current_score), color=0xffbf00)
        await ctx.send(embed = embed)

    @commands.command()
    async def leaderboard(self, ctx):

        addon_message = ""
        place_count = 0

        sorted_dict = get_leaderboard(ctx.message.guild.id)
        # Loop thorugh the list
        for i in sorted_dict:
            # Convert the user ID into a username
            id_in_int = int(i)
            user = self.bot.get_user(id_in_int)
            username = user.name

            place_count += 1
            if (place_count <= 5):
                addon_message += str(place_count) + ": " + username + ' ' + str(sorted_dict[i]) + "\n"
        
        await ctx.send(embed = discord.Embed(title="Swear jar Leaderboard:", description=addon_message, color=0xffbf00))

    @commands.command()
    @has_permissions(administrator=True)
    async def resetscore(self, ctx):
        pickle_out = open("pickles/swearjar.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()
        embed = discord.Embed(title="Swearjar Reset!", description="The swear jar has been reset. Are you happy now?", color=0xffbf00)
        await ctx.send(embed = embed)

def save_score(member_id, num, guild_id):
    # On command
    try:
        pickle_in = open("pickles/swearjar.pickle", "rb")

    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_out = open("pickles/swearjar.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("pickles/swearjar.pickle", "rb")
    full_file = pickle.load(pickle_in)

    dict = {}

    try:
        dict = full_file[guild_id]
    except KeyError:
        full_file[guild_id] = dict

    dict = full_file[guild_id]

    member_string = str(member_id)
    if member_string not in dict:
        dict[member_string] = num
    elif member_string in dict:
        dict[member_string] += num
        if dict[member_string] < 0:
            dict[member_string] = 0

    current_score = dict[member_string]

    full_file[guild_id] = dict

    # After editing dictionary, save it back into the pickle
    pickle_out = open("pickles/swearjar.pickle", "wb")
    pickle.dump(full_file, pickle_out)
    pickle_out.close()

    return(current_score)

def get_leaderboard(guild_id):
    try:
        pickle_in = open("pickles/swearjar.pickle", "rb")

    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_out = open("pickles/swearjar.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("pickles/swearjar.pickle", "rb")

    full_file = pickle.load(pickle_in)

    print(full_file)

    empty_dict = {}
    try:
        empty_dict = full_file[guild_id]
    except KeyError:
        return empty_dict

    score_dict = full_file[guild_id]

    # Sort the dictionary
    sorted_dict = dict(sorted(score_dict.items(), key=operator.itemgetter(1),reverse=True))

    return sorted_dict

def setup(bot):
    bot.add_cog(SwearjarCog(bot))