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

import torch
import numpy as np
from net import PacmanNet
import os
from util import manhattanDistance
from game import Directions
import random, util
#random.seed(42)  # For reproducibility
from game import Agent
from pacman import GameState
import math

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()



# def traditional_evaluation(state):
#     """
#     Evalúa el estado del juego usando únicamente heurísticas.
#     Retorna un score basado en la posición de los elementos.
#     """
#     # 1. Extracción de datos del estado
#     score = state.getScore()
#     pacman_pos = state.getPacmanPosition()
#     food = state.getFood().asList()
#     ghost_states = state.getGhostStates()
#     capsules = state.getCapsules()

#     # Factor 1: Distancia a la comida más cercana
#     if food:
#         min_food_distance = min(manhattanDistance(pacman_pos, food_pos) for food_pos in food)
#         score += 1.0 / (min_food_distance + 1)

#     # Factor 2: Proximidad a fantasmas
#     for ghost_state in ghost_states:
#         ghost_pos = ghost_state.getPosition()
#         ghost_distance = manhattanDistance(pacman_pos, ghost_pos)

#         if ghost_state.scaredTimer > 0:
#             # Si el fantasma está asustado, acercarse a él
#             score += 50 / (ghost_distance + 1)
#         else:
#             # Si no está asustado, evitarlo
#             if ghost_distance <= 2:
#                 score -= 200  # Gran penalización por estar demasiado cerca

#     # Factor 3: Cápsulas
#     if capsules:
#         min_capsule_distance = min(manhattanDistance(pacman_pos, cap_pos) for cap_pos in capsules)
#         score += 10 / (min_capsule_distance + 1)

#     # Factor 4: Densidad Local de Comida
#     nearby_food = sum(1 for food_pos in food if manhattanDistance(pacman_pos, food_pos) <= 4)
#     score += nearby_food * 2.0

#     # Factor 5: Radar Preventivo de Fantasmas
#     for ghost_state in ghost_states:
#         if ghost_state.scaredTimer == 0:
#             ghost_pos = ghost_state.getPosition()
#             ghost_distance = manhattanDistance(pacman_pos, ghost_pos)
#             if 2 < ghost_distance <= 5:
#                 score -= 20.0 / ghost_distance

#     # Factor 6: Prevención de Caza Suicida
#     for ghost_state in ghost_states:
#         if ghost_state.scaredTimer > 0:
#             ghost_pos = ghost_state.getPosition()
#             ghost_distance = manhattanDistance(pacman_pos, ghost_pos)
#             if ghost_distance > ghost_state.scaredTimer:
#                 score -= 50 / (ghost_distance + 1)

    # # Factor 7: No cazar si cerca de origen de fantasmas
    # for ghost_state in ghost_states:
    #     if ghost_state.scaredTimer > 0:
    #         walls = state.getWalls()
    #         width, height = walls.width, walls.height
    #         map_center_distance = manhattanDistance(pacman_pos, (width//2, height//2))
    #         score -= 50 / (map_center_distance + 1)

    # # Factor 8: Evitar esquinas
    # for ghost_state in ghost_states:
    #     if ghost_state.scaredTimer == 0:
    #         walls = state.getWalls() # Obtenemos dimensiones del mapa
    #         width, height = walls.width, walls.height
    #         corners = [(width-1, height-1), (1, 1), (1, height-1), (width-1, 1)]
    #         for corner_pos in corners:
    #             # Evitar comprobar si justo la esquina es un muro ciego
    #             if not walls[corner_pos[0]][corner_pos[1]]:
    #                 corner_distance = manhattanDistance(pacman_pos, corner_pos)
    #                 if corner_distance <= 5:
    #                     score -= 10.0 / (corner_distance + 1)

    # raw_score = score

    # # NORMALIZACIÓN SIGMOIDE (0 a 100)
    # # k=50 es la "pendiente". Si el score es 0, devuelve 50.
    # # Si el score es muy alto, tiende a 100. Si es muy bajo, tiende a 0.
    # try:
    #     norm_score = 100.0 / (1.0 + math.exp(-raw_score / 50.0))
    # except OverflowError:
    #     norm_score = 100.0 if raw_score > 0 else 0.0

    # #return norm_score
    # return score

