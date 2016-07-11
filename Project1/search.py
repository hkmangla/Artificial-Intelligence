# search.py
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    "*** YOUR CODE HERE ***"
    closset = []
    action = {}
    fringe = util.Stack()
    start = (problem.getStartState(),'Stop',0)
    fringe.push(start)
    while (1):
        if fringe.isEmpty():
            break
        node = fringe.pop()
        if problem.isGoalState(node[0]):
             return action[node[0]]    
        if node[0] not in closset:
            closset.append(node[0])
            for childNode,direction,cost in problem.getSuccessors(node[0]):
                 list2 = []
                 if node[0] !=  problem.getStartState():
                     for i in action[node[0]]:
                         list2.append(i)
                 list2.append(direction)
                 action[childNode] = list2
                 head = (childNode,direction,cost)   
                 fringe.push(head)             
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    closset = []
    action = {}
    #path = {}
    fringe = util.Queue()
    start = (problem.getStartState(),'Stop',0)
    #path[problem.getStartState()] = problem.getStartState()
    fringe.push(start)
    while (1):
        if fringe.isEmpty():
            break
        node = fringe.pop()
        if problem.isGoalState(node[0]):
             return action[node[0]]    
        if node[0] not in closset:
            closset.append(node[0])
            for childNode,direction,cost in problem.getSuccessors(node[0]):
                 if childNode not in action.keys():
                     list2 = []
                   #  list1 = []
                     if node[0] !=  problem.getStartState():
                         for i in action[node[0]]:
                             list2.append(i)
                      #   for i in path[node[0]]:
                       #      list2.append(i)
                     list2.append(direction)
                     #print childNode
                     action[childNode] = list2
                     #path[childNode] = list1
                 head = (childNode,direction,cost)   
                 fringe.push(head)             
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    closset = []
    action = {}
    fringe = util.PriorityQueue()
    start = (problem.getStartState(),'Stop',0)
    fringe.push(start,0)
    while (1):
        if fringe.isEmpty():
            break
        node = fringe.pop()
        if problem.isGoalState(node[0]):
             return action[node[0]]    
        if node[0] not in closset:
            closset.append(node[0])
            for childNode,direction,cost in problem.getSuccessors(node[0]):
                list2 = []
                if node[0] !=  problem.getStartState():
                    for i in action[node[0]]:
                        list2.append(i)
                list2.append(direction)
                childcost = problem.getCostOfActions(list2)
                if childNode in action.keys():
                    if childcost < problem.getCostOfActions(action[childNode]):
                        action[childNode] = list2
                if childNode not in action.keys():
                    action[childNode] = list2
                head = (childNode,direction,cost)
                if childNode !=  problem.getStartState():
                    priority = problem.getCostOfActions(action[childNode])
                if childNode ==  problem.getStartState():
                    priority = 0
                fringe.push(head,priority)             
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    closset = []
    action = {}
    fringe = util.PriorityQueue()
    start = (problem.getStartState(),'Stop',0)
    fringe.push(start,0)
    while (1):
        if fringe.isEmpty():
            break
        node = fringe.pop()
        if problem.isGoalState(node[0]):
             return action[node[0]]    
        if node[0] not in closset:
            closset.append(node[0])
            for childNode,direction,cost in problem.getSuccessors(node[0]):
                list2 = []
                if node[0] !=  problem.getStartState():
                    for i in action[node[0]]:
                        list2.append(i)
                list2.append(direction)
                childcost = problem.getCostOfActions(list2)
                if childNode in action.keys():
                    if childcost < problem.getCostOfActions(action[childNode]):
                        action[childNode] = list2
                if childNode not in action.keys():
                    action[childNode] = list2
                head = (childNode,direction,cost)
                if childNode !=  problem.getStartState():
                    priority = problem.getCostOfActions(action[childNode])
                if childNode ==  problem.getStartState():
                    priority = 0
                fringe.push(head,priority+heuristic(childNode,problem))             
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
