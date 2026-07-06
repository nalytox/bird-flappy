"""
Flappy Inverso — PARTE 4: control del jugador, colisiones y puntaje
---------------------------------------------------------------------
Cuarto avance: el jugador ya puede mover el hueco del barranco con el
teclado (flechas o W/S), hay detección de colisiones círculo–rectángulo
y sistema de puntaje. La dificultad ahora depende del puntaje (el
barranco se mueve más rápido y el hueco se achica). Todavía no hay
pantallas de inicio/fin ni mejor puntaje guardado — eso se agrega en
la Parte 5.

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
from gate import Gate, circle_rect_collides


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
    font_hud = pygame.font.Font(None, 26)

    landscape = build_landscape()
    bird = Bird()
    gate = Gate(0)
    score = 0
    move_up = move_down = False

    running = True
    while running:
        dt = min(0.033, clock.tick(s.FPS) / 1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    move_up = True
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    move_down = True
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_UP, pygame.K_w):
                    move_up = False
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    move_down = False

        bird.update(dt)
        gate.update(dt, move_up, move_down)

        overlaps_x = (
            gate.x < bird.x + s.BIRD_RADIUS
            and gate.x + s.GATE_WIDTH > bird.x - s.BIRD_RADIUS
        )
        if overlaps_x:
            hit = (
                circle_rect_collides(bird.x, bird.y, s.BIRD_RADIUS, gate.top_rect)
                or circle_rect_collides(bird.x, bird.y, s.BIRD_RADIUS, gate.bottom_rect)
            )
            if hit:
                # Por ahora, sin pantalla de fin de partida: solo se reinicia.
                bird = Bird()
                gate = Gate(0)
                score = 0

        if not gate.scored and gate.x + s.GATE_WIDTH < bird.x - s.BIRD_RADIUS:
            gate.scored = True
            score += 1

        if gate.offscreen:
            gate = Gate(score)

        screen.blit(landscape, (0, 0))
        gate.draw(screen)
        bird.draw(screen)

        hud_surf = font_hud.render(f"Puntaje {score}", True, s.CREAM)
        screen.blit(hud_surf, (12, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
