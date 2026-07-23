"""
Flappy Inverso — protagonizado por Barranquín (loro tricahue, mascota UOH)
---------------------------------------------------------------------
Configuración y constantes del juego. Equivalente a la sección
"1. Configuración y constantes" de la primera versión (hecha en
HTML/CSS/JS); aquí vive todo lo que se puede ajustar sin tocar la
lógica del juego.
---------------------------------------------------------------------
"""

# Ventana y tiempo
WIDTH = 400
HEIGHT = 640
FPS = 60
TITLE = "Flappy Inverso — Barranquín, mascota UOH"

# Física del vuelo de Barranquín: un oscilador amortiguado que persigue
# un objetivo. El objetivo se vuelve a sortear cada cierto tiempo (cada
# "aleteo") con una distribución normal centrada en la mitad de la
# pantalla. Se usa un resorte (fuerza simétrica) en vez de gravedad +
# impulsos hacia arriba: con gravedad constante, el promedio real del
# vuelo queda sesgado hacia abajo (lo comprobamos con una simulación:
# la media terminaba en ~448 de 640 en vez de ~320); con un resorte
# simétrico, la media queda centrada de verdad (~322 de 640).
FLAP_INTERVAL_MIN = 0.35        # segundos entre "aleteos" (recálculo del objetivo)
FLAP_INTERVAL_MAX = 0.95
SPRING_STRENGTH = 8.0           # qué tan fuerte "tira" hacia el objetivo actual
DAMPING = 4.0                   # amortiguación (evita que oscile sin control)

GAUSSIAN_SIGMA = 75              # dispersión típica del vuelo respecto al centro
FLIGHT_MARGIN_TOP = 90           # Barranquín no puede acercarse más que esto al tope
FLIGHT_MARGIN_BOTTOM = 90        # ni a este margen del fondo del área de juego

BIRD_X = 100
BIRD_RADIUS = 14
TRAIL_LENGTH = 26               # posiciones guardadas para dibujar la estela

# Barranco / compuerta (el obstáculo que controla el jugador)
GATE_WIDTH = 62
GATE_CONTROL_SPEED = 320.0      # px/s al mover el hueco con el teclado
GATE_SPAWN_MARGIN = 60

GAP_HEIGHT_START = 190
GAP_HEIGHT_MIN = 120
GAP_HEIGHT_STEP = 4              # se reduce por cada punto anotado

SPEED_START = 150.0              # px/s de avance del barranco
SPEED_MAX = 280.0
SPEED_STEP = 6.0                 # aumenta por cada punto anotado

# Niveles de dificultad. Cada modalidad define el punto de partida y
# la progresión del barranco a medida que aumenta el puntaje. La
# configuración normal conserva exactamente los valores originales del
# juego; fácil ofrece un hueco mayor y una progresión más suave, mientras
# que difícil comienza más rápido y reduce el hueco con mayor intensidad.
DEFAULT_DIFFICULTY = "normal"

DIFFICULTIES = {
    "easy": {
        "label": "Fácil",
        "gap_height_start": 220,
        "gap_height_min": 145,
        "gap_height_step": 3,
        "speed_start": 125.0,
        "speed_max": 240.0,
        "speed_step": 4.0,
    },
    "normal": {
        "label": "Normal",
        "gap_height_start": GAP_HEIGHT_START,
        "gap_height_min": GAP_HEIGHT_MIN,
        "gap_height_step": GAP_HEIGHT_STEP,
        "speed_start": SPEED_START,
        "speed_max": SPEED_MAX,
        "speed_step": SPEED_STEP,
    },
    "hard": {
        "label": "Difícil",
        "gap_height_start": 165,
        "gap_height_min": 100,
        "gap_height_step": 5,
        "speed_start": 180.0,
        "speed_max": 320.0,
        "speed_step": 8.0,
    },
}

# ---------------------------------------------------------------------
# Paleta: precordillera semiárida de la Región de O'Higgins (hábitat real
# del tricahue) + colores reales del plumaje de Barranquín.
# UOH_ACCENT es una aproximación al color institucional visible en los
# materiales públicos de la UOH; no se verificó un Pantone/HEX oficial,
# así que si tienes el manual de marca a mano, ajústalo aquí.
# ---------------------------------------------------------------------

SKY_TOP = (159, 209, 224)
SKY_MID = (232, 183, 125)
SKY_HORIZON = (201, 122, 74)
HILL_LIGHT = (180, 105, 61)
HILL_DARK = (140, 86, 48)

CLIFF_BASE = (201, 122, 74)
CLIFF_BAND = (168, 101, 58)
CLIFF_BORDER = (110, 64, 35)
BURROW = (59, 42, 32)
CONTROL_INDICATOR = (232, 179, 77)

BIRD_BODY = (91, 110, 58)
BIRD_WING = (62, 111, 160)
BIRD_CHEST = (124, 75, 65)
BIRD_BELLY = (214, 90, 46)
BIRD_EYE_RING = (247, 242, 231)
BIRD_EYE = (36, 26, 18)
BIRD_BEAK = (217, 201, 163)

TRAIL_COLOR = (232, 179, 77)

INK = (26, 18, 11)
CREAM = (247, 242, 231)
AMBER = (232, 179, 77)
UOH_ACCENT = (79, 191, 196)
