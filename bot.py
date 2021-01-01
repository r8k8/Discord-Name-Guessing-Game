import discord
import asyncio
import random
import os
#import csv
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
client = commands.Bot(command_prefix = "-- ", intents = intents)

userlist = [] 

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
#    with open("users.txt", "a") as users:
#        line_count = 0
#        user_writer = csv.writer(users, delimiter = "|")
#        user_writer.writerow(userlist)
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
async def describe(ctx):
    await ctx.author.send("Which user do you want to add a description to?")
    try:
        def check(message):
            return message.author == ctx.author
        msg = await client.wait_for("message", check = check, timeout = 30)
                
    except asyncio.TimeoutError as e:
            await ctx.author.send("You took too long to enter a username.")    

client.run("bot id")

