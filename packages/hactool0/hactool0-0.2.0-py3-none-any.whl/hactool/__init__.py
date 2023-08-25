

def listtostr(list:list=[],sep:str=""):
    '''
    listtostr([list],[sep]) -> a string

    Return a string.
    '''

    return sep.join(map(str,list)) 


def strtolist(string:str="",sep:str=" "):
    '''
    strtolist([str],[sep]) -> a list
    
    Return a list.
    '''

    l=[]
    if sep != "":
        l = list(string.split(sep))
        return l
    else:
        for i in string:
            l.append(i)
        return l


def strtotuple(string:str="",sep:str=" "):
    '''
    strtotuple([str],[sep]) -> a tuple
    
    Return a tuple.
    '''

    l=[]
    if sep != "":
        t = tuple(string.split(sep))
        return t
    else:
        for i in string:
            t.append(i)
        return t


def sleep(secs:int=0):
    '''
    sleep([second]) -> pause some seconds

    Pause script for some seconds.

    Return None
    '''

    from time import sleep
    sleep(secs)


def copy(text:str=""):
    '''
    copy([text]) -> text

    Return text    
    '''

    from pyperclip import copy
    copy(text)
    return text



def get_mouse_x():
    '''
    Get mouse x

    Return mouse x
    '''

    from pyautogui import position
    return position()[0]


def get_mouse_y():
    '''
    Get mouse y

    Return mouse y
    '''

    from pyautogui import position
    return position()[1]


def get_mouse_position():
    '''
    Get mouse x and y

    Return (x,y)
    '''

    return tuple(get_mouse_x(),get_mouse_y())


def playsound(path:str):
    '''
    Play some sound

    Return None
    '''

    from playsound import playsound
    try:
        playsound(path)
    except:
        raise "Can't play the sound"