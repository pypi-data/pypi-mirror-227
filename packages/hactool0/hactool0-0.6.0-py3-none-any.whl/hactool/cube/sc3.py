"""
A Scrambler for 3x3x3 Rubik's Cube
"""
from pyTwistyScrambler import scrambler333

def sc3(type:str="wca"):
    '''
    sc3([type])

    Return a scramble -> str

    Types:
    wca -> WCA Scramble
    bld -> BLD Scramble
    ran -> Random Scramble
    edge -> Edge Only Scramble
    corn -> Corner Only Scramble
    ll -> Lst Layer Scramble
    lsll -> Last Slot & Last Layer Scramble
    zbll -> ZBLL Scramble
    zzll -> ZZLL Scramble
    zbls -> ZBLS Scramble
    f2l -> F2L Scramble
    lse -> LSE Scramble
    eo -> EOline Scramble
    cmll -> CMLL Scramble
    cll -> CLL Scramble
    ell -> ELL Scramble
    ezc -> Easy Cross Scramble
    ru -> 2-gen RU only Scramble
    mu -> 2-gen MU Only Scramble
    fru -> 3-gen FRU Only Scramble
    rul -> 3-gen RUL Only Scramble
    hto -> Half Turns Scramble
    '''

    if type.lower()=="wca":
        return scrambler333.get_WCA_scramble()
    elif type.lower()=="bld":
        return scrambler333.get_3BLD_scramble()
    elif type.lower()=="ran":
        return scrambler333.get_random_scramble()
    elif type.lower()=="edge":
        return scrambler333.get_edges_scramble()
    elif type.lower()=="corn":
        return scrambler333.get_corners_scramble()
    elif type.lower()=="ll":
        return scrambler333.get_LL_scramble()
    elif type.lower()=="lsll":
        return scrambler333.get_LSLL_scramble()
    elif type.lower()=="zbll":
        return scrambler333.get_ZBLL_scramble()
    elif type.lower()=="zzll":
        return scrambler333.get_ZZLL_scramble()
    elif type.lower()=="zbls":
        return scrambler333.get_ZBLS_scramble()
    elif type.lower()=="f2l":
        return scrambler333.get_F2L_scramble()
    elif type.lower()=="lse":
        return scrambler333.get_LSE_scramble()
    elif type.lower()=="eo":
        return scrambler333.get_EOLine_scramble()
    elif type.lower()=="cmll":
        return scrambler333.get_CMLL_scramble()
    elif type.lower()=="cll":
        return scrambler333.get_CLL_scramble()
    elif type.lower()=="ell":
        return scrambler333.get_ELL_scramble()
    elif type.lower()=="ezc":
        return scrambler333.get_easy_cross_scramble()
    elif type.lower()=="ru":
        return scrambler333.get_2genRU_scramble()
    elif type.lower()=="mu":
        return scrambler333.get_2genMU_scramble()
    elif type.lower()=="fru":
        return scrambler333.get_3genFRU_scramble()
    elif type.lower()=="rul":
        return scrambler333.get_3genRrU_scramble()
    elif type.lower()=="hto":
        return scrambler333.get_half_turns_scramble()


def sc3_wca():
    '''
    Return a 3x3 WCA Scramble -> str
    '''

    return str(sc3("wca"))


def sc3_bld():
    '''
    Return a 3x3 BLD Scramble -> str
    '''
    
    return str(sc3("bld"))


def sc3_random():
    '''
    Return a 3x3 RANDOM Scramble -> str
    '''
    
    
    return str(sc3("ran"))


def sc3_edge():
    '''
    Return a 3x3 EDGE Scramble -> str
    '''
        
    return str(sc3("edge"))


def sc3_corner():
    '''
    Return a 3x3 CORNER Scramble -> str
    '''
    
    return str(sc3("corn"))


def sc3_ll():
    '''
    Return a 3x3 LAST LAYER Scramble -> str
    '''
    
    return str(sc3("ll"))

def sc3_zsll():
    '''
    Return a 3x3 ZSLL Scramble -> str
    '''
    
    return str(sc3("lsll"))


def sc3_zbll():
    '''
    Return a 3x3 ZBLL Scramble -> str
    '''
    
    return str(sc3("zbll"))


def sc3_zzll():
    '''
    Return a 3x3 ZZLL Scramble -> str
    '''
    
    return str(sc3("zzll"))


def sc3_zbls():
    '''
    Return a 3x3 ZBLS Scramble -> str
    '''
    
    return str(sc3("zbls"))


def sc3_f2l():
    '''
    Return a 3x3 F2L Scramble -> str
    '''
    
    return str(sc3("f2l"))


def sc3_lse():
    '''
    Return a 3x3 LSE Scramble -> str
    '''
    
    return str(sc3("lse"))


def sc3_eoline():
    '''
    Return a 3x3 EOLINE Scramble -> str
    '''
    
    return str(sc3("eo"))


def sc3_cmll():
    '''
    Return a 3x3 CMLL Scramble -> str
    '''
    
    return str(sc3("cmll"))


def sc3_cll():
    '''
    Return a 3x3 CLL Scramble -> str
    '''
    
    return str(sc3("cll"))


def sc3_ell():
    '''
    Return a 3x3 ELL Scramble -> str
    '''
    
    return str(sc3("ell"))


def sc3_easy_cross():
    '''
    Return a 3x3 EASY CROSS Scramble -> str
    '''
    
    return str(sc3("ezc"))


def sc3_2gen_RU():
    '''
    Return a 3x3 2-GEN Scramble with only RU moves -> str
    '''
    
    return str(sc3("ru"))


def sc3_2gen_MU():
    '''
    Return a 3x3 2-GEN Scramble with only MU moves -> str
    '''
    
    return str(sc3("mu"))


def sc3_3gen_FRU():
    '''
    Return a 3x3 3-GEN Scramble with only FRU moves -> str
    '''
    
    return str(sc3("fru"))


def sc3_3gen_RUL():
    '''
    Return a 3x3 3-GEN Scramble with only RUL moves -> str
    '''
    
    return str(sc3("rul"))


def sc3_helf_turns():
    '''
    Return a 3x3 Scramble with only HALF TURNS -> str
    '''
    
    return str(sc3("hto"))