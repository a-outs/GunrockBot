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
import os
import modloader

# initializes the prefixes and modules dictionaries
prefixes = {}
modules = {}

# admin whitelist
admins = [372696487290863618]

default_prefix = '!gunrock '

#a function to save new prefixes to the prefixes file
def prefix_saving():
    pickle_out = open("pickles/prefixes.pickle", "wb")
    pickle.dump(prefixes, pickle_out)
    pickle_out.close()

#the function to determine what the prefix is whenever a command is called
async def determine_prefix(bot, message):
    guild = message.guild
    if guild:
        return prefixes.get(guild.id, default_prefix)
    else:
        return default_prefix

initial_extensions = [
    #'cogs.reactroles',
    # 'cogs.swearjar',
    #'cogs.quotebook',
    'cogs.memes',
    'cogs.pings',
    'cogs.data'
    #'cogs.misc'
    #'cogs.nuke'
]

mod_list = [
    'memes',
    'data',
    'pings'
]

client = commands.Bot(command_prefix = determine_prefix, description="Gunrock the Bot!")

if __name__ == '__main__':
    #loads the prefixes file
    try:
        pickle_prefix_in = open("pickles/prefixes.pickle", "rb")
    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_prefix_out = open("pickles/prefixes.pickle", "wb")
        pickle.dump(prefixes, pickle_prefix_out)
        pickle_prefix_out.close()
    prefixes = pickle.load(pickle_prefix_in)

    #loads the modules file
    modules = modloader.modfile()

    #adds the cogs as extensions
    for extension in initial_extensions:
        client.load_extension(extension)

# when the bot's ready
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('!gunrock help'))
    print_onready_ascii_art()
    print('ready')

def print_onready_ascii_art():
    ascii_art = """ 
   ______                            __  
  / ____/_  ______  _________  _____/ /__
 / / __/ / / / __ \/ ___/ __ \/ ___/ //_/
/ /_/ / /_/ / / / / /  / /_/ / /__/ ,<   
\____/\__,_/_/ /_/_/   \____/\___/_/|_|  

    """
    print(ascii_art)

# on error
@client.event
async def on_command_error(ctx, error):
    embed = discord.Embed(title="Error!", description=str(error), color=0xd11313)
    await ctx.send(embed = embed)

#
# HELP COMMAND
#

client.remove_command('help')
@client.command()
async def help(ctx):
    # check if we're in a discord server, if we are then use its prefix, otherwise use default
    guild = ctx.guild
    prefix = ""
    if guild:
        prefix = prefixes.get(guild.id, default_prefix)
    else:
        prefix = default_prefix

    instructions = ''
    embed = discord.Embed(title="Commands:", description=instructions, color=0xffbf00)
    
    if(not guild or modloader.is_enabled('pings', ctx.guild.id)):
        tempvalue = ''
        tempvalue += prefix + "boomer @user\nCalls out a user for being a boomer\n\n"
        tempvalue += prefix + "dab @user\nDabs on dem haters\n\n"
        tempvalue += prefix + "cow @user\nTells you how much of a true Aggie they are\n\n"
        tempvalue += prefix + "bad @user\nCalls them out for being bad\n\n"
        tempvalue += prefix + "hydrate @user\nTells them to hydrate\n\n"
        tempvalue += prefix + "simp @user\nRates how much of a simp they are"
        embed.add_field(name="Pings:", value=tempvalue)

    if(not guild or modloader.is_enabled('data', ctx.guild.id)):
        tempvalue = ''
        tempvalue += prefix + "course [course code]\nGives you the full course name and description.\n\n"
        tempvalue += prefix + "crn [course code]\nGives you the CRN data of a course."
        embed.add_field(name="Course Data:", value=tempvalue)

    if(not guild or modloader.is_enabled('memes', ctx.guild.id)):
        tempvalue = ''
        tempvalue += prefix + "cheeto\nSends a random picture of cheeto"
        embed.add_field(name="Memes:", value=tempvalue)

    embed.add_field(name="Github",value="Check out our [github](https://github.com/a-outs/GunrockBot) for more info!")
    embed.set_footer(text="Contact timmie#6383 or Moragoh#7628 for help, questions, comments, or concerns.")

    await ctx.send(embed = embed)

