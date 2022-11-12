#Jani main
import validators
import discord
from modules import song
from modules.log import janiHandler
from discord.ext import commands

try:
    with open('./token.txt', 'r') as file:
        token = [i.rstrip() for i in file]
except FileNotFoundError:
    exit('Ei pass.txt tiedostoa. Katso README.md')

class Bot(commands.Bot):
    async def on_ready(self):
        print(f'{self.user} online...')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
Jani = Bot(command_prefix='!', intents=intents)

@Jani.command()
async def test(ctx, arg):
    await ctx.send(arg)

@Jani.command(aliases=['p', 'pl'])
async def play(ctx, arg):
    reqType = 'link' if validators.url(arg) else 'srch'
    if ctx.author.voice.channel == 'None':
        await ctx.send('Et ole kannulla!')
    else: song.search(ctx, reqType, arg)
    
#Eskekutse jamppa 8==D
Jani.run(token, reconnect=True, log_handler=janiHandler)