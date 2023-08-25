# -*- coding: utf-8 -*-

########## IMPORT LIBRARIES ##########

import csv
import ctypes
import glob as glob_
import os
import random as random_
import sys
import threading
import time
import tkinter as tk
from tkinter import filedialog as fdg

import choose as pick_
import keyboard as kb
import playsound as playsound_
import pyperclip
import tabulate as tabulate_

########## EXCEPTION ##########

class SoundException       (Exception): pass
class FileExistException   (Exception): pass

########## VALUES ##########

ON = True
OFF = False
N = None

########## MAIN ##########


### COLORS ###

# 0.11.0

reset = '\033[0m'
bold = '\033[01m'
disable = '\033[02m'
underline = '\033[04m'
reverse = '\033[07m' # reverse color
i = '\033[09m' # strike through
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


### FORMAT ###

# 0.1.0
def list2str(_list:list=[],sep:str=""):
    '''\
    list2str([list],[sep]) -> a string


    Return a string -> str
    '''
    
    return sep.join(map(str,_list))

# 0.8.0
def l2str(_list:list=[],sep:str=""):
    '''\
    l2s([list],[sep]) -> a string


    Return a string -> str
    '''

    return sep.join(map(str,_list))

# 0.1.0
def str2list(_str:str="",sep:str=" "):
    '''\
    str2list([str],[sep]) -> a list
    
    Return a list -> list
    '''

    return list(_str.split(sep))

# 0.8.0
def s2l(_str:str="",sep:str=" "):
    '''\
    s2l([str],[sep]) -> a list
    
    Return a list -> list
    '''

    return str2list(_str,sep)

# 0.1.0
def str2tuple(_str:str="",sep:str=" "):
    '''\
    str2tuple([str],[sep]) -> a tuple
    
    Return a tuple -> tuple
    '''

    return tuple(_str.split(sep))

# 0.8.0
def s2t(_str:str="",sep:str=" "):
    '''\
    s2t([str],[sep]) -> a tuple
    
    Return a tuple -> tuple
    '''

    return str2tuple(_str,sep)

# 0.13.1
def list2set(_list:list=[]):
    '''\
    list2set([_list]) -> a set
    
    Return a set -> Set
    '''

    output = set()
    for i in _list: output.add(i)
    return output

# 0.13.1
def l2set(_list:list=[]):
    '''\
    l2set([_list]) -> a set
    
    Return a set -> Set
    '''
    
    list2set(_list)

# 0.13.2
def list_format(_list:list=[],_format=str):
    output = []
    for i in _list: output.append(_format(i))
    return output

# 0.13.1
def hac_syntax(text):
    syntaxes = [
        Syntax('$n;','\n'),
        Syntax('$comma;',','),
        Syntax('$period;','.'),
        Syntax('$bang;','!'),
        Syntax('$quos;','?'),
        Syntax('$colon;',':'),
        Syntax('$semi;',';'),
        Syntax('$dash;','-'),
        Syntax('$lparen;','('),
        Syntax('$rparen;',')'),
        Syntax('$lsqubra;','['),
        Syntax('$rsqubra;',']'),
        Syntax('$lbrace;','{'),
        Syntax('$rbrace;','}'),
        Syntax('$lang;','<'),
        Syntax('$rang;','>'),
        Syntax('$apost;',"'"),
        Syntax('$slash;','/'),
        Syntax('$bslash;','\\'),
        Syntax('$under;','_'),
        Syntax('$pipe;','|'),
        Syntax('$tilde;','~'),
        Syntax('$backtick;','`'),
        Syntax('$at;','@'),
        Syntax('$hash;','#'),
        Syntax('$dollar;','$'),
        Syntax('$per;','%'),
        Syntax('$caret;','^'),
        Syntax('$and;','&'),
        Syntax('$aster;','*'),
        Syntax('$plus;','+'),
        Syntax('$min;','-'),
        Syntax('$mul;','×'),
        Syntax('$div;','÷'),
        Syntax('$equ;','='),
    ]
    
    output = text
    
    for i in syntaxes:
        output = i.trans(output)
    
    return output
    

# 0.13.0
def text(*values:object,_hac_syntax=ON,sep:str='',start:str='',end:str=''):
    '''\
    Format text
    
    Return -> str
    '''
    
    output = [start]
    
    for i in values: output.extend([str(i),sep])

    output.pop()
    output.append(end)
    output = l2str(output)
    
    if _hac_syntax: output = hac_syntax(output)
    
    return output

