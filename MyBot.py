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
    def registerInitialState(self, gameState: GameState):
        CaptureAgent.registerInitialState(self, gameState)
        self.game = gameState
        self.legalPositions = [p for p in gameState.getWalls().asList(False) if p[1] > 1]

        self.eaten = 0
        self.initFoodList(gameState.getInitialAgentPosition(self.index), gameState)

    def initFoodList(self, position, gameState):
        from pacman.util import manhattanDistance
        tempFood = []
        numrows = len(list(self.getFood(gameState)))
        numcols = len(list(self.getFood(gameState)[0]))

        self.foodList = []
        for i in range(numrows):
            for j in range(numcols):
                if gameState.hasFood(i, j) and self.getFood(gameState)[i][j]:
                    self.foodList.append((i, j))

        self.foodList.sort(key=lambda x: manhattanDistance(x, position))
        return self.foodList

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
        foodList = list(self.getFood(self.game))
        
        myState = gameState.getAgentState(self.index)
        myPos = myState.getPosition()
        actions = gameState.getLegalActions(self.index)

        if myPos == self.findReturnPos():
            self.eaten = 0
            self.initFoodList(myPos, gameState)
        
        if self.eaten > 4:
            pos = self.findReturnPos()
        else:
            pos = self.findReturnPos()
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
            if dist > succDist and action != "Jump_East" and action != "Jump_West" and action != "Jump_North" and action != "Jump_South":
                minDist = succDist
                bestA = action
            elif dist > succDist + 2:
                minDist = succDist
                bestA = action

        if minDist == 0:
            self.initFoodList(myPos, gameState)
            self.eaten += 1

        return bestA

class AgentTwo(CaptureAgent):
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
        self.indexEnemies = self.getOpponents(gameState)
    
    def chooseAction(self, gameState: GameState) -> str:
        actions = gameState.getLegalActions(self.index)
        if "FREEZE" in actions != -1: actions.remove("FREEZE")
        
        enemie1 = gameState.getAgentPosition(self.indexEnemies[0]) 
        enemie2 = gameState.getAgentPosition(self.indexEnemies[1])

        if enemie1[0] > enemie2[0]:
            if self.red:
                posX = enemie2[0]
                posY = enemie2[1]
            else:
                posX = enemie1[0]
                posY = enemie1[1]
        else:
            if self.red:
                posX = enemie1[0]
                posY = enemie1[1]
            else:
                posX = enemie2[0]
                posY = enemie2[1]
        
        if self.red:
            if posX > 16:
                posX = 16
        else:
            if posX < 17:
                posX = 17
        
        myState = gameState.getAgentState(self.index)
        myPos = myState.getPosition()
        curDistance = abs(myPos[0] - posX) + abs(myPos[1] - posY)

        for action in actions:
            gameState.generateSuccessor(self.index, action)
            newPos = myState.getPosition()
            dist = abs(newPos[0] - posX) + abs(newPos[1] - posY)
            if dist < curDistance:
                return action

        return random.choice(actions)