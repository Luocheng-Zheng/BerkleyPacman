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

        #Analizamos, para todas las acciones legales de un gameState:
        # - Si la accion es quedarse quieto, devolvemos un valor negativo
        # - Si la nueva posicion coincide con la de un fantasma devolvemos un valor negativo
        # - Tanto para la comida como para las capsulas, calculamos la distancia y la anadimos con valor negativo a la score. 
        # Devolvemos el valor maximo de la lista porque queremos el que tenga menor valor.

        #Informacion util de un gameState para la q1
        successorGameState = currentGameState.generatePacmanSuccessor(action) #generacion del siguiente estado con la accion
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        
        score = []

        #Si la accion es quedarse quieto, devolvemos directamente un valor negativo
        if action == 'Stop':
          return -25.0
        
        #Para todos los fantasmas del estado
        for ghostState in newGhostStates:
          #Si la posicion nueva que vayamos coincide con la de un fantasma y esta que no se puede comer
          if ghostState.scaredTimer is 0 and ghostState.getPosition() == newPos:
            return -25.0 #tambien devolvemos un valor negativo

        #Para toda la comida, calculamos la distancia que hay desde Pacman hasta cada comida, la guardamos
        #en la lista y el valor sera negativo. Contra mas lejos peor
        for food in currentGameState.getFood().asList():
          score.append(-1*util.manhattanDistance(food,newPos))
        
        #Hacemos igual para las capsulas
        for bigFood in currentGameState.getCapsules():
          score.append(-1*util.manhattanDistance(bigFood,newPos))

        return max(score) #finalmente devolvemos el valor que maximiza la score porque todos los valores son negativos

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

    #Variable que usamos globalmente para obtener el numero de agentes de un gameState
    numAgents = 0

    #Definicion de minimax. Esta funcion recursiva devuelve dado un gameState la mejor accion que debe tomar Pacman para maximizar
    #su score
    def minimax(self, gameState, depth, agent):

      #Primero de todo comprobamos que si hemos llegado al final de los nodos expandidos, si el estado hace que ganemos
      #o si el estado hace que perdamos, devolvemos una tupla conn la score de la funcion de evaluacion del gameState 
      #juntamente con un valor vacio (no hace falta hacer ninguna accion mas)
      if depth == 0 or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState), ""

      #Comprobamos que el agente sea el ultimo de todos y en caso de que si, el siguiente agente sera Pacman y
      #significa que tenemos que expandir los nodos del nivel superior. Por eso restamos 1 a la profundidad
      if agent == self.numAgents - 1:
        depth = depth - 1
        nextAgent = 0
      else:
        nextAgent = agent + 1 #en caso de que no, el siguiente agente sera agent++

      #Agent = 0 significa que el agente es Pacman. Como la funcion es recursiva, maximizamos para agent == 0
      if(agent == 0):
        v = (-float("INF"),)
        for action in gameState.getLegalActions(agent):#para cada accion legal de cada agente
          nextState = gameState.generateSuccessor(agent, action) #generamos el siguiente gameState
          result = self.minimax(nextState, depth, nextAgent) #llamamos a la funcion de manera recursiva
          v = max([v, (result[0], action)])#y finalmente hacemos el max de esta tupla. El max devolvera la accion y la score mas alta de todas, comprobando tambien la tupla

      #en caso de que sea un fantasma, queremos minimizar la score y obtener la mejor accion que lo consiga
      else:             
        v = (float("INF"),)
        for action in gameState.getLegalActions(agent):#para cada accion legal de cada agente
          nextState = gameState.generateSuccessor(agent, action) #generamos el siguiente gameState
          result = self.minimax(nextState, depth, nextAgent) #llamamos a la funcion de manera recursiva y cogemos la score y la accion mas pequena de todas del result y de la tupla v
          v = min([v, (result[0], action)])
      
      return v #en esta tupla devolvemos la score en v[0] y la accion en v[1]

    def getAction(self, gameState):

      self.numAgents = gameState.getNumAgents()
      return self.minimax(gameState, self.depth, 0)[1] #solo necesitamos la accion, asi que la obtenemos con [1]

