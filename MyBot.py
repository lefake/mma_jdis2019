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
    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at baselineTeam.py for more details about how to
    create an agent as this is the bare minimum.
    """

    def registerInitialState(self, gameState: GameState):
        """
        This method handles the initial setup of the
        agent to populate useful fields (such as what team
        we're on).

        A distanceCalculator instance caches the maze distances
        between each pair of positions, so your agents can use:
        self.distancer.getDistance(p1, p2)

        IMPORTANT: This method may run for at most 5 seconds.
        """

        '''
        Make sure you do not delete the following line. If you would like to
        use Manhattan distances instead of maze distances in order to save
        on initialization time, please take a look at
        CaptureAgent.registerInitialState in captureAgents.py.
        '''
        CaptureAgent.registerInitialState(self, gameState)

        '''
        Your initialization code goes here, if you need any.
        '''

    def chooseAction(self, gameState: GameState) -> str:
        """
        Picks among legal actions randomly.
        """
        actions = gameState.getLegalActions(self.index)

        return random.choice(actions)


class AgentTwo(CaptureAgent):
    def registerInitialState(self, gameState: GameState):
        CaptureAgent.registerInitialState(self, gameState)
    
    def chooseAction(self, gameState: GameState) -> str:
        capMultiplier = 3

        if self.red:
            capsules = gameState.getRedCapsules()
        else:
            capsules = gameState.getBlueCapsules()

        foodList = list(self.getFood(gameState))
        actions = gameState.getLegalActions(self.index)
                
        meanX = 0
        meanY = 0
        
        for i in range(len(foodList)):
            meanX = meanX + foodList[i][0]
            meanY = meanY + foodList[i][1]

        for cap in capsules:
            meanX = capMultiplier* meanX + cap[0]
            meanY = capMultiplier* meanY + cap[1]

        meanX = int(meanX/len(foodList))
        meanY = int(meanY/len(foodList))

        myState = gameState.getAgentState(self.index)
        myPos = myState.getPosition()

        curDistance = abs(myPos[0] - meanX) + abs(myPos[1] - meanY)


        '''if meanX > myPos[0]:
            if actions.__contains__('East'):
                return 'East'
        if meanX <= myPos[0]
            if actions.__contains__('West'):
                return 'West'
        if meanY > myPos[1]:
            if actions.__contains__('East'):
                return 'East'
        if meanY <= myPos[1]
            if actions.__contains__('West'):
                return 'West'
        '''


        for action in actions:
            gameState.generateSuccessor(self.index, action)
            newPos = myState.getPosition()
            dist = abs(newPos[0] - meanX) + abs(newPos[1] - meanY)
            if dist < curDistance:
                return action

        return random.choice(actions)
