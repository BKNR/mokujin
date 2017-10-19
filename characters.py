# -*- coding: utf-8 -*-
import json


with chara_misc_file open('json/character_misc.json') as contents:
    contents = chara_misc_file.read()
chara_misc_json = json.loads(contents)

def character_exists(chara_name):
    '''Checks if character exists in character_misc.json'''

    # Seems like you should go through the json only once, if the character
    # exists, the details should be saved somewhere
    chara_details = list(filter(lambda x: (x['name'] == chara_name), chara_misc_json))
    if chara_details:
        return True
    else:
        return False