# 0.13.0
def t(*values:object,hac_syntax:bool=ON,sep:str='',start:str='',end:str=''):
    '''\
    Same as "text"
    
    Return -> str
    '''
    
    output = text(l2str(values),_hac_syntax=hac_syntax,sep=sep,start=start,end=end)
    
    return output


### PAUSE ###

# 0.1.0
def sleep(secs:float=0):
    '''\
    sleep([second]) -> Pause some seconds

    Pause script for some seconds.


    Return None -> None
    '''

    time.sleep(secs)

# 0.8.0
def pause(secs:float=0):
    '''\
    pause([second]) -> Pause some seconds

    Pause script for some seconds.


    Return None -> None
    '''

    time.sleep(secs)

# 0.8.0
def wait(secs:float=0):
    '''\
    wait([second]) -> Pause some seconds

    Pause script for some seconds.


    Return None -> None
    '''

    time.sleep(secs)


### MOUSE POSITION ###

# 0.1.0
def get_mouse_x():
    '''\
    Get mouse x


    Return mouse x -> int
    '''
    
    return get_mouse_position()[0]

# 0.1.0
def get_mouse_y():
    '''\
    Get mouse y


    Return mouse y -> int
    '''

    return get_mouse_position()[1]

# 0.1.0
def get_mouse_position():
    '''\
    Get mouse x and y


    Return (x,y) -> tuple
    '''
    
    cursor = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    pos = (cursor.x, cursor.y)
    return (pos[0],pos[1])


### TERMINAL ###

# 0.8.0
def console(command):
    '''\
    Same as os.system
    '''
    
    os.system(command)

# 0.6.0
def clear(x=None):
    '''\
    clear terminal

    print x if x exist
    

    Return None -> None
    '''
    
    console('cls' if os.name in ('nt', 'dos') else 'clear')
    if x!=None: print(x)

# 0.3.0
def cls(x=None):
    '''\
    clear terminal (still there)

    print x if x exist


    Return None -> None
    '''

    print("\033[2J\033[1;1f")
    if x!=None: print(x)

# 0.13.0
def set_console_title(_title:str=''):
    '''\
    Set Console Title
    Return -> None
    '''
    
    ctypes.windll.kernel32.SetConsoleTitleW(_title)

### RANDOM ###

# 0.8.0
def randint(a:int=0,b:int=None):
    '''\
    Get a Random Integer from a to b
    
    Return a Integer -> int
    '''
    
    return random_.randint(a,b)

# 0.8.0
def random(a:int=0,b:int=None):
    '''\
    Get a Random Float from a to b


    Return a Float -> float
    '''

    return random_.uniform(a,b)

# 0.8.0
def choice(population,k:int=1):
    '''\
    Choose k Objects in population


    Return a List -> list
    '''

    return random_.sample(population,k)

# 0.10.0
def shuffle(_list:list):
    '''\
    shuffle a list
    
    Return a List -> list
    '''

    output,l = [],_list
    for i in range(len(l)):
        ran = randint(b=len(l)-1)
        output.append(l[ran]);del l[ran]
    return output


### KEYBOARD ###

# 0.8.0
def is_pressed(key:str):
    '''\
    If "key" is pressing, Return True
    
    If not, Return False


    Return -> bool
    '''

    return kb.is_pressed(key)

# 0.8.0
def is_release(key:str):
    '''\
    If "key" is releasing, Return True
    
    If not, Return False


    Return -> bool
    '''
    
    return kb.is_release(key)

# 0.8.0
def on_press():
    '''\
    Return all pressing keys
    
    Return on pressing keys -> list
    '''
    
    return kb.on_press()

# 0.10.0
def on_release():
    '''\
    Return all releasing keys
    
    Return on releasing keys -> list
    '''
    
    return kb.on_release()

# 0.8.0
def send(key:str):
    '''\
    send some keys


    Return "key" -> str
    '''
    
    kb.send(key)
    return key

# 0.8.0
def waitkey(key:str):
    '''\
    wait until "key" is pressed


    Return -> None
    '''
    
    kb.wait(key)


### FILE ###