# set prefix command
@client.command()
@has_permissions(manage_guild=True)
async def setprefix(ctx, arg):
    prefixes[ctx.guild.id] = arg
    prefix_saving()
    embed = discord.Embed(title="Prefix changed!", description="Prefix is now " + arg, color=0xffbf00)
    await ctx.send(embed = embed)

# change modules command
@client.command(name="enable module", aliases=['mod', 'module'])
@has_permissions(manage_roles=True)
async def module(ctx, arg):
    if(arg in mod_list):
        if(ctx.guild.id in modules):
            if(arg in modules[ctx.guild.id]):
                modules[ctx.guild.id][arg] = not modules[ctx.guild.id][arg]
            else: modules[ctx.guild.id][arg] = False
        else:
            modules[ctx.guild.id] = {}
            modules[ctx.guild.id][arg] = False
        embed = discord.Embed(title="Module changed!", description="Module " + arg + " is now " + str(modules[ctx.guild.id][arg]), color=0xffbf00)
    else:
        embed = discord.Embed(title="Invalid module", description=arg + " is not a valid module.", color=0xd11313)
    modloader.save_mods(modules)
    await ctx.send(embed = embed)

# modules channel whitelist command
@client.command(name="whitelist module", aliases=['modwhitelist'])
@has_permissions(manage_roles=True)
async def modwhitelist(ctx, *args):
    if(args[0] in mod_list):
        if(not ctx.guild.id in modules):
            modules[ctx.guild.id] = {}
        if(len(args) == 1):
            modules[ctx.guild.id][args[0] + "_whitelist"] = 0
            embed = discord.Embed(title="Module changed!", description="Commands for module " + args[0] + " are no longer restricted to any channel.", color=0xffbf00)
        else: 
            modules[ctx.guild.id][args[0] + "_whitelist"] = int(args[1])
            embed = discord.Embed(title="Module changed!", description="Commands for module " + args[0] + " are now restricted to channel with ID of  " + args[1], color=0xffbf00)
    else:
        embed = discord.Embed(title="Invalid module", description=arg + " is not a valid module.", color=0xd11313)
    modloader.save_mods(modules)
    await ctx.send(embed = embed)

# list modules command
@client.command(name="list modules", aliases=['listmods'])
@has_permissions(manage_roles=True)
async def list_modules(ctx):
    print(modules)
    mod_string = ''
    for mod in mod_list:
        mod_string += mod + " "
        if(ctx.guild.id in modules):
            if(mod in modules[ctx.guild.id]):
                mod_string += str(modules[ctx.guild.id][mod])
            else:
                mod_string += "True"
        else:
            mod_string += "True"
        mod_string += '\n'
    embed = discord.Embed(title="List of modules", description=mod_string, color=0xffbf00)
    await ctx.send(embed = embed)

# cog reload command
@client.command(name="reloadcog", aliases=['cog', 'reload'])
async def cog_reload(ctx, *, cog: str):
    if(ctx.author.id in admins):
        cog = "cogs." + cog

        try:
            client.unload_extension(cog)
            client.load_extension(cog)
        except Exception as e:
            if(type(e).__name__ == "ExtensionNotLoaded"):
                client.load_extension(cog)
                await ctx.send('**`SUCCESS`** The cog ' + cog + ' was unloaded, but I loaded it for you anyway!')
            else:
                await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`** Cog ' + cog + ' reloaded')
    else:
        await ctx.send("You don't have permissions for that!")

# cog load command
@client.command(name="loadcog", aliases=['load'])
async def cog_load(ctx, *, cog: str):
    if(ctx.author.id in admins):
        cog = "cogs." + cog

        try:
            client.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`** Cog ' + cog + ' loaded')
    else:
        await ctx.send("You don't have permissions for that!")

# cog unload command
@client.command(name="unloadcog", aliases=['unload'])
async def cog_unload(ctx, *, cog: str):
    if(ctx.author.id in admins):
        cog = "cogs." + cog

        try:
            client.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`** Cog ' + cog + ' unloaded')
    else:
        await ctx.send("You don't have permissions for that!")

client.run(open('tokens/discord.token', 'r').read())