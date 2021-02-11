import discord
import asyncio
import random
import os
import csv
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
client = commands.Bot(command_prefix = "-- ", intents = intents)

userlist = [] 
folder = "users/"
@client.event
async def on_ready():
    print("Name Guessing Game online!")
    
    guild = client.get_guild(793496567733682216)
    print(guild)
    idlist = guild.members       
    for member in idlist:
        if member.bot == False:
            r = member.name
            userlist.append(r)
    print(userlist) #List with User ID's of Guild Members     
    await client.change_presence(status = discord.Status.online, activity =discord.Game("Collecting user descriptions for you to guess!"), afk = False)    
    
@client.command()
@commands.has_permissions(administrator = True)
async def refresh_userlist(ctx):
    for name in userlist:
        usertxtfilename = folder + name + ".txt"
        with open(usertxtfilename, "a") as user:            
            user_writer = csv.writer(user, delimiter = "\n")
            line_count = 0 #useless code
            #user_writer.writerow(userlist)
    await ctx.send("Operation completed.")
    
@client.event
async def on_message(msg):
    await client.process_commands(msg)

@client.command()
async def test1(ctx, user):
    u = str(user)
    m = str(member)
    if u == m:
        print("b")

@client.command()
async def guess(ctx):
    randomuser = random.choice(userlist)
    usertxtfilename =folder + randomuser + ".txt"
    descriptions = []
    with open(usertxtfilename, "r") as user:
        for desc in user:
            descriptions.append(desc)
    chosendesc = random.choice(descriptions)
    await ctx.send("**Match this description to a user in this guild within the next 30 seconds:**\n" + chosendesc)
    try:
        def check(message):
            return message.author == ctx.author
        msg = await client.wait_for("message", check = check, timeout = 30)
        if msg.content.startswith(randomuser):
            await ctx.send("Correct!")
        else:
            await ctx.send("Incorrect.")        
    except asyncio.TimeoutError as e:
        await ctx.send("Time ran out. Game over!")
    

@client.command()
async def describe(ctx):
    name_entered = False
    given_name = ""
    await ctx.author.send("Which user do you want to add a description to? Make sure you spell the name of the user correctly.")
    try:
        def check(message):
            return message.author == ctx.author
        msg = await client.wait_for("message", check = check, timeout = 30)
        for name in userlist:
            if msg.content.startswith(name):
                name_entered = True
                given_name = name
                break                    
    except asyncio.TimeoutError as e:
            await ctx.author.send("You took too long to enter a username.")
    if name_entered:
        usertxtfilename = folder + given_name + ".txt"
        try:
            await ctx.author.send(f"Enter a description for {given_name}. Note that when no input is given within the next 3 minutes the process will be aborted. \n Alternatively, you can abort the process by entering: **!exit**")
            def check(message):
                return message.author == ctx.author
            desc = await client.wait_for("message", check = check, timeout = 180)
            if desc.content.startswith("!exit"):
                await ctx.author.send("Cancelled adding description.")
            else:
                with open(usertxtfilename, "a") as user:            
                    #user_writer = csv.writer(user, delimiter = "|")
                    #user_writer.writerow(desc.content)
                    user.write(f"{desc.content} \n")
                await ctx.author.send("Description successfully added.")
        except asyncio.TimeoutError as e:
            await ctx.author.send("Timed out.")

client.run("bot id")

