from discord import opus

import ctypes
import ctypes.util

def fixOpus():
    print("Finding opus...")
    a = ctypes.util.find_library('opus')
    if not a:
        exit('Opus not found!')
    else: print(a)
    
    print("Discord - Loading opus...:")
    b = opus.load_opus(a)
    print(b)