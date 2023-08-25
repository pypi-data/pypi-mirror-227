"""
A Scrambler for Clock Rubik's Cube
"""
from pyTwistyScrambler import clockScrambler

def scClock(type:str="wca"):
    '''
    scClock([type])

    Return a scramble -> str

    Types:
    wca -> WCA Scramble
    jaap -> JAAP Scramble
    con -> CONCISE Scramble
    epo -> EFFICITEN PIN ORDER Scramble
    '''

    if type.lower()=="wca":
        return clockScrambler.get_WCA_scramble()
    elif type.lower()=="jaap":
        return clockScrambler.get_face_turn_metric_scramble()
    elif type.lower=="con":
        return clockScrambler.get_twist_metric_scramble()
    elif type.lower=="epo":
        return clockScrambler.get_twist_metric_scramble()
    

def scClock_wca():
    '''
    Return a Clock WCA Scramble -> str
    '''

    return str(scClock("wca"))


def scClock_JAAP():
    '''
    Return a Clock JAAP Scramble -> str
    '''
    
    return str(scClock("jaap"))


def scClock_Concise():
    '''
    Return a Clock CONCISE Scramble -> str
    '''
    
    return str(scClock("con"))


def scClock_EfficitenPinOrder():
    '''
    Return a Clock EFFICITEN PIN ORDER Scramble -> str
    '''
    
    return str(scClock("epo"))