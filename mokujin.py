#!/usr/bin/env python3
import asyncio

import discord
from discord.ext import commands

import tkfinder

prefix = '.'
description = 'A Tekken 7 Frame bot in construction... Made by Baikonur'
bot = commands.Bot(command_prefix=prefix, description=description)

# Get token from local txt file
with open('token.txt') as token_file:
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

def error_embed(err):
    embed = discord.Embed(title='Error',
            colour=0xFF4500,
            description=err)

    return embed

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
    print('Testing...')
    embed = discord.Embed(title='Test title', description='A test embed thing.', colour=0x0000FF)
    embed.set_author(name='Test name', icon_url=bot.user.default_avatar_url)
    yield from bot.say(embed=embed, delete_after=60)

@bot.event
@asyncio.coroutine
def on_message(message):
    '''This has the main functionality of the bot. It has a lot of
    things that would be better suited elsewhere but I don't know
    if I'm going to change it.
    '''
    if message.content.startswith('!') and message.channel.name == 'tekken':
        user_message = message.content
        user_message = user_message.replace('!', '')
        user_message_list = user_message.split(' ', 1)

        if len(user_message_list) <= 1:
            # malformed command
            return

        chara_name = user_message_list[0].lower()
        chara_move = user_message_list[1]
        if chara_name == 'dj' or chara_name == 'dvj' or chara_name == 'devil' or chara_name == 'deviljin':
            chara_name = 'devil_jin'
        elif chara_name == 'sergei':
            chara_name = 'dragunov'
        elif chara_name == 'jack':
            chara_name = 'jack7'
        elif chara_name == 'chloe' or chara_name == 'lc' or chara_name == 'lucky':
            chara_name = 'lucky_chloe'
        elif chara_name == "hei":
            chara_name = 'heihachi'
        elif chara_name == 'raven':
            chara_name = 'master_raven'
        elif chara_name == 'yoshi':
            chara_name = 'yoshimitsu'
        elif chara_name == 'ling':
           chara_name = 'xiaoyu'

        character = tkfinder.get_character(chara_name)
        if character is not None:
            #All the console prints should be removed from the "release" version
            bot_msg = 'Character ' + chara_name + ' exists!'
            print(bot_msg)
            move = tkfinder.get_move(character, chara_move, True)
            
            #First checks the move as case sensitive, if it doesn't find it
            #it checks it case unsensitive
            
            if move is not None:
                embed = move_embed(character, move) 
                
                msg = yield from bot.send_message(message.channel, embed=embed)
                yield from asyncio.sleep(300)
                yield from bot.delete_message(msg)
            else:
                move = tkfinder.get_move(character, chara_move, False)
                if move is not None:
                    embed = move_embed(character, move)
                    
                    msg = yield from bot.send_message(message.channel, embed=embed)
                    yield from asyncio.sleep(300)
                    yield from bot.delete_message(msg)
                else:
                    print('Move not found: ' + chara_move)
                    embed = error_embed('Move not found: ' + chara_move)
                    
                    msg = yield from bot.send_message(message.channel, embed=embed)
                    yield from asyncio.sleep(150)
                    yield from bot.delete_message(msg)
        else:
            bot_msg = 'Character ' + chara_name + ' does not exist.'
            print(bot_msg)
            if chara_name == 'geese':
                bot_msg = 'Sori nyt ei pysty.'
            embed = error_embed(bot_msg)
            
            msg = yield from bot.send_message(message.channel, embed=embed)
            yield from asyncio.sleep(150)
            yield from bot.delete_message(msg)

            return
    yield from bot.process_commands(message)
bot.run(token)
