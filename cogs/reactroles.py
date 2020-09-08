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
# REACTION ROLE COMMANDS AND FUNCTIONS
#

class ReactrolesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # command to set up the role message, emojis, and roles
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def rolemessagesetup(self, ctx, *, args=""):
        default_description = "This command sets up the message, emojis, and relevant roles for a reaction role message.\n"
        default_description += "Command usage: rolemessagesetup [index of reaction role message],[reaction role message content],[emojis in their respective order, seperated by %],[role names, seperated by %]"
        embed = discord.Embed(title="How to use this command:", description=default_description, color=0xffbf00)

        rolemessage = []

        if len(args) > 0:
            args_array = args.split(',')
            if len(args_array) == 4:
                if len(args_array[2].split('%')) == len(args_array[3].split('%')):
                    for arg in args_array:
                        rolemessage.append(arg.strip())
                    set_rolemessage(rolemessage, int(args_array[0]), ctx.message.guild.id)
                    await ctx.send(embed = discord.Embed(title="Success!", description="The reaction roles message has been successfully made", color=0x00c700))
        else:
            await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def rolesetup(self, ctx, index):
        rolemessage = get_rolemessage(ctx.message.guild.id, int(index))
        role_message = rolemessage[1]

        role_setup_message = await ctx.send(role_message)
        # Update the rolesetup message id
        change_rolesetup_id(role_setup_message.id, int(index), ctx.guild.id)

        for role_emoji in rolemessage[2].split('%'):
            await role_setup_message.add_reaction(emoji=role_emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id

        rolesetup_id = get_rolesetup_id(payload)
        # If the message reacted to is the reaction role message
        for rolesetup_ids in rolesetup_id:
            if message_id == rolesetup_id[rolesetup_ids]:
                guild_id = payload.guild_id
                # Search all guilds and to find one that matches
                guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)

                rolemessage = get_rolemessage(guild.id, rolesetup_ids)
        
                for i, emoji in enumerate(rolemessage[2].split('%')):
                    if payload.emoji.name == emoji:
                        role = discord.utils.get(guild.roles, name = rolemessage[3].split('%')[i])
                        if role is not None:
                            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                            if member is not None:
                                await member.add_roles(role)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message_id = payload.message_id

        rolesetup_id = get_rolesetup_id(payload)
        # If the message reacted to is the reaction role message
        for rolesetup_ids in rolesetup_id:
            if message_id == rolesetup_id[rolesetup_ids]:
                guild_id = payload.guild_id
                # Search all guilds and to find one that matches
                guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)

                rolemessage = get_rolemessage(guild.id, rolesetup_ids)
        
                for i, emoji in enumerate(rolemessage[2].split('%')):
                    if payload.emoji.name == emoji:
                        role = discord.utils.get(guild.roles, name = rolemessage[3].split('%')[i])
                        if role is not None:
                            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                            if member is not None:
                                await member.remove_roles(role)

# Function for changing the rolesetup message id to the newest one
def change_rolesetup_id(id, index, guild_id):
    try:
        pickle_in = open("pickles/rolesetup_id.pickle", "rb")

    except FileNotFoundError:
        #print("new pickle file")
        # If the code is being run for the first time 
        pickle_out = open("pickles/rolesetup_id.pickle", "wb")
        rolesetup_id = {}
        pickle.dump(rolesetup_id, pickle_out)
        pickle_out.close()

    pickle_in = open("pickles/rolesetup_id.pickle", "rb")
    rolesetup_id = pickle.load(pickle_in)
    try:
        rolesetup_id[guild_id][index] = id
    except KeyError:
        rolesetup_id[guild_id] = {}
        rolesetup_id[guild_id][index] = id
    
    pickle_in.close()

    pickle_out = open("pickles/rolesetup_id.pickle", "wb")
    pickle.dump(rolesetup_id, pickle_out)
    pickle_out.close()

def get_rolesetup_id(payload):
    try:
        pickle_in = open("pickles/rolesetup_id.pickle", "rb") 

    except FileNotFoundError:
        return ''

    pickle_in = open("pickles/rolesetup_id.pickle", "rb")
    rolesetup_id = pickle.load(pickle_in)
    pickle_in.close()

    return rolesetup_id[payload.guild_id]

def set_rolemessage(rolemessage, index, guild_id):
    try:
        pickle_in = open("pickles/rolemessages.pickle", "rb")

    except FileNotFoundError: 
        pickle_out = open("pickles/rolemessages.pickle", "wb")
        rolemessages = {}
        pickle.dump(rolemessages, pickle_out)
        pickle_out.close()

    pickle_in = open("pickles/rolemessages.pickle", "rb")
    rolemessages = pickle.load(pickle_in)
    try:
        rolemessages[guild_id][index] = rolemessage

    except KeyError:
        rolemessages[guild_id] = {}
        rolemessages[guild_id][index] = rolemessage

    pickle_in.close()

    pickle_out = open("pickles/rolemessages.pickle", "wb")
    pickle.dump(rolemessages, pickle_out)
    pickle_out.close()

def get_rolemessage(guild_id, index):
    try:
        pickle_in = open("pickles/rolemessages.pickle", "rb") 

    except FileNotFoundError:
        return ''

    pickle_in = open("pickles/rolemessages.pickle", "rb")
    rolemessages = pickle.load(pickle_in)
    rolemessage = rolemessages[guild_id][index]
    pickle_in.close()

    return rolemessage

def setup(bot):
    bot.add_cog(ReactrolesCog(bot))