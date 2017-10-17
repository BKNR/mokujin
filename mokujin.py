#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix='.', description='This is a test bot by Baikonur')

#Get token from local txt file
token_file = open('token.txt', 'r')
token = token_file.read()
token_file.close()

@bot.event
@asyncio.coroutine 
def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
@asyncio.coroutine 
def test():
    embed = discord.Embed(title='Test title', description='A test embed thing.', colour=0x0000FF)
    embed.set_author(name='Test name', icon_url=bot.user.default_avatar_url)
    yield from bot.say(embed=embed, delete_after=60)
    	
bot.run(token)
