
########## IMPORT LIBRARIES ##########

import glob as Glob
import os.path as op
import random as rd
import sys
import time
from os import name, system

import colorama
import keyboard as kb
import pick as Pick
import playsound as Playsound
import pyperclip
import tabulate
from numpy import loadtxt
from pyautogui import position

########## EXCEPTION ##########

class Exception(Exception): pass

########## MAIN ##########


### COLORS ###

# 0.11.0

reset = '\033[0m'
bold = '\033[01m'
disable = '\033[02m'
underline = '\033[04m'
reverse = '\033[07m' # color reverse
i = '\033[09m' # strikethrough
invisible = '\033[08m' # hide
 
# fg
black = '\033[30m'
red = '\033[31m'
green = '\033[32m'
orange = '\033[33m'
blue = '\033[34m'
purple = '\033[35m'
cyan = '\033[36m'
lightgrey = '\033[37m'
darkgrey = '\033[90m'
lightred = '\033[91m'
lightgreen = '\033[92m'
yellow = '\033[93m'
lightblue = '\033[94m'
pink = '\033[95m'
lightcyan = '\033[96m'
 
# bg
bg_black = '\033[40m'
bg_red = '\033[41m'
bg_green = '\033[42m'
bg_orange = '\033[43m'
bg_blue = '\033[44m'
bg_purple = '\033[45m'
bg_cyan = '\033[46m'
bg_lightgrey = '\033[47m'


### COVERT ###

# 0.1.0
def list2str(list:list=[],sep:str=""):
    '''
    list2str([list],[sep]) -> a string


    Return a string -> str
    '''

    return sep.join(map(str,list))

# 0.8.0
def l2s(list:list=[],sep:str=""):
    '''
    l2s([list],[sep]) -> a string


    Return a string -> str
    '''

    return sep.join(map(str,list))

# 0.1.0
def str2list(string:str="",sep:str=" "):
    '''
    str2list([str],[sep]) -> a list
    
    
    Return a list -> list
    '''

    return list(string.split(sep))

# 0.8.0
def s2l(string:str="",sep:str=" "):
    '''
    s2l([str],[sep]) -> a list
    
    
    Return a list -> list
    '''

    return str2list(string,sep)

# 0.1.0
def str2tuple(string:str="",sep:str=" "):
    '''
    str2tuple([str],[sep]) -> a tuple
    
    
    Return a tuple -> tuple
    '''

    return  tuple(string.split(sep))

# 0.8.0
def s2t(string:str="",sep:str=" "):
    '''
    stt([str],[sep]) -> a tuple
    
    
    Return a tuple -> tuple
    '''

    return str2tuple(string,sep)


### PAUSE ###

# 0.1.0
def sleep(secs:float=0):
    '''
    sleep([second]) -> Pause some seconds

    Pause script for some seconds.


    Return None -> None
    '''

    time.sleep(secs)

# 0.8.0
def pause(secs:float=0):
    '''
    pause([second]) -> Pause some seconds

    Pause script for some seconds.


    Return None -> None
    '''

    time.sleep(secs)

# 0.8.0
def wait(secs:float=0):
    '''
    wait([second]) -> Pause some seconds

    Pause script for some seconds.


    Return None -> None
    '''

    time.sleep(secs)


### Mouse Position ###

# 0.1.0
def get_mouse_x():
    '''
    Get mouse x


    Return mouse x -> int
    '''
    
    return position()[0]

# 0.1.0
def get_mouse_y():
    '''
    Get mouse y


    Return mouse y -> int
    '''

    return position()[1]

# 0.1.0
def get_mouse_position():
    '''
    Get mouse x and y


    Return (x,y) -> tuple
    '''
    
    pos = position()
    return tuple([pos[0],pos[1]])


### Terminal ###

# 0.8.0
def console(command):
    '''
    Same as os.system
    '''
    system(command)

# 0.6.0
def clear(x=None):
    '''
    clear terminal

    print x if x exist
    

    Return None -> None
    '''
    
    console('cls' if name in ('nt', 'dos') else 'clear')
    if x!=None: print(x)

# 0.3.0
def cls(x=None):
    '''
    clear terminal (still there)

    print x if x exist


    Return None -> None
    '''

    colorama.init()
    print("\033[2J\033[1;1f")
    if x!=None: print(x)


### Random ###

# 0.8.0
def randint(a:int=0,b:int=None):
    '''
    Get a Random Integer from a to b
    
    
    Return a Integer -> int
    '''
    
    return rd.randint(a,b)

# 0.8.0
def random(a:int=0,b:int=None):
    '''
    Get a Random Float from a to b


    Return a Float -> float
    '''

    return rd.uniform(a,b)

