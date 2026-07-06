"""
Flappy Inverso — PARTE 3: el barranco aparece en pantalla
---------------------------------------------------------------------
Tercer avance: se agrega el barranco (gate.py). Por ahora solo se
mueve de derecha a izquierda y se regenera al salir de pantalla; el
jugador todavía no lo controla y no hay colisiones ni puntaje — eso
se agrega en la Parte 4.

Ejecución:
    pip install -r requirements.txt
    python3 main.py
---------------------------------------------------------------------
"""

import math
import sys

import pygame

import settings as s
from bird import Bird
from gate import Gate


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def build_landscape():
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
    bird = Bird()
    gate = Gate()

    running = True
    while running:
        dt = min(0.033, clock.tick(s.FPS) / 1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        bird.update(dt)
        gate.update(dt)
        if gate.offscreen:
            gate = Gate()

        screen.blit(landscape, (0, 0))
        gate.draw(screen)
        bird.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