# 0.9.0
# 0.13.0 update
def fileget(fname,delimiter=',',comments='#',encoding='utf-8'):
    '''\
    Load a file
    
    
    Usage:
    
    fname -> file name
    
    delimiter -> separator of file
    
    comments -> the opening symbol of comments
    
    encoding -> the encoding of file
    
    Return file contents -> list
    '''
    
    try:
        with open(fname,'r',encoding=encoding) as f:
            return list(csv.reader(filter(lambda row: row[0]!=comments,f)))
    except FileNotFoundError as e:
        raise FileExistException(e)
        

# 0.9.0
def glob(path):
    '''\
    Same as glob.glob
    
    Return all files -> list
    '''
    
    return glob_.glob(path)

# 0.12.1
def exist(path):
    '''\
    return True if file/folder exists
    
    return False if not
    
    Return exists -> bool
    '''
    
    return os.path.exists(path)

# 0.12.1
def if_file(path):
    '''\
    return True if it is a file
    
    return False if not
    
    Return bool -> bool
    '''
    
    return os.path.isfile(path)

# 0.12.1
def is_folder(path):
    '''\
    return True if it is a folder
    
    return False if not
    
    Return bool -> bool
    '''
    
    return os.path.isdir(path)

# 0.12.1
def is_dir(path):
    '''\
    return True if it is a dir
    
    return False if not
    
    Return bool -> bool
    '''
    
    return os.path.isdir(path)

# 0.13.2
def file_dialog(mode='open file',title:str='',initialdir:str='/',filetypes:tuple=(('All files','*.*'),)):
    '''\
    return a string of directory of file/folder
    
    modes:
        "open file"     : open file
        "open files"    : open multi files
        "save file"     : save file
        "save as file"  : save as file
        "ask dir"       : ask directory

    Return directory -> str
    '''
    
    tk.Tk().withdraw()
    
    if   mode=='open file'    : return fdg.askopenfilename  (title=title,initialdir=initialdir,filetypes=filetypes)
    elif mode=='open files'   : return fdg.askopenfilenames (title=title,initialdir=initialdir,filetypes=filetypes)
    elif mode=='save file'    : return fdg.asksaveasfilename(title=title,initialdir=initialdir,filetypes=filetypes)
    elif mode=='save as file' : return fdg.asksaveasfilename(title=title,initialdir=initialdir,filetypes=filetypes)
    elif mode=='ask dir'      : return fdg.askdirectory     (title=title,initialdir=initialdir,filetypes=filetypes)

### PRINT ###

# 0.10.0
def table(content:list,header:list,tablefmt:str="fancy_grid",align:str="center",show_index=False):
    '''\
    return a table
    
    Return table -> str
    '''
    
    return tabulate_(content,header,tablefmt=tablefmt,numalign=align,stralign=align,showindex=show_index)

# 0.11.1
def type_animate(text:str,sep:float=0.1):
    '''\
    a type animation
    
    Return None -> None
    '''
    
    for i in text:
        sys.stdout.write(i)
        sys.stdout.flush()
        wait(sep)

### CLIPBOARD ###

# 0.1.0
def copy(text:str=''):
    '''\
    copy([text]) -> text

    Return text -> str
    '''
    
    pyperclip.copy(text)
    return text

# 0.12.0
def paste(text:str=''):
    '''\
    paste([text]) -> text

    Return text -> str
    '''
    
    pyperclip.paste(text)
    return text


### FUNCTION ###

# 0.13.0
def check_func_arg(_args:dict=None):
    '''\
    check if any arg is None
    
    Usage:
    
    if check_func_arg(locals())==False:
        # do something
    
    
    if any arg is None Return False
    
    else Return True
    '''
    
    values = list(_args.values())
    if values.count(None)>0: return False
    else: return True
    

### OTHER ###

# 0.2.0
def playsound(path:str):
    '''\
    Play some sound


    Return None
    '''

    try: playsound_(path)
    except Exception as e: raise SoundException(e)

# 0.10.0
def ka():
    '''\
    A thing can stock in your code
    
    it's name is "stock" in chinese (卡 kǎ)
    
    
    It can do nothing
    '''
    
    return

