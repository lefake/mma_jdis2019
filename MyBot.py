# MyBot.py
# ---------
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

import random
from pacman.game import Directions
import pacman.util as util # Free utility functions like Stack or Queue ! 
from pacman.capture import GameState
from pacman.captureAgents import CaptureAgent

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed):
    """
    This function should return a list of two agents that will form the
    team, initialized using firstIndex and secondIndex as their agent
    index numbers. isRed is True if the red team is being created, and
    will be False if the blue team is being created.
    """

    # The following line is an example only; feel free to change it.
    return [AgentOne(firstIndex), AgentTwo(secondIndex)]

##########
# Agents #
##########

class AgentOne(CaptureAgent):
    def initFoodList(self):
        tempFood = []
        numrows = len(list(self.getFood(self.game)))   
        numcols = len(list(self.getFood(self.game)[0]))
        
        self.foodList = []
        for i in range(numrows):
            for j in range(numcols):
                if self.getFood(self.game)[i][j]:
                    self.foodList.append((i, j))

    def registerInitialState(self, gameState: GameState):
        CaptureAgent.registerInitialState(self, gameState)
        self.game = gameState
        self.legalPositions = [p for p in gameState.getWalls().asList(False) if p[1] > 1]
        self.hasEaten = False

    def findReturnPos(self):
        if self.red:
            posX = 16
            posY = 8
            while self.game.hasWall(posX, posY):
                posY = (posY + 1)%18
        else:
            posX = 18
            posY = 8
            while self.game.hasWall(posX, posY):
                posY = (posY + 1)%18
        return (posX, posY)

    def chooseAction(self, gameState: GameState) -> str:
        self.initFoodList()
        actions = gameState.getLegalActions(self.index)
        if "FREEZE" in actions != -1: actions.remove("FREEZE")
        if "Stop" in actions: actions.remove("Stop")        

        foodList = list(self.getFood(self.game))
        
        myState = gameState.getAgentState(self.index)
        myPos = myState.getPosition()
        actions = gameState.getLegalActions(self.index)

        self.initFoodList()
        if myPos == self.findReturnPos():
          self.hasEaten = False
        
        if self.hasEaten:
          pos = self.findReturnPos()
        else:
          for food in self.foodList:
            if gameState.hasFood(food[0], food[1]):
              pos = food
          
        bestA = actions[0]
        i = gameState.getRedTeamIndices()[0]
        dist = self.getMazeDistance(pos, myPos)
        minDist = dist
        bestA = actions[0]
        for action in actions:
              
          succ = gameState.generateSuccessor(self.index, action)
          myPosSucc = succ.getAgentPosition(self.index)
          succDist = self.getMazeDistance(pos, myPosSucc)
          if dist > succDist and action != "FREEZE" and action != "Stop":
            minDist = succDist
            bestA = action

        if minDist == 0:
          self.hasEaten = True

        return bestA

class AgentTwo(CaptureAgent):
    def initFoodDefList(self):
        tempFood = []
        numrows = len(list(self.getFoodYouAreDefending(self.game)))   
        numcols = len(list(self.getFoodYouAreDefending(self.game)[0]))
        
        self.foodDefList = []
        for i in range(numrows):
            for j in range(numcols):
                if self.getFoodYouAreDefending(self.game)[i][j]:
                    self.foodDefList.append((i, j))


    def registerInitialState(self, gameState: GameState):
        CaptureAgent.registerInitialState(self, gameState)
        self.game = gameState
        self.initFoodDefList()
    
    def chooseAction(self, gameState: GameState) -> str:
        capMultiplier = 2

        if self.red:
            capsules = gameState.getRedCapsules()
        else:
            capsules = gameState.getBlueCapsules()

        foodList = list(self.getFood(gameState))
        actions = gameState.getLegalActions(self.index)
        if "FREEZE" in actions != -1: actions.remove("FREEZE")
        if "Stop" in actions: actions.remove("Stop")
        
        meanX = 0
        meanY = 0
        
        for i in range(len(self.foodDefList)):
            meanX = meanX + self.foodDefList[i][0]
            meanY = meanY + self.foodDefList[i][1]

        for cap in capsules:
            meanX = capMultiplier* meanX + cap[0]
            meanY = capMultiplier* meanY + cap[1]

        meanX = int(meanX/len(foodList))
        meanY = int(meanY/len(foodList))

        myState = gameState.getAgentState(self.index)
        myPos = myState.getPosition()

        curDistance = abs(myPos[0] - meanX) + abs(myPos[1] - meanY)

        for action in actions:
            gameState.generateSuccessor(self.index, action)
            newPos = myState.getPosition()
            dist = abs(newPos[0] - meanX) + abs(newPos[1] - meanY)
            if dist < curDistance:
                return action

        return random.choice(actions)