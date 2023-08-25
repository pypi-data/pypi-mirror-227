"""
A Scrambler for 6x6x6 Rubik's Cube
"""
from pyTwistyScrambler import scrambler666

def sc6(type:str="wca",len:int=60):
    '''
    sc6([type],len)

    Return a scramble -> str

    Types:
    wca -> WCA Scramble
    sign -> SIGN Scramble
    ran -> Random Scramble
    edge -> Edge Scramble
    '''

    if type.lower()=="wca":
        return scrambler666.get_random_state_scramble(n=len)
    elif type.lower()=="sign":
        return scrambler666.get_SiGN_scramble(n=len)
    elif type.lower()=="ran":
        return scrambler666.get_WCA_scramble(n=len)
    elif type.lower()=="edge":
        return scrambler666.get_edges_scramble(n=len)
    

def sc6_wca(len:int=40):
    '''
    Return a 6x6 WCA Scramble -> str
    '''

    return str(sc6("wca",len))


def sc6_sign(len:int=40):
    '''
    Return a 6x6 SIGN Scramble -> str
    '''
    
    return str(sc6("sign",len))


def sc6_random(len:int=40):
    '''
    Return a 6x6 RANDOM Scramble -> str
    '''
    
    return str(sc6("ran",len))


def sc6_edge(len:int=8):
    '''
    Return a 6x6 EDGE Scramble -> str
    '''
    
    return str(sc6("edge",len))