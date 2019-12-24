#!/usr/bin/env python3
import os, sys
import datetime
import asyncio

import discord
from discord.ext import commands

import tkfinder
import config

prefix = '§'
description = 'The premier Tekken 7 Frame bot, made by Baikonur#4927'
bot = commands.Bot(command_prefix=prefix, description=description)

# Dict for searching special move types
move_types = {  'ra': 'Rage art',
                'rage_art': 'Rage art',
                'rd': 'Rage drive',
                'rage_drive': 'Rage drive',
                'wb': 'Wall bounce',
                'wall_bounce': 'Wall bounce',
                'ts': 'Tail spin',
                'tail_spin': 'Tail spin',
                'screw': 'Tail spin',
                'homing': 'Homing',
                'homari': 'Homing',
                'armor': 'Power crush',
                'armori': 'Power crush',
                'pc': 'Power crush',
                'power': 'Power crush',
                'power_crush': 'Power crush'}

# Get token from local txt file
dirname, pyfilename = os.path.split(os.path.abspath(sys.argv[0]))
tfilename = os.path.join(dirname, 'token.txt')

with open(tfilename) as token_file:
    token = token_file.read().strip()

def move_embed(character, move):
    '''Returns the embed message for character and move'''
    embed = discord.Embed(title=character['proper_name'],
            colour=0x00EAFF,
            url=character['online_webpage'],
            description='Move: ' + move['Command'])

    embed.set_thumbnail(url=character['portrait'])
    embed.add_field(name='Property', value=move['Hit level'])
    embed.add_field(name='Damage', value=move['Damage'])
    embed.add_field(name='Startup', value='i' + move['Start up frame'])
    embed.add_field(name='Block', value=move['Block frame'])
    embed.add_field(name='Hit', value=move['Hit frame'])
    embed.add_field(name='Counter Hit', value=move['Counter hit frame'])
    embed.add_field(name='Notes', value=move['Notes'])

    return embed

def move_list_embed(character, move_list, move_type):
    '''Returns the embed message for a list of moves matching to a special move type'''
    desc_string = ''
    for move in move_list:
        desc_string += move + '\n'

    embed = discord.Embed(title=character['proper_name'] + ' ' + move_type.lower() + ':',
            colour=0x00EAFF,
            description=desc_string)

    return embed

def error_embed(err):
    embed = discord.Embed(title='Error',
            colour=0xFF4500,
            description=err)

    return embed

@bot.event
async def on_ready():
    print(datetime.datetime.utcnow().isoformat())
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def test(ctx):
    print('Testing...')
    embed = discord.Embed(title='Test title', description='A test embed thing.', colour=0x0000FF)
    embed.set_author(name='Test name', icon_url=bot.user.default_avatar_url)
    await ctx.send(embed=embed, delete_after=60)

@bot.event
async def on_message(message):
    '''This has the main functionality of the bot. It has a lot of
    things that would be better suited elsewhere but I don't know
    if I'm going to change it.
    '''
    channel = message.channel
    if message.content.startswith('!') and ((isinstance(channel, discord.channel.DMChannel)) or (channel.name in config.CHANNELS)):

        user_message = message.content
        user_message = user_message.replace('!', '')
        user_message_list = user_message.split(' ', 1)

        if len(user_message_list) <= 1:
            # malformed command
            return

        chara_name = user_message_list[0].lower()
        chara_move = user_message_list[1]

        # iterate through character aliases in config for matching value
        chara_alias = list(filter(lambda x: (chara_name in x['alias']), config.CHARACTER_NAMES))
        if chara_alias:
            chara_name = chara_alias[0]['name']

        character = tkfinder.get_character(chara_name)
        if character is not None:
            if chara_move.lower() in move_types:
                chara_move = chara_move.lower()
                move_list = tkfinder.get_by_move_type(character, move_types[chara_move])
                if  len(move_list) < 1:
                    embed = error_embed('No ' + move_types[chara_move].lower() + ' for ' + character['proper_name'])
                    msg = await channel.send(embed=embed, delete_after=150)
                elif len(move_list) == 1:
                    move = tkfinder.get_move(character, move_list[0], False)
                    embed = move_embed(character, move)
                    msg = await channel.send(embed=embed, delete_after=300)
                elif len(move_list) > 1:
                    embed = move_list_embed(character, move_list, move_types[chara_move])
                    msg = await channel.send(embed=embed, delete_after=300)

            else:
                move = tkfinder.get_move(character, chara_move, True)

                #First checks the move as case sensitive, if it doesn't find it
                #it checks it case unsensitive

                if move is not None:
                    embed = move_embed(character, move)
                    msg = await channel.send(embed=embed, delete_after=300)
                else:
                    move = tkfinder.get_move(character, chara_move, False)
                    if move is not None:
                        embed = move_embed(character, move)
                        msg = await channel.send(embed=embed, delete_after=300)
                    else:
                        embed = error_embed('Move not found: ' + chara_move)
                        msg = await channel.send(embed=embed, delete_after=150)
        else:
            bot_msg = 'Character ' + chara_name + ' does not exist.'
            embed = error_embed(bot_msg)
            msg = await message.channel.send(embed=embed, delete_after=150)

            return
    await bot.process_commands(message)
bot.run(token)
