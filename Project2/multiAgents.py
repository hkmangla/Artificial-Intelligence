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


from util import manhattanDistance
from game import Directions
import random, util
import math
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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        ut = 10000000
        for i in newFood.asList():
            ut = min(ut,math.sqrt(pow(i[0]-newPos[0],2) + pow(i[1] - newPos[1],2)))
        ut = 1/(ut+1) 
        for i in range(len(newGhostStates)):
            if manhattanDistance(newPos,newGhostStates[i].getPosition()) <= 1:
                ut -= 100
        return ut + 100 - len(newFood.asList())

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
        """
        "*** YOUR CODE HERE ***"
        def max_value(GameState, agent, depth):
            v = float("-inf")
            actions = ''
            nextAgent = (agent+1)%GameState.getNumAgents()
            legalActions = GameState.getLegalActions(agent)
            if len(legalActions) == 0:
                return self.evaluationFunction(GameState)
            for action in legalActions:
                new_v = min_value(GameState.generateSuccessor(agent,action), nextAgent, depth)
                if new_v > v:
                    v = new_v
                    actions = action
            if depth == 1:
                return actions 
            return v

        def min_value(GameState, agent, depth):
            v = float("inf")
            nextAgent = (agent+1)%GameState.getNumAgents()
            legalActions = GameState.getLegalActions(agent)
            if len(legalActions) == 0:
                return self.evaluationFunction(GameState)
            for action in GameState.getLegalActions(agent):
                if nextAgent != 0:
                        v = min(v, min_value(GameState.generateSuccessor(agent,action), nextAgent, depth))
                else:
                    if depth < self.depth:
                        v = min(v, max_value(GameState.generateSuccessor(agent,action), nextAgent, depth+1))
                    else:
                        v = min(v, self.evaluationFunction(GameState.generateSuccessor(agent, action)))
            return v
        return  max_value(gameState, 0, 1)
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def max_value(GameState, agent, depth, alpha, beta):
            v = float("-inf")
            actions = ''
            nextAgent = (agent+1)%GameState.getNumAgents()
            legalActions = GameState.getLegalActions(agent)
            if len(legalActions) == 0:
                return self.evaluationFunction(GameState)
            for action in legalActions:
                new_v = min_value(GameState.generateSuccessor(agent,action), nextAgent, depth, alpha, beta)
                if new_v > v:
                    v = new_v
                    actions = action
                    if new_v > beta:
                        return new_v
                    alpha = max(alpha, new_v)
            if depth == 1:
                return actions 
            return v

        def min_value(GameState, agent, depth, alpha, beta):
            v = float("inf")
            nextAgent = (agent+1)%GameState.getNumAgents()
            legalActions = GameState.getLegalActions(agent)
            if len(legalActions) == 0:
                return self.evaluationFunction(GameState)
            for action in GameState.getLegalActions(agent):
                if nextAgent != 0:
                        v = min(v, min_value(GameState.generateSuccessor(agent,action), nextAgent, depth, alpha, beta))
                else:
                    if depth < self.depth:
                        v = min(v, max_value(GameState.generateSuccessor(agent,action), nextAgent, depth+1, alpha, beta))
                    else:
                        v = min(v, self.evaluationFunction(GameState.generateSuccessor(agent, action)))

                if v < alpha:
                    return v
                beta = min(beta, v)
            return v
        return  max_value(gameState, 0, 1, float("-inf"), float("inf"))
        
        util.raiseNotDefined()

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
        def max_value(GameState, agent, depth):
            v = float("-inf")
            actions = ''
            nextAgent = (agent+1)%GameState.getNumAgents()
            legalActions = GameState.getLegalActions(agent)
            if len(legalActions) == 0:
                return self.evaluationFunction(GameState)
            for action in legalActions:
                new_v = avg_value(GameState.generateSuccessor(agent,action), nextAgent, depth)
                if new_v > v:
                    v = new_v
                    actions = action
            if depth == 1:
                return actions 
            return v

        def avg_value(GameState, agent, depth):
            v = 0
            nextAgent = (agent+1)%GameState.getNumAgents()
            legalActions = GameState.getLegalActions(agent)
            if len(legalActions) == 0:
                return self.evaluationFunction(GameState)
            for action in legalActions:
                if nextAgent != 0:
                        v += avg_value(GameState.generateSuccessor(agent,action), nextAgent, depth)
                else:
                    if depth < self.depth:
                        v += max_value(GameState.generateSuccessor(agent,action), nextAgent, depth+1)
                    else:
                        v += self.evaluationFunction(GameState.generateSuccessor(agent, action))
            return v/float(len(legalActions))
        return  max_value(gameState, 0, 1)

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    ut = 10000
    if len(newFood.asList()) == 0:
        return ut
    for i in newFood.asList():
        ut = min(ut,math.sqrt(pow(i[0]-newPos[0],2) + pow(i[1] - newPos[1],2)))
    ut = 1/(ut+1)
    for i in range(len(newGhostStates)):
        ghostDis = manhattanDistance(newPos,newGhostStates[i].getPosition())
        if ghostDis <= 1: 
            if newScaredTimes[i] == 0:
                ut -= 100
            else:
                ut += 8
    ut = ut - 10*(len(newFood.asList())) - 2*len(currentGameState.getCapsules())
    return ut
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

