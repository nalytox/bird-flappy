"""
Flappy Inverso — protagonizado por Barranquín (loro tricahue, mascota UOH)
---------------------------------------------------------------------
Punto de entrada del juego: crea la ventana, maneja los tres estados
(inicio / jugando / fin de partida), procesa el teclado y dibuja cada
cuadro. La lógica de vuelo vive en bird.py y la del barranco en
gate.py; aquí solo se coordinan (equivale a las secciones "5. Estado
del juego y bucle principal", "6. Entrada de teclado" y "7. Dibujo" de
la primera versión, hecha en HTML/CSS/JS).

Ejecución:
    pip install -r requirements.txt
    python main.py
---------------------------------------------------------------------
"""

import json
import math
import sys
from pathlib import Path

import pygame

import settings as s
from bird import Bird
from gate import Gate, circle_rect_collides

BEST_SCORE_FILE = Path(__file__).parent / "best_score.json"

STATE_START = "start"
STATE_DIFFICULTY = "difficulty"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "over"


# ---------------------------------------------------------------------
# Persistencia simple del mejor puntaje (equivalente a los
# localStorageSafeGet/Set de la versión web, pero con un archivo local).
# ---------------------------------------------------------------------

def load_best_score():
    try:
        data = json.loads(BEST_SCORE_FILE.read_text())
        return int(data.get("best", 0))
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        return 0


def save_best_score(best):
    try:
        BEST_SCORE_FILE.write_text(json.dumps({"best": best}))
    except OSError:
        pass  # almacenamiento no disponible: se ignora silenciosamente


# ---------------------------------------------------------------------
# Fondo: precordillera de la Región de O'Higgins. Se dibuja una sola vez
# en una superficie y se reutiliza en cada cuadro (no cambia con el
# tiempo, así que no hace falta recalcularlo 60 veces por segundo).
# ---------------------------------------------------------------------

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


# ---------------------------------------------------------------------
# Texto y overlays (pantallas de inicio / fin de partida)
# ---------------------------------------------------------------------

def draw_text_center(surface, font, text, color, center):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=center)
    surface.blit(rendered, rect)
    return rect.height


def wrap_text(font, text, max_width):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if font.size(trial)[0] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_overlay(surface, fonts, heading_lines, body_text, button_text):
    tint = pygame.Surface((s.WIDTH, s.HEIGHT), pygame.SRCALPHA)
    tint.fill((*s.INK, 225))
    surface.blit(tint, (0, 0))

    y = s.HEIGHT * 0.28
    for text, font, color in heading_lines:
        h = draw_text_center(surface, font, text, color, (s.WIDTH / 2, y))
        y += h + 12

    y += 6
    for line in wrap_text(fonts["body"], body_text, s.WIDTH - 64):
        h = draw_text_center(surface, fonts["body"], line, s.CREAM, (s.WIDTH / 2, y))
        y += h + 4

    button_rect = pygame.Rect(0, 0, 230, 52)
    button_rect.center = (s.WIDTH / 2, s.HEIGHT * 0.8)
    pygame.draw.rect(surface, s.AMBER, button_rect, border_radius=10)
    draw_text_center(surface, fonts["button"], button_text, s.INK, button_rect.center)


def draw_difficulty_selection(surface, fonts, selected_difficulty):
    tint = pygame.Surface((s.WIDTH, s.HEIGHT), pygame.SRCALPHA)
    tint.fill((*s.INK, 225))
    surface.blit(tint, (0, 0))

    draw_text_center(
        surface,
        fonts["eyebrow"],
        "ELIGE TU DESAFÍO",
        s.BIRD_BELLY,
        (s.WIDTH / 2, 145),
    )
    draw_text_center(
        surface,
        fonts["title"],
        "Selecciona una dificultad",
        s.CREAM,
        (s.WIDTH / 2, 180),
    )

    option_width = 280
    option_height = 58
    option_x = (s.WIDTH - option_width) / 2
    option_y = 235

    for difficulty_key, difficulty in s.DIFFICULTIES.items():
        option_rect = pygame.Rect(option_x, option_y, option_width, option_height)
        is_selected = difficulty_key == selected_difficulty
        fill_color = s.AMBER if is_selected else s.CLIFF_BORDER
        text_color = s.INK if is_selected else s.CREAM

        pygame.draw.rect(surface, fill_color, option_rect, border_radius=10)
        if is_selected:
            pygame.draw.rect(surface, s.CREAM, option_rect, 2, border_radius=10)
        draw_text_center(
            surface,
            fonts["button"],
            difficulty["label"],
            text_color,
            option_rect.center,
        )
        option_y += option_height + 14

    draw_text_center(
        surface,
        fonts["body"],
        "Usa Arriba/Abajo o W/S y confirma con Espacio",
        s.CREAM,
        (s.WIDTH / 2, 495),
    )


