"""
A Scrambler for 7x7x7 Rubik's Cube
"""
from pyTwistyScrambler import scrambler777

def sc7(type:str="wca",len:int=60):
    '''
    sc7([type],len)

    Return a scramble -> str

    Types:
    wca -> WCA Scramble
    sign -> SIGN Scramble
    ran -> Random Scramble
    edge -> Edge Scramble
    '''

    if type.lower()=="wca":
        return scrambler777.get_random_state_scramble(n=len)
    elif type.lower()=="sign":
        return scrambler777.get_SiGN_scramble(n=len)
    elif type.lower()=="ran":
        return scrambler777.get_WCA_scramble(n=len)
    elif type.lower()=="edge":
        return scrambler777.get_edges_scramble(n=len)
    

def sc7_wca(len:int=40):
    '''
    Return a 7x7 WCA Scramble -> str
    '''

    return str(sc7("wca",len))


def sc7_sign(len:int=40):
    '''
    Return a 7x7 SIGN Scramble -> str
    '''
    
    return str(sc7("sign",len))


def sc7_random(len:int=40):
    '''
    Return a 7x7 RANDOM Scramble -> str
    '''
    
    return str(sc7("ran",len))


def sc7_edge(len:int=8):
    '''
    Return a 7x7 EDGE Scramble -> str
    '''
    
    return str(sc7("edge",len))