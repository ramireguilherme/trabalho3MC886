from game import Agent
from game import Directions
import numpy as np
import random

def enqueue(Q, e):
    Q.append(e)

def dequeue(Q):
    e = Q[0]
    del Q[0]
    return e

def isInGraph(x, y, width, height):
    return x >= 0 and y >= 0 and y < height and x < width

# ! A Q-value for a particular state-action combination is representative of the "quality" of an action taken from that state. 
# ! Better Q-values imply better chances of getting greater rewards.


class RLAgent(Agent):
    QTable = {}
    def __init__( self, alpha = 0.7, gamma = 0.9, epsilon = 0.3 ):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.actions = {'North': 0, 'East': 1, 'South': 2, 'West': 3, 'Stop': 4}
        self.possibleActions = ['North', 'East', 'South', 'West', 'Stop']

    def getNeighbours(self, x, y, width, height, state):
        n = []
        if state.hasWall(x, y):
            return []
        if isInGraph(x - 1, y, width, height) and not state.hasWall(x - 1, y):
            n.append((x-1, y))
        if isInGraph(x + 1, y, width, height) and not state.hasWall(x + 1, y):
            n.append((x + 1, y))
        if isInGraph(x, y + 1, width, height) and not state.hasWall(x, y + 1):
            n.append((x, y + 1))
        if isInGraph(x, y - 1, width, height) and not state.hasWall(x, y - 1):
            n.append((x, y - 1))
        return n

    # def initializeGraph(self, state):
    #     width, height = state.layout.width, state.layout.height
    #     getArrayIndex = lambda i, j: i*width + j
    #     self.mazeGraph = np.zeros(width * height, width * height)
    #     for i in range(height):
    #         for j in range(width):
    #             if state.hasWall(i, j):
    #                 continue
    #             elif isInGraph(i - 1, j, width, height) and not state.hasWall(i - 1, j):
    #                 self.mazeGraph[getArrayIndex(i, j), getArrayIndex(i - 1, j)] = 1
    #             elif isInGraph(i + 1, j, width, height) and not state.hasWall(i + 1, j):
    #                 self.mazeGraph[getArrayIndex(i, j), getArrayIndex(i + 1, j)] = 1
    #             elif isInGraph(i, j + 1, width, height) and not state.hasWall(i, j + 1):
    #                 self.mazeGraph[getArrayIndex(i, j), getArrayIndex(i, j + 1)] = 1
    #             elif isInGraph(i, j - 1, width, height) and not state.hasWall(i, j - 1):
    #                 self.mazeGraph[getArrayIndex(i, j), getArrayIndex(i, j - 1)] = 1 

    def getClosestFoodDistance(self, state):
        width, height = state.data.layout.width, state.data.layout.height

        visited = np.zeros((width, height))
        distanceFromPacman = np.zeros((width, height))
        pacmanPosition = state.getPacmanPosition()

        visited[pacmanPosition] = 1
        Q = []
        enqueue(Q, pacmanPosition)
        while len(Q) > 0:
            u = dequeue(Q)
            if distanceFromPacman[u] > 0 and state.hasFood(u[0], u[1]):
                return distanceFromPacman[u], u
            neighbours = self.getNeighbours(u[0], u[1], width, height, state)
            for v in neighbours:
                if np.equal(0, visited[v]):
                    visited[v] = 1
                    distanceFromPacman[v] = distanceFromPacman[u] + 1
                    enqueue(Q, v)
            visited[u] = 1
        return 0, pacmanPosition

    def getClosestGhostDistance(self, state):
        width, height = state.data.layout.width, state.data.layout.height
        ghosts = state.getGhostPositions()

        visited = np.zeros((width, height))
        distanceFromPacman = np.zeros((width, height))
        pacmanPosition = state.getPacmanPosition()

        visited[pacmanPosition] = 1
        Q = []
        enqueue(Q, pacmanPosition)
        while len(Q) > 0:
            u = dequeue(Q)
            for ghost in ghosts:
                if distanceFromPacman[u] > 0 and ghost == u:
                    return distanceFromPacman[u], u
            neighbours = self.getNeighbours(u[0], u[1], width, height, state)
            for v in neighbours:
                if np.equal(0, visited[v]):
                    visited[v] = 1
                    distanceFromPacman[v] = distanceFromPacman[u] + 1
                    enqueue(Q, v)
            visited[u] = 1
        return 0, pacmanPosition


    def fruitInRadius(self, radius, state):
        width, height = state.data.layout.width, state.data.layout.height
        n = 0
        pacmanPosition = state.getPacmanPosition()
        for x in range(pacmanPosition[0] - radius, pacmanPosition[0] + radius + 1): 
            for y in range(pacmanPosition[1] - radius, pacmanPosition[1] + radius + 1):
                if isInGraph(x, y, width, height) and state.hasFood(x, y):
                    n += 1
        return n

    def ghostsInRadius(self, radius, state):
        width, height = state.data.layout.width, state.data.layout.height
        ghosts, scaredGhosts = 0, 0
        ghostPositions = state.getGhostPositions()
        ghostStates = state.getGhostStates()
        pacmanPosition = state.getPacmanPosition()
        for i in range(len(ghostPositions)):
            if ghostPositions[i][0] >= pacmanPosition[0] - radius and ghostPositions[i][0] <= pacmanPosition[0] + radius and ghostPositions[i][1] >= pacmanPosition[1] - radius and ghostPositions[i][1] <= pacmanPosition[1] + radius:
                ghosts += 1
                if ghostStates[i].scaredTimer > 0:
                    scaredGhosts += 1
        return ghosts, scaredGhosts 


    def getRelativeQuadrant(self, pos, pacmanPosition):
        # 2 | 1
        # --|--
        # 3 | 4
        x, y = pos
        pacmanX, pacmanY = pacmanPosition 
        if x > pacmanX and y >= pacmanY:
            return 1
        elif x <= pacmanX and y > pacmanY:
            return 2
        elif x < pacmanX and y <= pacmanY:
            return 3
        elif x >= pacmanX and y < pacmanY:
            return 4
        else:
            return 0



    def getQState(self, state):
        closestFoodDistance, closestFoodPosition = self.getClosestFoodDistance(state)
        fruitIn2Radius = self.fruitInRadius(2, state)
        ghostsInRadius, scaredGhostsInRadius = self.ghostsInRadius(2, state)
        closestGhostDistance, closestGhostPosition = self.getClosestGhostDistance(state)
        pacmanPosition = state.getPacmanPosition()
        return (closestFoodDistance, fruitIn2Radius, self.getRelativeQuadrant(closestFoodPosition, pacmanPosition), ghostsInRadius, scaredGhostsInRadius, ghostsInRadius, closestGhostDistance, self.getRelativeQuadrant(closestGhostPosition, pacmanPosition))
        # return (pacmanPosition, self.getRelativeQuadrant(closestFoodPosition, pacmanPosition), self.getRelativeQuadrant(closestGhostPosition, pacmanPosition))





    def getRewardFromState(self, state):
        reward = 0
        a, b = self.ghostsInRadius(1, state)
        if a > 0:
            reward -= 40
        else:
            reward += 10

        c, _ = self.ghostsInRadius(2, state)
        if c > 0:
            reward -= 15

        if b > 0:
            reward += 10

        if self.fruitInRadius(2, state) > 5:
            reward += 5

        if self.getClosestFoodDistance(state)[0] < 5:
            reward += 15
        else:
            reward -= 1

        if self.getClosestGhostDistance(state)[0] <= 4:
            reward -= 20
        else:
            reward -= 5

        if state.getScore() < 0:
            reward -= 10
        
        if state.getNumFood() == 0:
            reward += 1000

        if state.getNumFood() <= 10:
            reward += 15


        return reward


    def getAction(self, state, training=True):
        self.pacmanPosition = state.getPacmanPosition()
        legal = state.getLegalPacmanActions()
        legal = [a for a in legal if a != Directions.STOP]
        newState = self.getQState(state)



        if newState not in RLAgent.QTable:
            RLAgent.QTable[newState] = np.zeros(5)
        # if state not in RLAgent.QTable:
            # RLAgent.QTable[state] = np.zeros(5)


        #  pacmanPosition (x, y)




        if training:
            if random.uniform(0, 1) < self.epsilon:
                action = random.choice(legal)
            else:
                legalIndexes = [self.actions[i] for i in legal]
                # action = legal[np.argmax(RLAgent.QTable[state][legalIndexes])] 
                action = legal[np.argmax(RLAgent.QTable[newState][legalIndexes])] 

            actionIndex = self.actions[action]       
            # nextState = state.generateSuccessor(0, action)
            nextState = self.getQState(state.generateSuccessor(0, action))
            # reward = self.getRewardFromState(nextState)
            reward = self.getRewardFromState(state.generateSuccessor(0, action))

            if nextState not in RLAgent.QTable:
                RLAgent.QTable[nextState] = np.zeros(5)


            # RLAgent.QTable[state][actionIndex] = (1 - self.alpha) * RLAgent.QTable[state][actionIndex] + self.alpha * (reward + self.gamma * np.max(RLAgent.QTable[nextState]))
            RLAgent.QTable[newState][actionIndex] = (1 - self.alpha) * RLAgent.QTable[newState][actionIndex] + self.alpha * (reward + self.gamma * np.max(RLAgent.QTable[nextState]))
        else:
            # action = legal[np.argmax(RLAgent.QTable[state][legalIndexes])] 
            action = legal[np.argmax(RLAgent.QTable[newState][legalIndexes])] 

        return action

    def final(self, state):
        return


