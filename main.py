
# main.py
# Este es el archivo principal del juego que coordina el flujo por turnos.

import numpy as np
import variables
import funciones

print("\nVersión de Python del juego HUNDIR LA FLOTA.")
print("********************************************\n")
nombre_jugador = input("Introduce el nombre del jugador: ")

# Creación de los 4 tableros de juego
tablero_barcos_jugador = funciones.crear_tablero()
tablero_disparos_jugador = funciones.crear_tablero()
tablero_barcos_rival = funciones.crear_tablero()
tablero_disparos_rival = funciones.crear_tablero()
    
# Colocación de barcos 
tablero_barcos_jugador = funciones.colocar_flota(tablero_barcos_jugador)
tablero_barcos_rival = funciones.colocar_flota(tablero_barcos_rival)

# Determinar aleatoriamente quién empieza la partida (el turno de inicio)
turno_jugador = False
turno_de_inicio = np.random.randint(0, 2) # 1 = Turno Jugador, 0 = Turno Máquina
if turno_de_inicio == 1:
    turno_jugador = True
    print("Empiezas jugando tú", nombre_jugador)
else:
    print("Empieza jugando LA MÁQUINA 🤖...")
juego_activo = True
while juego_activo:
    if turno_jugador:
        print("\nEs tu turno", nombre_jugador)
        funciones.mostrar_tableros_jugador(tablero_barcos_jugador, tablero_disparos_jugador)
        
        # Entrada de coordenadas por terminal/consola 
        fila_valida = False
        while not fila_valida:
            try:
                fila_entrada = int(input("🎯 introduce fila (0-" + str(variables.TAMANO_TABLERO-1) + "): "))
                if 0 <= fila_entrada < variables.TAMANO_TABLERO:
                    fila_valida = True
                else:
                    print("⚠️ Fila fuera de rango. Prueba otra vez", nombre_jugador)
            except ValueError:
                print("⚠️ Error: ¡Debes introducir un dígito numérico para la fila!", nombre_jugador)
        columna_valida = False
        while not columna_valida:
            try:
                columna_entrada = int(input("🎯 introduce columna (0-" + str(variables.TAMANO_TABLERO-1) + "): "))
                if 0 <= columna_entrada < variables.TAMANO_TABLERO:
                    columna_valida = True
                else:
                    print("⚠️ Columna fuera de rango. Prueba otra vez", nombre_jugador)
            except ValueError:
                print("⚠️ Error: ¡Debes introducir un dígito numérico para la columna!", nombre_jugador)
        casilla_disparo = (fila_entrada, columna_entrada)

        # Ejecutando el disparo 
        acierto = funciones.disparar(casilla_disparo, tablero_barcos_rival, tablero_disparos_jugador)
        if acierto:
            print("\nTOCADO! 💥 Tu disparo ha acertado en uno de los barcos enemigos 🚢💥... ")
            # Al comprobar el fin del juego, si es verdadero, termina la partida
            if funciones.comprobar_fin_juego(tablero_barcos_rival):
                print("\n¡ENHORABUENA", nombre_jugador,"!. Has 🔥 TOCADO Y HUNDIDO 🔥 todos los barcos de la máquina. ¡HAS GANADO!")
                juego_activo = False
        else:
            print("\n¡AGUA! 💦 Has fallado tu disparo.")
            turno_jugador = False # Cambio de turno


    else: # Es el turno de LA MÁQUINA
        print("\nEs el turno de LA MÁQUINA 🤖...")

        if variables.IA_MODO_CAZA and variables.IA_ADYACENTES_PENDIENTES: # DETERMINAR COORDENADAS DE DISPARO
            casilla_maquina = variables.IA_ADYACENTES_PENDIENTES.pop(0) # Extrae la siguiente casilla adyacente de la lista
            fila_maquina, columna_maquina = casilla_maquina
        else: # dispara al azar (si no está en modo caza o se le acabaron las adyacentes)
            intento_valido = False 

            while not intento_valido: # Aseguramos que no repita una casilla ya disparada al azar
                fila_maquina = np.random.randint(0, variables.TAMANO_TABLERO)
                columna_maquina = np.random.randint(0, variables.TAMANO_TABLERO)

                if tablero_disparos_rival[fila_maquina, columna_maquina] == variables.AGUA:
                    intento_valido = True
            casilla_maquina = (fila_maquina, columna_maquina)

        print("La máquina dispara a la casilla: 🎯 Fila:", fila_maquina, "y Columna:", columna_maquina)
        acierto_maquina = funciones.disparar(casilla_maquina, tablero_barcos_jugador, tablero_disparos_rival)
        
        if acierto_maquina: # GESTIÓN DEL DISPARO CONTRA EL JUGADOR
            print("¡La máquina te ha TOCADO uno de tus barcos! 🚢💥... la máquina activa el modo caza 🤬")
            variables.IA_MODO_CAZA = True # ACTIVAR MODO CAZA
            variables.IA_ULTIMO_TOCADO = casilla_maquina
            nuevas_adyacentes = funciones.obtener_adyacentes_validas(casilla_maquina, tablero_disparos_rival) # Obtener nuevas adyacentes desde este nuevo impacto y sumarlas a la lista de objetivos
            
            for adyacente in nuevas_adyacentes:
                if adyacente not in variables.IA_ADYACENTES_PENDIENTES:
                    variables.IA_ADYACENTES_PENDIENTES.append(adyacente)
        
            if funciones.comprobar_fin_juego(tablero_barcos_jugador): # Comprobar si la máquina ha ganado
                print("\n¡Lo siento! La máquina ha 🔥 TOCADO Y HUNDIDO 🔥 todos tus barcos. ¡HAS PERDIDO", nombre_jugador, "! Gracias por jugar.")
                juego_activo = False
        else:
            print("La máquina ha disparado al AGUA... 💦")
            
            if len(variables.IA_ADYACENTES_PENDIENTES) == 0: # Si se quedó sin adyacentes que probar tras este fallo, apaga el modo caza
                variables.IA_MODO_CAZA = False
                
            turno_jugador = True # Cambio de turno