# 0.10.0
def pick(
    title:str='',options:list=[],indicator:str='> ',default_index:int=0,
    multi_select:bool=False,
    min_selection_count:int=0,
    options_map=None,
    multi_select_foreground_color:str='COLOR_GREEN',
    multi_select_background_color:str='COLOR_WHITE'
    ):
    '''\
    same as pick2.pick
    
    Return option,index -> str, int
    '''
    
    return pick(
        title=title,options=options,indicator=indicator,default_index=default_index,
        multi_select=multi_select,
        min_selection_count=min_selection_count,
        options_map=options_map,
        multi_select_foreground_color=multi_select_foreground_color,
        multi_select_background_color=multi_select_background_color
        )

# 0.11.2
def time_str(sep:str='_'):
    '''\
    sep default is "_"
    
    
    Get a str of "year" sep "month" sep "date" sep "hour" sep "min" sep "sec"
    
    Return str -> str
    '''
    
    now = Now()
    return f'{now.year()}_{now.mon()}_{now.date()}_{now.hour()}_{now.min()}_{now.sec()}'

# 0.11.2
def exit():
    '''\
    exit script
    
    Return None -> None
    '''
    
    sys.exit()



### CLASS ###

# 0.8.0
class Now:
    def __init__(self):
        self.update()

    # 0.8.0
    def update(self):
        
        now = time.localtime()
        self._year  = now.tm_year
        self._mon   = now.tm_mon
        self._date  = now.tm_mday
        self._hour  = now.tm_hour
        self._min   = now.tm_min
        self._sec   = now.tm_sec
        self._day   = now.tm_wday
        self._yday  = now.tm_yday
        self._isdst = now.tm_isdst
        del now
    
    # 0.8.0
    def get_time(self,type):
        
        if   (type=='year') : return self._year
        elif (type=='mon')  : return self._mon
        elif (type=='date') : return self._date
        elif (type=='hour') : return self._hour
        elif (type=='min')  : return self._min
        elif (type=='sec')  : return self._sec
        elif (type=='day')  : return self._day
        elif (type=='yday') : return self._yday
        elif (type=='isdst'): return self._isdst
        else: return None
    
    # 0.8.0
    def year(self) : return self.get_time('year')
    def mon(self)  : return self.get_time('mon')
    def date(self) : return self.get_time('date')
    def hour(self) : return self.get_time('hour')
    def min(self)  : return self.get_time('min')
    def sec(self)  : return self.get_time('sec')
    def day(self)  : return self.get_time('day')
    def yday(self) : return self.get_time('yday')
    def isdst(self): return self.get_time('isdst')
    
    # 0.11.2
    def get_times(self):
        return {
            'year' :self.year(),
            'month':self.mon(),
            'date' :self.date(),
            'hour' :self.hour(),
            'min'  :self.min(),
            'sec'  :self.sec(),
            'day'  :self.day(),
            'yday' :self.yday(),
            'isdst':self.isdst()
        }
        
    # 0.11.2
    def time_str(self):
        return f'{self.year()}_{self.mon()}_{self.date()}_{self.hour()}_{self.min()}_{self.sec()}'

# 0.8.0
class Path:
    def __init__(self,path):
        self.path = path
        self.info()
    
    # 0.8.0
    def info(self):
        self._full   = os.path.abspath(self.path)
        self._drive  = os.path.splitdrive(self.path)[0]
        self._dir    = os.path.dirname(self.path)
        self._file   = os.path.basename(self.path)
        self._exists = os.path.exists(self.path)
        if self.exists==True: self._size = os.path.getsize(self.path)
        else: self._size = 0
        if os.path.isfile(self._path): self.type='file'
        elif os.path.isdir(self._path): self.type='dir'

    # 0.8.0
    def set(self,NewPath):
        self.path = NewPath
        self.info()
    
    # 0.8.0
    def getinfo(self):
        return {'full':self.full,'drive':self.drive,'dir':self.dir,'file':self.file,'exists':self.exists,'size':self.size,'type':self.type}


# 0.12.0
class Thread:
    def __init__(self,func):
        self._do = threading.Thread(target=func)
    
    # 0.12.0
    def start(self):
        self._do.start()
    
    # 0.12.0
    def stop(self):
        self._do._stop()

   
# 0.13.1
class Syntax:
    def __init__(self,before,after):
        self._before = before
        self._after  = after
    
    # 0.13.1
    def trans(self,_str):
        return _str \
        .replace(f'\{self._before}','༼ై༽༽ై༼༼ై༽') \
        .replace(self._before,self._after) \
        .replace('༼ై༽༽ై༼༼ై༽',self._before)

