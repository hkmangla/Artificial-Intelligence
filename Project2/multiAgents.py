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
        state = newPos
        md = 100000
        for i in newFood.asList():
            d = math.sqrt(pow(i[0]-state[0],2)+pow(i[1]-state[1],2))
            if d < md:
                md = d
        #for i in range(len(newGhostStates)):
        i = currentGameState.getGhostPosition(1)
        l1 = i[0]-state[0]
        l2 = i[1] - state[1]
        if l1 < 0:
            l1 = -l1
        if l2 < 0:
            l2 = -l2
        dd = l1 + l2    
        d = 0
        l = len(newFood.asList())
        if dd <= 1:
            d = -100
        return 1/(md+1) + d + (100-l)

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
        agent = gameState.getNumAgents()
        ghossts = self.depth*agent
        def maxvalue(gamestate,ghosts):
            v = float("-inf")
            i = 0
            for action in gamestate.getLegalActions(0):
                i= i + 1
                if minvalue(gamestate.generateSuccessor(0,action),ghosts-1) > v:
                    v = minvalue(gamestate.generateSuccessor(0,action),ghosts-1)
                    ans = action
            if i == 0:
                v = self.evaluationFunction(gamestate)
            if ghosts == ghossts:
                return ans
            if ghosts!= ghossts:
                return v
        def minvalue(gamestate,ghosts):
            v = float("inf")
            i = 0
            for action in gamestate.getLegalActions(agent-ghosts%agent):
                i= i+1;
                if ghosts % agent == 1:
                    if ghosts != 1:
                        v = min(v,maxvalue(gamestate.generateSuccessor(agent-ghosts%agent,action),ghosts-1))
                    if ghosts == 1:
                        v = min(v,self.evaluationFunction(gamestate.generateSuccessor(agent-ghosts%agent,action)))
                if ghosts % agent != 1:
                    v = min(v,minvalue(gamestate.generateSuccessor(agent-ghosts%agent,action),ghosts-1))
            if i == 0:
                v = self.evaluationFunction(gamestate)
            return v
        m = maxvalue(gameState,ghossts)
        return m
     
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
        a = float("-inf")
        b = float("inf")
        agent = gameState.getNumAgents()
        ghossts = self.depth*agent
        def maxvalue(gamestate, a,b,ghosts):
            v = float("-inf")
            i = 0
            for action in gamestate.getLegalActions(0):
                i= i + 1
                if minvalue(gamestate.generateSuccessor(0,action),a,b,ghosts-1) > v:
                    v = minvalue(gamestate.generateSuccessor(0,action),a,b,ghosts-1)
                    ans = action
                if v > b :
                    if ghosts == ghossts:
                        return ans
                    if ghosts!= ghossts:
                        return v
                a = max(a,v)
            if i == 0:
                v = self.evaluationFunction(gamestate)
                a = max(a,v)
            if ghosts == ghossts:
                return ans
            if ghosts!= ghossts:
                return v
        def minvalue(gamestate,a,b,ghosts):
            v = float("inf")
            i = 0
            for action in gamestate.getLegalActions(agent-ghosts%agent):
                i= i+1;
                if ghosts % agent == 1:
                    if ghosts != 1:
                        v = min(v,maxvalue(gamestate.generateSuccessor(agent-ghosts%agent,action),a,b,ghosts-1))
                    if ghosts == 1:
                        v = min(v,self.evaluationFunction(gamestate.generateSuccessor(agent-ghosts%agent,action)))
                if ghosts % agent != 1:
                    v = min(v,minvalue(gamestate.generateSuccessor(agent-ghosts%agent,action),a,b,ghosts-1))
                if v < a :
                    return v
                b = min(b,v)
            if i == 0:
                v = self.evaluationFunction(gamestate)
                b = min(b,v)
            return v
        m = maxvalue(gameState,a,b,ghossts)
        return m
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
        agent = gameState.getNumAgents()
        ghossts = self.depth*agent
        def maxvalue(gamestate,ghosts):
            v = float("-inf")
            i = 0
            for action in gamestate.getLegalActions(0):
                i= i + 1
                if minvalue(gamestate.generateSuccessor(0,action),ghosts-1) > v:
                    v = minvalue(gamestate.generateSuccessor(0,action),ghosts-1)
                    ans = action
            if i == 0:
                v = self.evaluationFunction(gamestate)
            if ghosts == ghossts:
                return ans
            if ghosts!= ghossts:
                return v
        def minvalue(gamestate,ghosts):
            i = 0.0
            v = 0.0
            for action in gamestate.getLegalActions(agent-ghosts%agent):
                i= i+1;
                if ghosts % agent == 1:
                    if ghosts != 1:
                        v = v + maxvalue(gamestate.generateSuccessor(agent-ghosts%agent,action),ghosts-1)
                    if ghosts == 1:
                        v = v + self.evaluationFunction(gamestate.generateSuccessor(agent-ghosts%agent,action))
                if ghosts % agent != 1:
                    v = v + minvalue(gamestate.generateSuccessor(agent-ghosts%agent,action),ghosts-1)
            if i != 0.0:
                v = v/i
            if i == 0.0:
                v = self.evaluationFunction(gamestate)
            return v
        m = maxvalue(gameState,ghossts)
        return m
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
        #successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    capsules = currentGameState.getCapsules()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    state = newPos
    md = 100000
    for i in newFood.asList():
        d = math.sqrt(pow(i[0]-state[0],2)+pow(i[1]-state[1],2))
        if d < md:
            md = d
    i = currentGameState.getGhostPosition(1)
    l1 = i[0]-state[0]
    l2 = i[1] - state[1]
    if l1 < 0:
        l1 = -l1
    if l2 < 0:
        l2 = -l2
    dd = l1 + l2    
    d = 0
    l = len(newFood.asList()) + 2*len(capsules)
    if dd <= 1:
        d = -100
    return 1/(md+1) + d + (100-l)
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

