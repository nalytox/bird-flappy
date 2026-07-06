"""
Flappy Inverso — protagonizado por Barranquín (loro tricahue, mascota UOH)
---------------------------------------------------------------------
Configuración y constantes del juego. Este archivo va a ir creciendo a
medida que se agreguen nuevas partes (Barranquín, el barranco, etc.).
Por ahora solo tiene lo necesario para la ventana y el fondo.
---------------------------------------------------------------------
"""

# Ventana y tiempo
WIDTH = 400
HEIGHT = 640
FPS = 60
TITLE = "Flappy Inverso — Barranquín, mascota UOH"

# Paleta: precordillera semiárida de la Región de O'Higgins (hábitat
# real del tricahue).
SKY_TOP = (159, 209, 224)
SKY_MID = (232, 183, 125)
SKY_HORIZON = (201, 122, 74)
HILL_LIGHT = (180, 105, 61)
HILL_DARK = (140, 86, 48)

CREAM = (247, 242, 231)
INK = (26, 18, 11)
AMBER = (232, 179, 77)

# ---------------------------------------------------------------------
# Barranquín (el pájaro): vuelo con distribución normal
# ---------------------------------------------------------------------
FLAP_INTERVAL_MIN = 0.35        # segundos entre "aleteos" (recálculo del objetivo)
FLAP_INTERVAL_MAX = 0.95
SPRING_STRENGTH = 8.0           # qué tan fuerte "tira" hacia el objetivo actual
DAMPING = 4.0                   # amortiguación (evita que oscile sin control)

GAUSSIAN_SIGMA = 75              # dispersión típica del vuelo respecto al centro
FLIGHT_MARGIN_TOP = 90           # Barranquín no puede acercarse más que esto al tope
FLIGHT_MARGIN_BOTTOM = 90        # ni a este margen del fondo del área de juego

BIRD_X = 100
BIRD_RADIUS = 14
TRAIL_LENGTH = 26                # posiciones guardadas para dibujar la estela

BIRD_BODY = (91, 110, 58)
BIRD_WING = (62, 111, 160)
BIRD_CHEST = (124, 75, 65)
BIRD_BELLY = (214, 90, 46)
BIRD_EYE_RING = (247, 242, 231)
BIRD_EYE = (36, 26, 18)
BIRD_BEAK = (217, 201, 163)
TRAIL_COLOR = (232, 179, 77)
