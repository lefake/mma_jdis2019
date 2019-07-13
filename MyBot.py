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
        self.initFoodList()

    def chooseAction(self, gameState: GameState) -> str:
        actions = gameState.getLegalActions(self.index)
        if "FREEZE" in actions != -1: actions.remove("FREEZE")
        if "Stop" in actions: actions.remove("Stop")
        if "Jump_East" in actions: actions.remove("Jump_East")
        if "Jump_West" in actions: actions.remove("Jump_West")
        if "Jump_West" in actions: actions.remove("Jump_West")
        if "Jump_North" in actions: actions.remove("Jump_North")
        if "Jump_South" in actions: actions.remove("Jump_South")
        
        myState = gameState.getAgentState(self.index)
        myPos = myState.getPosition()

        closest = self.foodList[0]

        for food in self.foodList:
            if self.getMazeDistance(myPos, food) < self.getMazeDistance(myPos, closest):
                closest = food

        
        
        return random.choice(actions)


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
        if "Jump_East" in actions: actions.remove("Jump_East")
        if "Jump_West" in actions: actions.remove("Jump_West")
        if "Jump_West" in actions: actions.remove("Jump_West")
        if "Jump_North" in actions: actions.remove("Jump_North")
        if "Jump_South" in actions: actions.remove("Jump_South")
        
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