def traditional_evaluation(state):
    """
    Evalúa el estado del juego usando únicamente heurísticas.
    Retorna un score basado en la posición de los elementos.

    Mejoras aplicadas:
    - Penalizaciones incrementales por distancia a fantasmas (1, 2, 3 metros)
    - Persecución inteligente de fantasmas asustados con verificación de alcance temporal
    - Las cápsulas solo dan alto incentivo si hay fantasmas asustados cerca
    - Penalización anti-estancamiento en esquinas y pasillos
    - Penalización en zona de spawn de fantasmas
    """
    score = state.getScore()
    pacman_pos = state.getPacmanPosition()
    food = state.getFood().asList()
    ghost_states = state.getGhostStates()
    capsules = state.getCapsules()
    legal_actions = state.getLegalActions()
    # Factor 1: Distancia a la comida más cercana
    if food:
        min_food_distance = min(manhattanDistance(pacman_pos, food_pos) for food_pos in food)
        score += 3.0 / (min_food_distance + 1)

    # Factor 2: Proximidad a fantasmas
    for ghost_state in ghost_states:
        ghost_pos = ghost_state.getPosition()
        ghost_distance = manhattanDistance(pacman_pos, ghost_pos)

        if ghost_state.scaredTimer > 0:
            # Si el fantasma está asustado, acercarse a él
            score += 100 / (ghost_distance + 1)
        else:
            # Si no está asustado, evitarlo (penalización graduada)
            if ghost_distance <= 1:
                score -= 300
            elif ghost_distance == 2:
                score -= 150
            elif ghost_distance == 3:
                score -= 50
            
    # Factor 3: Cápsulas (defensivo y ofensivo)
    if capsules:
        min_cap_dist = min(manhattanDistance(pacman_pos, c) for c in capsules)
        # ¿Hay fantasmas peligrosos cerca?
        danger_close = any(
            g.scaredTimer == 0 and manhattanDistance(pacman_pos, g.getPosition()) <= 3
            for g in ghost_states
        )
        if danger_close:
            score += 100.0 / (min_cap_dist + 1)
        else:
            score += 5.0 / (min_cap_dist + 1)

    # Factor 4: Densidad local de comida
    nearby_food = sum(1 for f in food if manhattanDistance(pacman_pos, f) <= 4)
    score += nearby_food * 2.0

    # Factor 5: Radar preventivo de fantasmas (evitar a distancia 4-5)
    for g in ghost_states:
        if g.scaredTimer == 0:
            dist = manhattanDistance(pacman_pos, g.getPosition())
            if 3 < dist <= 5:
                score -= 30.0 / dist

    # Factor 6: Anti‑caza suicida
    for g in ghost_states:
        if g.scaredTimer > 0:
            dist = manhattanDistance(pacman_pos, g.getPosition())
            if dist > g.scaredTimer:
                score -= 100.0 / (dist + 1)

    # Factor 7: Bonus de movilidad con detección de acorralamiento
    legal_actions = state.getLegalActions(0)
    if len(legal_actions) <= 2:
        # Verificar si hay fantasmas peligrosos en un radio de 4
        ghost_nearby = False
        for g in ghost_states:
            if g.scaredTimer == 0:
                dist = manhattanDistance(pacman_pos, g.getPosition())
                if dist <= 4:
                    ghost_nearby = True
                    # Penalización escalada: dist=1 → -200, dist=4 → -50
                    score -= 500.0 / (dist + 1)
        if not ghost_nearby:
            # Solo es un pasillo estrecho, sin amenaza inminente
            score -= 40


    # # Factor 3: Cápsulas
    # capsules = state.getCapsules()
    # if capsules:
    #     min_capsule_distance = min(manhattanDistance(pacman_pos, cap_pos) for cap_pos in capsules)
    #     score += 10 / (min_capsule_distance + 1)

    # # Factor 4: Densidad Local de Comida
    # # Cuenta cuánta comida hay en un radio de 4 pasos y premia ir hacia grupos grandes.
    # nearby_food = sum(1 for food_pos in food if manhattanDistance(pacman_pos, food_pos) <= 4)
    # score += nearby_food * 2.0  # Cada comida cercana aporta +2.0

    # # Factor 5: Radar Preventivo de Fantasmas
    # for ghost_state in ghost_states:
    #     if ghost_state.scaredTimer == 0:  # Solo si son peligrosos
    #         ghost_pos = ghost_state.getPosition()
    #         ghost_distance = manhattanDistance(pacman_pos, ghost_pos)
    #         if 2 < ghost_distance <= 5:  # Si están cerca pero no en rango letal
    #             score -= 20.0 / ghost_distance

    # # Factor 6: Prevención de Caza Suicida
    # # Si un fantasma asustado va a "despertar" antes de que lleguemos, anulamos la atracción.
    # for ghost_state in ghost_states:
    #     if ghost_state.scaredTimer > 0:
    #         ghost_pos = ghost_state.getPosition()
    #         ghost_distance = manhattanDistance(pacman_pos, ghost_pos)

    #         # Si estamos más lejos que el tiempo que le queda de miedo
    #         if ghost_distance > ghost_state.scaredTimer:
    #             # Anulamos el incentivo de ir tras él
    #             score -= 50 / (ghost_distance + 1)

    # # -----------------------------------------------------------------------
    # # Factor 1: Progresión en la comida
    # # -----------------------------------------------------------------------
    # if food:
    #     min_food_dist = min(manhattanDistance(pacman_pos, f) for f in food)
    #     score += 2.0 / (min_food_dist + 1)
    #     # Penalizar la cantidad de comida restante
    #     score -= 0.5 * len(food)

    # # -----------------------------------------------------------------------
    # # Factor 2: Gestión de Fantasmas
    # # -----------------------------------------------------------------------
    # for ghost_state in ghost_states:
    #     ghost_pos = ghost_state.getPosition()
    #     ghost_dist = manhattanDistance(pacman_pos, ghost_pos)

    #     if ghost_state.scaredTimer > 0:
    #         # --- FANTASMA ASUSTADO: Decidir si perseguir ---
    #         if ghost_dist <= ghost_state.scaredTimer:
    #             # Podemos alcanzarlo antes de que despierte -> PERSECUCIÓN
    #             score += 200 / (ghost_dist + 1)
    #             # Bonus extra si está a tiro (distancia 1) -> COMERLO da 200+ puntos
    #             if ghost_dist <= 1:
    #                 score += 300
    #         else:
    #             # Se despertará antes de que lleguemos -> penalización leve
    #             score -= 30 / (ghost_dist + 1)
    #     else:
    #         # --- FANTASMA PELIGROSO: Penalización incremental por distancia ---
    #         if ghost_dist <= 1:
    #             score -= 2000  # ¡Muerte inminente!
    #         elif ghost_dist == 2:
    #             score -= 500   # Muy peligroso
    #         elif ghost_dist == 3:
    #             score -= 150   # Peligroso
    #         elif ghost_dist <= 5:
    #             score -= 30.0 / ghost_dist  # Zona de precaución

    # # -----------------------------------------------------------------------
    # # Factor 3: Cápsulas (con valor defensivo y ofensivo)
    # # -----------------------------------------------------------------------
    # if capsules:
    #     min_cap_dist = min(manhattanDistance(pacman_pos, c) for c in capsules)

    #     # (A) Valor DEFENSIVO: ¿hay fantasmas peligrosos cerca (dist <= 4)?
    #     # Si sí, la cápsula es una ruta de escape -> altísima prioridad
    #     hay_fantasma_peligroso_cerca = any(
    #         ghost_state.scaredTimer == 0 and
    #         manhattanDistance(pacman_pos, ghost_state.getPosition()) <= 4
    #         for ghost_state in ghost_states
    #     )

    #     # (B) Valor OFENSIVO: ¿hay fantasmas asustados ALCANZABLES?
    #     # Un fantasma es alcanzable si está a una distancia que podamos recorrer
    #     # antes de que se le acabe el temporizador de miedo
    #     hay_fantasma_para_cazar = any(
    #         ghost_state.scaredTimer > 0 and 
    #         manhattanDistance(pacman_pos, ghost_state.getPosition()) <= ghost_state.scaredTimer
    #         for ghost_state in ghost_states
    #     )

    #     if hay_fantasma_peligroso_cerca:
    #         # ESCAPE: comerse la cápsula ahuyenta a los fantasmas cercanos
    #         score += 100 / (min_cap_dist + 1)
    #     elif hay_fantasma_para_cazar:
    #         # ATAQUE: podemos comernos los fantasmas asustados
    #         score += 40 / (min_cap_dist + 1)
    #     else:
    #         # Valor base: solo por puntos
    #         score += 5 / (min_cap_dist + 1)

    # # -----------------------------------------------------------------------
    # # Factor 4: Densidad Local de Comida
    # # -----------------------------------------------------------------------
    # nearby_food = sum(1 for f in food if manhattanDistance(pacman_pos, f) <= 5)
    # score += nearby_food * 3.0

    # # -----------------------------------------------------------------------
    # # Factor 5: Anti-estancamiento en esquinas
    # # -----------------------------------------------------------------------
    # if len(legal_actions) <= 2:
    #     # Penalización por estar en pasillo sin salida o esquina.
    #     # Si hay comida muy cerca, reducimos la penalización para no 
    #     # desincentivar entrar por ella.
    #     food_nearby_in_dead_end = sum(1 for f in food if manhattanDistance(pacman_pos, f) <= 3)
    #     corner_penalty = 100 - food_nearby_in_dead_end * 20
    #     score -= max(corner_penalty, 20) # Mínimo -20 aunque haya comida

    # # -----------------------------------------------------------------------
    # # Factor 6: Evitar zona de spawn de fantasmas
    # # -----------------------------------------------------------------------
    # walls = state.getWalls()
    # width, height = walls.width, walls.height
    # center = (width // 2, height // 2)
    # dist_to_center = manhattanDistance(pacman_pos, center)

    # if dist_to_center <= 4:
    #     for ghost_state in ghost_states:
    #         if ghost_state.scaredTimer == 0:
    #             ghost_pos = ghost_state.getPosition()
    #             ghost_dist = manhattanDistance(pacman_pos, ghost_pos)
    #             if ghost_dist <= 8:
    #                 score -= 100 / (ghost_dist + 1)
                    

    return score


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

