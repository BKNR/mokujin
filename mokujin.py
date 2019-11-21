#!/usr/bin/env python3
import os, sys
import datetime
import logging
import discord
from discord.ext import commands

from config import const
import tkfinder

prefix = '§'
description = 'The premier Tekken 7 Frame bot, made by Baikonur#4927'
bot = commands.Bot(command_prefix=prefix, description=description)

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
file_handler = logging.FileHandler('config/logfile.log')

formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Get token from local txt file
dirname, pyfilename = os.path.split(os.path.abspath(sys.argv[0]))
tfilename = os.path.join(dirname + "/config/", 'token.txt')

with open(tfilename) as token_file:
    token = token_file.read().strip()


def move_embed(character, move):
    '''Returns the embed message for character and move'''
    embed = discord.Embed(title=character['proper_name'],
                          colour=0x00EAFF,
                          url=character['online_webpage'],
                          description='**Move: ' + move['Command'] + '**')

    embed.set_thumbnail(url=character['portrait'])
    embed.add_field(name='Property', value=move['Hit level'])
    embed.add_field(name='Damage', value=move['Damage'])
    embed.add_field(name='Startup', value='i' + move['Start up frame'])
    embed.add_field(name='Block', value=move['Block frame'])
    embed.add_field(name='Hit', value=move['Hit frame'])
    embed.add_field(name='Counter Hit', value=move['Counter hit frame'])
    embed.add_field(name='Notes', value=(move['Notes'] if move['Notes'] else "-"))
    if move['Gif']:
        embed.add_field(name='Gif', value=move['Gif'], inline=False)

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


def similar_moves_embed(similar_moves):
    embed = discord.Embed(title='Move not found', colour=0xfcba03,
                          description='Similar moves:\n**{}**'
                          .format('** **\n'.join(similar_moves)))
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

    try:
        channel = message.channel

        if message.content == '?help':
            msg = await channel.send(embed=help_embed())

        if message.content == '!delete-data':
            deleted = await channel.purge(limit=200, check=is_me)
            return

        if message.content.startswith('!'):

            delete_after = 13
            if ('tekken' in channel.name) or ('frame' in channel.name):
                delete_after = None

            user_message = message.content
            user_message = user_message.replace('!', '')
            user_message_list = user_message.split(' ', 1)

            if len(user_message_list) <= 1:
                # malformed command
                return

            chara_name = user_message_list[0].lower()
            chara_move = user_message_list[1]

            chara_name = tkfinder.correct_character_name(chara_name)
            character = tkfinder.get_character_data(chara_name)
            if character is not None:
                if chara_move.lower() in const.MOVE_TYPES:
                    chara_move = chara_move.lower()
                    move_list = tkfinder.get_by_move_type(character, const.MOVE_TYPES[chara_move])
                    if len(move_list) < 1:
                        embed = error_embed(
                            'No ' + const.MOVE_TYPES[chara_move].lower() + ' for ' + character['proper_name'])
                        msg = await channel.send(embed=embed, delete_after=delete_after)
                    elif len(move_list) == 1:
                        move = tkfinder.get_move(character, move_list[0], False)
                        embed = move_embed(character, move)
                        msg = await channel.send(embed=embed, delete_after=delete_after)
                    elif len(move_list) > 1:
                        embed = move_list_embed(character, move_list, const.MOVE_TYPES[chara_move])
                        msg = await channel.send(embed=embed, delete_after=delete_after)

                else:
                    move = tkfinder.get_move(character, chara_move, True)

                    # First checks the move as case sensitive, if it doesn't find it
                    # it checks it case unsensitive

                    if move is not None:
                        embed = move_embed(character, move)
                        msg = await channel.send(embed=embed, delete_after=delete_after)
                    else:
                        move = tkfinder.get_move(character, chara_move, False)
                        if move is not None:
                            embed = move_embed(character, move)
                            msg = await channel.send(embed=embed, delete_after=delete_after)
                        else:
                            similar_moves = tkfinder.get_similar_moves(chara_move, chara_name)
                            embed = similar_moves_embed(similar_moves)
                            msg = await channel.send(embed=embed, delete_after=delete_after)
            else:
                bot_msg = 'Character ' + chara_name + ' does not exist.'
                embed = error_embed(bot_msg)
                msg = await message.channel.send(embed=embed, delete_after=5)
                return
        await bot.process_commands(message)
    except Exception as e:
        print(e)
        logger.error(e)


def help_embed():
    text = "```" \
           "!character move -   get frame data of a move from a character \n" \
           "!delete-data -      deletes bot's last own messages\n" \
           "\n" \
           "The bot automatically deletes it's own messages after 10 seconds except in channel with the 'tekken' or 'frame' in it```\n\n" \
           "Much thanks and love to T7Chicken Team, Ruxx, BKNR, Dramen, Dreamotion, Jacket, Cangu and Vesper. \n\n" \
           "This project won't be possible without you guys <3"
    embed = discord.Embed(title='Commands', description=text, colour=0x37ba25)
    embed.set_author(name='Author: Tib')

    return embed


def is_me(m):
    return m.author == bot.user


bot.run(token)
