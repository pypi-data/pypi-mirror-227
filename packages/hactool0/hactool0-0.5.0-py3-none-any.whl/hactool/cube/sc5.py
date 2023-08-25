"""
A Scrambler for 5x5x5 Rubik's Cube
"""
from pyTwistyScrambler import scrambler555

def sc5(type:str="wca",len:int=60):
    '''
    sc5([type],len)

    Return a scramble -> str

    Types:
    wca -> WCA Scramble
    bld -> BLD Scramble
    sign -> Sign Scramble
    ran -> Random Scramble
    edge -> Edge Scramble
    '''

    if type.lower()=="wca":
        return scrambler555.get_random_state_scramble(n=len)
    elif type.lower()=="bld":
        return scrambler555.get_4BLD_scramble(n=len)
    elif type.lower()=="sign":
        return scrambler555.get_SiGN_scramble(n=len)
    elif type.lower()=="ran":
        return scrambler555.get_WCA_scramble(n=len)
    elif type.lower()=="edge":
        return scrambler555.get_edges_scramble(n=len)
    

def sc5_wca(len:int=40):
    '''
    Return a 5x5 WCA Scramble -> str
    '''

    return str(sc5("wca",len))


def sc5_bld(len:int=40):
    '''
    Return a 5x5 BLD Scramble -> str
    '''
    
    return str(sc5("bld",len))


def sc5_sign(len:int=40):
    '''
    Return a 5x5 SUGN Scramble -> str
    '''
    
    return str(sc5("sign",len))


def sc5_random(len:int=40):
    '''
    Return a 5x5 RANDOM Scramble -> str
    '''
    
    return str(sc5("ran",len))


def sc5_edge(len:int=8):
    '''
    Return a 5x5 EDGE Scramble -> str
    '''
    
    return str(sc5("edge",len))