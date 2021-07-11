from numpy.core.fromnumeric import choose
from captureGraphicsDisplay import PacmanGraphics
import random
import copy
class StateMachine:
    def __init__(self,p):
        self.p = p
        pass
        
    def getmove(self,distance,corridor_type,state):
        if distance > self.p[0]:
            move = self.explore(corridor_type,state)
        else:
            move = self.retreat(corridor_type,state)
        return move

    def choose_move(self,p,state):
        print(state.getLegalActions(0), "estado")
        print(p, "p")
        # never stop pacman
        a = copy.deepcopy(p)
        a.append(0)
        print(a,'a')
        escolha = random.choices(state.getLegalActions(0),cum_weights=a)
        
        return escolha[0] 

    def explore(self,corridor_type,state):
        next_move = ""
        if corridor_type == "+":
            next_move = self.choose_move(self.p[1:5],state)
        elif corridor_type == "L":
            next_move = self.choose_move(self.p[5:7],state)
        elif corridor_type == "T":
            next_move = self.choose_move(self.p[7:10],state)
        elif corridor_type == "C":
            next_move = self.choose_move(self.p[10:12],state)
        elif corridor_type == "":
            next_move = random.choice( state.getLegalActions( 0 ) )
        
        print("explore")
        return next_move

    def retreat(self,corridor_type,state):
        
#        if corridor_type == "C":
#            next_move = 
#        elif corridor_type == "L":
#            next_move = 
#        elif corridor_type == "T":
#            next_move = 
#        elif corridor_type == "+":
#            next_move =        
#        elif corridor_type == "":
#            next_move = random.choice( state.getLegalActions( 0 ) )
        print("retreat")
        next_move = random.choice( state.getLegalActions( 0 ) )
        return next_move