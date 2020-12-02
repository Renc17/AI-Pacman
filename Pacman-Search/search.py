# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman-Search AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman-Search agents (in searchAgents.py).
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
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    # ALL the methods push a tuple of ( position , list with stores path to solution )

    setOfExplored = set()

    frontier = util.Stack()
    frontier.push((problem.getStartState(), []))            # push starting position in stack

    while not frontier.isEmpty():
        state, actions = frontier.pop()                     # pop the last element pushed

        if problem.isGoalState(state):                      # if it is our goal return path to it
            return actions

        setOfExplored.add(state)                            # else mark it as explored

        for item in problem.getSuccessors(state):           # all possible directions(next states of pacman) are stacked , if they are not explored yet and the paths are updated
            next_state = item[0]
            if next_state not in setOfExplored:
                directionsTo = item[1]
                frontier.push((next_state, actions + [directionsTo]))
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    setOfExplored = set()

    frontier = util.Queue()
    frontier.push((problem.getStartState(), []))            # push to queue first position
    setOfExplored.add(problem.getStartState())              # mark as explored

    while not frontier.isEmpty():
        state, actions = frontier.pop()                     # pop first element pushed

        if problem.isGoalState(state):                      # if it is our goal return path to get there
            return actions

        for item in problem.getSuccessors(state):           # all possible directions(next states of pacman) are queued, if they are not explored yet, mark them as explored and the paths are updated
            next_state = item[0]
            directionsTo = item[1]
            if next_state not in setOfExplored:
                frontier.push((next_state, actions + [directionsTo]))
                setOfExplored.add(next_state)

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    setOfExplored = set()

    frontier = util.PriorityQueue()
    frontier.push((problem.getStartState(), []), 0)         # push to a priority queue first position

    while not frontier.isEmpty():
        flag = 0
        state, actions = frontier.pop()                     # pop first element pushed

        if problem.isGoalState(state):                      # if it is our goal return path to get there
            return actions

        setOfExplored.add(state)                            # else mark it as explored

        for item in problem.getSuccessors(state):           # all possible directions(next states of pacman) are queued, if they are not explored yet with, prioritized by cost to get to a point and the paths are updated
            next_state = item[0]                            # or updated by priority if they are in queue with another path
            directionsTo = item[1]
            if next_state not in setOfExplored:
                for i in frontier.heap:
                    if next_state == i[2][0]:
                        flag = 1
                        if problem.getCostOfActions(i[2][1]) > problem.getCostOfActions(actions + [directionsTo]):
                            frontier.update((next_state, actions + [directionsTo]), problem.getCostOfActions(actions + [directionsTo]))
                if flag == 0:
                    frontier.push((next_state, actions + [directionsTo]), problem.getCostOfActions(actions + [directionsTo]))
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

    setOfExplored = set()

    frontier = util.PriorityQueue()
    frontier.push((problem.getStartState(), []), heuristic(problem.getStartState(), problem))

    while not frontier.isEmpty():
        flag = 0
        state, actions = frontier.pop()

        if problem.isGoalState(state):
            return actions

        setOfExplored.add(state)

        for item in problem.getSuccessors(state):       # all possible directions(next states of pacman) are queued, if they are not explored yet with, prioritized by cost to get to a point + heuristic value, and the paths are updated
            next_state = item[0]                        # or updated by priority if they are in queue with another path
            directionsTo = item[1]
            if next_state not in setOfExplored:
                for i in frontier.heap:
                    if next_state == i[2][0]:
                        flag = 1
                        if problem.getCostOfActions(i[2][1]) > problem.getCostOfActions(actions + [directionsTo]) + heuristic(next_state, problem):
                            frontier.update((next_state, actions + [directionsTo]), (problem.getCostOfActions(actions + [directionsTo]) + heuristic(next_state, problem)))
                if flag == 0:
                    frontier.push((next_state, actions + [directionsTo]), (problem.getCostOfActions(actions + [directionsTo]) + heuristic(next_state, problem)))


    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
