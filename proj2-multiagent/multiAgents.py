# multiAgents.py
# --------------
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


from sys import int_info
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newGhostPos = successorGameState.getGhostPositions()
        newFoodPos = newFood.asList()
        if min(newScaredTimes) == 0 and (newPos in newGhostPos):
            return -1.0
        if newPos in currentGameState.getFood().asList(): # TODO: Why newFoodPos doesn't work?
            return 1.0
        ghostDis = [util.manhattanDistance(newPos, x) for x in newGhostPos]
        foodDis = [util.manhattanDistance(newPos, x) for x in newFoodPos]
        return 1.0 / min(foodDis) - 1.0 / min(ghostDis)

        

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """

    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        ghostIndex = [i for i in range(1,gameState.getNumAgents())]
        def terminal(gameState, depth):
            return gameState.isWin() or gameState.isLose() or self.depth == depth
        
        def max_value(gameState, depth):
            if (terminal(gameState, depth)):
                return self.evaluationFunction(gameState)
            v = -9999999
            for action in gameState.getLegalActions(0):
                v = max(v, min_value(gameState.generateSuccessor(0, action), depth, 1))
            return v


        def min_value(gameState, depth, ghost):
            if (terminal(gameState, depth)):
                return self.evaluationFunction(gameState)
            v = 9999999
            for action in gameState.getLegalActions(ghost):
                if ghost == ghostIndex[-1]:
                    v = min(v, max_value(gameState.generateSuccessor(ghost, action), depth+1))
                else:
                    v = min(v, min_value(gameState.generateSuccessor(ghost, action), depth, ghost+1))
            return v

        result = [(action, min_value(gameState.generateSuccessor(0, action), 0, 1)) for action in gameState.getLegalActions()]
        result.sort(key=lambda x: x[1]) 
        return result[-1][0] 


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        ghostIndex = [i for i in range(1,gameState.getNumAgents())]
        def terminal(gameState, depth):
            return gameState.isWin() or gameState.isLose() or self.depth == depth
        
        def max_value(gameState, depth, alpha, beta):
            if (terminal(gameState, depth)):
                return self.evaluationFunction(gameState)
            v = -9999999
            for action in gameState.getLegalActions(0):
                v = max(v, min_value(gameState.generateSuccessor(0, action), depth, 1, alpha, beta))
                if v > beta: return v
                alpha = max(alpha, v)
            return v


        def min_value(gameState, depth, ghost, alpha, beta):
            if (terminal(gameState, depth)):
                return self.evaluationFunction(gameState)
            v = 9999999
            for action in gameState.getLegalActions(ghost):
                if ghost == ghostIndex[-1]:
                    v = min(v, max_value(gameState.generateSuccessor(ghost, action), depth+1, alpha, beta))
                else:
                    v = min(v, min_value(gameState.generateSuccessor(ghost, action), depth, ghost+1, alpha, beta))
                if v < alpha: return v
                beta = min(beta, v)
            return v

        alpha = -9999999
        beta = 9999999
        v = -9999999
        act = None 
        for action in gameState.getLegalActions(0):
            tmp = min_value(gameState.generateSuccessor(0, action), 0, 1, alpha, beta)
            if v < tmp:
                v = tmp
                act = action 
            if v > beta:
                return v
            alpha = max(alpha, v) 
        return act  


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        ghostIndex = [i for i in range(1,gameState.getNumAgents())]
        def terminal(gameState, depth):
            return gameState.isWin() or gameState.isLose() or self.depth == depth
        
        def max_value(gameState, depth):
            if (terminal(gameState, depth)):
                return self.evaluationFunction(gameState)
            v = -9999999
            for action in gameState.getLegalActions(0):
                v = max(v, e_value(gameState.generateSuccessor(0, action), depth, 1))
            return v


        def e_value(gameState, depth, ghost):
            if (terminal(gameState, depth)):
                return self.evaluationFunction(gameState)
            v = 0
            for action in gameState.getLegalActions(ghost):
                if ghost == ghostIndex[-1]:
                    v += max_value(gameState.generateSuccessor(ghost, action), depth+1)
                else:
                    v += e_value(gameState.generateSuccessor(ghost, action), depth, ghost+1)

            return v / len(gameState.getLegalActions(ghost))

        result = [(action, e_value(gameState.generateSuccessor(0, action), 0, 1)) for action in gameState.getLegalActions()]
        result.sort(key=lambda x: x[1]) 
        return result[-1][0] 

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    foodPos = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostPos = currentGameState.getGhostPositions()
    inf = -999999999
    if min(scaredTimes) == 0 and (pos in ghostPos):
        return inf 
    score = 0
    if len(currentGameState.getCapsules()) < 2:
        score += 100
    ghostDis = [util.manhattanDistance(pos, x) for x in ghostPos]
    foodDis = [util.manhattanDistance(pos, x) for x in foodPos]
    if len(foodDis) == 0 or len(ghostDis) == 0:
        score += scoreEvaluationFunction(currentGameState) + 10
    else:
        score += scoreEvaluationFunction(currentGameState) + 10 / min(foodDis)
    return score 
    

# Abbreviation
better = betterEvaluationFunction
