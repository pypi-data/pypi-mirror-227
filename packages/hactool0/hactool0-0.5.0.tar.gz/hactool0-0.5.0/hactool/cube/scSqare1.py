"""
A Scrambler for Sqare-1 Rubik's Cube
"""
from pyTwistyScrambler import squareOneScrambler

def scSqare(type:str="wca",len:int=40):
    '''
    scSqare([type])

    Return a scramble -> str

    Types:
    wca -> WCA Scramble
    ftm -> FACE TURN METRIC Scramble
    tm -> TWIST METRIC Scramble
    '''

    if type.lower()=="wca":
        return squareOneScrambler.get_WCA_scramble()
    elif type.lower()=="ftm":
        return squareOneScrambler.get_face_turn_metric_scramble(n=len)
    elif type.lower=="tm":
        return squareOneScrambler.get_twist_metric_scramble(n=len)
    

def scSqare_wca():
    '''
    Return a Sqare-1 WCA Scramble -> str
    '''

    return str(scSqare("wca"))


def scSqare_FaceTurnMetric(len:int=40):
    '''
    Return a Sqare-1 FACE TURN METRIC Scramble -> str
    '''
    
    return str(scSqare("ftm",len))


def scSqare_TwistMetric(len:int=20):
    '''
    Return a Sqare-1 TWIST METRIC Scramble -> str
    '''
    
    return str(scSqare("tm",len))