'''Python Plus'''

'''
Versions:

┌───────────┬───────────┐
│    pyp    │  hactool  │
├───────────┼───────────┤
│   0.0.1   │   0.13.2  │
├───────────┼───────────┤
│   0.0.2   │   0.13.3  │
├───────────┼───────────┤
│           │           │
└───────────┴───────────┘
'''

import sys
import __init__ as ht

# 0.0.2
ON  = True
OFF = False
T   = True
F   = False
N   = None

# 0.0.1
def print(*values:object, start:str='', sep:str='', end:str='\n'):

    ht.list_format(values)
    text = sep.join(values)
    text = str(start) + str(text)
    text += str(end)

    sys.stdout.write(text)
    sys.stdout.flush()


