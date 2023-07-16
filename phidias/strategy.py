import sys

from pathlib import Path
CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../lib")

from phidias.Types import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

# --------------------------------------------------------------------
# Queue
# --------------------------------------------------------------------
class queue_element(Belief): pass
class add(Procedure): pass
class go(Procedure): pass
class clear(Procedure): pass

# --------------------------------------------------------------------
# Web Socket
# --------------------------------------------------------------------
class go_to(Belief): pass
class target_reached(Reactor): pass


def_vars('X', 'Y', 'F')

# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------
class main(Agent):
    def main(self):
        add(X,Y) >> [ +queue_element(X,Y) ]
        go() / queue_element(X,Y) >> [ -queue_element(X,Y), go(X,Y), show_line("Nuovo target: (", X, ",", Y, ")")]
        clear() / queue_element(X,Y) >> [ -queue_element(X,Y), clear(), show_line("La coppia (", X, ",", Y, ") è stata cancellata.") ]
        
        # Web socket
        go(X,Y) >> [ +go_to(X,Y)[{'to': 'robot@127.0.0.1:6566'}] ]
        +target_reached()[{'from':F}] >> [ show_line("Target raggiunto"), go() ]

ag = main()
ag.start()

PHIDIAS.run_net(globals(), 'http')
PHIDIAS.shell(globals())
