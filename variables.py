# variables.py
# Este archivo contiene las (constantes) variables y la configuración inicial.

# Configuración del tablero
TAMANO_TABLERO = 10

# Representaciones del juego
#AGUA = "_" 
#BARCO = "O"
#TOCADO = "X"
#FALLO = "A"
AGUA = "🟦"
BARCO = "🚢"
TOCADO = "💥"
FALLO = "❌"

# esloras: Configuración de los barcos 
#ESLORAS_BARCOS = [2, 2, 2, 3, 3, 4] # en teoria (mas colisiones al pisarse) sería menos eficiente 
ESLORAS_BARCOS = [4, 3, 3, 2, 2, 2]