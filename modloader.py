import pickle
import discord
from discord.ext import commands

def modfile():
    try:
        pickle_modules_in = open("pickles/modules.pickle", "rb")
    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_modules_out = open("pickles/modules.pickle", "wb")
        pickle.dump({}, pickle_modules_out)
        pickle_modules_out.close()
        pickle_modules_in = open("pickles/modules.pickle", "rb")
    return pickle.load(pickle_modules_in)

def save_mods(modules):
    pickle_out = open("pickles/modules.pickle", "wb")
    pickle.dump(modules, pickle_out)
    pickle_out.close()

def modcheck(mod_name):
    async def predicate(ctx):
        if(not ctx.guild): return True
        pickle_in = open("pickles/modules.pickle", "rb")
        modules = pickle.load(pickle_in)
        pickle_in.close()
        if(ctx.guild.id in modules):
            if(mod_name in modules[ctx.guild.id]):
                if mod_name + "_whitelist" in modules[ctx.guild.id]:
                    if modules[ctx.guild.id][mod_name + "_whitelist"] == ctx.channel.id:
                        return modules[ctx.guild.id][mod_name]
                    else: return False
                else: return modules[ctx.guild.id]
            else: 
                if mod_name + "_whitelist" in modules[ctx.guild.id]:
                    if modules[ctx.guild.id][mod_name + "_whitelist"] == 0 or modules[ctx.guild.id][mod_name + "_whitelist"] == ctx.channel.id:
                        return True
                    else: return False
                else: return True
        else: return True
    return commands.check(predicate)

def is_enabled(mod_name, guild_id):
    pickle_in = open("pickles/modules.pickle", "rb")
    modules = pickle.load(pickle_in)
    pickle_in.close()
    if(guild_id in modules):
        if(mod_name in modules[guild_id]):
            return modules[guild_id][mod_name]
        else: return True
    else: return True