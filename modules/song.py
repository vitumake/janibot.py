#Returns audio
import pafy
from discord import FFmpegPCMAudio, FFmpegOpusAudio
from youtube_dl import YoutubeDL
from requests import get

#Solves some problem. Idk ripped from stackoverflow
FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


#Queues
queue = {}

async def playSong(guildQueue:dict):
    ctx = guildQueue['ctx']
    conn = guildQueue['conn']
    source = guildQueue['songs'][0]['url']
    print(f'Playing {guildQueue["songs"][0]["title"]}...')
    await ctx.send(f'Now playing {guildQueue["songs"][0]["title"]}')
    
    #Using pafy. Maybe work better :)
    conn.play(FFmpegOpusAudio(source, pipe=True), after=await playNext(guildQueue))
    
    #Old ffmpeg audio. Doesnt seem to work too well
    #conn.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=await playNext(guildQueue))

async def playNext(guildQueue):
    if guildQueue['songs']:
        guildQueue['songs'].pop(0)
        await initPlay(guildQueue)
    else:
        guildQueue.update({'conn':None})
        await guildQueue['ctx'].guild.voice_client.disconnect()

async def initPlay(guildQueue):
    if guildQueue['conn'] == None:
        try:
            conn = await guildQueue['ctx'].author.voice.channel.connect()
            guildQueue.update({'conn':conn})
        except:
            print('Connection error!')
            return Exception('ConnErr')
    if not guildQueue['conn'].is_playing():
        if guildQueue['songs']:
            await playSong(guildQueue)
async def addSong(ctx, song:dict):
    if ctx.guild.id not in queue.keys():
        print(f'Creating que for {ctx.guild.name}')
        queConst = {
            'ctx': ctx,
            'songs': [],
            'conn': None
        }
        queue.update({ctx.guild.id:queConst})
    else: await ctx.send(f'Added to queue {song["title"]}')
    guildQueue = queue[ctx.guild.id]
    guildQueue['songs'].append(song)
    await initPlay(guildQueue)

async def srchSong(ctx, srch:str):
    print(f'Searching for "{srch}"... in "{ctx.guild.name}"')
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]}
    with YoutubeDL(ydl_opts) as ydl:
        try: get(srch)
        except: info = ydl.extract_info(f"ytsearch:{srch}", download=False)['entries'][0]
        else: info = ydl.extract_info(srch, download=False)
    song = {
        'title': info['title'],
        #'duration': info['formats'][0]['duration'],
        'url': info['formats'][0]['url']
    }
    await addSong(ctx, song)
    
    