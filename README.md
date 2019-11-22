# Mokujin

Mokujin (v1.0.1) is a discord bot that fetches Tekken 7 framedata.  
It uses [discord.py](https://github.com/Rapptz/discord.py) v1.2.5+ and is updated to use Python 3.6+

The bot now has all the functionalities currently planned and it seems to work well and is somewhat stable. Currently, the data the bot uses is being updated to season 3, and the rest of the season 3 data will be updated either on request or when we see a mistake.

Framedata acquired from RBNorway, lot of help and inspiration [hanyaa's TkPublic bot](https://github.com/hanyaah/TkPublic).

On 2019-04-17 the project was migrated to discord.py rewrite (v1.0). 

## If you want to use this:

Clone this to a linux server that has Python 3.6.0+ with [discord.py](https://github.com/Rapptz/discord.py) library.
You need your own discord bot ([instruction](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)) and have the token in a token.txt file in the `/config` directory.
The executable is `src/mokujin.py`.

The bot only listens to and responses to messages in channels with tekken or frame. You can change that in the `mokujin.py`
```
if ('tekken' in channel.name) or ('frame' in channel.name)
```

Commands
```
!character move -   get frame data of a move from a character
!delete-data -      deletes bot's last own messages
```
