# Mokujin

Mokujin (v1.0) is a discord bot that fetches Tekken 7 framedata.  
It uses [discord.py](https://github.com/Rapptz/discord.py) v1.0+ and is updated to use Python 3.6+

The bot now has all the functionalities currently planned and it seems to work well and is somewhat stable, so I'm going to call this one v1.0. There is no plans for future updates, except for bug fixes should the need arise. If there are to be additional characters released to Tekken 7 past current version (2.20), it's likely, but not absolutely certain that they will be added to the bot. 

Framedata acquired from RBNorway, lot of help and inspiration [hanyaa's TkPublic bot](https://github.com/hanyaah/TkPublic).

On 2019-04-17 the project was migrated to discord.py rewrite (v1.0). 

## If you want to use this:

Clone this to a linux server that has Python 3.6.0+ with [discord.py](https://github.com/Rapptz/discord.py) library.
You need your own discord bot ([here's how](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)) and have the token in a token.txt file in the same directory.
The executable is mokujin.py.

The bot only listens to and responses to messages in channels called #tekken or #raamikysely, if you want to change that, you do it in mokujin.py, at the time of writing line 68:

```python
if message.content.startswith('!') and (message.channel.name == 'tekken' or message.channel.name == 'raamikysely'):
```
