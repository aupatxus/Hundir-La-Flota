# Hundir-La-Flota
Hundir La Flota http://es.battleship-game.org/

<img src="https://images4.wikia.nocookie.net/battleship/images/8/88/Battleship_Brand_Timeline.jpg">


<img src="https://dam.elcorteingles.es/producto/www-001059766200022-03.jpg">



## Estructura de Archivos (Arquitectura de Módulos)
````
       ┌─────────────────┐
       │   variables.py  │  ◄──────────────────────────┐
       │(Datos estáticos)│                             │
       └────────┬────────┘                             │
                ▲                                      │ Imports
        Imports │                                      │ variables
                │                                      │
       ┌────────┴────────┐      Lógica Interna         │
       │   funciones.py  │  ◄──────────────────┐       │
       │(Motor del Juego)│                     │       │
       └────────▲────────┘                     │       │
                │                              │       │
        Imports │                              │       │
       funciones│                              │       │
                │                              │       │
       ┌────────┴────────┐                     │       │
       │     main.py     │  ───────────────────┴───────┘
       │(Flujo Principal)│  Controla el Bucle y los Turnos
       └─────────────────┘

````
## Estructura de Datos y Funciones 
````
📁 variables.py [Configuración del Sistema]
 └── TAMANO_TABLERO (10)
 └── Simbología Gráfica (🟦, 🚢, 💥, ❌)
 └── ESLORAS_BARCOS ([2, 2, 2, 3, 3, 4])

📁 funciones.py [Lógica de Control Automática]
 ├── 🛠️ crear_tablero()          ──► Genera matrices vacías con NumPy
 ├── ⚙️ colocar_barco()          ──► Modifica celdas para incrustar un barco 
 ├── 🎲 crear_barco()            ──► Algoritmo de posicionamiento aleatorio (H/V)
 ├── 🔄 colocar_barcos()         ──► Bucle de reintentos anti-solapamiento
 ├── 🎯 disparar()               ──► Evalúa el impacto y actualiza los tableros
 ├── 🏁 comprobar_fin_juego()    ──► Valida si la condición de victoria se cumple
 └── 📺 mostrar_tableros_jugador ──► Formatea y dibuja la interfaz en la consola

📁 main.py [Orquestador e Interfaz con el Usuario]
 ├── 1. Inicialización ──► Pide el nombre y genera los 4 tableros requeridos
 ├── 2. Setup Inicial  ──► Invoca la distribución aleatoria de las dos flotas
 ├── 3. Sorteo Turno   ──► De modo aleatorio se establece el turno de inicio para ver quién ataca primero
 └── 4. Bucle Activo   ──► Ciclo continuo que alterna turnos de disparo (Try/Except)
````


## El Flujo de Ejecución (El Ciclo de Vida del Juego)

1. Fase de Setup (Inicio): El main.py arranca ──► Llama a funciones.crear_tablero() 4 veces ──► Almacena las matrices en las variables de juego ──► Llama a funciones.colocar_barcos() para poblar el mapa del usuario y el de la máquina.
2. Fase de Juego (Bucle Continuo):
	* Si es Turno Jugador: main.py llama a mostrar_tableros_jugador() ──► Captura las coordenadas de la terminal ──► Llama a disparar() ──► Si es acierto (True), repite turno; si es fallo (False), cambia el booleano turno_jugador = False.
	* Si es Turno Máquina: Genera coordenadas random ──► Llama a disparar() sobre el tablero del jugador ──► Evalúa resultados y cambia o mantiene el turno.
3. Fase de Cierre (Finalización): Tras cada disparo acertado, el flujo pasa por comprobar_fin_juego(). En cuanto retorna True (no quedan 🚢), rompe el bucle cambiando juego_activo = False, imprime el ganador y el programa finaliza.


## Flujo de datos


1. Estado Inicial de la Memoria (La Creación del Espacio de Datos)

Cuando arranca el programa, el flujo de datos comienza llamando a crear_tablero(). Esta función reserva espacio en memoria RAM a través de NumPy mediante matrices bidimensionales indexadas por coordenadas (X, Y).

