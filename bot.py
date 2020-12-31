import discord
import asyncio
import random
import os
from discord.ext import commands

client = commands.Bot(command_prefix = "-- ")

@client.event
async def on_ready():
    print("Name Guessing Game online!")
    #ud = open("userdata.txt", "w+")
    await bot.change_presence(status = discord.Status.online, activity =discord.Game("Collecting user descriptions for you to guess!"), afk = False)    

@client.event
async def on_message(msg):
    await bot.process_commands(msg)

@client.command
async def describe(ctx):
    await ctx.author.send("Which user do you want to add a description to?")
    try:
        def check(message):
            return message.author == ctx.author
        msg = await client.wait_for("message", check = check, timeout = 30)
                
    except asyncio.TimeoutError as e:
            await ctx.send("You took too long to enter a username.")    

client.run("Bot Token")

