# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from statemachine import StateMachine
from pacman import Directions
from game import Agent
import random
import game
import util
from statemachine import StateMachine
from util import manhattanDistance
class LeftTurnAgent(game.Agent):
    "An agent that turns left at every opportunity"

    def getAction(self, state):
        legal = state.getLegalPacmanActions()
        current = state.getPacmanState().configuration.direction
        if current == Directions.STOP: current = Directions.NORTH
        left = Directions.LEFT[current]
        if left in legal: return left
        if current in legal: return current
        if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
        if Directions.LEFT[left] in legal: return Directions.LEFT[left]
        return Directions.STOP

class GreedyAgent(Agent):
    def __init__(self, evalFn="scoreEvaluation"):
        self.evaluationFunction = util.lookup(evalFn, globals())
        assert self.evaluationFunction != None

    def getAction(self, state):
        # Generate candidate actions
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)

        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        scored = [(self.evaluationFunction(state), action) for state, action in successors]
        bestScore = max(scored)[0]
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        return random.choice(bestActions)

class evolAgent( Agent ):
  """
  Evolutionary Agent.
  """
  def __init__(self, p):
      self.index = 0
      self.p = p
      self.statemachine = StateMachine(p)

  def getCorridorType(self,state):
      pac_pos = state.getPacmanPosition()
      corridor_type = ""
      front = state.hasWall(pac_pos[0]+1,pac_pos[1])
      back = state.hasWall(pac_pos[0]-1,pac_pos[1])#atras
      left = state.hasWall(pac_pos[0],pac_pos[1]+1)#direita 
      right = state.hasWall(pac_pos[0],pac_pos[1]-1)#esquerda
      if (front and back and left and right):
          corridor_type = "+"
      elif(() or ()):
          corridor_type = ""
      return corridor_type

  def getAction( self, state ):
    #print(state.getPacmanState())
    #distance = manhattanDistance(pacmanpostion, ghostposition)
    #print(state.getGhostPositions())
    ghostpositions = state.getGhostPositions()
    distances = []
    for ghostposition in ghostpositions:
        distance = manhattanDistance(ghostposition, state.getPacmanPosition())
        distances.append(distance)
        print(manhattanDistance(state.getPacmanPosition(), ghostposition))
    min_distance = min(distances)
    
    #move = self.statemachine.getmove(distance)

    return random.choice( state.getLegalActions( self.index ) )

def scoreEvaluation(state):
    return state.getScore()