El flujo de datos en esta fase es:
* Entrada: La constante TAMANO_TABLERO (10) y el string AGUA (🟦).
* Transformación: NumPy crea un array de strings de 10 × 10.
* Almacenamiento: Se asignan 4 variables independientes en memoria:
	* tablero_barcos_jugador
	* tablero_disparos_jugador
	* tablero_barcos_rival
	* tablero_disparos_rival



2. Flujo de Colocación (Transformación de Matrices Vías Coordenadas)

El juego pasa de un estado vacío a un estado poblado mediante el paso de tuplas de coordenadas:

````
Variables:
ESLORAS_BARCOS [2, 2, 2, 3, 3, 4] 
                 │
                 ▼
          crear_barco() ──(Genera lista de tuplas)──► [(Fila, Columna), (Fila, Columna)]
                                                            │
                                                            ▼
          colocar_barco() ◄──(Escribe en la matriz)─────────┘

````

* Flujo del algoritmo: crear_barco() genera una lista de propuesta de posiciones (ej. [(0,1), (0,2)]). Lee la matriz defensora actual: si en esas celdas encuentra 🟦, valida la operación; si encuentra 🚢, descarta los datos y vuelve al bucle hasta encontrar una propuesta válida.
* Al ser validada, colocar_barco() reescribe esas celdas específicas en la matriz correspondiente, cambiando el dato 🟦 por 🚢.



3. El Ciclo de Datos en el Turno (Entrada, Procesamiento y Salida)

Durante el juego, los datos fluyen en un circuito cerrado:
````
 [ENTRADA] Usuario/IA ingresa Coordenadas (Fila, Columna)
   │
   ▼
 [PROCESAMIENTO] Función disparar() cruza las coordenadas con las Matrices
   │
   ├──► Consulta: ¿tablero_defensor[Fila, Columna] == "🚢"?
   │      │
   │      ├──► SÍ (Acierto): 
   │      │     * Actualiza celda defensor a "💥"
   │      │     * Actualiza celda atacante a "💥"
   │      │     * Retorna Booleano: True (Mantiene Turno)
   │      │
   │      └──► NO (Agua / Ya disparado):
   │            * Si era "🟦", actualiza celdas a "❌"
   │            * Retorna Booleano: False (Cambio de Turno)
   │
   ▼
 [SALIDA / INTERFAZ] mostrar_tableros_jugador() 
   * Lee las matrices actualizadas de la memoria.
   * Limpia los datos de NumPy (.join() elimina corchetes y comillas).
   * Imprime la cuadrícula final en la terminal del usuario.

````

4. Flujo de Datos para la Condición de Cierre

Tras cada disparo exitoso (True), se ejecuta la función comprobar_fin_juego(). El flujo de control aquí gracias a NumPy es  más eficiente :
1. Escaneo de memoria: La función realiza una búsqueda booleana directa en la matriz defensora: variables.BARCO in tablero_barcos.
2. Evaluación: NumPy no recorre celda por celda de forma lenta en Python; hace una búsqueda vectorizada a nivel de C (lenguaje nativo de NumPy) buscando el string 🚢.
3. Decisión:
	* Si el resultado es True (queda al menos un barco), el flujo del bucle principal (juego_activo) continúa.
	* Si el resultado es False (el caracter 🚢 se ha extinguido por completo del array), el flujo de datos de la partida se interrumpe modificando el flag juego_activo = False, provocando la ruptura del bucle while y la finalización del programa.


## Pseudocódigo (Descripción simplificada del algoritmo)
````
// ==========================================
// CONFIGURACIÓN Y VARIABLES GLOBALES
// ==========================================
CONSTANTE TAMANO_TABLERO = 10
CONSTANTE AGUA = "🟦"
CONSTANTE BARCO = "🚢"
CONSTANTE TOCADO = "💥"
CONSTANTE FALLO = "❌"
CONSTANTE ESLORAS_BARCOS = [2, 2, 2, 3, 3, 4]

// ==========================================
// MÓDULO DE FUNCIONES Y LÓGICA
// ==========================================

