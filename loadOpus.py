from discord import opus

import ctypes
import ctypes.util

def fixOpus():
    print("ctypes - Find opus:")
    a = ctypes.util.find_library('opus')
    print(a)
    
    print("Discord - Load Opus:")
    b = opus.load_opus(a)
    print(b)
    
    print("Discord - Is loaded:")
    c = opus.is_loaded()
    print(c + '\n')