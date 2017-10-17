#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import asyncio

prefix = '.'
description 'A Tekken 7 Frame bot in construction... Made by Baikonur'
bot = commands.Bot(command_prefix=prefix, description=description)

# Get token from local txt file
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

@bot.event
@asyncio.coroutine
def on_message(message):
    if message.content.startswith('!')
        user_message = message.content
        user_message = user_message.replace('!', '')
        user_message_list = user_message.split(' ', 1)

        if len(user_message_list) <= 1:
            # malformed command
            return

        user_chara_name = user_message_list[0].lower()
        user_chara_move = user_message_list[1]

        # TODO: VALIDATE CHARACTER NAME

        # if character_exists:
            # move_dict = get_move_details(user_chara_name, user_chara_move)
            # if validate move:
                # construct the message
                # send message
            # else move doesn't exist:
                # construct error msg
                # send error msg
            # return
        # else:
            # send char doesn't exist msg
            # return

bot.run(token)
