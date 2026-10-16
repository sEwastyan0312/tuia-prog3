"""
Módulo de estrategias para el juego del Tateti

Este módulo contiene las estrategias para elegir la acción a realizar.
Los alumnos deben implementar la estrategia minimax.

Por defecto, se incluye una estrategia aleatoria como ejemplo base.
"""

import random
from typing import List, Tuple
from tateti import Tateti, JUGADOR_MAX, JUGADOR_MIN

def estrategia_aleatoria(tateti: Tateti, estado: List[List[str]]) -> Tuple[int, int]:
    """
    Estrategia aleatoria: elige una acción al azar entre las disponibles.
  
    Args:
        tateti: Instancia de la clase Tateti
        estado: Estado actual del tablero
        
    Returns:
        Tuple[int, int]: Acción elegida (fila, columna)

    Raises:
        ValueError: Si no hay acciones disponibles
    """
    acciones_disponibles = tateti.acciones(estado)
    if not acciones_disponibles:
        raise ValueError("No hay acciones disponibles")
    
    return random.choice(acciones_disponibles)

def estrategia_minimax(tateti: Tateti, estado: List[List[str]]) -> Tuple[int, int]:
    """
    Estrategia minimax: elige la mejor acción usando el algoritmo minimax.
    
    Args:
        tateti: Instancia de la clase Tateti
        estado: Estado actual del tablero
        
    Returns:
        Tuple[int, int]: Acción elegida (fila, columna)
        
    Raises:
        NotImplementedError: Hasta que el alumno implemente el algoritmo
    """

     jugador_actual = tateti.jugador(estado)

    def max_value(estado):
        if tateti.test_terminal(estado):
            return tateti.utilidad(estado, JUGADOR_MAX)

        v = float("-inf")
        for accion in tateti.acciones(estado):
            v = max(v, min_value(tateti.resultado(estado, accion)))
        return v

    def min_value(estado):
        if tateti.test_terminal(estado):
            return tateti.utilidad(estado, JUGADOR_MAX)

        v = float("inf")
        for accion in tateti.acciones(estado):
            v = min(v, max_value(tateti.resultado(estado, accion)))
        return v

    mejor_accion = None

    if jugador_actual == JUGADOR_MAX:
        mejor_valor = float("-inf")
        for accion in tateti.acciones(estado):
            valor = min_value(tateti.resultado(estado, accion))
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_accion = accion
    else:
        mejor_valor = float("inf")
        for accion in tateti.acciones(estado):
            valor = max_value(tateti.resultado(estado, accion))
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_accion = accion

    return mejor_accion
    # TODO: Implementar algoritmo minimax

    # INSTRUCCIONES:
    # 1. Eliminar la línea 'raise NotImplementedError...' de abajo
    # 2. Implementar el algoritmo minimax aquí
    # 3. La función debe retornar una tupla (fila, columna) con la mejor jugada

    # raise NotImplementedError(
    #    "\n" + "="*60 +
    #    "\n🚫 ALGORITMO MINIMAX NO IMPLEMENTADO" +
    #    "\n" + "="*60 +
    #    "\n\nPara usar la estrategia Minimax debe implementarla primero." +
    #    "\n\nInstrucciones:" +
    #    "\n1. Abra el archivo 'estrategias.py'" +
    #    "\n2. Busque la función 'estrategia_minimax()'" +
    #    "\n3. Elimine la línea 'raise NotImplementedError(...)'" +
    #    "\n4. Implemente el algoritmo minimax" +
    #    "\n\nMientras tanto, use la 'Estrategia Aleatoria'." +
    #    "\n" + "="*60
    # )