# class MinimaxAgent(MultiAgentSearchAgent):
#     """
#     Your minimax agent (question 2)
#     """

#     def getAction(self, gameState: GameState):
#         """
#         Returns the minimax action from the current gameState using self.depth
#         and self.evaluationFunction.

#         Here are some method calls that might be useful when implementing minimax.

#         gameState.getLegalActions(agentIndex):
#         Returns a list of legal actions for an agent
#         agentIndex=0 means Pacman, ghosts are >= 1

#         gameState.generateSuccessor(agentIndex, action):
#         Returns the successor game state after an agent takes an action

#         gameState.getNumAgents():
#         Returns the total number of agents in the game

#         gameState.isWin():
#         Returns whether or not the game state is a winning state

#         gameState.isLose():
#         Returns whether or not the game state is a losing state
#         """
#         "*** YOUR CODE HERE ***"
#         util.raiseNotDefined()

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Minimax agent for Pacman with multiple ghosts
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction.
        """

        def minimax(agentIndex, depth, gameState):
            """
            Recursive minimax function

            Args:
            - agentIndex: Current agent (0=Pacman, 1+=Ghosts)
            - depth: Current depth in the game tree
            - gameState: Current state of the game

            Returns:
            - Best evaluation score for this state
            """
            # Base case: terminal state or maximum depth reached
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            # Pacman's turn (Maximizer)
            if agentIndex == 0:
                return maxValue(agentIndex, depth, gameState)
            # Ghost's turn (Minimizer)
            else:
                return minValue(agentIndex, depth, gameState)

        def maxValue(agentIndex, depth, gameState):
            """
            Handles Pacman's moves (maximizing player)
            """
            v = float('-inf')  # Start with worst possible value
            legalActions = gameState.getLegalActions(agentIndex)

            # No legal actions available
            if not legalActions:
                return self.evaluationFunction(gameState)

            # Try each possible action and choose the best
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                # After Pacman moves, first ghost plays (agent 1)
                v = max(v, minimax(1, depth, successor))
            return v

        def minValue(agentIndex, depth, gameState):
            """
            Handles Ghost moves (minimizing players)
            """
            v = float('inf')  # Start with best possible value for Pacman
            legalActions = gameState.getLegalActions(agentIndex)

            # No legal actions available
            if not legalActions:
                return self.evaluationFunction(gameState)

            # Determine next agent and depth
            nextAgent = agentIndex + 1
            nextDepth = depth

            # If all ghosts have moved, return to Pacman and increment depth
            if nextAgent == gameState.getNumAgents():
                nextAgent = 0      # Back to Pacman
                nextDepth = depth + 1  # New ply begins

            # Try each possible action and choose the worst for Pacman
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                v = min(v, minimax(nextAgent, nextDepth, successor))
            return v

        # Main decision logic for Pacman
        bestAction = None
        bestScore = float('-inf')

        # Try each legal action for Pacman
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            # Start minimax with first ghost (agent 1) at current depth
            score = minimax(1, 0, successor)

            if score > bestScore:
                bestScore = score
                bestAction = action

        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphabeta(agentIndex, depth, gameState, alpha, beta):
 
            if (gameState.isWin() or
                gameState.isLose() or
                depth == self.depth):
                return self.evaluationFunction(gameState)

            #Max (Pacman)
            if agentIndex == 0:
                return maxValue(agentIndex,depth,gameState,alpha,beta)

            #Min (Fantasmas)
            return minValue(agentIndex,depth,gameState,alpha,beta)

        def maxValue(agentIndex,depth,gameState,alpha,beta):

            v = float('-inf')
            legalActions = gameState.getLegalActions(agentIndex)

            if not legalActions:
                return self.evaluationFunction(gameState)

            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex,action)
                value = alphabeta(1,depth,successor,alpha,beta)
                v = max(v,value)

                #Hacemos poda
                if v >= beta:
                    return v

                alpha = max(alpha, v)

            return v


        def minValue(agentIndex,depth,gameState,alpha,beta):
            v = float('inf')


            legalActions = gameState.getLegalActions(agentIndex)

            if not legalActions:
                return self.evaluationFunction(gameState)

            nextAgent = agentIndex+1
            nextDepth = depth

            if nextAgent == gameState.getNumAgents():
                nextAgent = 0
                nextDepth = depth + 1

            for action in legalActions:

                successor = gameState.generateSuccessor(agentIndex,action)

                value= alphabeta(nextAgent,nextDepth,successor,alpha,beta)

                v = min(v,value)

                #Hacemos poda
                if v <= alpha:
                    return v

                beta = min(beta, v)

            return v

        alpha = float('-inf')
        beta = float('inf')

        bestAction = None
        bestScore = float('-inf')

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0,action)

            score = alphabeta(1,0,successor,alpha,beta)

            if score > bestScore:
                bestScore = score
                bestAction = action

            alpha = max(alpha,bestScore)

        return bestAction













class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction


###########################################################################
# Ahmed
###########################################################################

class NeuralAgentDummy(Agent):
    """
    Un agente de Pacman que utiliza una red neuronal para tomar decisiones
    basado en la evaluación del estado del juego.
    """
    def __init__(self, model_path="models/pacman_model.pth"):
        super().__init__()
        self.model = None
        self.input_size = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.load_model(model_path)

        # Mapeo de índices a acciones
        self.idx_to_action = {
            0: Directions.STOP,
            1: Directions.NORTH,
            2: Directions.SOUTH,
            3: Directions.EAST,
            4: Directions.WEST
        }

        # Para evaluar alternativas
        self.action_to_idx = {v: k for k, v in self.idx_to_action.items()}

        # Contador de movimientos
        self.move_count = 0

        print(f"NeuralAgent inicializado, usando dispositivo: {self.device}")

    def load_model(self, model_path):
        """Carga el modelo desde el archivo guardado"""
        try:
            if not os.path.exists(model_path):
                print(f"ERROR: No se encontró el modelo en {model_path}")
                return False

            # Cargar el modelo
            checkpoint = torch.load(model_path, map_location=self.device)
            self.input_size = checkpoint['input_size']

            # Crear y cargar el modelo
            self.model = PacmanNet(self.input_size, 128, 5).to(self.device)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.model.eval()  # Modo evaluación

            print(f"Modelo cargado correctamente desde {model_path}")
            print(f"Tamaño de entrada: {self.input_size}")
            return True
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")
            return False

    def state_to_matrix(self, state):
        """Convierte el estado del juego en una matriz numérica normalizada"""
        # Obtener dimensiones del tablero
        walls = state.getWalls()
        width, height = walls.width, walls.height

        # Crear una matriz numérica
        # 0: pared, 1: espacio vacío, 2: comida, 3: cápsula, 4: fantasma, 5: Pacman
        numeric_map = np.zeros((width, height), dtype=np.float32)

        # Establecer espacios vacíos (todo lo que no es pared comienza como espacio vacío)
        for x in range(width):
            for y in range(height):
                if not walls[x][y]:
                    numeric_map[x][y] = 1

        # Agregar comida
        food = state.getFood()
        for x in range(width):
            for y in range(height):
                if food[x][y]:
                    numeric_map[x][y] = 2

        # Agregar cápsulas
        for x, y in state.getCapsules():
            numeric_map[x][y] = 3

        # Agregar fantasmas
        for ghost_state in state.getGhostStates():
            ghost_x, ghost_y = int(ghost_state.getPosition()[0]), int(ghost_state.getPosition()[1])
            # Si el fantasma está asustado, marcarlo diferente
            if ghost_state.scaredTimer > 0:
                numeric_map[ghost_x][ghost_y] = 6  # Fantasma asustado
            else:
                numeric_map[ghost_x][ghost_y] = 4  # Fantasma normal

        # Agregar Pacman
        pacman_x, pacman_y = state.getPacmanPosition()
        numeric_map[int(pacman_x)][int(pacman_y)] = 5

        # Normalizar
        numeric_map = numeric_map / 6.0

        return numeric_map

    def neural_evaluation(self, state):
        """
        Una función de evaluación basada en la red neuronal y en heurísticas adicionales.
        """
        if self.model is None:
            return 0  # Si no hay modelo, devolver 0

        # Convertir a matriz
        state_matrix = self.state_to_matrix(state)

        # Convertir a tensor
        state_tensor = torch.FloatTensor(state_matrix).unsqueeze(0).to(self.device)

        # Obtener predicciones
        with torch.no_grad():
            output = self.model(state_tensor)
            probabilities = torch.nn.functional.softmax(output, dim=1).cpu().numpy()[0]

        # En lugar de sumar todas las probabilidades de acciones legales (que suele dar casi 100),
        # usamos la probabilidad de la MEJOR acción como indicador de calidad del estado.
        # Si la mejor acción tiene mucha probabilidad, es un estado "claro" y bueno.
        legal_actions = state.getLegalActions()
        action_probs = [probabilities[self.action_to_idx[action]] for action in legal_actions]

        if not action_probs:
            return 0

        # Normalización: El valor máximo posible es 1.0 (100%).
        # Multiplicamos por 100 para estar en la misma escala que la heurística.

        #norm_nn = max(action_probs) * 100.0
        norm_nn = max(action_probs)
        return norm_nn


    def getAction(self, state):
        """
        Devuelve la mejor acción basada en la evaluación de la red neuronal
        y heurísticas adicionales.
        """
        self.move_count += 1

        # Si no hay modelo, hacer un movimiento aleatorio
        if self.model is None:
            print("ERROR: Modelo no cargado. Haciendo movimiento aleatorio.")
            exit()
            legal_actions = state.getLegalActions()
            return random.choice(legal_actions)

        # Obtener acciones legales
        legal_actions = state.getLegalActions()

        # Evaluación directa con la red neuronal
        state_matrix = self.state_to_matrix(state)
        state_tensor = torch.FloatTensor(state_matrix).unsqueeze(0).to(self.device)

        with torch.no_grad():
            output = self.model(state_tensor)
            probabilities = torch.nn.functional.softmax(output, dim=1).cpu().numpy()[0]

        # Mapear índices del modelo a acciones del juego
        action_probs = []
        for idx, prob in enumerate(probabilities):
            action = self.idx_to_action[idx]
            if action in legal_actions:
                action_probs.append((action, prob))

        # Ordenar por probabilidad (mayor a menor)
        action_probs.sort(key=lambda x: x[1], reverse=True)

        # Exploración: con una probabilidad decreciente, elegir aleatoriamente
        exploration_rate = 0.2 * (0.99 ** self.move_count)  # Disminuye con el tiempo
        if random.random() < exploration_rate:
            # Excluir STOP si es posible
            if len(legal_actions) > 1 and Directions.STOP in legal_actions:
                legal_actions.remove(Directions.STOP)
            return random.choice(legal_actions)

        # Evaluación alternativa: generar sucesores y evaluar cada uno
        successors = []
        for action in legal_actions:
            successor = state.generateSuccessor(0, action)
            eval_score = self.neural_evaluation(successor)

            # Penalizar STOP a menos que sea la única opción
            if action == Directions.STOP and len(legal_actions) > 1:
                eval_score -= 50

            successors.append((action, eval_score))

        # Ordenar por puntuación combinada
        successors.sort(key=lambda x: x[1], reverse=True)

        # Devolver la mejor acción
        return successors[0][0]


class NeuralAgent(NeuralAgentDummy):
    """
    Un agente de Pacman que utiliza una red neuronal para tomar decisiones
    basado en la evaluación del estado del juego.
    """
    def __init__(self, model_path="models/pacman_model.pth"):
        super().__init__(model_path)

    def evaluationFunction(self, state):
        """
        Una función de evaluación basada en la red neuronal y en heurísticas adicionales.
        """
        # Obtener puntuación de la Red Neuronal
        nn_score = self.neural_evaluation(state)

        # Obtener puntuación de Heurísticas
        trad_score = traditional_evaluation(state)

        # Combinación de los resultados de la red y las heurísticas
        return nn_score + trad_score
        

    def getAction(self, state):
        """
        Devuelve la mejor acción basada en la evaluación de la red neuronal
        y heurísticas adicionales.
        """
        self.move_count += 1

        # Si no hay modelo, hacer un movimiento aleatorio
        if self.model is None:
            print("ERROR: Modelo no cargado. Haciendo movimiento aleatorio.")
            exit()
            legal_actions = state.getLegalActions()
            return random.choice(legal_actions)

        # Obtener acciones legales
        legal_actions = state.getLegalActions()

        # Evaluación directa con la red neuronal
        state_matrix = self.state_to_matrix(state)
        state_tensor = torch.FloatTensor(state_matrix).unsqueeze(0).to(self.device)

        with torch.no_grad():
            output = self.model(state_tensor)
            probabilities = torch.nn.functional.softmax(output, dim=1).cpu().numpy()[0]

        # Mapear índices del modelo a acciones del juego
        action_probs = []
        for idx, prob in enumerate(probabilities):
            action = self.idx_to_action[idx]
            if action in legal_actions:
                action_probs.append((action, prob))

        # Ordenar por probabilidad (mayor a menor)
        action_probs.sort(key=lambda x: x[1], reverse=True)

        # Exploración: con una probabilidad decreciente, elegir aleatoriamente
        exploration_rate = 0.2 * (0.99 ** self.move_count)  # Disminuye con el tiempo
        if random.random() < exploration_rate:
            # Excluir STOP si es posible
            if len(legal_actions) > 1 and Directions.STOP in legal_actions:
                legal_actions.remove(Directions.STOP)
            return random.choice(legal_actions)

        # Evaluación alternativa: generar sucesores y evaluar cada uno
        successors = []
        for action in legal_actions:
            successor = state.generateSuccessor(0, action)
            eval_score = self.evaluationFunction(successor)

            # Penalizar STOP a menos que sea la única opción
            if action == Directions.STOP and len(legal_actions) > 1:
                eval_score -= 50

            successors.append((action, eval_score))

        # Ordenar por puntuación combinada
        successors.sort(key=lambda x: x[1], reverse=True)

        # Devolver la mejor acción
        return successors[0][0]


# class NeuralAgent(Agent):
#     """
#     Un agente de Pacman que utiliza una red neuronal para tomar decisiones
#     basado en la evaluación del estado del juego.
#     """
#     def __init__(self, model_path="models/pacman_model.pth"):
#         super().__init__()
#         self.model = None
#         self.input_size = None
#         self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#         self.load_model(model_path)