# 0.8.0
def choice(population,k:int=1):
    '''
    Choose k Objects in population


    Return a List -> list
    '''

    return rd.sample(population,k)

# 0.10.0
def shuffle(_list:list):
    '''
    shuffle a list
    
    
    Return a List -> list
    '''

    output,l = [],_list
    for i in range(len(l)): ran = randint(b=len(l)-1);output.append(l[ran]);del l[ran]
    return output

## Keyboard ##

# 0.8.0
def on_press():
    '''
    Return all pressing keys
    
    
    Return on pressing keys -> list
    '''
    
    return kb.on_press()

# 0.8.0
def is_pressed(key):
    '''
    If "key" is pressing, Return True
    
    If not, Return False


    Return -> bool
    '''

    return kb.is_pressed(key)

# 0.8.0
def is_release(key):
    '''
    If "key" is releasing, Return True
    
    If not, Return False


    Return -> bool
    '''
    return kb.is_release(key)

# 0.10.0
def on_release():
    '''
    Return all releasing keys
    
    
    Return on releasing keys -> list
    '''
    
    return kb.on_release()

# 0.8.0
def send(key):
    '''
    send some keys


    Return "key" -> str
    '''
    
    kb.send(key)
    return key

# 0.8.0
def waitkey(key):
    '''
    wait until "key" is pressed


    Return -> None
    '''
    
    kb.wait(key)


### File ###

# 0.9.0
def fileget(fname,dtype=str,delimiter='',comments='#',encoding='utf-8'):
    '''
    Same as numpy.loadtxt()
    
    Return file contents -> list
    '''
    
    if op.exists(fname): return list(loadtxt(fname=fname,delimiter=delimiter,dtype=dtype,comments=comments,encoding=encoding))


# 0.9.0
def glob(path):
    '''
    Same as glob.glob
    
    Return all files -> list
    '''
    
    return Glob.glob(path)


### PRINT ###

# 0.10.0
def tprint(content:list,header:list):
    '''
    return a table
    
    
    Return table -> str
    '''
    
    return tabulate.tabulate(content,header,tablefmt="fancy_grid")

# 0.11.1
def type_animate(text:str,sep:float=0.0):
    '''
    a type animation
    
    Return None -> None
    '''
    for i in text: print(i,end="");sleep(sep)
    sys.stdout.flush()


### Others ###

# 0.1.0
def copy(text:str=''):
    '''
    copy([text]) -> text


    Return text -> str
    '''
    
    pyperclip.copy(text)
    return text

# 0.2.0
def playsound(path:str):
    '''
    Play some sound


    Return None
    '''

    try:
        Playsound.playsound(path)
    except Exception as e:
        raise Exception(e)

# 0.10.0
def ka():
    '''
    A thing can stock in your code
    
    it's name is "stock" in chinese (卡 kǎ)
    
    
    It can do nothing
    '''
    
    return

# 0.10.0
def pick(title:str='',options:list=[],indicator:str='> ',default_index:int=0):
    '''
    same as pick.pick
    
    
    Return option,index -> str, int
    '''
    
    return Pick.pick(title=title, options=options, indicator=indicator, default_index=default_index)

# 0.11.2
def time_str():
    '''
    Get a str of "year_month_date_hour_min_sec"
    
    Return str -> str
    '''
    now = Now()
    return f'{now.year()}_{now.mon()}_{now.date()}_{now.hour()}_{now.min()}_{now.sec()}'

# 0.11.2
def exit():
    '''
    exit script
    
    Return None -> None
    '''
    sys.exit()


### Class ###

# 0.8.0
class Now:
    def __init__(self):
        self.set_time()

    # 0.8.0
    def set_time(self):
        
        now = time.localtime()
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
    
    # 0.8.0
    def get_time(self,type):
        
        self.set_time()
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
    
    # 0.8.0
    def year(self):return self.gettime('year')
    def mon(self):return self.gettime('mon')
    def date(self):return self.gettime('date')
    def hour(self):return self.gettime('hour')
    def min(self):return self.gettime('min')
    def sec(self):return self.gettime('sec')
    def day(self):return self.gettime('day')
    def yday(self):return self.gettime('yday')
    def isdst(self):return self.gettime('isdst')
    
    # 0.11.2
    def get_times(self):
        return {'year':self.year(),'month':self.mon(),'date':self.date(),
                'hour':self.hour(),'min':self.min(),'sec':self.sec(),
                'day':self.day(),'yday':self.yday(),'isdst':self.isdst()}
    # 0.11.2
    def time_str(self):
        return f'{self.year()}_{self.mon()}_{self.date()}_{self.hour()}_{self.min()}_{self.sec()}'

# 0.8.0
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
