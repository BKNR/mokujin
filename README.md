# Mokujin

Mokujin (v1.0.1) is a discord bot that fetches Tekken 7 framedata.  
It uses [discord.py](https://github.com/Rapptz/discord.py) v1.2.5+ and is updated to use Python 3.6+

The bot now has all the functionalities currently planned and it seems to work well and is somewhat stable. Currently, the data the bot uses is being updated to season 3, and the rest of the season 3 data will be updated as it appears to RBNorway, and when rest of the season 3 characters are released, they will also be updated to the bot.  

Framedata acquired from RBNorway, lot of help and inspiration [hanyaa's TkPublic bot](https://github.com/hanyaah/TkPublic).

On 2019-04-17 the project was migrated to discord.py rewrite (v1.0). 

2019-11-19 Update: **HOX! You need to update discord.py to v1.2.5+**
## If you want to use this:

Clone this to a linux server that has Python 3.6.0+ with [discord.py](https://github.com/Rapptz/discord.py) library.
You need your own discord bot ([here's how](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)) and have the token in a token.txt file in the same directory.
The executable is mokujin.py.

The bot only listens to and responses to messages in channels called #tekken or #raamikysely, if you want to change that, you do that in config.py, where you can also set the character aliases.
