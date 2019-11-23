# -*- coding: utf-8 -*-
import os
import json
import difflib
from config import const

basepath = os.path.dirname(__file__)


def load_characters_config():
    filepath = os.path.abspath(os.path.join(basepath, "..", "config", "character_misc.json"))
    with open(filepath) as chara_misc_file:
        contents = chara_misc_file.read()

    chara_misc_json = json.loads(contents)
    return chara_misc_json


def correct_character_name(input: str) -> str:
    # check if input in dictionary or in dictionary values
    if input in const.CHARACTER_ALIAS or input in const.CHARACTER_ALIAS.values():
        return input

    return None


def get_character_json(character):
    os.path.abspath(os.path.join(basepath, "..", "json", character.get('local_json')))
    filepath = os.path.abspath(os.path.join(basepath, "..", "json", character.get('local_json')))
    with open(filepath) as move_file:
        move_file_contents = move_file.read()
    move_json = json.loads(move_file_contents)

    return move_json


def get_commands_from(chara_name: str) -> list:
    character = get_character_data(chara_name)
    move_json = get_character_json(character)
    result = []
    for move in move_json:
        result.append(move["Command"])

    return list(result)


def get_similar_moves(move: str, chara_name: str) -> list:
    movelist = get_commands_from(chara_name)
    moves = difflib.get_close_matches(move, movelist, 5)
    return list(moves)


def get_character_data(chara_name: str) -> dict:
    '''Gets character details from character_misc.json, if character exists
    returns character details as dict if exists, else None
    '''

    chara_misc_json = load_characters_config()
    chara_details = list(filter(lambda x: (x['name'] == chara_name), chara_misc_json))

    if chara_details:
        return chara_details[0]
    else:
        return None


def get_move(character: dict, move_command: str, case_important: bool) -> dict:
    '''Gets move from local_json, if exists
    returns move if exists, else None
    '''

    move_json = get_character_json(character)

    if case_important:
        move = list(filter(lambda x: (x['Command'] == move_command), move_json))
    else:
        move = list(filter(lambda x: (move_simplifier(x['Command'].lower())
                                      == move_simplifier(move_command.lower())), move_json))
        if not move:
            move = list(filter(lambda x: move_simplifier(move_command.lower())
                                         in move_simplifier(x['Command'].lower()), move_json))
            if not move:
                move = list(filter(lambda x: (is_command_in_alias(move_command, x)), move_json))

    if move:
        return move[0]
    else:
        return None


def get_by_move_type(character: dict, move_type: str) -> list:
    '''Gets a list of moves that match move_type from local_json
    returns a list of move Commands if finds match(es), else empty list'''

    move_json = get_character_json(character)

    moves = list(filter(lambda x: (move_type.lower() in x['Notes'].lower()), move_json))

    if moves:
        move_list = []
        for move in moves:
            move_list.append(move['Command'])
        return list(set(move_list))
    else:
        return []


def is_command_in_alias(command: str, item: dict) -> bool:
    if 'Alias' in item:
        command = command.lower().strip()

        words = item['Alias'].split(",")
        newWords = []
        for word in words:
            newWords.append(str(word).strip().lower())

        if not command in newWords:
            for newWord in newWords:
                if move_simplifier(command) == move_simplifier(newWord):
                    return True

        return command in newWords


def move_simplifier(move_input):
    '''Removes bells and whistles from the move_input'''

    short_input = move_input.replace('ff', 'f,f')
    short_input = short_input.replace(' ', '')
    short_input = short_input.replace('/', '')
    short_input = short_input.replace('+', '')

    # cd works, ewgf doesn't, for some reason
    if short_input[:2].lower() == 'cd' and short_input[:3].lower() != 'cds':
        short_input = short_input.lower().replace('cd', 'f,n,d,df')
    if short_input[:2].lower() == 'wr':
        short_input = short_input.lower().replace('wr', 'f,f,f')

    return short_input
