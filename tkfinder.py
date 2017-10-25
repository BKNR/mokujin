# -*- coding: utf-8 -*-
import json

def get_character(chara_name: str) -> dict:
    '''Gets character details from character_misc.json, if character exists
    returns character details as dict if exists, else None
    '''

    with open('json/character_misc.json') as chara_misc_file:
        contents = chara_misc_file.read()
    
    chara_misc_json = json.loads(contents) 
    chara_details = list(filter(lambda x: (x['name'] == chara_name), chara_misc_json))

    if chara_details:
        return chara_details[0]
    else:
        return None

def get_move(character: dict, move_command: str, case_important: bool) -> dict:
    '''Gets move from local_json, if exists
    returns move if exists, else None
    '''
    move_file_name = 'json/' + character.get('local_json')
    with open(move_file_name) as move_file:
        move_file_contents = move_file.read()
    move_json = json.loads(move_file_contents)
    
    if case_important:
        move = list(filter(lambda x: (x['Command'] == move_command), move_json))
    else: 
        move = list(filter(lambda x: (x['Command'].lower() == move_command.lower()), move_json)
    if  move:
        return move[0]
    else:
        return None