FUNCIÓN crear_tablero()
    RETORNAR una matriz de tamaño TAMANO_TABLERO x TAMANO_TABLERO rellena con AGUA
FIN FUNCIÓN

FUNCIÓN colocar_barco(lista_casillas, tablero)
    PARA CADA (fila, columna) EN lista_casillas HACER
        tablero[fila, columna] = BARCO
    FIN PARA
    RETORNAR tablero
FIN FUNCIÓN

FUNCIÓN crear_barco_aleatorio(eslora, tablero)
    orientacion = Número aleatorio entre 0 (Horizontal) y 1 (Vertical)
    casillas_propuestas = Lista vacía
    valido = Verdadero

    SI orientacion == 0 ENTONCES // Horizontal
        fila_inicial = Número aleatorio entre 0 y (TAMANO_TABLERO - 1)
        columna_inicial = Número aleatorio entre 0 y (TAMANO_TABLERO - eslora)
        
        PARA desplazamiento DESDE 0 HASTA (eslora - 1) HACER
            columna_actual = columna_inicial + desplazamiento
            SI tablero[fila_inicial, columna_actual] == BARCO ENTONCES
                valido = Falso
            SINO
                Añadir (fila_inicial, columna_actual) a casillas_propuestas
            FIN SI
        FIN PARA
    SINO // Vertical
        fila_inicial = Número aleatorio entre 0 y (TAMANO_TABLERO - eslora)
        columna_inicial = Número aleatorio entre 0 y (TAMANO_TABLERO - 1)
        
        PARA desplazamiento DESDE 0 HASTA (eslora - 1) HACER
            fila_actual = fila_inicial + desplazamiento
            SI tablero[fila_actual, columna_inicial] == BARCO ENTONCES
                valido = Falso
            SINO
                Añadir (fila_actual, columna_inicial) a casillas_propuestas
            FIN SI
        FIN PARA
    FIN SI

    SI valido ENTONCES
        RETORNAR casillas_propuestas
    SINO
        RETORNAR Lista vacía
    FIN SI
FIN FUNCIÓN

FUNCIÓN colocar_todos_los_barcos(tablero)
    PARA CADA eslora EN ESLORAS_BARCOS HACER
        barco_colocado = Falso
        MIENTRAS barco_colocado sea Falso HACER
            lista_casillas = crear_barco_aleatorio(eslora, tablero)
            SI longitud(lista_casillas) > 0 ENTONCES
                tablero = colocar_barco(lista_casillas, tablero)
                barco_colocado = Verdadero
            FIN SI
        FIN MIENTRAS
    FIN PARA
    RETORNAR tablero
FIN FUNCIÓN

FUNCIÓN disparar(fila, columna, tablero_defensor, tablero_disparos_atacante)
    SI tablero_defensor[fila, columna] == BARCO ENTONCES
        tablero_defensor[fila, columna] = TOCADO
        tablero_disparos_atacante[fila, columna] = TOCADO
        RETORNAR Verdadero // Acierto
    SINO
        SI tablero_defensor[fila, columna] == AGUA ENTONCES
            tablero_defensor[fila, columna] = FALLO
            tablero_disparos_atacante[fila, columna] = FALLO
        FIN SI
        RETORNAR Falso // Fallo
    FIN SI
FIN FUNCIÓN

FUNCIÓN comprobar_fin_juego(tablero_barcos)
    SI BARCO existe en tablero_barcos ENTONCES
        RETORNAR Falso
    SINO
        RETORNAR Verdadero // No quedan barcos
    FIN SI
FIN FUNCIÓN

FUNCIÓN mostrar_tableros_jugador(tablero_barcos, tablero_disparos)
    IMPRIMIR "Encabezado Columnas: 0 a 9"
    PARA CADA fila EN tablero_barcos HACER
        IMPRIMIR Número_Fila + Contenido de la fila sin corchetes
    FIN PARA
    
    IMPRIMIR "Encabezado Columnas: 0 a 9"
    PARA CADA fila EN tablero_disparos HACER
        IMPRIMIR Número_Fila + Contenido de la fila sin corchetes
    FIN PARA
