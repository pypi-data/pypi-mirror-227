"""
A Scrambler for Megaminx Rubik's Cube
"""
from pyTwistyScrambler import megaminxScrambler

def scMega(type:str="wca",len:int=40):
    '''
    scMega([type])

    Return a scramble -> str

    Types:
    wca -> WCA Scramble
    car -> CARROT Scramble
    old -> OLD STYLE Scramble
    '''

    if type.lower()=="wca":
        return megaminxScrambler.get_WCA_scramble(len)
    elif type.lower()=="CAR":
        return megaminxScrambler.get_Carrot_scramble(len)
    elif type.lower=="OLD":
        return megaminxScrambler.get_old_style_scramble(len)
    

def scMega_wca(len=70):
    '''
    Return a Sqare-1 WCA Scramble -> str
    '''

    return str(scMega("wca",len))


def scMega_carrot(len:int=70):
    '''
    Return a Sqare-1 CARROT Scramble -> str
    '''
    
    return str(scMega("car",len))


def scMega_oldStyle(len:int=70):
    '''
    Return a Sqare-1 OLD STYLE Scramble -> str
    '''
    
    return str(scMega("old",len))