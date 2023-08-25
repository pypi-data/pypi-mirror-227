"""
A Scrambler for Pyraminx Rubik's Cube
"""
from pyTwistyScrambler import pyraminxScrambler

def scPyraminx(type:str="wca"):
    '''
    scPyraminx([type])

    Return a scramble -> str

    Types:
    wca -> WCA Scramble
    opt -> Optimal Scramble
    '''

    if type.lower()=="wca":
        return pyraminxScrambler.get_WCA_scramble()
    elif type.lower()=="opt":
        return pyraminxScrambler.get_optimal_scramble()



def scPyraminx_wca():
    '''
    Return a Pyraminx WCA Scramble -> str
    '''

    return str(scPyraminx("wca"))


def scPyraminx_optimal():
    '''
    Return a Pyraminx OPTIMAL Scramble -> str
    '''
    
    return str(scPyraminx("opt"))