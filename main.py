
# main.py
# Este es el archivo principal del juego que coordina el flujo por turnos.

import numpy as np
import variables
import funciones

print("\nVersión de Python del juego HUNDIR LA FLOTA.")
print("********************************************")
nombre_jugador = input("Introduce el nombre del jugador: ")

# Creación de los 4 tableros de juego
tablero_barcos_jugador = funciones.crear_tablero()
tablero_disparos_jugador = funciones.crear_tablero()
tablero_barcos_rival = funciones.crear_tablero()
tablero_disparos_rival = funciones.crear_tablero()
    
# Colocación de barcos v0
# tablero_barcos_jugador = funciones.colocar_flota(tablero_barcos_jugador)
# tablero_barcos_rival = funciones.colocar_flota(tablero_barcos_rival)

# Colocación de barcos v1 (añadimos el argumento para identificar el dueño)
tablero_barcos_jugador = funciones.colocar_flota(tablero_barcos_jugador, es_jugador=True)
tablero_barcos_rival = funciones.colocar_flota(tablero_barcos_rival, es_jugador=False)

# Determinar aleatoriamente quién empieza la partida (el turno de inicio)
turno_jugador = False
turno_de_inicio = np.random.randint(0, 2) # 1 = Turno Jugador, 0 = Turno Máquina

if turno_de_inicio == 1:
    turno_jugador = True
    print("Empiezas disparando tú, Sargento", nombre_jugador)
else:
    print("La guerra empieza disparando LA MÁQUINA 🤖...")
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
                    print("⚠️ Fila fuera de rango❗ Prueba otra vez", nombre_jugador)
            except ValueError:
                print("⚠️ Error❗ Debes introducir un dígito numérico para la fila", nombre_jugador)
        columna_valida = False

        while not columna_valida:
            try:
                columna_entrada = int(input("🎯 introduce columna (0-" + str(variables.TAMANO_TABLERO-1) + "): "))
                if 0 <= columna_entrada < variables.TAMANO_TABLERO:
                    columna_valida = True
                else:
                    print("⚠️ Columna fuera de rango❗ Prueba otra vez", nombre_jugador)
            except ValueError:
                print("⚠️ Error❗ Debes introducir un dígito numérico para la columna", nombre_jugador)
        casilla_disparo = (fila_entrada, columna_entrada)

        # Ejecutando el disparo 
        impactos_antes = np.sum(tablero_disparos_jugador == variables.TOCADO) # Contamos cuántos impactos exitosos tenía el jugador ANTES de este disparo
        acierto = funciones.disparar(casilla_disparo, tablero_barcos_rival, tablero_disparos_jugador)
        
        if acierto:
            print("\n💥 ¡TOCADO! 🔥 Tu disparo ha acertado en uno de los barcos enemigos 🚢💥🔥... ")
            impactos_actuales = impactos_antes + 1 # Calculamos los rangos militares usando los impactos actualizados
            
            if impactos_actuales < len(variables.rango_jugador): # Controlamos que el índice no supere el tamaño de la lista
                rango_anterior = variables.rango_jugador[impactos_antes]
                rango_nuevo = variables.rango_jugador[impactos_actuales]
                print("⚓ INFORME DE LA ARMADA para:", nombre_jugador.upper(), "🎖️")
                print("⚓ ¡Impacto confirmado! 👉 Asciendes del rango de", rango_anterior, "al rango de:", rango_nuevo.upper(), "🎖️")
            
            # CÁLCULO Y MUESTRA DE BARCOS HUNDIDOS DEL ENEMIGO
            total_barcos = len(variables.ESLORAS_BARCOS)
            maquina_hundidos = funciones.contar_barcos_hundidos(variables.FLOTA_MAQUINA, tablero_barcos_rival)
            print("ℹ️ 📄 Informe de Inteligencia 📢 Se han hundido "+ str(maquina_hundidos)+ " barcos de la flota de "+str(total_barcos)+" barcos enemigos.")
            
            if funciones.comprobar_fin_juego(tablero_barcos_rival): # Al comprobar el fin del juego, si es verdadero, termina la partida
                print("\n📣 ¡ENHORABUENA", nombre_jugador, "!. 🥳 🎉 Has TOCADO Y HUNDIDO 🔥 toda la flota enemiga")
                print("\n🏆 ¡HAS GANADO LA GUERRA! 🎖️ Y has alcanzado el rango de:", variables.rango_jugador[-1].upper() )
                juego_activo = False

        else:
            print("¡AGUA! 💦 Has fallado tu disparo.")
            turno_jugador = False # Cambio de turno


    else: # Es el turno de LA MÁQUINA
        print("Es el turno de LA MÁQUINA 🤖...")

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

        print("🤖 La máquina dispara a la casilla: 🎯 Fila:", fila_maquina, "y Columna:", columna_maquina)
        acierto_maquina = funciones.disparar(casilla_maquina, tablero_barcos_jugador, tablero_disparos_rival)

        if acierto_maquina: # GESTIÓN DEL DISPARO CONTRA EL JUGADOR
            print("🤖 ¡La máquina te ha TOCADO uno de tus barcos! 🚢💥... ⚠️ la máquina ha activado el modo inteligencia de guerra 🤬")
            
            # CÁLCULO DE BARCOS HUNDIDOS DEL JUGADOR
            total_barcos = len(variables.ESLORAS_BARCOS)
            jugador_hundidos = funciones.contar_barcos_hundidos(variables.FLOTA_JUGADOR, tablero_barcos_jugador)
            print("ℹ️ ¡Informe de Inteligencia📄! 📢 ¡Atención! 🤖 La máquina ha hundido "+str(jugador_hundidos) +" barcos de tu flota de " +str(total_barcos) +" barcos.")
            
            variables.IA_MODO_CAZA = True # ACTIVAR MODO CAZA
            variables.IA_ULTIMO_TOCADO = casilla_maquina
            nuevas_adyacentes = funciones.obtener_adyacentes_validas(casilla_maquina, tablero_disparos_rival) # Obtener nuevas adyacentes desde este nuevo impacto y sumarlas a la lista de objetivos
            
            for adyacente in nuevas_adyacentes:
                if adyacente not in variables.IA_ADYACENTES_PENDIENTES:
                    variables.IA_ADYACENTES_PENDIENTES.append(adyacente)

            if funciones.comprobar_fin_juego(tablero_barcos_jugador): # Comprobar si la máquina ha ganado
                print("\n¡Lo siento! 🤖 La máquina ha TOCADO Y HUNDIDO 🔥 todos tus barcos. 📣 ¡HAS PERDIDO LA GUERRA", nombre_jugador, "! Gracias por jugar.")
                juego_activo = False
        else:
            print("🤖 La máquina ha disparado al AGUA... 💦")
            
            if len(variables.IA_ADYACENTES_PENDIENTES) == 0: # Si se quedó sin adyacentes que probar tras este fallo, apaga el modo caza
                variables.IA_MODO_CAZA = False
                
            turno_jugador = True # Cambio de turno
