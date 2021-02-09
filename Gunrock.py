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

# initializes the prefixes dictionary
prefixes = {}

#loads the prefixes file
try:
    pickle_prefix_in = open("pickles/prefixes.pickle", "rb")
except FileNotFoundError:
    # If the code is being run for the first time and therefore a dictionary does not exist
    pickle_prefix_out = open("pickles/prefixes.pickle", "wb")
    pickle.dump(prefixes, pickle_prefix_out)
    pickle_prefix_out.close()

prefixes = pickle.load(pickle_prefix_in)

default_prefix = '.'

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
    'cogs.data',
    #'cogs.misc'
    'cogs.nuke'
]
client = commands.Bot(command_prefix = determine_prefix, description="Gunrock the Bot!")

if __name__ == '__main__':
    #adds the cogs as extensions
    for extension in initial_extensions:
        client.load_extension(extension)

# when the bot's ready
@client.event
async def on_ready():
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

# when a member joins
@client.event
async def on_member_join(member):
    #channel = discord.utils.get(member.guild.channels, name = "👋welcome")
    #role = get(member.guild.roles, name = "Aggie")
    #await member.add_roles(role)
    #await channel.send(f"Fellow Aggie {member.mention} has joined! Go pick a role in #roles and introduce yourself in #introductions! Please join us in the voice chats as well!")
    #print(f'Fellow Aggie {member} has joined!')

# when a member leaves
@client.event
async def on_member_remove(member):
    #print(f'{member} yeeted away from the server.')

#
# HELP COMMAND
#

client.remove_command('help')
@client.command()
async def help(ctx):
    guild = ctx.guild
    prefix = ""
    if guild:
        prefix = prefixes.get(guild.id, default_prefix)
    else:
        prefix = default_prefix

    instructions = ''
    #instructions += prefix + "add @user [number]: Adds [number] points to the mentioned user's swear jar. \n\n"
    #instructions += prefix + "remove @user [nummber]: Removes [number] points from the mentioned user's swear jar. \n\n"
    #instructions += prefix + "leaderboard: Shows the top 5 in the swear jar. \n\n"
    #instructions += prefix + "addquote @user [quote]: Add a quote to the mentioned user's quotebook. \n\n"
    #instructions += prefix + "quote @user: Outputs the random quote from the mentioned user's quotenook. \n\n"
    #instructions += prefix + "listquotes @user: Lists all of the mentioned user's quotes. \n\n"
    #instructions += prefix + "removequote @user [quote number]: Removes the designated quote from the mentioned user's quote book. \n\n"
    #instructions += prefix + "editquote @user [quote number] [new quote]: Overwrites the user's quote at [number] with [new quote]. \n\n"
    instructions += prefix + "course [course code]: Gives you the full course name and description. Make sure to put in zeros! For example, to get data about DRA 001, make sure those two 0's are there. Ex: " + prefix + "getcourse DRA 001 \n\n"
    instructions += prefix + "crn [course code]: Gives you the CRN data of a singular course. Make sure to put in zeros! For example, to get data about DRA 001, make sure those two 0's are there. Ex: " + prefix + "getcourse DRA 001 "

    embed = discord.Embed(title="Commands:", description=instructions, color=0xffbf00)

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

# cog reload command
@client.command(name="reloadcog", aliases=['cog', 'reload'])
@has_permissions(manage_guild=True)
async def cog_reload(ctx, *, cog: str):
    # Command which Reloads a Module.

    cog = "cogs." + cog

    try:
        client.unload_extension(cog)
        client.load_extension(cog)
    except Exception as e:
        await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
    else:
        await ctx.send('**`SUCCESS`**')

# cog load command
@client.command(name="loadcog", aliases=['load'])
@has_permissions(manage_guild=True)
async def cog_load(ctx, *, cog: str):
    # Command which loads a Module.

    cog = "cogs." + cog

    try:
        client.load_extension(cog)
    except Exception as e:
        await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
    else:
        await ctx.send('**`SUCCESS`**')

#client.run(sys.argv[1])

# For deployment using heroku
client.run(os.environ['bot_token'])