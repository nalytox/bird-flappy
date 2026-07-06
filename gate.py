"""
Clase Gate — el barranco. PARTE 3: todavía sin control del jugador ni
colisiones, solo se mueve de derecha a izquierda a velocidad
constante y se dibuja como una pared de roca estratificada.
"""

import random

import pygame

import settings as s


class Gate:
    def __init__(self):
        self.x = float(s.WIDTH + s.GATE_WIDTH)
        self.gap_height = s.GAP_HEIGHT
        self.speed = s.SPEED
        self.gap_y = random.uniform(
            s.GATE_SPAWN_MARGIN + self.gap_height / 2,
            s.HEIGHT - s.GATE_SPAWN_MARGIN - self.gap_height / 2,
        )

    def update(self, dt):
        self.x -= self.speed * dt

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
        # tal como las que cava el tricahue para anidar.
        hole_x = int(self.x + s.GATE_WIDTH / 2)
        pygame.draw.circle(surface, s.BURROW, (hole_x, top.bottom), 14)
        pygame.draw.circle(surface, s.BURROW, (hole_x, bottom.top), 14)

    def _draw_cliff_block(self, surface, rect):
        if rect.height <= 0:
            return
        pygame.draw.rect(surface, s.CLIFF_BASE, rect)

        band_height = 22
        y = rect.top
        while y < rect.bottom:
            band = pygame.Rect(rect.x, y, rect.width, min(band_height, rect.bottom - y))
            pygame.draw.rect(surface, s.CLIFF_BAND, band)
            y += band_height * 2

        pygame.draw.rect(surface, s.CLIFF_BORDER, rect, 3)
