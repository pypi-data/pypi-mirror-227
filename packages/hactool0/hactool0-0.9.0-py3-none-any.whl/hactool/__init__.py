"""
A lot of useful tools
"""

# import libraries
import time
from pyperclip import copy
from pyautogui import position
from playsound import playsound
from os import system,name
from time import localtime
from random import randint as rdi
from random import uniform,sample
import os.path as op
import keyboard as kb
import colorama
import glob
from numpy import loadtxt




########## MAIN ##########


### COVERT ###

# 0.0.1
def list2str(list:list=[],sep:str=""):
    '''
    list2str([list],[sep]) -> a string

    Return a string -> str
    '''

    return sep.join(map(str,list))

# 0.0.8
def l2s(list:list=[],sep:str=""):
    '''
    l2s([list],[sep]) -> a string

    Return a string -> str
    '''

    return sep.join(map(str,list))

# 0.0.1
def str2list(string:str="",sep:str=" "):
    '''
    str2list([str],[sep]) -> a list
    
    Return a list -> list
    '''

    l=[]
    if sep != "":
        l = list(string.split(sep))
        return l
    else:
        for i in string:
            l.append(i)
        return l

# 0.0.8
def s2l(string:str="",sep:str=" "):
    '''
    s2l([str],[sep]) -> a list
    
    Return a list -> list
    '''

    return str2list(string,sep)

# 0.0.1
def str2tuple(string:str="",sep:str=" "):
    '''
    str2tuple([str],[sep]) -> a tuple
    
    Return a tuple -> tuple
    '''

    l=[]
    if sep != "":
        t = tuple(string.split(sep))
        return t
    else:
        for i in string:
            t.append(i)
        return t

# 0.0.8
def s2t(string:str="",sep:str=" "):
    '''
    stt([str],[sep]) -> a tuple
    
    Return a tuple -> tuple
    '''

    return str2tuple(string,sep)


### PAUSE ###

# 0.0.1
def sleep(secs:int=0):
    '''
    sleep([second]) -> Pause some seconds

    Pause script for some seconds.

    Return None -> None
    '''

    time.sleep(secs)

# 0.0.8
def pause(secs:int=0):
    '''
    pause([second]) -> Pause some seconds

    Pause script for some seconds.

    Return None -> None
    '''

    time.sleep(secs)

# 0.0.8
def wait(secs:int=0):
    '''
    wait([second]) -> Pause some seconds

    Pause script for some seconds.

    Return None -> None
    '''

    time.sleep(secs)


### Mouse Position ###

# 0.0.1
def get_mouse_x():
    '''
    Get mouse x

    Return mouse x -> int
    '''
    
    return position()[0]

# 0.0.1
def get_mouse_y():
    '''
    Get mouse y

    Return mouse y -> int
    '''

    return position()[1]

# 0.0.1
def get_mouse_position():
    '''
    Get mouse x and y

    Return (x,y) -> tuple
    '''
    
    pos = position()
    return tuple([pos[0],pos[1]])


### Terminal ###

# 0.0.8
def console(command):
    '''
    Same as os.system
    '''
    system(command)

# 0.0.6
def clear():
    '''
    clear terminal

    Return None -> None
    '''
    
    console('cls' if name in ('nt', 'dos') else 'clear')

# 0.0.3
def cls():
    '''
    clear terminal (still there)

    Return None -> None
    '''

    colorama.init()
    print("\033[2J\033[1;1f")


### Random ###

# 0.0.8
def randint(a:int,b:int):
    '''
    Get a Random Integer from a to b
    
    Return a Integer -> int
    '''
    
    return rdi(a,b)

# 0.0.8
def random(a:int,b:int):
    '''
    Get a Random Float from a to b

    Return a Float -> float
    '''

    return uniform(a,b)


# 0.0.8
def choice(population,k:int=1):
    '''
    Choose k Objects in population

    Return a List -> list
    '''

    return sample(population,k)