FIN FUNCIÓN


// ==========================================
// PROGRAMA PRINCIPAL (FLUJO DEL JUEGO)
// ==========================================

INICIO
    IMPRIMIR "Versión de Python del juego HUNDIR LA FLOTA"
    nombre_jugador = LEER Entrada del usuario
    
    // Inicializar los 4 tableros vacíos
    tablero_barcos_jugador = crear_tablero()
    tablero_disparos_jugador = crear_tablero()
    tablero_barcos_rival = crear_tablero()
    tablero_disparos_rival = crear_tablero()
    
    // Colocar la flota de forma aleatoria
    tablero_barcos_jugador = colocar_todos_los_barcos(tablero_barcos_jugador)
    tablero_barcos_rival = colocar_todos_los_barcos(tablero_barcos_rival)
    
    // Sorteo de turno de inicio
    turno_de_inicio_partida = Número aleatorio entre 0 y 1
    SI turno_de_inicio_partida == 1 ENTONCES
        turno_jugador = Verdadero
        IMPRIMIR "Empiezas jugando tú"
    SINO
        turno_jugador = Falso
        IMPRIMIR "Empieza jugando la máquina..."
    FIN SI
    
    juego_activo = Verdadero
    
    // Bucle principal de la partida
    MIENTRAS juego_activo sea Verdadero HACER
        
        SI turno_jugador == Verdadero ENTONCES
            IMPRIMIR "Es tu turno"
            mostrar_tableros_jugador(tablero_barcos_jugador, tablero_disparos_jugador)
            
            // Solicitar coordenadas válidas
            coordenada_valida = Falso
            MIENTRAS coordenada_valida sea Falso HACER
                INTENTAR
                    fila = LEER número entero
                    columna = LEER número entero
                    SI (0 <= fila < TAMANO_TABLERO) Y (0 <= columna < TAMANO_TABLERO) ENTONCES
                        coordenada_valida = Verdadero
                    SINO
                        IMPRIMIR "Coordenadas fuera de rango. Prueba otra vez."
                    FIN SI
                CAPTURA ERROR
                    IMPRIMIR "Introduce números enteros válidos."
                FIN INTENTAR
            FIN MIENTRAS
            
            // Procesar disparo del jugador
            acierto = disparar(fila, columna, tablero_barcos_rival, tablero_disparos_jugador)
            
            SI acierto == Verdadero ENTONCES
                IMPRIMIR "¡TOCADO! Sigues jugando."
                SI comprobar_fin_juego(tablero_barcos_rival) ENTONCES
                    IMPRIMIR "¡HAS GANADO LA PARTIDA!"
                    juego_activo = Falso
                FIN SI
            SINO
                IMPRIMIR "¡AGUA! Has fallado."
                turno_jugador = Falso // Cambio de turno a la máquina
            FIN SI
            
        SINO // Turno de la máquina
            IMPRIMIR "Es el turno de LA MÁQUINA..."
            
            // La máquina elige coordenadas al azar 
            fila_maquina = Número aleatorio entre 0 y (TAMANO_TABLERO - 1)
            columna_maquina = Número aleatorio entre 0 y (TAMANO_TABLERO - 1)
            
            // Procesar disparo de la máquina
            acierto_maquina = disparar(fila_maquina, columna_maquina, tablero_barcos_jugador, tablero_disparos_rival)
            
            SI acierto_maquina == Verdadero ENTONCES
                IMPRIMIR "La máquina te ha TOCADO un barco. Sigue la máquina."
                SI comprobar_fin_juego(tablero_barcos_jugador) ENTONCES
                    IMPRIMIR "La máquina ha hundido tu flota. ¡HAS PERDIDO!"
                    juego_activo = Falso
                FIN SI
            SINO
                IMPRIMIR "La máquina ha disparado al AGUA."
                turno_jugador = Verdadero // Cambio de turno al jugador
            FIN SI
            
        FIN SI
        
    FIN MIENTRAS
FIN
````