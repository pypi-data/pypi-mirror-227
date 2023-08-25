"""
A Scrambler for 2x2x2 Rubik's Cube
"""
from pyTwistyScrambler import scrambler222

def sc2(type:str="wca"):
    '''
    sc2([type])

    Return a scramble -> str

    Types:
    wca -> WCA Scramble
    ran -> RANDOM Scramble
    opt -> Optimal Scramble
    '''

    if type.lower()=="wca":
        return scrambler222.get_WCA_scramble()
    elif type.lower()=="ran":
        return scrambler222.get_random_scramble()
    elif type.lower()=="opt":
        return scrambler222.get_optimal_scramble()



def sc2_wca():
    '''
    Return a 2x2 WCA Scramble -> str
    '''

    return str(sc2("wca"))


def sc2_random():
    '''
    Return a 2x2 RANDOM Scramble -> str
    '''
    
    return str(sc2("ran"))


def sc2_optimal():
    '''
    Return a 2x2 OPTIMAL Scramble -> str
    '''
    
    return str(sc2("opt"))