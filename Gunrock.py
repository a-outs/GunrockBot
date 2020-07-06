import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import has_permissions
import operator
import random
import pickle
import datetime
import csv
import sys

# initializes the prefixes dictionary
prefixes = {}

#loads the prefixes file
try:
    pickle_prefix_in = open("prefixes.pickle", "rb")
except FileNotFoundError:
    # If the code is being run for the first time and therefore a dictionary does not exist
    pickle_prefix_out = open("prefixes.pickle", "wb")
    pickle.dump(prefixes, pickle_prefix_out)
    pickle_prefix_out.close()

prefixes = pickle.load(pickle_prefix_in)

default_prefix = '.'

#a function to save new prefixes to the prefixes file
def prefix_saving():
    pickle_out = open("prefixes.pickle", "wb")
    pickle.dump(prefixes, pickle_out)
    pickle_out.close()

#the function to determine what the prefix is whenever a command is called
async def determine_prefix(bot, message):
    guild = message.guild

    if guild:
        return prefixes.get(guild.id, default_prefix)
    else:
        return default_prefix

client = commands.Bot(command_prefix = determine_prefix)

# Events
@client.event
async def on_ready():
    print('ready')

@client.event
async def on_command_error(ctx, error):
    await ctx.send(error)

@client.event
async def on_member_join(member):
    print(f'Fellow Aggie {member} has joined!')

@client.event
async def on_member_remove(member):
    print(f'{member} yeeted away from the server.')

client.remove_command('help')
@client.command()
async def help(ctx):
    guild = ctx.guild
    prefix = ""
    if guild:
        prefix = prefixes.get(guild.id, default_prefix)
    else:
        prefix = default_prefix
    instructions = " ```Here are the commands: \n\n"
    instructions += prefix + "add @user (1 or 5 after @user): Adds 1 or 5 point to the mentioned user's swear jar. \n\n"
    instructions += prefix + "remove @user (1 or 5 after @user): Adds 1 or 5 point to the mentioned user's swear jar. \n\n"
    instructions += prefix + "leaderboard: Shows the top 5 in the swear jar. \n\n"
    instructions += prefix + "addquote @user (type quote after @user): Add a quote to the mentioned user's quotebook. \n\n"
    instructions += prefix + "quote @user: Outputs the random quote from the mentioned user's quotenook. \n\n"
    instructions += prefix + "listquotes @user: Lists all of the mentioned user's quotes. \n\n"
    instructions += prefix + "removequote @user (insert quote number here): Removes the designated quote from the mentioned user's quote book. \n\n"
    instructions += prefix + "getcourse [course code]: Gives you the full course name and description. Ex. " + prefix + "getcourse MAT 021A```"

    await ctx.send(instructions)

@client.command()
@has_permissions(manage_guild=True)
async def setprefix(ctx, arg):
    prefixes[ctx.guild.id] = arg
    prefix_saving()
    await ctx.send("Prefix changed to " + arg)

@client.command()
async def boomer(ctx, member : discord.Member):
    member_id = member.id
    member_id = str(member_id)
    member_as_mention = "<@" + member_id + ">"
    await ctx.send(member_as_mention + " okay boomer")

@client.command()
async def dab(ctx, member : discord.Member):
    member_id = member.id
    member_id = str(member_id)
    member_as_mention = "<@" + member_id + ">"
    await ctx.send(member_as_mention + " get dabbed on! <O/")

@client.command()
async def telltime(ctx):
    await ctx.send(datetime.datetime.now().strftime("%b %d, %Y @ %I:%M %p"))

@client.command()
async def add(ctx, member : discord.Member, num):
    member_id = member.id
    username = member.display_name
    num_int = int(num)

    # Save to pickle
    current_score = save_score(member_id, num_int)
    await ctx.send(f"Gotcha, added {num} points to " + username + "'s swear jar! Current score: " + str(current_score))

    #else:
    #    await ctx.send("Looks like you set the number value to be something other than 1 or 5. Why, did someone say something egregiously bad?")

@client.command()
async def remove(ctx, member : discord.Member, num):
    member_id = member.id
    username = member.display_name
    num_int = int(num)

    # Save to pickle
    current_score = remove_score(member_id, num_int)
    await ctx.send(f"Gotcha, removed {num} points from " + username + "'s swear jar! Current score: " + str(current_score))

    #else:
    #    await ctx.send("Looks like you set the number value to be something other than 1 or 5.")

@client.command()
async def leaderboard(ctx):
    #bot_message = get_leaderboard()
    await ctx.send(get_leaderboard())

