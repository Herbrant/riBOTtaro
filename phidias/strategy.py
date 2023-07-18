import sys

from pathlib import Path
CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../lib")

from phidias.Types import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

class go_to(Belief): pass

# --------------------------------------------------------------------
# Target Queue
# --------------------------------------------------------------------
class queue_element(Belief): pass
class add(Procedure): pass
class go(Procedure): pass
class clear(Procedure): pass

# --------------------------------------------------------------------
# Minitarget Queue
# --------------------------------------------------------------------
class minitarget(Belief): pass
class add_minitarget(Procedure): pass
class clear_minitarget(Procedure): pass
class go_to_minitarget(Procedure): pass
class minitarget_reached(Reactor): pass

# --------------------------------------------------------------------
# Web Socket
# --------------------------------------------------------------------
class add_minitarget_reactor(Reactor): pass  
class go_to_minitarget_reactor(Reactor): pass
class target_reached(Reactor): pass


def_vars('X', 'Y', 'F')

# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------
class main(Agent):
    def main(self):
        # Target queue
        add(X,Y) >> [ +queue_element(X,Y), show_line("Aggiunto (", X, ",", Y, ") alla coda di target.") ]
        go() / queue_element(X,Y) >> [ -queue_element(X,Y), go(X,Y), show_line("Nuovo target: (", X, ",", Y, ")"), go() ]
        clear() / queue_element(X,Y) >> [ -queue_element(X,Y), clear(), show_line("La coppia (", X, ",", Y, ") è stata cancellata.") ]
        
        # Minitarget queue
        add_minitarget(X,Y) >> [ +minitarget(X,Y) ]
        clear_minitarget() / minitarget(X,Y) >> [ -minitarget(X,Y), show_line("Rimozione minitarget...") ]
        
        # Web socket
        
        # richiede al path planner i mini-target
        go(X,Y) >> [ clear_minitarget(), +go_to(X,Y)[{'to': 'robot@127.0.0.1:6567'}] ]
        
        # invia al robot il minitarget da raggiungere
        go_to_minitarget() / minitarget(X,Y) >> [ +go_to(X,Y)[{'to': 'robot@127.0.0.1:6566'}] ]
        
        # handler per il raggiungimento del minitarget
        +target_reached()[{'from': F}] >> [ show_line("minitarget raggiunto"), clear_minitarget(), go_to_minitarget() ]
        
        # handler per il path planner
        +add_minitarget_reactor(X,Y)[{'from': F}] >> [ show_line(F, ": add_minitarget(", X, ",", Y, ")."), add_minitarget(X,Y) ]
        +go_to_minitarget_reactor()[{'from': F}] >> [ show_line(F, ": go_to_minitarget_reactor"), go_to_minitarget() ]

ag = main()
ag.start()

PHIDIAS.run_net(globals(), 'http')
PHIDIAS.shell(globals())