#         # Mapeo de índices a acciones
#         self.idx_to_action = {
#             0: Directions.STOP,
#             1: Directions.NORTH,
#             2: Directions.SOUTH,
#             3: Directions.EAST,
#             4: Directions.WEST
#         }

#         # Para evaluar alternativas
#         self.action_to_idx = {v: k for k, v in self.idx_to_action.items()}

#         # Contador de movimientos
#         self.move_count = 0

#         print(f"NeuralAgent inicializado, usando dispositivo: {self.device}")

#     def load_model(self, model_path):
#         """Carga el modelo desde el archivo guardado"""
#         try:
#             if not os.path.exists(model_path):
#                 print(f"ERROR: No se encontró el modelo en {model_path}")
#                 return False

#             # Cargar el modelo
#             checkpoint = torch.load(model_path, map_location=self.device)
#             self.input_size = checkpoint['input_size']

#             # Crear y cargar el modelo
#             self.model = PacmanNet(self.input_size, 128, 5).to(self.device)
#             self.model.load_state_dict(checkpoint['model_state_dict'])
#             self.model.eval()  # Modo evaluación

#             print(f"Modelo cargado correctamente desde {model_path}")
#             print(f"Tamaño de entrada: {self.input_size}")
#             return True
#         except Exception as e:
#             print(f"Error al cargar el modelo: {e}")
#             return False