@client.command()
async def resetscore(ctx):
    if ctx.message.author.id == 140698580590657536:
        pickle_out = open("swearjar.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()
        await ctx.send("Swear jar reset")
    else:
        await ctx.send("You don't have permission to do that, you absolute boomer.")


@client.command()
async def addquote(ctx, member : discord.Member, *, message):
    member_id = member.id
    username = member.display_name
    save_quote(member_id, message)

    await ctx.send("Okie, added to " + username + f"'s quotebook: {message}")

@client.command()
async def quote(ctx, member: discord.Member):
    member_id = member.id
    await ctx.send(get_random_quote(member_id))

@client.command()
async def listquotes(ctx, member: discord.Member):
    member_id = member.id
    #all_quotes =
    await ctx.send(list_quotes(member_id, member.display_name))

@client.command()
async def removequote(ctx, member: discord.Member, num):
    member_id = member.id
    await ctx.send(remove_quote(member_id, num))

@client.command()
async def getcourse(ctx, course_prefix, course_suffix):
    await ctx.send(get_course_data(course_prefix + " " + course_suffix))

def save_score(member_id, num):
    # On command
    try:
        pickle_in = open("swearjar.pickle", "rb")

    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_out = open("swearjar.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("swearjar.pickle", "rb")
    dict = pickle.load(pickle_in)


    member_string = str(member_id)
    if member_string not in dict:
        dict[member_string] = num
    elif member_string in dict:
        dict[member_string] += num

    current_score = dict[member_string]

    # After editing dictionary, save it back into the pickle
    pickle_out = open("swearjar.pickle", "wb")
    pickle.dump(dict, pickle_out)
    pickle_out.close()

    return(current_score)

def remove_score(member_id, num):
    # On command
    try:
        pickle_in = open("swearjar.pickle", "rb")

    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_out = open("swearjar.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("swearjar.pickle", "rb")
    dict = pickle.load(pickle_in)


    member_string = str(member_id)
    if member_string not in dict:
        dict[member_string] = num
    elif member_string in dict:
        dict[member_string] -= num

        if dict[member_string] < 0:
            dict[member_string] = 0
    current_score = dict[member_string]

    # After editing dictionary, save it back into the pickle
    pickle_out = open("swearjar.pickle", "wb")
    pickle.dump(dict, pickle_out)
    pickle_out.close()

    return(current_score)

def get_leaderboard():
    try:
        pickle_in = open("swearjar.pickle", "rb")

    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_out = open("swearjar.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("swearjar.pickle", "rb")
    score_dict = pickle.load(pickle_in)

    # Sort the dictionary
    sorted_dict = dict(sorted(score_dict.items(), key=operator.itemgetter(1),reverse=True))

    bot_message = "Swear jar Leaderboards:\n"
    addon_message = ""
    place_count = 0;

    # Loop thorugh the list
    for i in sorted_dict:
        # Convert the user ID into a username
        id_in_int = int(i)
        user = client.get_user(id_in_int)
        username = user.name

        place_count += 1;
        if (place_count <= 5):
            addon_message += str(place_count) + ": " + username + ' ' + str(sorted_dict[i]) + "\n"
            #print(addon_message)
    addon_message = "```" + addon_message + "```"
    return(addon_message)

def save_quote(member_id, quote):
    try:
        pickle_in = open("quotebook.pickle", "rb")

    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_out = open("quotebook.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("quotebook.pickle", "rb")
    dict = pickle.load(pickle_in)

    quote = datetime.datetime.now().strftime("%b %d, %Y @ %I:%M %p") + " - \"" + quote + "\"" # <-- typical freedom format
    member_string = str(member_id)
    if member_string not in dict:
        dict[member_string] = []
        dict[member_string].append(quote)
    elif member_string in dict:
        #print(quote)
        dict[member_string].append(quote)

    # Save to pickle
    pickle_out = open("quotebook.pickle", "wb")
    pickle.dump(dict, pickle_out)
    #print(dict)
    pickle_out.close()

def list_quotes(member_id, member_display_name):
    try:
        pickle_in = open("quotebook.pickle", "rb")

    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_out = open("quotebook.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("quotebook.pickle", "rb")
    dict = pickle.load(pickle_in)

    member_string = str(member_id)
    if member_string not in dict:
        return("That user ain't got no quotes to quote bruh.")
    elif member_string in dict:
        quote_list = dict[member_string]

    all_quotes = member_display_name + "\'s Quotes:\n"
    place_count = 0
    # Loop through the user's quotes and print them out in one message
    for i in quote_list:
        place_count += 1
        place_count_str = str(place_count)
        all_quotes += place_count_str + ": " + i  + "\n"
    return all_quotes

def get_random_quote(member_id):
    try:
        pickle_in = open("quotebook.pickle", "rb")

    except FileNotFoundError:
        pickle_out = open("quotebook.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("quotebook.pickle", "rb")
    dict = pickle.load(pickle_in)


    member_string = str(member_id)
    if member_string not in dict:
        # Say that that user doesn't exist
        return("That user doesn't have any quotes, you absolute boomer.")
    elif member_string in dict:
        quote_list = dict[member_string]
        random_quote = random.choice(quote_list)
        return('"' + random_quote + '"')

def remove_quote(member_id, num):
    num = int(num)

    try:
        pickle_in = open("quotebook.pickle", "rb")

    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_out = open("quotebook.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("quotebook.pickle", "rb")
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
    pickle_out = open("quotebook.pickle", "wb")
    pickle.dump(dict, pickle_out)
    #print(dict)
    pickle_out.close()

    return("Removed quote!")

def get_course_data(course_code):
    with open("20202021GenCat.txt", "r", encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = []
        for row in csv_reader:
            if(len(header) == 0):
                header = row
            if(row[0].find(course_code) == 0):
                output_string = "Here's your data!\n~~       ~~\n"
                output_string += "**" + course_code + " - " + row[1] + "**\n > " + row[14] + "\n\n"
                output_string += "Credits: " + row[2] + "\n"
                for x in range(3, 14):
                    if x == 6:
                        output_string += "\n"
                    output_string += header[x]
                    if(len(row[x]) > 0):
                        output_string += " :white_check_mark: "
                    else:
                        output_string += " :x: "
                    output_string += " "
                    if x != 5:
                        if x != 13:
                            output_string += "| "
                return output_string + "\n~~       ~~"

client.run(sys.argv[1])
