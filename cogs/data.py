import discord
from discord.ext import menus
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot
from discord.ext.commands import has_permissions
from discord_webhook import DiscordWebhook
import operator
import random
import pickle
import datetime
import csv
import sys
import math
import re
import json
import requests
from modloader import modcheck

#
# DATA COMMANDS
#

mod = 'data'

current_term = 202110

class DataCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='course', aliases=['getcourse'])
    @modcheck(mod)
    async def getcourse(self, ctx, course_prefix, course_suffix):
        message = await ctx.send("Getting data, please wait...")
        embed = get_course_data(parse_course_code(course_prefix, course_suffix))
        await timeout_logic(embed, ctx, message)

    @commands.command(name='crn', aliases=['getCRNs', 'getcrns', 'crns', 'CRN', 'CRNs'])
    @modcheck(mod)
    async def crn(self, ctx, course_prefix, course_suffix):
        message = await ctx.send("Getting data, please wait...")
        embed = fetch_CRN_data(parse_course_code(course_prefix, course_suffix))
        await timeout_logic(embed, ctx, message)

    @commands.command(name='set timeout', aliases=['timeout'])
    @has_permissions(manage_guild=True)
    @modcheck(mod)
    async def set_timeout(self, ctx, timeout_length):
        if(timeout_length.isnumeric()):
            data_settings = get_settings()
            if(not ctx.guild.id in data_settings):
                data_settings[ctx.guild.id] = {}
            data_settings[ctx.guild.id]['timeout'] = timeout_length
            write_settings(data_settings)
            desc_string = "Data messages will now delete themselves after " + timeout_length + " seconds"
            if(int(timeout_length) == 0): desc_string = "Data messages will now never delete themselves"
            await ctx.send(embed = discord.Embed(title="Timeout set!", description=desc_string))
        else:
            await ctx.send(embed = discord.Embed(title="Invalid input!", description="The timeout length needs to be an integer..."))

# initializes data_settings pickle if it doesn't already exist
def init_settings(): 
    try:
        try:
            with open("pickles/data_settings.pickle","rb") as data_settings:
                pickle.load(data_settings)
        except EOFError as error:
            with open("pickles/data_settings.pickle","wb") as file:
                pickle.dump({}, file)
    except FileNotFoundError as error:
        with open("pickles/data_settings.pickle","wb") as file:
            pickle.dump({}, file)

# returns the entire data settings dictionary
def get_settings(): 
    with open("pickles/data_settings.pickle","rb") as data_settings:
        return pickle.load(data_settings)

# writes an entire dictionary to the data settings file
def write_settings(data_settings): 
    with open("pickles/data_settings.pickle","wb") as file:
        pickle.dump(data_settings, file)

# returns the timeout for a specified server
def get_timeout(guild_id): 
    with open("pickles/data_settings.pickle","rb") as file:
        data_settings = pickle.load(file)
        if(not guild_id in data_settings):
            return 0
        else:
            if(not 'timeout' in data_settings[guild_id]):
                return 0
            else:
                return data_settings[guild_id]['timeout']

def parse_course_code(course_prefix, course_suffix):
    return course_prefix + " " + course_suffix.zfill(len(course_suffix) + (3 - len(re.sub("\D", "", course_suffix))))

async def timeout_logic(embed, ctx, message):
    timeout = 0
    if(ctx.guild): timeout = int(get_timeout(ctx.guild.id))
    if(timeout > 0):
        embed.set_footer(text="This message will self-destruct in " + str(timeout) + " seconds.")
        await message.edit(content="", embed = embed, delete_after=timeout)
    else:
        await message.edit(content="", embed = embed)

def get_course_data(course_code):
    with open("data/20212022GenCat.txt", "r", encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = []
        for row in csv_reader:
            if(len(header) == 0):
                header = row
            if(row[0] == course_code.upper()):
                embed = discord.Embed(title=row[0] + " - " + row[1], description=row[14], color=0xffbf00)
                field_name = "Credits: " + row[2]
                field_data = ""
                for x in range(3, 14):
                    if x == 6:
                        field_data += "\n"
                    field_data += header[x]
                    if(len(row[x]) > 0):
                        field_data += " :white_check_mark: "
                    else:
                        field_data += " :x: "
                    field_data += " "
                    if x != 5:
                        if x != 13:
                            field_data += "| "
                embed.add_field(name=field_name, value=field_data, inline=True)
                embed.set_footer(text="Run the command crn " + row[0] + " to see data about this course's CRNs")
                return embed
        embed = discord.Embed(title="Course Not Found!", description="I couldn't find that course!", color=0xd11313)
        return embed

def get_CRN_data(course_code, term_code):
    description_string = ""
    classes_found = 0
    crn_data_dict = {}
    embed = discord.Embed(title="CRN Data for " + course_code.upper(), description=description_string, color=0xffbf00)
    with open("data/" + str(term_code) + " CRN Data.csv", "r", encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if(row[11].find(course_code.upper()) == 0):
                classes_found += 1
                value_string = ""
                for x in range(1, 10, 2):
                    if(row[x] != ""):
                        if(x == 1): value_string += "M: "
                        elif(x == 3): value_string += "T: "
                        elif(x == 5): value_string += "W: "
                        elif(x == 7): value_string += "R: "
                        elif(x == 9): value_string += "F: "
                        value_string += str(math.trunc(int(row[x])/60)) + ":" + str(int(row[x])%60).zfill(2) + " - " + str(math.trunc(int(row[x + 1])/60)) + ":" + str(int(row[x + 1])%60).zfill(2) + "\n"
                try:
                    crn_data_dict[row[0]] += value_string
                except KeyError:
                    crn_data_dict[row[0]] = value_string
    if classes_found == 0:
        embed.add_field(name="Error!", value="Class not found!")
    else:
        for key, value in crn_data_dict.items():
            embed.add_field(name=key, value=value, inline=False)
    return embed

def fetch_CRN_data(course_code):
    embed = discord.Embed(title="CRN Data for " + course_code.upper(), color=0xffbf00)
    discipline = course_code.upper().split(' ')[0]
    number = course_code.upper().split(' ')[1]
    hed = {'Authorization': 'Bearer ' + open("tokens/bearer.token", "r").read()}
    courseJson = requests.get("https://mydegree.ucdavis.edu/responsiveDashboard/api/course-link?discipline=" + discipline + "&number=" + number + "&", headers=hed).json()
    print(courseJson)
    if("error" in courseJson): #if the api request fails, fall back to the old function and send a ping to tim to fix
        DiscordWebhook(url='https://discord.com/api/webhooks/796594761742024705/3yLjjHvru14K-ughlwjAZhE5P5vPo_leDeKIvjN9PEybFrIuXb3Vrpxcvs2mdM_LvgDL', content='<@372696487290863618> The bearer token has expired, please fix!').execute()
        return get_CRN_data(course_code, current_term)

    if("error" in courseJson["courseInformation"]): #if the course isn't found
        embed.add_field(name="Error!", value="Class not found!")
        return embed

    for section in courseJson["courseInformation"]["courses"][0]["sections"]:
        value_string = "Term: " + section["termLiteral"]
        value_string += "\nSeats left: " + section["seatsAvailable"]
        for meeting in section["meetings"]:
            value_string += "\n" + meeting["monday"] + meeting["tuesday"] + meeting["wednesday"] + meeting["thursday"] + meeting["friday"] + " " + meeting["beginTime"] + "-" + meeting["endTime"]
        embed.add_field(name=section["courseReferenceNumber"], value=value_string, inline=False)

    return embed

def setup(bot):
    init_settings()
    bot.add_cog(DataCog(bot))