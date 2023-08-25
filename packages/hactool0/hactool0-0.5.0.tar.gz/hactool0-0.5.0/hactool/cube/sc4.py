"""
A Scrambler for 4x4x4 Rubik's Cube
"""
from pyTwistyScrambler import scrambler444

def sc4(type:str="wca",len:int=40):
    '''
    sc4([type],len)

    Return a scramble -> str

    Types:
    wca -> WCA Scramble
    bld -> BLD Scramble
    sign -> SIGN Scramble
    ran -> Random Scramble
    edge -> Edge Scramble
    '''

    if type.lower()=="wca":
        return scrambler444.get_random_state_scramble(n=len)
    elif type.lower()=="bld":
        return scrambler444.get_4BLD_scramble(n=len)
    elif type.lower()=="sign":
        return scrambler444.get_SiGN_scramble(n=len)
    elif type.lower()=="ran":
        return scrambler444.get_WCA_scramble(n=len)
    elif type.lower()=="edge":
        return scrambler444.get_edges_scramble(n=len)
    

def sc4_wca(len:int=40):
    '''
    Return a 4x4 WCA Scramble -> str
    '''

    return str(sc4("wca",len))


def sc4_bld(len:int=40):
    '''
    Return a 4x4 BLD Scramble -> str
    '''
    
    return str(sc4("bld",len))


def sc4_sign(len:int=40):
    '''
    Return a 4x4 SIGN Scramble -> str
    '''
    
    return str(sc4("sign",len))


def sc4_random(len:int=40):
    '''
    Return a 4x4 RANDOM Scramble -> str
    '''
    
    return str(sc4("ran",len))


def sc4_edge(len:int=8):
    '''
    Return a 4x4 EDGE Scramble -> str
    '''
    
    return str(sc4("edge",len))