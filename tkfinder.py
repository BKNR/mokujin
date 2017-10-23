# -*- coding: utf-8 -*-
import json

def get_character(chara_name):
    '''Gets character details from character_misc.json, if character exists
    returns character details if exists, else None
    '''

    with open('json/character_misc.json') as chara_misc_file:
        contents = chara_misc_file.read()
    chara_misc_json = json.loads(contents)
    
    chara_details = list(filter(lambda x: (x['name'] == chara_name), chara_misc_json))
    if chara_details:
        return chara_details
    else:
        return None

def get_move(character, move_command):
    '''Gets move from local_json, if exists
    returns move if exists, else None
    '''
    move_file_name = 'json/' + character + '.json'
    with open(move_file_name) as move_file:
        move_file_contents = move_file.read()
    move_json = json.loads(move_file_contents)
    
    move = list(filter(lambda x: (x['Command'] == move_command), move_json))
    if  move:
        return move
    else:
        return None