# ---------------------------------------------------------------------
# Bucle principal
# ---------------------------------------------------------------------

def main():
    pygame.init()
    pygame.display.set_caption(s.TITLE)
    screen = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
    clock = pygame.time.Clock()

    fonts = {
        "title": pygame.font.Font(None, 30),
        "eyebrow": pygame.font.Font(None, 20),
        "body": pygame.font.Font(None, 22),
        "button": pygame.font.Font(None, 24),
        "hud": pygame.font.Font(None, 26),
    }

    landscape = build_landscape()

    state = STATE_START
    bird = Bird()
    gate = Gate(0)
    score = 0
    best = load_best_score()
    difficulty_keys = list(s.DIFFICULTIES)
    selected_difficulty = s.DEFAULT_DIFFICULTY
    move_up = move_down = False

    def reset_game():
        nonlocal bird, gate, score
        bird = Bird()
        gate = Gate(0)
        score = 0

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

                if state == STATE_DIFFICULTY and event.key in (pygame.K_UP, pygame.K_w):
                    current_index = difficulty_keys.index(selected_difficulty)
                    selected_difficulty = difficulty_keys[(current_index - 1) % len(difficulty_keys)]
                elif state == STATE_DIFFICULTY and event.key in (pygame.K_DOWN, pygame.K_s):
                    current_index = difficulty_keys.index(selected_difficulty)
                    selected_difficulty = difficulty_keys[(current_index + 1) % len(difficulty_keys)]

                if event.key == pygame.K_SPACE and state == STATE_START:
                    state = STATE_DIFFICULTY
                elif event.key == pygame.K_SPACE and state == STATE_DIFFICULTY:
                    reset_game()
                    state = STATE_PLAYING
                elif event.key == pygame.K_SPACE and state == STATE_GAME_OVER:
                    reset_game()
                    state = STATE_PLAYING
                if event.key == pygame.K_ESCAPE:
                    if state == STATE_DIFFICULTY:
                        state = STATE_START
                    else:
                        running = False
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_UP, pygame.K_w):
                    move_up = False
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    move_down = False

        if state == STATE_PLAYING:
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
                    state = STATE_GAME_OVER
                    if score > best:
                        best = score
                        save_best_score(best)

            if not gate.scored and gate.x + s.GATE_WIDTH < bird.x - s.BIRD_RADIUS:
                gate.scored = True
                score += 1

            if gate.offscreen:
                gate = Gate(score)

        # --- Dibujo ---
        screen.blit(landscape, (0, 0))
        gate.draw(screen)
        bird.draw(screen)

        hud_text = f"Puntaje {score}   ·   Mejor {best}"
        hud_surf = fonts["hud"].render(hud_text, True, s.CREAM)
        screen.blit(hud_surf, (12, 10))

        if state == STATE_START:
            draw_overlay(
                screen,
                fonts,
                heading_lines=[
                    ("TÚ NO ERES BARRANQUÍN", fonts["eyebrow"], s.BIRD_BELLY),
                    ("Tú controlas el barranco", fonts["title"], s.CREAM),
                ],
                body_text=(
                    "Barranquín, el loro tricahue de la UOH, vuela solo y ronda el "
                    "centro de la pantalla de forma impredecible. Mueve el hueco del "
                    "barranco con las flechas (arriba/abajo) o W/S para que encaje "
                    "con él a tiempo."
                ),
                button_text="Continuar (Espacio)",
            )
        elif state == STATE_DIFFICULTY:
            draw_difficulty_selection(screen, fonts, selected_difficulty)
        elif state == STATE_GAME_OVER:
            draw_overlay(
                screen,
                fonts,
                heading_lines=[
                    ("CHOQUE", fonts["eyebrow"], s.BIRD_BELLY),
                    ("Barranquín no encajó", fonts["title"], s.CREAM),
                    (f"Puntaje final: {score}", fonts["body"], s.AMBER),
                ],
                body_text="",
                button_text="Reintentar (Espacio)",
            )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