#     def state_to_matrix(self, state):
#         """Convierte el estado del juego en una matriz numérica normalizada"""
#         # Obtener dimensiones del tablero
#         walls = state.getWalls()
#         width, height = walls.width, walls.height

#         # Crear una matriz numérica
#         # 0: pared, 1: espacio vacío, 2: comida, 3: cápsula, 4: fantasma, 5: Pacman
#         numeric_map = np.zeros((width, height), dtype=np.float32)

#         # Establecer espacios vacíos (todo lo que no es pared comienza como espacio vacío)
#         for x in range(width):
#             for y in range(height):
#                 if not walls[x][y]:
#                     numeric_map[x][y] = 1

#         # Agregar comida
#         food = state.getFood()
#         for x in range(width):
#             for y in range(height):
#                 if food[x][y]:
#                     numeric_map[x][y] = 2

#         # Agregar cápsulas
#         for x, y in state.getCapsules():
#             numeric_map[x][y] = 3

#         # Agregar fantasmas
#         for ghost_state in state.getGhostStates():
#             ghost_x, ghost_y = int(ghost_state.getPosition()[0]), int(ghost_state.getPosition()[1])
#             # Si el fantasma está asustado, marcarlo diferente
#             if ghost_state.scaredTimer > 0:
#                 numeric_map[ghost_x][ghost_y] = 6  # Fantasma asustado
#             else:
#                 numeric_map[ghost_x][ghost_y] = 4  # Fantasma normal

