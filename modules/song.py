#Returns audio
from discord import FFmpegOpusAudio
from youtube_dl import YoutubeDL
from requests import get

#Solves latter error
#[tls @ 0x55a7d8228980] The specified session has been invalidated for some reason.
FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


#Queues
queue = {}

async def playSong(guildQueue:dict):
    ctx = guildQueue['ctx']
    conn = guildQueue['conn']
    source = guildQueue['songs'][0]['url']
    print(f'Playing {guildQueue["songs"][0]["title"]}...')
    await ctx.send(f'Now playing {guildQueue["songs"][0]["title"]}')
    print(conn)
    print(source)
    conn.play(FFmpegOpusAudio(source, **FFMPEG_OPTS), after=await playNext(guildQueue))
    
    #ffmpegpcm audio. Doesnt seem to work too well
    #conn.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=await playNext(guildQueue))

async def playNext(guildQueue):
    guildQueue['songs'].pop(0)
    if guildQueue['songs']:
        print('starting play...')
        await initPlay(guildQueue)
    else:
        print('No song qued...')
        await guildQueue['conn'].disconnect()
        await guildQueue['ctx'].send('Nähää bro!')
        queue.pop(guildQueue['ctx'].guild.id)

async def initPlay(guildQueue):
    try:
        conn = await guildQueue['ctx'].author.voice.channel.connect()
    except:
        print('Connection error!')
        return Exception('ConnErr')
    guildQueue.update({'conn':conn})
    await playSong(guildQueue)
        
async def addSong(ctx, song:dict):
    if ctx.guild.id not in queue.keys():
        print(f'Creating que for {ctx.guild.name}')
        queue.update({ctx.guild.id:{
            'ctx': ctx,
            'songs': [],
            'conn': None
        }})
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
        try:
            try: get(srch)
            except: info = ydl.extract_info(f"ytsearch:{srch}", download=False)['entries'][0]
            else: info = ydl.extract_info(srch, download=False)
        
            song = {
                'title': info['title'],
                #'duration': info['formats'][0]['duration'],
                'url': info['formats'][0]['url']
            }
        except Exception as err:
            print(err)
            return Exception('Videota ei löytynyt...')
        await addSong(ctx, song)
    
    