class AlphaBetaAgent(MultiAgentSearchAgent):

    #El funcionamento de este agente es muy parecida a la desarrollada en el Minimax Q2, salvo que usamos alpha-beta prunning para
    #evitar expandir nodos.
    #Se basa en reducir el numero de nodos evaluados en cada arbol
    #Creemos que el planteamiento de alpha beta es correcto pero expande una vez mas despues de podar y se acumula el error
    numAgents = 0

    def alphaBeta(self, gameState, depth, agent , alpha, beta):

      if depth == 0 or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState), "" 

      if agent == self.numAgents - 1:
        depth = depth - 1
        nextAgent = 0
      else:
        nextAgent = agent + 1

      #Evaluamos de la misma forma que minimax, teniendo en cuenta que:
      #Alpha es el valor que designa a la mejor opcion por el camino recorrido en el maximo
      #Beta es el valor que designa la mejor opcion por el camino recorrido en el minimo
      if(agent == 0):
        v = (-float("inf"),)
        for action in gameState.getLegalActions(agent):
          nextState = gameState.generateSuccessor(agent, action)
          result = self.alphaBeta(nextState, depth, nextAgent, alpha, beta)
          v = max([v, (result[0], action)])#Calculamos de nuevo el maximo (pacman) dado los valores de la funcion recursiva
          if v > beta: #Si el valor es peor que el valor actual, procedemos a podar
            return v #podamos el siguiente nodo de alpha
          alpha = max([alpha, v])#actualizamos el nuevo valor de alpha
      else:             
        v = (float("inf"),)
        for action in gameState.getLegalActions(agent):
          nextState = gameState.generateSuccessor(agent, action)
          result = self.alphaBeta(nextState, depth, nextAgent, alpha, beta)
          v = min([v, (result[0], action)])#Calculamos de nuevo el minimo (fantasmas) dado los valores de la funcion recursiva
          if v < alpha: #Si el valor de alpha es peor que el actual podamos
            return v #podamos el siguiente nodo de beta
          beta = min([beta, v]) #actualizamos el nuevo valor de beta

      return v

    def getAction(self, gameState):

      self.numAgents = gameState.getNumAgents()
      return self.alphaBeta(gameState, self.depth, 0, (-float("inf"),),(float("inf"),))[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    #El funcionamento de este agente tambien es muy parecida a la desarrollada en el Minimax Q2, salvo que en este caso en lugar de 
    #devolver la score en los fantasmas, devolveremos la score acumulada y ponderada por la probabilidad de tomar cada accion

    numAgents = 0

    def expectimax(self, gameState, depth, agent):

      if depth == 0 or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState), "" 

      if agent == self.numAgents - 1:
        depth = depth - 1
        nextAgent = 0
      else:
        nextAgent = agent + 1

      if(agent == 0):
        v = (-float("INF"),)
        for action in gameState.getLegalActions(agent):
          nextState = gameState.generateSuccessor(agent, action)
          result = self.expectimax(nextState, depth, nextAgent)
          v = max([v, (result[0], action)])
        return v
      else:             
        v = (0.0,)
        p = 1.0/float(len(gameState.getLegalActions(agent)) ) #calculamos la probabilidad de que tome la accion el fantasma
        #de manera que dara un valor normalizado. Ejemplos: 0.25 = 25% si tiene 4 acciones posibles
        for action in gameState.getLegalActions(agent):
          nextState = gameState.generateSuccessor(agent, action)
          result = self.expectimax(nextState, depth, nextAgent)

          #aqui sumamos la v actual junto con la score obtenida ponderada por la probabilidad de la accion
          value = v[0]
          resultat = result[0]
          value = value + p * resultat
          v = value,
        return v

    def getAction(self, gameState):

      self.numAgents = gameState.getNumAgents()
      return self.expectimax(gameState, self.depth, 0)[1] #Mismo modus operandi para obtener la mejor accion

def betterEvaluationFunction(currentGameState):

    #Hemos utilizado una logica parecida a la de la Q1 en la Q5, aunque en este caso no estamos observando acciones si no estados.
    #Por eso hemos observado que los valores mas importantes de un estado a la hora de ser evaluados son:
    # - Huir del fantasma. Menos dis
    # - Comer el fantasma solo si se puede.
    # - La distancia respecto la comida. Contra mas distancia, peor score.
    # - La score del gameState. Esta puede ser la mas importante, ya que ayuda a que la funcion de evaluacion nueva sea mas precisa

    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()

    score = 0.0

    for ghostState in GhostStates:
      if ghostState.scaredTimer == 0:
      	score -= 5.0 * manhattanDistance(ghostState.getPosition(),Pos)
      if ghostState.scaredTimer > 1:
        score += 6.0 * manhattanDistance(ghostState.getPosition(),Pos)

    for food in currentGameState.getFood().asList():
      score -= manhattanDistance(food,Pos)

    score += currentGameState.getScore()

    return score

# Abbreviation
better = betterEvaluationFunction