#         # Agregar Pacman
#         pacman_x, pacman_y = state.getPacmanPosition()
#         numeric_map[int(pacman_x)][int(pacman_y)] = 5

#         # Normalizar
#         numeric_map = numeric_map / 6.0

#         return numeric_map

#     def evaluationFunction(self, state):
#         """
#         Una función de evaluación basada en la red neuronal y en heurísticas adicionales.
#         """
#         if self.model is None:
#             return 0  # Si no hay modelo, devolver 0

#         # Convertir a matriz
#         state_matrix = self.state_to_matrix(state)

#         # Convertir a tensor
#         state_tensor = torch.FloatTensor(state_matrix).unsqueeze(0).to(self.device)

#         # Obtener predicciones
#         with torch.no_grad():
#             output = self.model(state_tensor)
#             probabilities = torch.nn.functional.softmax(output, dim=1).cpu().numpy()[0]

#         # Obtener acciones legales
#         legal_actions = state.getLegalActions()

#         # Aplicar heurísticas adicionales, similar a betterEvaluationFunction
#         score = state.getScore()

#         # Mejorar la evaluación con conocimiento del dominio
#         pacman_pos = state.getPacmanPosition()
#         food = state.getFood().asList()
#         ghost_states = state.getGhostStates()

#         # Factor 1: Distancia a la comida más cercana
#         if food:
#             min_food_distance = min(manhattanDistance(pacman_pos, food_pos) for food_pos in food)
#             score += 1.0 / (min_food_distance + 1)

