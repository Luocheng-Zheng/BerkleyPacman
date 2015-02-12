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


def checkExists(problem, stack):

    if stack.isEmpty():
        raise ValueError('This stack is empty!')

""" 
El algoritmo de busqueda recursiva para DFS y BFS parece expandir bien los nodos y funcionar bien en el juego pero 
a la hora de determinar el autograder su funcionamiento este hace terminar la ejecucion del programa inesperadamente.
"""

#Funcion que devuelve las acciones 
def getActions(stack):

    result = []

    for s in stack.list[1:]:
        result.append(s[1])

    return result

#Algoritmo recursivo para BFS y DFS basado en lectura preorden (no funciona correctamente con autograder)
#Esta basado en la llamada recursiva para leer en preorden un algoritmo
def recAlg(problem, stack, check):

    if problem.isGoalState(stack.list[len(stack.list) - 1][0]): #Si hemos llegado al final devolvemos las acciones
        global globalvar
        globalvar = util.Stack()
        globalvar = getActions(stack)
        return globalvar

    if not checkVisit(check,stack.list[len(stack.list) - 1][0]) == True: # COmprobar nodos cerrados

        check.append(stack.list[len(stack.list) - 1][0])

        succesors = []
        succesors = problem.getSuccessors(stack.list[len(stack.list) - 1][0])

        for s in succesors:
            newStack = util.Stack()
            newStack.list = stack.list[:]
            newStack.push(s)
            return recAlg(problem, newStack, check)

    return []

###############################################################################
#                           Algoritmos de busqueda                            #
#                              (DFS,BFS,UCS,A*)                               #
###############################################################################

#Funcion utilizada para saber si el elemento se encuentra dentro de la lista
#MUY IMPORTANTE para obtener asi los nodos cerrados
def checkVisit(lista,item):

    if item in lista:
        return True

    return False

#Algoritmo BFS y DFS (fuerza bruta), ambos utilizan la misma funcion 
def algBF(problem,struct,moves):

    nodelist = []
    struct.push((problem.getStartState(),[],[]))# Introducimos el primer nodo dentro de la estructura
    moves.push([])

    while not struct.isEmpty(): #mientras no este vacia iteramos
        actual = struct.pop() #estructura para nodos
        actual2 = moves.pop() #estructura para acciones
        node, actions, cost = actual 

        if problem.isGoalState(node): #Si hemos llegado al goal devolvemos las acciones!
            return actual2  

        if not checkVisit(nodelist,node): #si se encuentra dentro de closed no lo visitamos
            nodelist.append(node)
            for node, actions, cost in problem.getSuccessors(node): #expandimos con sus succesores
                struct.push((node,actions,cost)) #pusheamos cada succesor
                moves.push(actual2 + [actions]) #pusheamos al successor y sus movimientos

#Algoritmo DeepFirstSearch, busqueda en profundidad (LIFO)
def depthFirstSearch(problem):

    #Utilizamos dos stacks aunque no es necesario pero nos parecio mas claro separar acciones de nodos para iterar
    stack = util.Stack()
    moves = util.Stack()
    result = algBF(problem,stack,moves) #obtenemos el resultado desde la misma funcion
    return result

#Algoritmo BreadthFirstSearch, busqueda en amplitud (FIFO)
def breadthFirstSearch(problem):

    #Utilizamos dos colas aunque no es necesario pero nos parecio mas claro separar acciones de nodos para iterar
    stack = util.Queue()
    moves = util.Queue()
    result = algBF(problem,stack,moves)
    return result

#Algoritmo de coste uniforme, buscamos el camino que menos coste tenga!
#Es decir, vamos buscando dado el coste encontrado en cada rama, aquel camino con el menor coste.
def uniformCostSearch(problem):

    #Como anteriormente, pero en este caso necesitamos el uso de colas de prioridad, donde la prioridad viene indicada por el coste!
    nodelist = []
    cola = util.PriorityQueue()
    moves = util.PriorityQueue()
    cola.push([(problem.getStartState(),[],[]),0],0)#En este caso guardamos la acumulacion del coste para cada camino y le pasamos su prioridad como coste
    moves.push([],0)

    while not cola.isEmpty():# Mientras tengamos elementos en la cola iteramos
        actual = cola.pop()
        actual2 = moves.pop()
        node, actions, cost = actual[0] #Obtenemos el nodo, accion y coste del primero elemento de la cola que ha sido sustraido 

        if problem.isGoalState(node): # Si hemos llegado al estado objetivo devolvemos las acciones
            return actual2
        
        if not checkVisit(nodelist,node): #De nuevo volvemos a comprobar si no es un nodo cerrado
            nodelist.append(node)
            for hnode, hactions, hcost in problem.getSuccessors(node):
                cola.push([(hnode,hactions,hcost),actual[1] + hcost], actual[1] + hcost) # Como en BFS y DFS pero esta vez utilizamos el coste como prioridad!
                moves.push(actual2 + [hactions],actual[1] + hcost) #guardamos las acciones en una cola aparte
        
#Heuristica nula, en este caso siempre sera cero ya que es nula!
#Es una fuicion que devuelve un estimacion del coste que falta respecto el estado actual para llegar a la meta
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

#Algoritmo A*, este algoritmo funciona de la misma manera que UCS pero en este caso tenemos una funcion heuristica
#Es decir, utiliza una funcion de evaluacion tal que f(n) = g(n) + h(n) donde h(n) es nuestra funcion heuristica  
def aStarSearch(problem, heuristic=nullHeuristic):
    
    nodelist = []
    cola = util.PriorityQueue() #Utilizamos dos colas de prioridad de nuevo ya que trabajamos con costes
    moves = util.PriorityQueue()
    startValue = heuristic(problem.getStartState(),problem) #Obtenemos nuestro valor inicial agregado al coste mediante la funcion heuristica
    cola.push([(problem.getStartState(),[],[]),startValue],startValue) #Agregamos el primer elemento
    moves.push([],startValue)

    while not cola.isEmpty(): #Iteramos sobre la cola de nuevo
        actual = cola.pop()
        actual2 = moves.pop()
        node, actions, cost = actual[0] #Valor (nodo,acciones,coste) del ultimo elemento sustraido

        if problem.isGoalState(node): #Si hemos llegado al estado objetivo devolvemos las acciones y hemos concluido
            return actual2 

        if not checkVisit(nodelist,node): #Comprobacion de nodos cerrados
            nodelist.append(node)
            for hnode, hactions, hcost in problem.getSuccessors(node): #Expandimos con los nodos succesores
                cola.push([(hnode,hactions,hcost),actual[1] + hcost], actual[1] + hcost + heuristic(hnode,problem)) # De la mima forma que en UCS pero al coste le agregamos el valor obtenido por la heuristica!!!
                moves.push(actual2 + [hactions],actual[1] + hcost + heuristic(hnode,problem)) #Guardamos las acciones por separado como antes

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
