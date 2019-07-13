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
    return [OffensiveAgent(firstIndex), DefensiveAgent(secondIndex)]

##########
# Agents #
##########

class OffensiveAgent(CaptureAgent):
    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at baselineTeam.py for more details about how to
    create an agent as this is the bare minimum.
    """
    
    def initFoodList(self):
        tempFood = []
        numrows = len(list(self.getFood(self.game)))   
        numcols = len(list(self.getFood(self.game)[0]))
        
        self.foodList = []
        for i in range(numrows):
            for j in range(numcols):
                if self.getFood(self.game)[i][j]:
                    self.foodList.append((i, j))
                    
        print(self.foodList)
    
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
        self.game = gameState
        print(self.game.getLegalActions(self.index))

        self.initFoodList()
        
        myState = gameState.getAgentState(self.index)
        myPos = myState.getPosition()
        actions = gameState.getLegalActions(self.index)
        
        minDistance = 99999
        index = None
        
        
        
        for i in range(len(self.foodList)):
           foodX = self.foodList[i][0]
           foodY = self.foodList[i][1]
           distance = abs(myPos[0] - foodX) + abs(myPos[1] - foodY)
           if distance < minDistance:
              minDistance = distance
              index = i
        
        self.path = []
        self.path = self.aStarSearch(gameState, foodX, foodY)
        
        self.food = 0
        
        self.game = gameState
        myState = gameState.getAgentState(self.index)
        pos = myState.getPosition()
        
        self.initialPos = pos
        
        '''
        Your initialization code goes here, if you need any.
        '''

    def chooseAction(self, gameState: GameState) -> str:
        """
        Picks among legal actions randomly.
        """

            
        
        if len(self.path) == 0:
            if len(list(self.getFood(self.game))) <= 5:
              #self.breadthSearchWithPos(gameState, self.initialPos) 
              bob = 1+1
            else:
                self.breadthSearch(gameState) 

        
        
        
        return self.path.pop(0)
            

    
    def aStarSearch(self, gameState, foodx, foody):
        """Search the node that has the lowest combined cost and heuristic first."""
        from pacman.util import manhattanDistance
        
        #Declare both nodes
        
        myState = gameState.getAgentState(self.index)
        myPos = myState.getPosition()
        
        position = (foodx,foody)
        
        firstNode = (gameState, [], 0) 
        secondNode= (gameState, [], 0) 


        openList = []
        closedList = []

        openList.append(firstNode)
        while True:
            if not openList:
                return []
            
            openList.sort(key=lambda x: x[2] + manhattanDistance(x[0].getAgentPosition(self.index), position))
            firstNode = openList.pop(0)
            closedList.append(firstNode)
            if firstNode[0].getAgentPosition(self.index) == position:
                print (firstNode[1])
                return firstNode[1]
            else:
                print (firstNode[1] , position)
            successors = []    
            
            for action in firstNode[0].getLegalActions(self.index) :
                if action.find("Jump") == -1 and action.find("FREEZE") == -1:
                    successors.append((gameState.generateSuccessor(self.index, action), action, 1))

            for x in successors:
                path = firstNode[1]
                path.append(x[1])
                secondNode = (x[0], path , x[2] + firstNode[2])
                
                #ClosedList
                mappedClosedList = list(map(lambda x: x[0].getAgentPosition(self.index), closedList))
                mappedOpenList = list(map(lambda x: x[0].getAgentPosition(self.index), openList))
                if secondNode[0].getAgentPosition(self.index) in mappedClosedList:
                    indexElement = mappedClosedList.index(secondNode[0].getAgentPosition(self.index))
                    if secondNode[2] < closedList[indexElement][2]: 
                        closedList.pop(indexElement)
                        openList.append(secondNode)

                #OpenList
                elif secondNode[0].getAgentPosition(self.index) in mappedOpenList:
                    indexElement = mappedOpenList.index(secondNode[0].getAgentPosition(self.index))
                    if secondNode[2] < openList[indexElement][2] :
                        openList.pop(indexElement)
                        openList.append(secondNode)

                #Neither
                else :
                    openList.append(secondNode)

        return []

    
    def breadthSearch(self, gameState):
        
        openList = [(gameState, [], 0, 0, [])]
        while not len(openList) == 0:
            openList.sort(key=lambda x: x[2])
            state = openList.pop(0)
            actions = state[0].getLegalActions(self.index)
            for action in actions :
                newGameState = gameState.generateSuccessor(self.index, action)
                myState = newGameState.getAgentState(self.index)
                newPos = myState.getPosition()
                
                if newPos in state[1]:
                    break

                newPath = state[1]
                newPath.append(action)
                newCost = state[2] + 1
                
                if self.red:
                    if newGameState.getBlueFood()[int(newPos[0])][int(newPos[1])]:
                        return newPath
                else:
                    if newGameState.getRedFood()[int(newPos[0])][int(newPos[1])]:
                        return newPath
                     
                    
                if action.find("skip") != -1:
                    if state[3] > 0:
                        break
                    openList.append((newGameState, newPath, newCost, 4, state[1]))
                else:

                    newCost += 5
                    openList.append((newGameState, newPath, newCost, state[3]-1, state[1]))
            
    def breadthSearchWithPos(self, gameState, goalPos):
        
        openList = (gameState, [], 0)
        while not len(openList) == 0:
            state = openList.pop(0)
            actions = state[0].getLegalActions(self.index)
            for action in actions :
                newGameState = gameState.generateSuccessor(self.index, action)
                myState = newGameState.getAgentState(self.index)
                newPos = myState.getPosition()


                newPath = state[1]
                newPath.append(action)
                newCost = state[2] + 1
                
                if newPos == goalPos:
                   return newPath
                   
                if action.find("skip") != -1:
                    openList.append((newGameState, newPath, newCost))
                else:
                    newCost += 5
                    openList.append((newGameState, newPath, newCost))
            
                   
        
        
        
class DefensiveAgent(CaptureAgent):
    def registerInitialState(self, gameState: GameState):
        CaptureAgent.registerInitialState(self, gameState)
    
    def chooseAction(self, gameState: GameState) -> str:
        actions = gameState.getLegalActions(self.index)
        return random.choice(actions)