#         # Factor 2: Proximidad a fantasmas
#         for ghost_state in ghost_states:
#             ghost_pos = ghost_state.getPosition()
#             ghost_distance = manhattanDistance(pacman_pos, ghost_pos)

#             if ghost_state.scaredTimer > 0:
#                 # Si el fantasma está asustado, acercarse a él
#                 score += 50 / (ghost_distance + 1)
#             else:
#                 # Si no está asustado, evitarlo
#                 if ghost_distance <= 2:
#                     score -= 200  # Gran penalización por estar demasiado cerca

#         # Factor 3: Cápsulas
#         capsules = state.getCapsules()
#         if capsules:
#             min_capsule_distance = min(manhattanDistance(pacman_pos, cap_pos) for cap_pos in capsules)
#             score += 10 / (min_capsule_distance + 1)

#         # Factor 4: Densidad Local de Comida
#         # Cuenta cuánta comida hay en un radio de 4 pasos y premia ir hacia grupos grandes.
#         nearby_food = sum(1 for food_pos in food if manhattanDistance(pacman_pos, food_pos) <= 4)
#         score += nearby_food * 2.0  # Cada comida cercana aporta +2.0

#         # Factor 5: Radar Preventivo de Fantasmas
#         for ghost_state in ghost_states:
#             if ghost_state.scaredTimer == 0:  # Solo si son peligrosos
#                 ghost_pos = ghost_state.getPosition()
#                 ghost_distance = manhattanDistance(pacman_pos, ghost_pos)
#                 if 2 < ghost_distance <= 5:  # Si están cerca pero no en rango letal
#                     score -= 20.0 / ghost_distance

#         # Factor 6: Prevención de Caza Suicida
#         # Si un fantasma asustado va a "despertar" antes de que lleguemos, anulamos la atracción.
#         for ghost_state in ghost_states:
#             if ghost_state.scaredTimer > 0:
#                 ghost_pos = ghost_state.getPosition()
#                 ghost_distance = manhattanDistance(pacman_pos, ghost_pos)

#                 # Si estamos más lejos que el tiempo que le queda de miedo
#                 if ghost_distance > ghost_state.scaredTimer:
#                     # Anulamos el incentivo de ir tras él
#                     score -= 50 / (ghost_distance + 1)


#         #################
#         # Sergi
#         #################
#         # Factor 7: No cazar si cerca de origen de fantasmas
#         for ghost_state in ghost_states:
#             if ghost_state.scaredTimer > 0:
#                 walls = state.getWalls() #Obtenemos dimensiones del mapa
#                 width, height = walls.width, walls.height
#                 #Suponemos que el spawn de los fantasmas siempre está en el centro del mapa
#                 map_center_distance = manhattanDistance(pacman_pos,
#                                                      (width//2,
#                                                       height//2))
#                 #Evitamos cazar cerca del spawn de fantasmas
#                 score -= 50 / (map_center_distance + 1)


#         # Factor 8: Evitar esquinas
#         for ghost_states in ghost_states:
#             if ghost_state.scaredTimer == 0:
#                 walls = state.getWalls() #Obtenemos dimensiones del mapa
#                 width, height = walls.width, walls.height
#                 # Coordenadas de las esquiinas del mapa
#                 corners = [(width,height),(0,0),(0,height),(width,0)]
#                 for corner_pos in corners:
#                     corner_distance = manhattanDistance(pacman_pos, corner_pos)
#                     if corner_distance<=5:
#                         # Intentar evitar esquinas
#                         # Reducimos poco el score para que solo evite las esquinas si no queda comida por esa zona
#                         score -= 10 / corner_distance + 1

#         # Combinar la puntuación de la red con la heurística
#         neural_score = 0
#         for i, action in enumerate(self.idx_to_action.values()):
#             if action in legal_actions:
#                 neural_score += probabilities[i] * 100

#         return score + neural_score

#     def getAction(self, state):
#         """
#         Devuelve la mejor acción basada en la evaluación de la red neuronal
#         y heurísticas adicionales.
#         """
#         self.move_count += 1

#         # Si no hay modelo, hacer un movimiento aleatorio
#         if self.model is None:
#             print("ERROR: Modelo no cargado. Haciendo movimiento aleatorio.")
#             exit()
#             legal_actions = state.getLegalActions()
#             return random.choice(legal_actions)

#         # Obtener acciones legales
#         legal_actions = state.getLegalActions()

#         # Evaluación directa con la red neuronal
#         state_matrix = self.state_to_matrix(state)
#         state_tensor = torch.FloatTensor(state_matrix).unsqueeze(0).to(self.device)

#         with torch.no_grad():
#             output = self.model(state_tensor)
#             probabilities = torch.nn.functional.softmax(output, dim=1).cpu().numpy()[0]

#         # Mapear índices del modelo a acciones del juego
#         action_probs = []
#         for idx, prob in enumerate(probabilities):
#             action = self.idx_to_action[idx]
#             if action in legal_actions:
#                 action_probs.append((action, prob))

#         # Ordenar por probabilidad (mayor a menor)
#         action_probs.sort(key=lambda x: x[1], reverse=True)

#         # Exploración: con una probabilidad decreciente, elegir aleatoriamente
#         exploration_rate = 0.2 * (0.99 ** self.move_count)  # Disminuye con el tiempo
#         if random.random() < exploration_rate:
#             # Excluir STOP si es posible
#             if len(legal_actions) > 1 and Directions.STOP in legal_actions:
#                 legal_actions.remove(Directions.STOP)
#             return random.choice(legal_actions)

