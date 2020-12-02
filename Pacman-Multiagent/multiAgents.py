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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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

        closestFood = []
        for food in newFood.asList():
            closestFood.append(manhattanDistance(newPos, food))

        if currentGameState.getPacmanPosition() == newPos:  # penalty if pacman chooses to stay in the same place
            return float('-inf')

        closestGhost = float('inf')
        for ghostPos in newGhostStates:
            if ghostPos.getPosition() == newPos:            # if in the next move pacman meets ghost dont make it
                return float('-inf')
            closestGhost = min(closestGhost, manhattanDistance(newPos, ghostPos.getPosition()))
            if closestGhost < 2:                            # if a ghost next to ghost get out of there
                return float('-inf')

        if len(closestFood) == 0:           # if there is no food left return "victory" score
            return float('inf')

        score = 60.0 / sum(closestFood) + 1000.0 / len(newFood.asList())            # calculate score
                                                                                    # seems a little like Expectimax
        return score


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

        depth = 0
        value_max = float('-inf')
        action = None               # at first there is no action for pacman to make

        for a in gameState.getLegalActions(self.index):             # for all legal actions pacman can make calculate all ghosts response
            state = gameState.generateSuccessor(self.index, a)
            m = self.min_value(depth, state, 1)
            if m > value_max:           # select the max value and action
                value_max = m
                action = a

        return action

        util.raiseNotDefined()

    def min_value(self, d, game, player):
        if game.isWin() == True or game.isLose() == True:
            return self.evaluationFunction(game)

        v = float('inf')
        for successor in game.getLegalActions(player):
            if player < game.getNumAgents() - 1:
                v = min(v, self.min_value(d, game.generateSuccessor(player, successor), player + 1))
            else:
                v = min(v, self.max_value(d + 1, game.generateSuccessor(player, successor)))
        return v

    def max_value(self, d, game):
        if d == self.depth or game.isWin() == True or game.isLose() == True:
            return self.evaluationFunction(game)

        v = float('-inf')
        for successor in game.getLegalActions(self.index):
            game.generateSuccessor(self.index, successor)
            v = max(v, self.min_value(d, game.generateSuccessor(self.index, successor), 1))
        return v


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        depth = 0
        alpha = float('-inf')
        beta = float('inf')
        action = None           # at first there is no action for pacman to make

        for a in gameState.getLegalActions(self.index):     # for all legal actions pacman can make calculate all ghosts response
            value_max = self.Min_Value(gameState.generateSuccessor(self.index, a), alpha, beta, 1, depth)
            if alpha < value_max:       # keep the best action for pacman
                alpha = value_max
                action = a

        return action

        util.raiseNotDefined()

    def Max_Value(self, state, a, b, depth):

        if depth == self.depth or state.isWin() == True or state.isLose() == True:
            return self.evaluationFunction(state)

        v = float('-inf')
        for successor in state.getLegalActions(self.index):
            state.generateSuccessor(self.index, successor)
            v = max(v, self.Min_Value(state.generateSuccessor(self.index, successor), a, b, 1, depth))
            if v > b:
                return v
            a = max(a, v)
        return v

    def Min_Value(self, state, a, b, player, depth):

        if state.isWin() == True or state.isLose() == True:
            return self.evaluationFunction(state)

        v = float('inf')
        for successor in state.getLegalActions(player):
            if player < state.getNumAgents() - 1:
                v = min(v, self.Min_Value(state.generateSuccessor(player, successor), a, b, player + 1, depth))
            else:
                v = min(v, self.Max_Value(state.generateSuccessor(player, successor), a, b, depth + 1))
            if v < a:
                return v
            b = min(b, v)
        return v


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
        depth = 0
        value_max = float('-inf')
        action = None

        for a in gameState.getLegalActions(self.index):
            state = gameState.generateSuccessor(self.index, a)
            m = self.min_value(depth, state, 1)
            if m > value_max:
                value_max = m
                action = a
        return action
        util.raiseNotDefined()

    def min_value(self, d, game, player):
        if len(game.getLegalActions(player)) == 0:
            return self.evaluationFunction(game)

        v = 0
        for successor in game.getLegalActions(player):  # for every legal move find average value
            if player < game.getNumAgents() - 1:
                v += self.min_value(d, game.generateSuccessor(player, successor), player + 1)
            else:
                v += self.max_value(d + 1, game.generateSuccessor(player, successor))
        return v / float(len(game.getLegalActions(player)))

    def max_value(self, d, game):
        if (d == self.depth) or (len(game.getLegalActions(0)) == 0):
            return self.evaluationFunction(game)

        v = float('-inf')
        for successor in game.getLegalActions(self.index):
            game.generateSuccessor(self.index, successor)
            v = max(v, self.min_value(d, game.generateSuccessor(self.index, successor), 1))
        return v


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    FoodList = currentGameState.getFood().asList()
    CapsuleList = currentGameState.getCapsules()
    GhostStates = currentGameState.getGhostStates()
    PacmanPos = currentGameState.getPacmanPosition()

    score = 0

    closestGhost = float('inf')
    for ghost in GhostStates:
        closestGhost = min(closestGhost, manhattanDistance(PacmanPos, ghost.getPosition())) # find where the closest ghost is
        if closestGhost < 2:            # if ghost stands next to pacman that's bad
            return float('-inf')
        score -= 1.0 / closestGhost     # sub every ghost distance

    closestFood = float('inf')
    for food in FoodList:
        closestFood = min(closestFood, manhattanDistance(PacmanPos, food))
    score += 1.0 / closestFood          # reward for the closest food
    score -= currentGameState.getNumFood()  # but there is more food so subtract the amount left

    closestCapsule = float('inf')
    for food in CapsuleList:
        closestCapsule = min(closestCapsule, manhattanDistance(PacmanPos, food))
    score += 1.0 / closestCapsule       # reward finding the closest capsule but there is more so... you know the drill
    score -= len(CapsuleList)

    return score


# Abbreviation
better = betterEvaluationFunction
