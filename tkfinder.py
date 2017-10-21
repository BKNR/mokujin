# -*- coding: utf-8 -*-
import json



def character_exists(chara_name):
    '''Checks if character exists in character_misc.json'''

    with open('json/character_misc.json') as chara_misc_file:
        contents = chara_misc_file.read()
    chara_misc_json = json.loads(contents)
    
    chara_details = list(filter(lambda x: (x['name'] == chara_name), chara_misc_json))
    if chara_details:
        return True
    else:
        return False

def get_move(character, move_command):
    #untested
    '''Gets move from [character].json, if exists
    returns move if exists, else None
    '''
    move_file_name = character + '.json'
    with open(move_file_name) as move_file:
        move_file_contents = move_file.read()
    move_json = json.loads(move_file_contents)
    
    move = list(filter(lambda x (x['command'] == move_command), move_json))
    if  move:
        return move
    else:
        return None
