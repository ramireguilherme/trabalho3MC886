from numpy.core.fromnumeric import choose
from captureGraphicsDisplay import PacmanGraphics
from util import manhattanDistance
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
    def min_x(self,lista):
        n_list = [l[0] for l in lista]
        return n_list(index(min(n_list)))

    def ghost_pacman_pos(self,state):
        ghostpositions = state.getGhostPositions()
        ghost_dict = {ghost:None for ghost in ghostpositions}
        for ghostposition in ghostpositions:
            distance = manhattanDistance(ghostposition, state.getPacmanPosition())
            ghost_dict[ghostposition] = distance
        ghost = min(ghost_dict, key=ghost_dict.get)
        ghost_x,ghost_y = ghost[0],ghost[1]
        pac_x,pac_y = state.getPacmanPosition()[0],state.getPacmanPosition()[1]
        position = ""
        if pac_y < ghost_y and pac_x == ghost_x:
            position = "back"
        elif pac_y < ghost_y and pac_x < ghost_x:
            position = "back_l"
        elif pac_y < ghost_y and pac_x > ghost_x:
            position = "back_r"
        elif pac_y > ghost_y and pac_x < ghost_x:
            position = "forward"
        elif pac_y > ghost_y and pac_x > ghost_x:
            position = "forward_l"
        elif pac_y < ghost_y and pac_x == ghost_x:
            position = "forward_r"
        elif pac_y == ghost_y and pac_x < ghost_x:
            position = "left"
        elif pac_y == ghost_y and pac_x > ghost_x:
            position = "right"

        return position
    def retreat(self,corridor_type,state):
        print(self.ghost_pacman_pos(state), "RELATIVE")
        rel_pos = self.ghost_pacman_pos(state)
        next_move = ""
        if corridor_type == "C":
            if rel_pos == "forward" or "forward_l" or "forward_r":
                next_move = self.choose_move(self.p[12:14],state)
            else:
                next_move = self.choose_move(self.p[14:16],state)
        elif corridor_type == "L":
            if rel_pos == "forward" or "forward_l" or "forward_r":
                next_move = self.choose_move(self.p[16:18],state)
            else:
                next_move = self.choose_move(self.p[18:20],state)
        elif corridor_type == "T":
            if rel_pos == "forward" or "forward_l" or "forward_r":
                next_move = self.choose_move(self.p[20:23],state)
            else:
                next_move = self.choose_move(self.p[23:26],state)
        elif corridor_type == "+":
            if rel_pos == "right" or rel_pos == "forward_r":
                next_move = self.choose_move(self.p[26:30],state)
            else:
                next_move = self.choose_move(self.p[30:34],state)
        elif corridor_type == "" or next_move == "":
            next_move = random.choice( state.getLegalActions( 0 ) )
        print("retreat")
        next_move = random.choice( state.getLegalActions( 0 ) )
        return next_move