# funciones.py
# Este archivo contiene la lógica y mecánicas del juego: inicialización, colocación aleatoria, disparos, comprobaciones, ...

# crear_tableros(tamaño)
# colocar_barco(barco, tablero)
# disparar(casilla, tablero_barcos, tablero_disparos)
# crear_barco(eslora, tamaño_tablero=10)
# colocar_flota(tablero)
# comprobar_fin_juego(tablero_barcos)
# mostrar_tableros_jugador(tablero_barcos, tablero_disparos)
# obtener_adyacentes_validas(casilla, tablero_disparos_rival)

import numpy as np
import variables

def crear_tablero(tamano=variables.TAMANO_TABLERO):
    """Crea un tablero de tamaño NxN relleno con el carácter "_" de agua."""
    tablero = np.full((tamano, tamano), variables.AGUA, dtype=str)
    return tablero

def colocar_barco(barco, tablero):
    """Coloca las casillas de un barco ('O') en el tablero dado."""
    for casilla in barco:
        fila = casilla[0]
        columna = casilla[1]
        tablero[fila, columna] = variables.BARCO
    return tablero

def disparar(casilla, tablero_barcos_defensor, tablero_disparos_atacante):
    """
    Se procesa el disparo en una casilla. Modifica los tableros correspondientes.
    Devuelve True si es un acierto (Tocado) y False si es agua o ya se había disparado en esa casilla.
    """
    fila = casilla[0]
    columna = casilla[1]
    if tablero_barcos_defensor[fila, columna] == variables.BARCO: # Si hay un barco, es un acierto
        tablero_barcos_defensor[fila, columna] = variables.TOCADO
        tablero_disparos_atacante[fila, columna] = variables.TOCADO
        return True
    else:
        if tablero_barcos_defensor[fila, columna] == variables.AGUA: # Si es agua, se procesa como fallo
            tablero_barcos_defensor[fila, columna] = variables.FALLO
            tablero_disparos_atacante[fila, columna] = variables.FALLO
        else: # Si ya se había disparado antes (X ó A), se queda igual pero se procesa como fallo y pérdida de turno
            pass
        return False

def crear_barco(eslora, tablero):
    """
    Intenta crear una lista de casillas para un barco de forma aleatoria (horizontal o vertical).
    Verifica que no se salga del tablero y que no se solape con barcos existentes.
    Devuelve la lista de casillas si es válido, o una lista vacía si hay conflicto.
    """
    orientacion = np.random.randint(0, 2) # 0 para Horizontal, 1 para Vertical
    if orientacion == 0: # Horizontal
        fila_inicial = np.random.randint(0, variables.TAMANO_TABLERO)
        columna_inicial = np.random.randint(0, variables.TAMANO_TABLERO - eslora + 1)
        casillas_propuestas = []
        valido = True
        for desplazamiento in range(eslora): # Comprobar solapamientos
            columna_actual = columna_inicial + desplazamiento
            if tablero[fila_inicial, columna_actual] == variables.BARCO:
                valido = False
            else:
                casillas_propuestas.append((fila_inicial, columna_actual))
        if valido:
            return casillas_propuestas
        else:
            return []
    else: # Vertical
        fila_inicial = np.random.randint(0, variables.TAMANO_TABLERO - eslora + 1)
        columna_inicial = np.random.randint(0, variables.TAMANO_TABLERO)
        casillas_propuestas = []
        valido = True
        for desplazamiento in range(eslora): # Comprobar solapamientos
            fila_actual = fila_inicial + desplazamiento
            if tablero[fila_actual, columna_inicial] == variables.BARCO:
                valido = False
            else:
                casillas_propuestas.append((fila_actual, columna_inicial))
        if valido:
            return casillas_propuestas
        else:
            return []

def colocar_flota(tablero):
    """Genera y coloca todos los barcos de la lista de esloras en el tablero de forma aleatoria."""
    for eslora in variables.ESLORAS_BARCOS:
        barco_colocado = False
        while not barco_colocado: # Bucle de reintento hasta que el barco encuentra un sitio válido sin solaparse
            lista_casillas = crear_barco(eslora, tablero)
            if len(lista_casillas) > 0:
                tablero = colocar_barco(lista_casillas, tablero)
                barco_colocado = True
    return tablero

def comprobar_fin_juego(tablero_barcos):
    """Devuelve True si ya no quedan barcos ('O') en el tablero."""
    quedan_barcos = variables.BARCO in tablero_barcos
    if not quedan_barcos:
        return True
    else:
        return False

def mostrar_tableros_jugador(tablero_barcos, tablero_disparos):
    """Muestra por terminal o consola los tableros del jugador con coordenadas filas y columnas."""
    cabecera_columnas = "  0  1  2  3  4  5  6  7  8  9"
    print("\n***** MI FLOTA DE BARCOS ******")
    print(cabecera_columnas)
    for i, fila in enumerate(tablero_barcos):
        # Imprime el número de fila (0-9) 
        print(str(i) + " ".join(fila))
    print("\n***** LA FLOTA DEL ENEMIGO ****")   
    print(cabecera_columnas)
    for i, fila in enumerate(tablero_disparos):
        print(str(i) + " ".join(fila))
    print("*******************************\n")

def obtener_adyacentes_validas(casilla, tablero_disparos_rival):
    """Devuelve una lista de casillas vecinas (N, S, E, O) válidas y no disparadas."""
    fila, columna = casilla
    adyacentes = []
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Posibles movimientos: Arriba, Abajo, Izquierda, Derecha
    for df, dc in movimientos:
        nueva_f = fila + df
        nueva_c = columna + dc
        if 0 <= nueva_f < variables.TAMANO_TABLERO and 0 <= nueva_c < variables.TAMANO_TABLERO: # Comprobar que está dentro del tablero
            if tablero_disparos_rival[nueva_f, nueva_c] == variables.AGUA: # Comprobar que no se haya disparado ya en esa casilla (que siga siendo AGUA o BARCO oculto)
                adyacentes.append((nueva_f, nueva_c))
    return adyacentes
