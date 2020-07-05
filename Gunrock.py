import discord
from discord.ext import commands
from discord.ext.commands import Bot
import operator
import random
import pickle

client = commands.Bot(command_prefix = '-')

# Events
@client.event
async def on_ready():
    print('ready')

'''
@client.event
async def on_command_error(ctx, error):
    await ctx.send("Command error: do .manual to see the availible commands in their correct format")
'''


@client.event
async def on_member_join(member):
    print(f'Fellow Aggie {member} has joined!')

@client.event
async def on_member_remove(member):
    print(f'{member} yeeted away from the server.')

@client.command()
async def manual(ctx):
    instructions = " ```Here are the commands: \n\n"
    instructions += ".add @user (1 or 5 after @user): Adds 1 or 5 point to the mentioned user's swear jar. \n\n"
    instructions += ".remove @user (1 or 5 after @user): Adds 1 or 5 point to the mentioned user's swear jar. \n\n"
    instructions += ".leaderboard: Shows the top 5 in the swear jar. \n\n"
    instructions += ".addquote @user (type quote after @user): Add a quote to the mentioned user's quotebook. \n\n"
    instructions += ".quote @user: Outputs the random quote from the mentioned user's quotenook. \n\n"
    instructions += ".listquotes @user: Lists all of the mentioned user's quotes. \n\n"
    instructions += ".removequote @user (insert quote number here): Removes the designated quote from the mentioned user's quote book. ```"

    await ctx.send(instructions)


@client.command()
async def boomer(ctx, member : discord.Member):
    member_id = member.id
    member_id = str(member_id)
    member_as_mention = "<@" + member_id + ">"
    await ctx.send(member_as_mention + " okay boomer")


@client.command()
async def add(ctx, member : discord.Member, num):
    member_id = member.id
    num_int = int(num)

    # Save to pickle
    current_score = save_score(member_id, num_int)
    await ctx.send(f"Gotcha, added {num} points to {member}'s swear jar! Current score: " + str(current_score))

    #else:
    #    await ctx.send("Looks like you set the number value to be something other than 1 or 5. Why, did someone say something egregiously bad?")

@client.command()
async def remove(ctx, member : discord.Member, num):
    member_id = member.id
    num_int = int(num)

    # Save to pickle
    current_score = remove_score(member_id, num_int)
    await ctx.send(f"Gotcha, removed {num} points to {member}'s swear jar! Current score: " + str(current_score))

    #else:
    #    await ctx.send("Looks like you set the number value to be something other than 1 or 5.")

@client.command()
async def leaderboard(ctx):
    #bot_message = get_leaderboard()
    await ctx.send(get_leaderboard())

@client.command()
async def resetscore(ctx):
    if ctx.message.author.id == 140698580590657536:
        pickle_out = open("test.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()
        await ctx.send("Swear jar reset")
    else:
        await ctx.send("You don't have permission to do that, you absolute boomer.")


@client.command()
async def addquote(ctx, member : discord.Member, *, message):
    member_id = member.id
    save_quote(member_id, message)

    await ctx.send(f"Okie, added to {member}'s quotebook: {message}")

@client.command()
async def quote(ctx, member: discord.Member):
    member_id = member.id
    await ctx.send(get_random_quote(member_id))

@client.command()
async def listquotes(ctx, member: discord.Member):
    member_id = member.id
    #all_quotes =
    await ctx.send(list_quotes(member_id))

@client.command()
async def removequote(ctx, member: discord.Member, num):
    member_id = member.id
    await ctx.send(remove_quote(member_id, num))

def save_score(member_id, num):
    # On command
    try:
        pickle_in = open("test.pickle", "rb")

    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_out = open("test.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("test.pickle", "rb")
    dict = pickle.load(pickle_in)


    member_string = str(member_id)
    if member_string not in dict:
        dict[member_string] = num
    elif member_string in dict:
        dict[member_string] += num

    current_score = dict[member_string]

    # After editing dictionary, save it back into the pickle
    pickle_out = open("test.pickle", "wb")
    pickle.dump(dict, pickle_out)
    pickle_out.close()

    return(current_score)

def remove_score(member_id, num):
    # On command
    try:
        pickle_in = open("test.pickle", "rb")

    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_out = open("test.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("test.pickle", "rb")
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
    pickle_out = open("test.pickle", "wb")
    pickle.dump(dict, pickle_out)
    pickle_out.close()

    return(current_score)

def get_leaderboard():
    try:
        pickle_in = open("test.pickle", "rb")

    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_out = open("test.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("test.pickle", "rb")
    score_dict = pickle.load(pickle_in)

    # Sort the dictionary
    sorted_dict = dict(sorted(score_dict.items(), key=operator.itemgetter(1),reverse=True))

    bot_message = "Swear jar Leaderboards:\n"
    addon_message = ""
    place_count = 0;

    # Loop thorugh the list
    for i in sorted_dict:
        print(place_count)

        # Convert the user ID into a member object
        #user = client.fetch_user(i)
        print(user)


        place_count += 1;
        if (place_count <= 5):
            addon_message += str(place_count) + ": " + username_in_str + ' ' + str(sorted_dict[i]) + "\n"
            print(addon_message)
    addon_message = "```" + addon_message + "```"
    return(addon_message)

def save_quote(member_id, quote):
    try:
        pickle_in = open("test2.pickle", "rb")

    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_out = open("test2.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("test2.pickle", "rb")
    dict = pickle.load(pickle_in)

    member_string = str(member_id)
    if member_string not in dict:
        dict[member_string] = []
        dict[member_string].append(quote)
    elif member_string in dict:
        print(quote)
        dict[member_string].append(quote)

    # Save to pickle
    pickle_out = open("test2.pickle", "wb")
    pickle.dump(dict, pickle_out)
    print(dict)
    pickle_out.close()

def list_quotes(member_id):
    try:
        pickle_in = open("test2.pickle", "rb")

    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_out = open("test2.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("test2.pickle", "rb")
    dict = pickle.load(pickle_in)

    member_string = str(member_id)
    if member_string not in dict:
        return("That user ain't got no quotes to quote bruh.")
    elif member_string in dict:
        quote_list = dict[member_string]

    all_quotes = ''
    place_count = 0
    # Loop through the user's quotes and print them out in one message
    for i in quote_list:
        place_count += 1
        place_count_str = str(place_count)
        all_quotes += place_count_str + ": " +i  + "\n"
    return all_quotes

def get_random_quote(member_id):
    try:
        pickle_in = open("test2.pickle", "rb")

    except FileNotFoundError:
        pickle_out = open("test2.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("test2.pickle", "rb")
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
        pickle_in = open("test2.pickle", "rb")

    except FileNotFoundError:
        # If the code is being run for the first time and therefore a dictionary does not exist
        pickle_out = open("test2.pickle", "wb")
        empty_dict = {}
        pickle.dump(empty_dict, pickle_out)
        pickle_out.close()

    pickle_in = open("test2.pickle", "rb")
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
    pickle_out = open("test2.pickle", "wb")
    pickle.dump(dict, pickle_out)
    print(dict)
    pickle_out.close()

    return("Removed quote!")

<<<<<<< Updated upstream
client.run("")
=======
client.run("NzI4ODgyNTIwOTk2NzA4NDA0.XwFqHA.PO81aQVjhI53ommHhda38aOWzwo")
>>>>>>> Stashed changes
