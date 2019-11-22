#!/usr/bin/env python3
import os
import datetime
import logging
from discord.ext import commands

from config import const
import tkfinder
import embed

basepath = os.path.dirname(__file__)
prefix = '§'
description = 'The premier Tekken 7 Frame bot, made by Baikonur#4927'
bot = commands.Bot(command_prefix=prefix, description=description)

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
file_handler = logging.FileHandler(os.path.abspath(os.path.join(basepath, "..", "config", "logfile.log")))
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Get token from local txt file
tfilename = os.path.abspath(os.path.join(basepath, "..", "config", "token.txt"))

with open(tfilename) as token_file:
    token = token_file.read().strip()


@bot.event
async def on_ready():
    print(datetime.datetime.utcnow().isoformat())
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message(message):
    '''This has the main functionality of the bot. It has a lot of
    things that would be better suited elsewhere but I don't know
    if I'm going to change it.
    '''

    try:
        channel = message.channel

        if message.content == '?help':
            msg = await channel.send(embed=embed.help_embed())

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
                        result = embed.error_embed(
                            'No ' + const.MOVE_TYPES[chara_move].lower() + ' for ' + character['proper_name'])
                        msg = await channel.send(embed=result, delete_after=delete_after)
                    elif len(move_list) == 1:
                        move = tkfinder.get_move(character, move_list[0], False)
                        result = embed.move_embed(character, move)
                        msg = await channel.send(embed=result, delete_after=delete_after)
                    elif len(move_list) > 1:
                        result = embed.move_list_embed(character, move_list, const.MOVE_TYPES[chara_move])
                        msg = await channel.send(embed=result, delete_after=delete_after)

                else:
                    move = tkfinder.get_move(character, chara_move, True)

                    # First checks the move as case sensitive, if it doesn't find it
                    # it checks it case unsensitive

                    if move is not None:
                        result = embed.move_embed(character, move)
                        msg = await channel.send(embed=result, delete_after=delete_after)
                    else:
                        move = tkfinder.get_move(character, chara_move, False)
                        if move is not None:
                            result = embed.move_embed(character, move)
                            msg = await channel.send(embed=result, delete_after=delete_after)
                        else:
                            similar_moves = tkfinder.get_similar_moves(chara_move, chara_name)
                            result = embed.similar_moves_embed(similar_moves)
                            msg = await channel.send(embed=result, delete_after=delete_after)
            else:
                bot_msg = 'Character ' + chara_name + ' does not exist.'
                result = embed.error_embed(bot_msg)
                msg = await message.channel.send(embed=result, delete_after=5)
                return
        await bot.process_commands(message)
    except Exception as e:
        print(e)
        logger.error(e)


def is_me(m):
    return m.author == bot.user


bot.run(token)
