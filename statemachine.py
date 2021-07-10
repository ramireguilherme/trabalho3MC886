from captureGraphicsDisplay import PacmanGraphics
class StateMachine:
    def __init__(self,p):
        self.p = p
        pass

    def getCorridorType():
        
        pass
    def getmove(self,distance):
        corridor_type = self.getCorridorType()
        if distance > self.p[0]:
            move = self.expore(corridor_type)
        else:
            move = self.retreat(corridor_type)

    def explore(self,corridor_type):
#        if corridor_type == "I":
 #           next_move = random(self.p)
  #      elif corridor_type == "L":
   #         pass
    #    return next_move
        pass
    def retreat(self,corridor_type):
#        if corridor_type == "I":
 #           next_move = 
  #          pass
   #     elif corridor_type == "L":
    #        pass
     #   return next_move
        pass