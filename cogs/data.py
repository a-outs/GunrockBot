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

class DataCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='course', aliases=['getcourse'])
    async def getcourse(self, ctx, course_prefix, course_suffix):
        await ctx.send(embed = get_course_data(course_prefix + " " + course_suffix))

    @commands.command(name='crn', aliases=['getCRNs', 'getcrns', 'crns', 'CRN', 'CRNs'])
    async def getCRNdata(self, ctx, course_prefix, course_suffix):
        await ctx.send(embed = get_CRN_data(course_prefix + " " + course_suffix, 202010))

def get_course_data(course_code):
    with open("data/20202021GenCat.txt", "r", encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = []
        for row in csv_reader:
            if(len(header) == 0):
                header = row
            if(row[0].find(course_code.upper()) == 0):
                embed = discord.Embed(title=course_code.upper() + " - " + row[1], description=row[14], color=0xffbf00)
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
                embed.set_footer(text="Run the command crn " + course_code.upper() + " to see data about this course's CRNs")
                return embed
        embed = discord.Embed(title="Course Not Found!", description="I couldn't find that course! In your requested course code, make sure to put in zeros! For example, to get data about DRA 001, make sure those two 0's are there.", color=0xd11313)
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
        embed.add_field(name="Error!", value="Class not found! Don't forget to include zero's if the course code has them.")
    else:
        for key, value in crn_data_dict.items():
            embed.add_field(name=key, value=value, inline=False)
        embed.set_footer(text="Run the command course " + course_code.upper() + " to see overall data about this course")
    return embed

def setup(bot):
    bot.add_cog(DataCog(bot))