"""
This is hactool!
"""

# -*- coding: utf-8 -*-

########## INFO ##########
__version__ = "0.14.1"

########## IMPORT LIBRARIES ##########

import csv
import ctypes
import glob as glob_
import json
import os
import random as random_
import sys
import types
import threading
import time
import tkinter as tk
import webbrowser
from getpass import getpass
from tkinter import filedialog as fdg

import keyboard as kb
import pyperclip
from .module import pick as pick_
from .module import tabulate as tabulate_

########## EXCEPTION ##########

class SoundException       (Exception): pass
class FileExistException   (Exception): pass

########## VAR ##########

NEWTAB = "newtab"
NEWWIN = "newwin"

########## MAIN ##########


### COLORS ###

# 0.11.0

reset        = "\033[0m"
bold         = "\033[01m"
disable      = "\033[02m"
underline    = "\033[04m"
reverse      = "\033[07m" # reverse color
i            = "\033[09m" # strike through
invisible    = "\033[08m" # hide

# fg
black        = "\033[30m"
red          = "\033[31m"
green        = "\033[32m"
orange       = "\033[33m"
blue         = "\033[34m"
purple       = "\033[35m"
cyan         = "\033[36m"
lightgrey    = "\033[37m"
darkgrey     = "\033[90m"
lightred     = "\033[91m"
lightgreen   = "\033[92m"
yellow       = "\033[93m"
lightblue    = "\033[94m"
pink         = "\033[95m"
lightcyan    = "\033[96m"

# bg
bg_black     = "\033[40m"
bg_red       = "\033[41m"
bg_green     = "\033[42m"
bg_orange    = "\033[43m"
bg_blue      = "\033[44m"
bg_purple    = "\033[45m"
bg_cyan      = "\033[46m"
bg_lightgrey = "\033[47m"


### FORMAT ###

# 0.14.0
def toString(inp, sep=""):
    '''\
    turn list, tuple and set into string
    '''
    if type(inp) in [list, tuple, set]:
        return sep.join(map(str, inp))

# 0.14.0
def toList(inp, sep:str=" "):
    '''\
    turn str, tuple and set into list
    '''
    if type(inp) in [str]:
        return list(inp.split(sep))
    if type(inp) in [tuple, set]:
        return list(inp)

# 0.14.0
def toTuple(inp, sep:  str=" "):
    '''\
    turn str, list and set into tuple
    '''
    if type(inp) in [str]:
        return tuple(inp.split(sep))
    if type(inp) in [list, set]:
        return tuple(inp)

# 0.14.0
def toSet(inp, sep=" "):
    '''\
    turn str, list and tuple into set
    '''
    output = set()
    if type(inp)==str: inp = toList(inp, sep)
    if type(inp) in [list, tuple]:
        for i in inp: output.add(i)
        return output


# 0.13.2
def list_format(list_:list=[], format_=str):
    return list(map(lambda x: format_(x), list_))

# 0.13.1
def hac_syntax(text):
    syntaxes = [
        Syntax('$n;', '\n'),
        Syntax('$comma;', ', '),
        Syntax('$period;', '.'),
        Syntax('$bang;', '!'),
        Syntax('$quos;', '?'),
        Syntax('$colon;', ':'),
        Syntax('$semi;', ';'),
        Syntax('$dash;', '-'),
        Syntax('$lparen;', '('),
        Syntax('$rparen;', ')'),
        Syntax('$lsqubra;', '['),
        Syntax('$rsqubra;', ']'),
        Syntax('$lbrace;', '{'),
        Syntax('$rbrace;', '}'),
        Syntax('$lang;', '<'),
        Syntax('$rang;', '>'),
        Syntax('$apost;', "'"),
        Syntax('$slash;', '/'),
        Syntax('$bslash;', '\\'),
        Syntax('$under;', '_'),
        Syntax('$pipe;', '|'),
        Syntax('$tilde;', '~'),
        Syntax('$backtick;', '`'),
        Syntax('$at;', '@'),
        Syntax('$hash;', '#'),
        Syntax('$dollar;', '$'),
        Syntax('$per;', '%'),
        Syntax('$caret;', '^'),
        Syntax('$and;', '&'),
        Syntax('$aster;', '*'),
        Syntax('$plus;', '+'),
        Syntax('$min;', '-'),
        Syntax('$mul;', '×'),
        Syntax('$div;', '÷'),
        Syntax('$equ;', '='),
    ]

    output = text

    for i in syntaxes: output = i.trans(output)

    return output


# 0.13.0
def text(*values:object, hac_syntax_=False, sep:str='', start:str='', end:str=''):
    '''\
    Format text
    Return -> str
    '''

    output = [start]

    for i in values: output.extend([str(i), sep])

    output.pop()
    output.append(end)
    output = toString(output)

    if hac_syntax_: output = hac_syntax(output)

    return output

