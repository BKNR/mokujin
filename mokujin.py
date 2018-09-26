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
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def test():
    print('Testing...')
    embed = discord.Embed(title='Test title', description='A test embed thing.', colour=0x0000FF)
    embed.set_author(name='Test name', icon_url=bot.user.default_avatar_url)
    await bot.say(embed=embed, delete_after=60)

@bot.event
async def on_message(message):
    '''This has the main functionality of the bot. It has a lot of
    things that would be better suited elsewhere but I don't know
    if I'm going to change it.
    '''
    if message.content.startswith('!') and (message.channel.name == 'tekken' or message.channel.name == 'raamikysely'):
        user_message = message.content
        user_message = user_message.replace('!', '')
        user_message_list = user_message.split(' ', 1)

        if len(user_message_list) <= 1:
            # malformed command
            return

        chara_name = user_message_list[0].lower()
        chara_move = user_message_list[1]
        if chara_name == 'dj' or chara_name == 'dvj' or chara_name == 'djin' or chara_name == 'devil' or chara_name == 'deviljin' or chara_name == 'diablojim':
            chara_name = 'devil_jin'
        elif chara_name == 'sergei' or chara_name == 'drag':
            chara_name = 'dragunov'
        elif chara_name == 'goose':
            chara_name = 'geese'
        elif chara_name == 'hwo' or chara_name == 'hwoa':
            chara_name = 'hwoarang'
        elif chara_name == 'jack':
            chara_name = 'jack7'
        elif chara_name == 'chloe' or chara_name == 'lc' or chara_name == 'lucky':
            chara_name = 'lucky_chloe'
        elif chara_name == 'hei' or chara_name == 'hessu' or chara_name == 'heiska':
            chara_name = 'heihachi'
        elif chara_name == 'kata':
            chara_name = 'katarina'
        elif chara_name == 'kaz':
            chara_name = 'kazuya'
        elif chara_name == 'raven' or chara_name == 'mraven' or chara_name == 'masterraven':
            chara_name = 'master_raven'
        elif chara_name == 'yoshi':
            chara_name = 'yoshimitsu'
        elif chara_name == 'ling':
           chara_name = 'xiaoyu'

        character = tkfinder.get_character(chara_name)
        if character is not None:
            move = tkfinder.get_move(character, chara_move, True)
            
            #First checks the move as case sensitive, if it doesn't find it
            #it checks it case unsensitive
            
            if move is not None:
                embed = move_embed(character, move) 
                
                msg = await bot.send_message(message.channel, embed=embed)
                await asyncio.sleep(300)
                await bot.delete_message(msg)
            else:
                move = tkfinder.get_move(character, chara_move, False)
                if move is not None:
                    embed = move_embed(character, move)
                    
                    msg = await bot.send_message(message.channel, embed=embed)
                    await asyncio.sleep(300)
                    await bot.delete_message(msg)
                else:
                    print('Move not found: ' + chara_move)
                    embed = error_embed('Move not found: ' + chara_move)
                    
                    msg = await bot.send_message(message.channel, embed=embed)
                    await asyncio.sleep(150)
                    await bot.delete_message(msg)
        
        elif chara_name == 'anna':
            bot_msg = 'Ei ota, ei Anna.'
            embed = error_embed(bot_msg)
            msg = await bot.send_message(message.channel, embed=embed)
            await asyncio.sleep(150)
            await bot.delete_message(msg)

        elif chara_name == 'lei':
            bot_msg = 'Lei: havaijilainen kaulaseppele.'
            embed = error_embed(bot_msg)
            msg = await bot.send_message(message.channel, embed=embed)
            await asyncio.sleep(150)
            await bot.delete_message(msg)
        
        else:
            bot_msg = 'Character ' + chara_name + ' does not exist.'
            print(bot_msg)
            embed = error_embed(bot_msg)
            
            msg = await bot.send_message(message.channel, embed=embed)
            await asyncio.sleep(150)
            await bot.delete_message(msg)

            return
    await bot.process_commands(message)
bot.run(token)
