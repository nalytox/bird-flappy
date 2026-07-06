"""
Flappy Inverso — PARTE 1: ventana y fondo
---------------------------------------------------------------------
Primer avance: solo se abre la ventana y se dibuja el paisaje de fondo
(la precordillera de la Región de O'Higgins). Todavía no hay pájaro ni
barranco: eso se agrega en las siguientes partes.

Ejecución:
    pip install -r requirements.txt
    python3 main.py
---------------------------------------------------------------------
"""

import math
import sys

import pygame

import settings as s


def lerp_color(c1, c2, t):
    """Interpola linealmente entre dos colores RGB según t en [0, 1]."""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def build_landscape():
    """Dibuja el cielo (degradado) y los cerros una sola vez, en una
    superficie que se reutiliza en cada cuadro (el fondo no cambia)."""
    surface = pygame.Surface((s.WIDTH, s.HEIGHT))
    for y in range(s.HEIGHT):
        t = y / s.HEIGHT
        if t < 0.55:
            color = lerp_color(s.SKY_TOP, s.SKY_MID, t / 0.55)
        else:
            color = lerp_color(s.SKY_MID, s.SKY_HORIZON, (t - 0.55) / 0.45)
        pygame.draw.line(surface, color, (0, y), (s.WIDTH, y))

    _draw_hill_layer(surface, s.HEIGHT * 0.72, 46, s.HILL_LIGHT)
    _draw_hill_layer(surface, s.HEIGHT * 0.84, 60, s.HILL_DARK)
    return surface


def _draw_hill_layer(surface, base_y, amplitude, color):
    points = [(0, s.HEIGHT), (0, base_y)]
    x = 0
    while x <= s.WIDTH:
        y = base_y - amplitude * math.sin(x / 90 + base_y) * 0.5 - amplitude * 0.3
        points.append((x, y))
        x += 20
    points.append((s.WIDTH, s.HEIGHT))
    pygame.draw.polygon(surface, color, points)


def main():
    pygame.init()
    pygame.display.set_caption(s.TITLE)
    screen = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
    clock = pygame.time.Clock()

    landscape = build_landscape()

    running = True
    while running:
        clock.tick(s.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.blit(landscape, (0, 0))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
