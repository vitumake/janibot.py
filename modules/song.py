#Returns audio
from pytube import YouTube
from pytube import Search
import validators

#Queues
class Queue:
    def __init__(self, guildId) -> None:
         self.guildId = guildId
         self.songs = []
    
    def __str__(self) -> str:
         return self.guildId
async def srchSong(ctx, srch:str) -> dict:
    if srch.startswith('https://youtube.com/'):
        pass
    else: 
        pass

    song = {
    'title': title,
    'duration': duration,
    'link': link
        }
    

def play(ctx, audio) -> None:
    pass