## Keyboard ##

# 0.0.8
def on_press():
    '''
    Get all pressing key.

    Return a List -> list
    '''

    return kb.on_press()

# 0.0.8
def is_pressed(key):
    '''
    If "key" is pressing, Return True
    If not, Return False

    Return -> bool
    '''

    return kb.is_pressed(key)

# 0.0.8
def is_release(key):
    '''
    If "key" is releasing, Return True
    If not, Return False

    Return -> bool
    '''
    return kb.is_release(key)

# 0.0.8
def send(key):
    '''
    send some keys

    Return key you input -> str
    '''
    
    kb.send(key)

# 0.0.8
def waitkey(key):
    '''
    wait until "key" is pressed

    Return -> None
    '''
    
    kb.wait(key)


### File ###

# 0.0.9
def fileget(_file,dtype=str,delimiter='',comments='#',encoding='utf-8'):
    '''
    Open a File and Read all of it
    If the file doesn't exist, Return None -> None

    if mode is str:
    Return a content of the file -> str
    else if mode is list:
    Return a content of the file to a list -> list
    '''
    
    try:
        return (loadtxt(fname=_file,delimiter=delimiter,dtype=dtype,comments=comments,encoding=encoding))
    except FileNotFoundError:
        raise f'File {_file} Not Found'
    except TypeError:
        raise f'Type {dtype} Error'
    except:pass

def glob(pathname, *, recursive=False):
    '''
    Same as glob.glob
    '''
    
    glob.glob(pathname,recursive=recursive)

### Other ###

# 0.0.1
def copy(text:str=""):
    '''
    copy([text]) -> text

    Return text -> str
    '''
    
    copy(text)
    return text

# 0.0.2
def playsound(path:str):
    '''
    Play some sound

    Return None
    '''

    try:
        playsound(path)
    except:
        raise "Can't play the sound"


### Class ###

# 0.0.8
class Now:
    def __init__(self):
        self.settime()

    def settime(self):
        
        now = localtime()
        self._year = now.tm_year
        self._mon = now.tm_mon
        self._date = now.tm_mday
        self._hour = now.tm_hour
        self._min = now.tm_min
        self._sec = now.tm_sec
        self._day = now.tm_wday
        self._yday = now.tm_yday
        self._isdst = now.tm_isdst
        del now
    
    def gettime(self,type):
        
        self.settime()
        if (type=='year'):return self._year
        elif (type=='mon'):return self._mon
        elif (type=='date'):return self._date
        elif (type=='hour'):return self._hour
        elif (type=='min'):return self._min
        elif (type=='sec'):return self._sec
        elif (type=='day'):return self._day
        elif (type=='yday'):return self._yday
        elif (type=='isdst'):return self._isdst
        else:return None
    
    def year(self):return self.gettime('year')
    def mon(self):return self.gettime('mon')
    def date(self):return self.gettime('date')
    def hour(self):return self.gettime('hour')
    def min(self):return self.gettime('min')
    def sec(self):return self.gettime('sec')
    def day(self):return self.gettime('day')
    def yday(self):return self.gettime('yday')
    def isdst(self):return self.gettime('isdst')

# 0.0.8
class Path:
    def __init__(self,path):
        self.path = path
        self.info()
    
    def info(self):
        self.full = op.abspath(self.path)
        self.drive = op.splitdrive(self.path)[0]
        self.dir = op.dirname(self.path)
        self.file = op.basename(self.path)
        self.exists = op.exists(self.path)
        if self.exists==True:self.size = op.getsize(self.path)
        else:self.size = 0
        if op.isfile(self.path):self.type='file'
        elif op.isdir(self.path):self.type='dir'

    def set(self,NewPath):
        self.path = NewPath
        self.info()
    
    def getinfo(self):
        return {'full':self.full,'drive':self.drive,'dir':self.dir,'file':self.file,'exists':self.exists,'size':self.size,'type':self.type}


