"""
A lot of useful tools
"""

# import libraries
import time
from pyperclip import copy
from pyautogui import position
from playsound import playsound
from os import system
from time import localtime
from random import randint as rdi
from random import uniform,sample
import os.path as op
import keyboard as kb



########## MAIN ##########


### COVERNT ###

# 0.0.1
def listtostr(list:list=[],sep:str=""):
    '''
    listtostr([list],[sep]) -> a string

    Return a string -> str
    '''

    return sep.join(map(str,list)) 

# 0.0.8
def lts(list:list=[],sep:str=""):
    '''
    lts([list],[sep]) -> a string

    Return a string -> str
    '''

    return sep.join(map(str,list))

# 0.0.1
def strtolist(string:str="",sep:str=" "):
    '''
    strtolist([str],[sep]) -> a list
    
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
def stl(string:str="",sep:str=" "):
    '''
    stl([str],[sep]) -> a list
    
    Return a list -> list
    '''

    return strtolist(string,sep)

# 0.0.1
def strtotuple(string:str="",sep:str=" "):
    '''
    strtotuple([str],[sep]) -> a tuple
    
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
def stt(string:str="",sep:str=" "):
    '''
    stt([str],[sep]) -> a tuple
    
    Return a tuple -> tuple
    '''

    return strtotuple(string,sep)


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
def cmd(command):
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

    try:
        cmd("clear")
    except:
        cmd("cls")

# 0.0.3
def cls():
    '''
    clear termanal

    Return None -> None
    '''

    try:
        cmd("clear")
    except:
        cmd("cls")


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
def choise(population,k:int=1):
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

# 0.0.8
def openfile(filename,mode:str,encoding:str='utf-8'):
    '''
    Open a file
    Same as "open()" but this encoding default is utf-8
    '''

    return open(file=filename,mode=mode,encoding=encoding)


def fileget(file):
    '''
    Open a File and Read all of it
    If the file doesn't exist, Return None -> None

    Return a content of the file -> str
    '''
    
    try:
        with open(file,'r',encoding='utf-8') as f: return f.read()
    except:return

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
        self.nowyear = now.tm_year
        self.nowmon = now.tm_mon
        self.nowdate = now.tm_mday
        self.nowhour = now.tm_hour
        self.nowmin = now.tm_min
        self.nowsec = now.tm_sec
        self.nowday = now.tm_wday
        self.nowyday = now.tm_yday
        self.nowisdst = now.tm_isdst
        del now
    
    def gettime(self,type):
        
        self.settime()
        if (type=='year'):return self.nowyear
        elif (type=='mon'):return self.nowmon
        elif (type=='date'):return self.nowdate
        elif (type=='hour'):return self.nowhour
        elif (type=='min'):return self.nowmin
        elif (type=='sec'):return self.nowsec
        elif (type=='day'):return self.nowday
        elif (type=='yday'):return self.nowyday
        elif (type=='isdst'):return self.nowisdst
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


