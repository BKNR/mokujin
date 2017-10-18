# -*- coding: utf-8 -*-

def character_exists(chara_name):
    if chara_name == 'dj' or chara_name == 'dvj' or chara_name == 'devil' or chara_name == 'deviljin':
        chara_name = 'devil_jin'
    elif chara_name == 'sergei':
        chara_name = 'dragunov'
    elif chara_name == 'jack':
        chara_name = 'jack7'
    elif chara_name == 'chloe' or chara_name == 'lc' or chara_name == 'lucky':
        chara_name = 'lucky_chloe'
    elif chara_name == 'raven':
        chara_name = 'master_raven'
    elif chara_name == 'yoshi'
        chara_name = 'yoshimitsu'
    elif chara_name = 'ling':
        chara_name = 'xiouyu'

    # TODO: check if character exists in json/character_misc.json
