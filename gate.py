"""
Clase Gate — el barranco / compuerta controlada por el jugador.
Equivalente a la sección "4. Clase Gate" de la primera versión.
"""

import random

import pygame

import settings as s
from utils import clamp


class Gate:
    def __init__(self, score):
        self.x = float(s.WIDTH + s.GATE_WIDTH)
        self.gap_height = max(s.GAP_HEIGHT_MIN, s.GAP_HEIGHT_START - score * s.GAP_HEIGHT_STEP)
        self.speed = min(s.SPEED_MAX, s.SPEED_START + score * s.SPEED_STEP)
        self.gap_y = random.uniform(
            s.GATE_SPAWN_MARGIN + self.gap_height / 2,
            s.HEIGHT - s.GATE_SPAWN_MARGIN - self.gap_height / 2,
        )
        self.scored = False

    def update(self, dt, move_up, move_down):
        self.x -= self.speed * dt

        if move_up:
            self.gap_y -= s.GATE_CONTROL_SPEED * dt
        if move_down:
            self.gap_y += s.GATE_CONTROL_SPEED * dt

        half = self.gap_height / 2
        self.gap_y = clamp(self.gap_y, half + 6, s.HEIGHT - half - 6)

    @property
    def top_rect(self):
        height = self.gap_y - self.gap_height / 2
        return pygame.Rect(int(self.x), 0, s.GATE_WIDTH, int(height))

    @property
    def bottom_rect(self):
        gap_bottom = self.gap_y + self.gap_height / 2
        return pygame.Rect(int(self.x), int(gap_bottom), s.GATE_WIDTH, int(s.HEIGHT - gap_bottom))

    @property
    def offscreen(self):
        return self.x + s.GATE_WIDTH < 0

    def draw(self, surface):
        top = self.top_rect
        bottom = self.bottom_rect
        self._draw_cliff_block(surface, top)
        self._draw_cliff_block(surface, bottom)

        # "Lorera": la entrada de una madriguera excavada en el barranco,
        # tal como las que cava el tricahue para anidar (de ahí el nombre
        # "Barranquín" y "loro barranquero").
        hole_x = int(self.x + s.GATE_WIDTH / 2)
        pygame.draw.circle(surface, s.BURROW, (hole_x, top.bottom), 14)
        pygame.draw.circle(surface, s.BURROW, (hole_x, bottom.top), 14)

        # Franja dorada en el borde del hueco: recuerda que el jugador
        # controla este barranco (a diferencia del Flappy Bird original).
        pygame.draw.rect(surface, s.CONTROL_INDICATOR,
                          (self.x - 4, top.bottom - 3, s.GATE_WIDTH + 8, 6))
        pygame.draw.rect(surface, s.CONTROL_INDICATOR,
                          (self.x - 4, bottom.top - 3, s.GATE_WIDTH + 8, 6))

    def _draw_cliff_block(self, surface, rect):
        if rect.height <= 0:
            return

        # Roca base color arena/terracota.
        pygame.draw.rect(surface, s.CLIFF_BASE, rect)

        # Estratos sedimentarios alternados, como los de un barranco real.
        band_height = 22
        y = rect.top
        while y < rect.bottom:
            band = pygame.Rect(rect.x, y, rect.width, min(band_height, rect.bottom - y))
            pygame.draw.rect(surface, s.CLIFF_BAND, band)
            y += band_height * 2

        pygame.draw.rect(surface, s.CLIFF_BORDER, rect, 3)


def circle_rect_collides(cx, cy, r, rect):
    closest_x = clamp(cx, rect.left, rect.right)
    closest_y = clamp(cy, rect.top, rect.bottom)
    dx = cx - closest_x
    dy = cy - closest_y
    return dx * dx + dy * dy < r * r
