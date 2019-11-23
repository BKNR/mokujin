#!/usr/bin/env python3
import os, datetime, logging
import sys

# Insert you location of mokujin here
sys.path.insert(1, 'absolute/path/to/mokujin')

from discord.ext import commands
from src.resources import const, embed
from src import tkfinder

base_path = os.path.dirname(__file__)
prefix = '§'
description = 'The premier Tekken 7 Frame bot, made by Baikonur#4927, continued by Tib#1303'
bot = commands.Bot(command_prefix=prefix, description=description)

# Set logger to log errors
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

logfile_path = os.path.abspath(os.path.join(base_path, "..", "log", "logfile.log"))
# Create logfile if not exists
if not os.path.isfile(logfile_path):
    open(logfile_path, "w")
file_handler = logging.FileHandler(logfile_path)

formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Get token from local txt file
t_filename = os.path.abspath(os.path.join(base_path, "resources", "token.txt"))

with open(t_filename) as token_file:
    token = token_file.read().strip()


def add_feedback(sender_name: str, server_name: str, message: str):
    path = os.path.abspath(os.path.join(base_path, "..", "log", "feedback.csv"))
    # Create file if not exists
    if not os.path.isfile(path):
        open(path, "w")

    with open(path, "a") as feedback_file:
        result = "{};{};{};\n".format(sender_name, server_name, message)
        feedback_file.write(result)


@bot.event
async def on_ready():
    print(datetime.datetime.utcnow().isoformat())
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message(message):
    """This has the main functionality of the bot. It has a lot of
    things that would be better suited elsewhere but I don't know
    if I'm going to change it."""

    try:
        channel = message.channel

        if message.content == "?credit":
            await channel.send(embed=embed.thank_embed())
            return

        elif message.content == '?help':
            await channel.send(embed=embed.help_embed())
            return

        elif message.content == '!clear-messages':
            await channel.purge(limit=200, check=is_me)
            return

        elif message.content.startswith('?feedback'):
            user_message = message.content.split(' ', 1)[1]
            server_name = str(message.channel.guild)
            try:
                add_feedback(str(message.author), server_name, user_message)
                await channel.send(embed=embed.success_embed("Feedback sent"))
            except Exception as e:
                await channel.send(embed=embed.error_embed("Feedback couldn't be sent caused by: " + e))
            return

        elif message.content.startswith('!'):

            delete_after = 13
            if ('tekken' in channel.name) or ('frame' in channel.name):
                delete_after = None

            user_message = message.content
            command = user_message[1:]
            user_message_list = command.split(' ', 1)

            if len(user_message_list) <= 1:
                # malformed command
                return

            original_name = user_message_list[0].lower()
            original_move = user_message_list[1]

            character_name = tkfinder.correct_character_name(original_name)

            if character_name is not None:
                character = tkfinder.get_character_data(character_name)
                if original_name.lower() in const.MOVE_TYPES:

                    character_move = original_name.lower()
                    move_list = tkfinder.get_by_move_type(character, const.MOVE_TYPES[character_move])
                    if len(move_list) < 1:
                        result = embed.error_embed(
                            'No ' + const.MOVE_TYPES[character_move].lower() + ' for ' + character['proper_name'])
                        await channel.send(embed=result, delete_after=delete_after)
                    elif len(move_list) == 1:
                        character_move = tkfinder.get_move(character, move_list[0], False)
                        result = embed.move_embed(character, character_move)
                        await channel.send(embed=result, delete_after=delete_after)
                    elif len(move_list) > 1:
                        result = embed.move_list_embed(character, move_list, const.MOVE_TYPES[character_move])
                        await channel.send(embed=result, delete_after=delete_after)

                else:
                    character_move = tkfinder.get_move(character, original_move, True)

                    # First checks the move as case sensitive, if it doesn't find it
                    # it checks it case insensitive

                    if character_move is not None:
                        result = embed.move_embed(character, character_move)
                        await channel.send(embed=result, delete_after=delete_after)
                    else:
                        character_move = tkfinder.get_move(character, original_move, False)
                        if character_move is not None:
                            result = embed.move_embed(character, character_move)
                            await channel.send(embed=result, delete_after=delete_after)
                        else:
                            similar_moves = tkfinder.get_similar_moves(original_move, character_name)
                            result = embed.similar_moves_embed(similar_moves)
                            await channel.send(embed=result, delete_after=delete_after)
            else:
                bot_msg = f'Character {original_name} does not exist.'
                result = embed.error_embed(bot_msg)
                await message.channel.send(embed=result, delete_after=5)
                return
        await bot.process_commands(message)
    except Exception as e:
        print(e)
        logger.error(e)


def is_me(m):
    return m.author == bot.user


bot.run(token)
