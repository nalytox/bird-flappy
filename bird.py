"""
Clase Bird — Barranquín, el loro tricahue de la UOH.
Equivalente a la sección "3. Clase Bird" de la primera versión.

Barranquín vuela solo. Cada aleteo "apunta" a una altura objetivo
tomada de una distribución NORMAL (campana de Gauss) centrada en la
mitad de la pantalla, así su vuelo ronda el centro y queda acotado a
una franja segura: nunca toca el tope ni el fondo del área de juego.
"""

import math
import random
from collections import deque

import pygame

import settings as s
from utils import clamp


class Bird:
    def __init__(self):
        self.x = s.BIRD_X
        self.y = s.HEIGHT / 2
        self.vy = 0.0
        self.target = s.HEIGHT / 2
        self.flap_timer = 0.0
        self.flap_interval = random.uniform(s.FLAP_INTERVAL_MIN, s.FLAP_INTERVAL_MAX)
        self.trail = deque(maxlen=s.TRAIL_LENGTH)

    def update(self, dt):
        # Cada cierto tiempo aleatorio, Barranquín sortea un nuevo
        # objetivo de altura (ver _pick_new_target()).
        self.flap_timer += dt
        if self.flap_timer >= self.flap_interval:
            self._pick_new_target()
            self.flap_timer = 0.0
            self.flap_interval = random.uniform(s.FLAP_INTERVAL_MIN, s.FLAP_INTERVAL_MAX)

        # Oscilador amortiguado: una fuerza proporcional a la distancia
        # al objetivo actual (como un resorte), frenada por una
        # amortiguación proporcional a la velocidad. A diferencia de la
        # gravedad (que siempre tira hacia abajo), esta fuerza es
        # simétrica: tira hacia arriba o hacia abajo según corresponda,
        # así el vuelo queda realmente centrado en el promedio.
        acceleration = s.SPRING_STRENGTH * (self.target - self.y) - s.DAMPING * self.vy
        self.vy += acceleration * dt
        self.y += self.vy * dt

        # El vuelo queda acotado a una franja segura: nunca toca el tope
        # ni el fondo del área de juego.
        if self.y < s.FLIGHT_MARGIN_TOP:
            self.y = s.FLIGHT_MARGIN_TOP
            self.vy = 0.0
        elif self.y > s.HEIGHT - s.FLIGHT_MARGIN_BOTTOM:
            self.y = s.HEIGHT - s.FLIGHT_MARGIN_BOTTOM
            self.vy = 0.0

        # Estela: guarda posiciones recientes para dibujar el camino errático.
        self.trail.append((self.x, self.y))

    def _pick_new_target(self):
        # random.gauss(mean, stdDev) genera un número con distribución
        # normal (la librería estándar ya implementa la transformada de
        # Box-Muller internamente, no hace falta escribirla a mano). La
        # mayoría de los objetivos caen cerca del centro; los que caen
        # lejos (colas de la campana) son mucho menos frecuentes.
        target = random.gauss(s.HEIGHT / 2, s.GAUSSIAN_SIGMA)
        self.target = clamp(target, s.FLIGHT_MARGIN_TOP, s.HEIGHT - s.FLIGHT_MARGIN_BOTTOM)

    def draw(self, surface):
        self._draw_trail(surface)
        angle = clamp(self.vy / 500, -0.5, 0.5)
        self._draw_barranquin(surface, angle)

    def _draw_trail(self, surface):
        total = len(self.trail)
        for i, (tx, ty) in enumerate(self.trail):
            t = i / total if total else 0
            radius = 2
            alpha = int(t * 130)
            dot = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(dot, (*s.TRAIL_COLOR, alpha), (radius, radius), radius)
            surface.blit(dot, (tx - radius, ty - radius))

    def _draw_barranquin(self, surface, angle):
        # Barranquín: loro tricahue (Cyanoliseus patagonus bloxami).
        # Colores reales de la subespecie: cuerpo verde oliva oscuro,
        # anillo periocular blanco, pecho pardo-vinoso, mancha ventral
        # rojo-anaranjada grande y definida, y plumas de vuelo azuladas.
        size = 56
        origin = size // 2  # el (0,0) del pájaro queda en el centro del sprite
        sprite = pygame.Surface((size, size), pygame.SRCALPHA)
        r = s.BIRD_RADIUS

        # Cuerpo.
        pygame.draw.ellipse(
            sprite, s.BIRD_BODY,
            (origin - (r + 2), origin - r, (r + 2) * 2, r * 2),
        )
        # Ala (plumas de vuelo azules). Simplificación: sin la leve
        # inclinación que tenía en la versión web (pygame no rota
        # elipses individuales sin dibujar en una sub-superficie aparte).
        pygame.draw.ellipse(sprite, s.BIRD_WING, (origin - 12, origin - 2, 18, 10))
        # Pecho pardo-vinoso.
        pygame.draw.ellipse(sprite, s.BIRD_CHEST, (origin, origin - 7, 12, 10))
        # Mancha ventral rojo-anaranjada.
        pygame.draw.ellipse(sprite, s.BIRD_BELLY, (origin + 2, origin + 1, 10, 8))
        # Anillo periocular blanco y ojo.
        pygame.draw.circle(sprite, s.BIRD_EYE_RING, (origin + 9, origin - 5), 4, 2)
        pygame.draw.circle(sprite, s.BIRD_EYE, (origin + 9, origin - 5), 2)
        # Pico.
        pygame.draw.polygon(
            sprite, s.BIRD_BEAK,
            [(origin + 14, origin - 4), (origin + 20, origin - 2), (origin + 14, origin)],
        )

        # Pygame rota en sentido antihorario para ángulos positivos; el
        # canvas de la versión web rota en sentido horario, así que se
        # invierte el signo para que el efecto visual sea el mismo.
        rotated = pygame.transform.rotate(sprite, -math.degrees(angle))
        rect = rotated.get_rect(center=(self.x, self.y))
        surface.blit(rotated, rect)
