# -*- coding: utf-8 -*-
import os, json, difflib
from src.resources import const

base_path = os.path.dirname(__file__)


def load_characters_config():
    filepath = os.path.abspath(os.path.join(base_path, "resources", "character_misc.json"))
    with open(filepath) as chara_misc_file:
        contents = chara_misc_file.read()

    chara_misc_json = json.loads(contents)
    return chara_misc_json


def correct_character_name(alias: str):
    # check if input in dictionary or in dictionary values
    if alias in const.CHARACTER_ALIAS:
        return alias

    for key, value in const.CHARACTER_ALIAS.items():
        if alias in value:
            return key

    return None


def get_character_json(character):
    os.path.abspath(os.path.join(base_path, "..", "json", character.get('local_json')))
    filepath = os.path.abspath(os.path.join(base_path, "..", "json", character.get('local_json')))
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
    move_list = get_commands_from(chara_name)
    moves = difflib.get_close_matches(move, move_list, 5)
    return list(moves)


def get_character_data(chara_name: str) -> dict:
    """Gets character details from character_misc.json, if character exists
    returns character details as dict if exists, else None"""

    chara_misc_json = load_characters_config()
    chara_details = list(filter(lambda x: (x['name'] == chara_name), chara_misc_json))

    if chara_details:
        return chara_details[0]
    else:
        return None


def get_move(character: dict, move_command: str) -> dict:
    """Gets move from local_json, if exists
    returns move if exists, else None"""

    move_json = get_character_json(character)

    move = list(filter(lambda x: (move_simplifier(x['Command'])
                                  == move_simplifier(move_command)), move_json))
    if not move:
        move = list(filter(lambda x: (is_command_in_alias(move_command, x)), move_json))

        if not move:
            move = list(filter(lambda x: move_simplifier(move_command)
                                         in move_simplifier(x['Command']), move_json))
    if move:
        return move[0]
    else:
        return None


def get_by_move_type(character: dict, move_type: str) -> list:
    """Gets a list of moves that match move_type from local_json
    returns a list of move Commands if finds match(es), else empty list"""

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
        aliases = item['Alias']
        for alias in aliases:
            if move_simplifier(command) == move_simplifier(alias):
                return True
    return False


def move_simplifier(move_input) -> str:
    """Removes bells and whistles from the move_input"""

    short_input = move_input.strip().lower()

    for old, new in const.REPLACE.items():
        short_input = short_input.replace(old, new)

    # cd works, ewgf doesn't, for some reason
    if short_input[:2].lower() == 'cd' and short_input[:3].lower() != 'cds':
        short_input = short_input.lower().replace('cd', 'fnddf')
    if short_input[:2].lower() == 'wr':
        short_input = short_input.lower().replace('wr', 'fff')
    return short_input