#         # Evaluación alternativa: generar sucesores y evaluar cada uno
#         successors = []
#         for action in legal_actions:
#             successor = state.generateSuccessor(0, action)
#             eval_score = self.evaluationFunction(successor)
#             neural_score = 0
#             for a, p in action_probs:
#                 if a == action:
#                     neural_score = p * 100
#                     break
#             # Combinar evaluación heurística con la predicción de la red
#             combined_score = eval_score + neural_score

#             # Penalizar STOP a menos que sea la única opción
#             if action == Directions.STOP and len(legal_actions) > 1:
#                 combined_score -= 50

#             successors.append((action, combined_score))

#         # Ordenar por puntuación combinada
#         successors.sort(key=lambda x: x[1], reverse=True)

#         # Devolver la mejor acción
#         return successors[0][0]

# Definir una función para crear el agente
def createNeuralAgent(model_path="models/pacman_model.pth"):
    """
    Función de fábrica para crear un agente neuronal.
    Útil para integrarse con la estructura de pacman.py.
    """
    return NeuralAgent(model_path)



class AlphaBetaNeuralAgent(AlphaBetaAgent):
    
    def __init__(self,
                 evalFn='scoreEvaluationFunction',
                 depth='3',
                 start_heuristicsWeight=0.3,  # Peso de AlphaBeta al INICIO
                 start_nnWeight=0.7,          # Peso de la Red Neuronal al INICIO
                 end_heuristicsWeight=0.7,    # Peso de AlphaBeta al FINAL
                 end_nnWeight=0.3):           # Peso de la Red Neuronal al FINAL):
        super().__init__(evalFn, depth)

        self.evaluationFunction = self.evaluation_combined
        
        # Guardamos los límites de la transición
        self.start_w_heuristic = start_heuristicsWeight
        self.start_w_neural = start_nnWeight
        self.end_w_heuristic = end_heuristicsWeight
        self.end_w_neural = end_nnWeight
        
        # Pesos actuales que usará evaluation_combined
        self.w_heuristic = self.start_w_heuristic
        self.w_neural = self.start_w_neural
        
        self.neural_agent_dummy = NeuralAgentDummy()
        
        # Guardaremos la cantidad inicial de comida para calcular el progreso
        self.initial_food = None
    
    def evaluation_combined(self, state):
        # 1) Traditional score (with the new heuristics from Task 1)
        trad_score = traditional_evaluation(state)
        #print(f"Heuristic score: {trad_score}")

        # 2) Neural network score
        neural_score = self.neural_agent_dummy.neural_evaluation(state)
        #print(f"Neural network score: {neural_score}")

        # 3) Weighted combination
        return self.w_heuristic * trad_score + self.w_neural * neural_score


    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # 1. Registrar la comida inicial en el primer turno
        if self.initial_food is None:
            self.initial_food = gameState.getNumFood()
            # Si el mapa empieza sin comida (raro, pero previene división por cero)
            if self.initial_food == 0:
                self.initial_food = 1 

        # 2. Calcular el progreso del juego (de 0.0 al inicio, a 1.0 al final)
        current_food = gameState.getNumFood()
        progress = 1.0 - (current_food / self.initial_food)

        # 3. Interpolación lineal de los pesos
        self.w_heuristic = self.start_w_heuristic * (1 - progress) + self.end_w_heuristic * progress
        self.w_neural = self.start_w_neural * (1 - progress) + self.end_w_neural * progress


        def alphabeta(agentIndex, depth, gameState, alpha, beta):

            if (gameState.isWin() or
                gameState.isLose() or
                depth == self.depth):
                return self.evaluationFunction(gameState)
                # heuristic = traditional_evaluation(gameState)
                # nnScore = AlphaBetaNeuralAgent.neural_agent_dummy.neural_evaluation(gameState)
                # print(heuristic)
                # print(nnScore)
                # return (0.7*heuristic + 0.3*nnScore)

            #Max (Pacman)
            if agentIndex == 0:
                return maxValue(agentIndex,depth,gameState,alpha,beta)

            #Min (Fantasmas)
            return minValue(agentIndex,depth,gameState,alpha,beta)

        def maxValue(agentIndex,depth,gameState,alpha,beta):

            v = float('-inf')
            legalActions = gameState.getLegalActions(agentIndex)

            if not legalActions:
                return self.evaluationFunction(gameState)

            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex,action)
                value = alphabeta(1,depth,successor,alpha,beta)
                v = max(v,value)

                #Hacemos poda
                if v >= beta:
                    return v

                alpha = max(alpha, v)

            return v


        def minValue(agentIndex,depth,gameState,alpha,beta):
            v = float('inf')


            legalActions = gameState.getLegalActions(agentIndex)

            if not legalActions:
                return self.evaluationFunction(gameState)

            nextAgent = agentIndex+1
            nextDepth = depth

            if nextAgent == gameState.getNumAgents():
                nextAgent = 0
                nextDepth = depth + 1

            for action in legalActions:

                successor = gameState.generateSuccessor(agentIndex,action)

                value= alphabeta(nextAgent,nextDepth,successor,alpha,beta)

                v = min(v,value)

                #Hacemos poda
                if v <= alpha:
                    return v

                beta = min(beta, v)

            return v

        alpha = float('-inf')
        beta = float('inf')

        bestAction = None
        bestScore = float('-inf')

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0,action)

            score = alphabeta(1,0,successor,alpha,beta)

            if score > bestScore:
                bestScore = score
                bestAction = action

            alpha = max(alpha,bestScore)

        return bestAction


