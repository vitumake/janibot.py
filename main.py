#Jani main
import validators
import discord
from modules import song
from modules.log import janiHandler
from discord.ext import commands
from loadOpus import fixOpus
from sys import platform

if not platform == 'win32': fixOpus()
else: print('Using windows. Skipping opus check...')

print("Discord - Opus loaded:")
c = discord.opus.is_loaded()
print(str(c) + '\n')

try:
    with open('./token.txt', 'r') as file:
        token = [i.rstrip() for i in file]
except FileNotFoundError:
    exit('No token.txt file. See README.md')

class Bot(commands.Bot):
    async def on_ready(self):
        print(f'{self.user} online...')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
Jani = Bot(command_prefix='!', intents=intents)

@Jani.command()
async def test(ctx, *args):
    arg = ' '.join(args)
    await ctx.send(arg)

@Jani.command(aliases=['p', 'P'])
async def play(ctx, *args):
    arg = ' '.join(args)
    try:
        await song.srchSong(ctx, arg)
    except Exception as e:
        await ctx.send(e)

@Jani.command(aliases=['q', 'Q', 'que', 'Que'])
async def queue(ctx):
    guildSongs = song.queue[ctx.guild.id]['songs']
    for i in guildSongs:
        await ctx.send(f'{i["title"]}')

@Jani.command(aliases=['s', 'S', 'Skip'])
async def skip(ctx):
    guildQueue = song.queue[ctx.guild.id]
    guildQueue['conn'].stop()
    await song.playNext(guildQueue)
        
#Eskekutse jamppa 8==D
Jani.run(token[0], reconnect=True, log_handler=janiHandler)