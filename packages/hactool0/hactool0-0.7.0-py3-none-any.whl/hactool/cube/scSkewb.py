"""
A Scrambler for Skewb Rubik's Cube
"""
from pyTwistyScrambler import skewbScrambler

def scSkewb(type:str="wca"):
    '''
    scSkewb([type])

    Return a scramble -> str

    Types:
    wca -> WCA Scramble
    ulrb -> ULRB Scramble
    '''

    if type.lower()=="wca":
        return skewbScrambler.get_WCA_scramble()
    elif type.lower()=="urlb":
        return skewbScrambler.get_ULRB_scramble
    

def scSkewb_wca():
    '''
    Return a Skewb WCA Scramble -> str
    '''

    return str(scSkewb("wca"))


def scSkewb_URLB():
    '''
    Return a Skewb URLB Scramble -> str
    '''
    
    return str(scSkewb("urlb"))