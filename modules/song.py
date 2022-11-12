#Returns audio

from youtube_search import YoutubeSearch

#Queues
queue = {}

def searchYt(srch:str) -> dict:
    result = YoutubeSearch(srch).to_dict()[0]
    return {
        'title': result['title'],
        'duration': result['duration'],
        'link': f'https://youtube.com{result["url_suffix"]}'
        
    }
    
def play(ctx, link) -> None:
    if ctx.guild in list(queue.keys()): serverQueue = queue[ctx.guild]
    else:
        queue[ctx.guild.id] = {
            'ctx': ctx,
            'songs': [],
            'conn': None
        }
    