# 0.13.0
def t(*values:object, hac_syntax_:bool=True, sep:str='', start:str='', end:str=''):
    '''\
    Same as "text"
    Return -> str
    '''

    output = text(toString(values), hac_syntax_=hac_syntax_, sep=sep, start=start, end=end)

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

    Return (x, y) -> tuple
    '''

    cursor = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    pos = (cursor.x, cursor.y)
    return (pos[0], pos[1])


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
    clear terminal

    print x if x exist

    Return None -> None
    '''

    print("\033[2J\033[1;1f")
    if x!=None: print(x)

# 0.13.0
def set_console_title(title_:str=''):
    '''\
    Set Console Title
    Return -> None
    '''

    ctypes.windll.kernel32.SetConsoleTitleW(title_)

# 0.14.0
def input_password(prompt=""):
    '''\
    Get input that is invisible

    Return input -> str
    '''
    return getpass(prompt=prompt)

# 0.15.0
def terminal_size():
    '''\
    get size of the terminal

    return (width, height) -> tuple
    '''
    return tuple(os.get_terminal_size())

### RANDOM ###

# 0.8.0
def randint(a:int=0, b:int=None):
    '''\
    Get a Random Integer from a to b
    Return a Integer -> int
    '''
    if b==None: return random_.randint(0, a)
    if b!=None: return random_.randint(a, b)

# 0.8.0
def random(a:int=None, b:int=None):
    '''\
    Get a Random Float from a to b

    Return a Float -> float
    '''
    if b==None: return random_.uniform(0, a)
    if b!=None: return random_.uniform(a, b)

# 0.8.0
def choice(population, k:int=1):
    '''\
    Choose k Objects in population

    Return a List -> list
    '''

    return random_.sample(population, k)

# 0.10.0
def shuffle(list_:list):
    '''\
    shuffle a list
    Return a List -> list
    '''

    output, l = [], list_
    for i in range(len(l)):
        ran = randint(b=len(l)-1)
        output.append(l[ran])
        del l[ran]
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

# 0.15.0
def press_and_released(key: str):
    if (is_pressed(key)):
        while (is_pressed(key)): pass
        return True
    else: return False

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

# 0.15.0
def add_hotkey(hotkey, func, args=(), suppress=False, timeout=1, trigger_on_release=False):
    '''\
    add a hotkey
    '''
    kb.add_hotkey(hotkey, func, args, suppress, timeout, trigger_on_release)

### BROWSER ###

# 0.15.0
def open_url(url, mode=NEWTAB):
    '''\
    open link in browser
    '''
    if (mode==NEWTAB): webbrowser.open_new_tab(url)
    if (mode==NEWWIN): webbrowser.open_new(url)


### FILE ###

# 0.15.0
def txtget(fname, encoding='utf-8'):
    '''\
    Load a txt file


    Usage:

    fname -> file name

    encoding -> the encoding of file

    Return file contents -> string
    '''

    try:
        with open(fname, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError as e:
        raise FileExistException(e)

# 0.9.0
# 0.13.0 update
# 0.14.0
def csvget(fname, delimiter=', ', comments='#', encoding='utf-8'):
    '''\
    Load a csv file


    Usage:

    fname -> file name

    delimiter -> separator of file

    comments -> the opening symbol of comments

    encoding -> the encoding of file
    Return file contents -> list
    '''

    try:
        with open(fname, 'r', encoding=encoding) as f:
            return list(csv.reader(filter(lambda row: row[0]!=comments, f)))
    except FileNotFoundError as e:
        raise FileExistException(e)

# 0.14.0
def jsonget(fname, encoding='utf-8'):
    '''\
    Load a json file


    Usage:

    fname -> file name

    encoding -> the encoding of file

    Return file contents -> dict
    '''

    try:
        with open(fname, 'r', encoding=encoding) as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise FileExistException(e)

# 0.9.0
def glob(pathname):
    '''\
    Same as glob.glob
    Return all files -> list
    '''

    return glob_.glob(pathname)

# 0.12.1
def exist(path):
    '''\
    return True if file/folder exists

    return False if not

    Return exists -> bool
    '''

    return os.path.exists(path)

# 0.12.1
def is_file(path):
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
def file_dialog(mode='open file', title:str='', initialdir:str='/', filetypes:tuple=(('All files', '*.*'), )):
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

    if   mode=='open file'    : return fdg.askopenfilename  (title=title, initialdir=initialdir, filetypes=filetypes)
    elif mode=='open files'   : return fdg.askopenfilenames (title=title, initialdir=initialdir, filetypes=filetypes)
    elif mode=='save file'    : return fdg.asksaveasfilename(title=title, initialdir=initialdir, filetypes=filetypes)
    elif mode=='save as file' : return fdg.asksaveasfilename(title=title, initialdir=initialdir, filetypes=filetypes)
    elif mode=='ask dir'      : return fdg.askdirectory     (title=title, initialdir=initialdir, filetypes=filetypes)

### PRINT ###

# 0.10.0
def table(content:list, header:list, tablefmt:str="fancy_grid", align:str="center", show_index=False):
    '''\
    return a table

    Return table -> str
    '''

    return tabulate_.tabulate(content, header, tablefmt=tablefmt, num_align=align, str_align=align, show_index=show_index)

# 0.11.1
def type_animate(text:str, sep:float=0.1):
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


### OTHER ###

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
    title:str='', options:list=[], indicator:str='> ', default_index:int=0,
    multi_select:bool=False,
    min_selection_count:int=0,
    options_map=None,
    multi_select_fg:str='COLOR_GREEN',
    multi_select_bg:str='COLOR_WHITE'
    ):
    '''\
    same as pick2.pick
    Return option, index -> str, int
    '''

    return pick_.pick(
        title=title, options=options, indicator=indicator, default_index=default_index,
        multi_select=multi_select,
        min_selection_count=min_selection_count,
        options_map=options_map,
        multi_select_foreground_color=multi_select_fg,
        multi_select_background_color=multi_select_bg
        )

# 0.11.2
def time_str(format_: str='$Y/$mn/$D ($d) $H:$m:$s'):
    '''\
    $Y  xxxx year
    $y  xx year
    $Mo month
    $mo month(short)
    $mn month(number)
    $D  date
    $d  day
    $H  24 hour
    $h  12 hour
    $m  minute
    $s  second
    $yd yday
    $wd wday
    $i  isdst

    Return str -> str
    '''

    now = Now()
    return now.time_str(format_)


# 0.11.2
def exit(x:str=""):
    '''\
    print x then exit script
    Return None -> None
    '''

    print(x)
    sys.exit()

# 0.15.0
def just_try(func):
    try: return func()
    except: pass

# 0.15.0
def apply(obj, *func):
    """\
    apply functions to object
    """
    for f in func:
        obj = f(obj)
    return obj

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
        if now.tm_wday==0: self._day = 'Monday'
        if now.tm_wday==2: self._day = 'Tuesday'
        if now.tm_wday==3: self._day = 'Wednesday'
        if now.tm_wday==4: self._day = 'Thursday'
        if now.tm_wday==5: self._day = 'Friday'
        if now.tm_wday==6: self._day = 'Saturday'
        if now.tm_wday==7: self._day = 'Sunday'
        self._yday  = now.tm_yday
        self._wday  = now.tm_wday + 1
        self._isdst = bool(now.tm_isdst)
        del now

    # 0.8.0
    def get_time(self, type):

        if   (type=='year') : return self._year
        elif (type=='mon')  : return self._mon
        elif (type=='date') : return self._date
        elif (type=='hour') : return self._hour
        elif (type=='min')  : return self._min
        elif (type=='sec')  : return self._sec
        elif (type=='day')  : return self._day
        elif (type=='yday') : return self._yday
        elif (type=='wday') : return self._wday
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
    def wday(self) : return self.get_time('wday')
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
    def time_str(self, format_:str='$Y/$mn/$D ($d) $H:$m:$s'):

        d_month = { 'January': 'Jan.'  , 'February': 'Feb.', 'March'    : 'Mar.', 'April'   : 'Apr.' , 'May'     : 'May.', 'June': 'June.', 
                    'July'   : 'July.' , 'August'  : 'Aug.', 'September': 'Sep.', 'October' : 'Oct.' , 'November': 'Nov.', 'December:': 'Dec.', }
        l_month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', ]
        return format_ \
            .replace('$Y'  , str(self.year())) \
            .replace('$Mo' , l_month[int(self.mon())-1]) \
            .replace('$mo' , d_month[l_month[int(self.mon())-1]]) \
            .replace('$mn' , str(self.mon())) \
            .replace('$D'  , str(self.date())) \
            .replace('$d'  , str(self.day())) \
            .replace('$H'  , str(self.hour())) \
            .replace('$h'  , str(self.hour()) if self.hour()<12 else str(self.hour()-12)) \
            .replace('$m'  , str(self.min())) \
            .replace('$s'  , str(self.sec())) \
            .replace('$yd' , str(self.yday())) \
            .replace('$y'  , str(self.year())[2:])  \
            .replace('$wd' , str(self.wday()) ) \
            .replace('$i'  , str((self.isdst())))


# 0.12.0
class Thread:
    def __init__(self, target):
        self._do = threading.Thread(target=target)

    # 0.12.0
    def start(self):
        self._do.start()

    # 0.12.0
    def stop(self):
        self._do._stop()


# 0.13.1
class Syntax:
    def __init__(self, before, after):
        self._before = before
        self._after  = after

    # 0.13.1
    def trans(self, str_):
        return str_ \
        .replace(f'\{self._before}', '༼ై༽༽ై༼༼ై༽') \
        .replace(self._before, self._after) \
        .replace('༼ై༽༽ై༼༼ై༽', self._before)

