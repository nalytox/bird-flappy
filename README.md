# Flappy Inverso — con Barranquín (versión Python)

Variante invertida de *Flappy Bird*: el jugador **no controla al pájaro**, controla el
**barranco**. El protagonista es Barranquín, el loro tricahue (*Cyanoliseus patagonus
bloxami*) mascota de la Universidad de O'Higgins. Vuela solo, con un movimiento
pseudo-aleatorio que **sigue una distribución normal sobre el eje Y**: su vuelo ronda el
centro de la pantalla con más frecuencia que los extremos, y nunca toca el tope ni el
fondo del área de juego. El jugador debe mover el hueco del barranco en tiempo real para
que Barranquín pase sin chocar.

Hecho en **Python puro + Pygame**, sin dependencias adicionales.

La paleta visual y la temática están inspiradas en la precordillera semiárida de la
Región de O'Higgins (hábitat real del tricahue) y en los colores de su plumaje: verde
oliva, pecho pardo-vinoso, mancha ventral rojo-anaranjada y alas azuladas. El acento
`UOH_ACCENT` en `settings.py` es una aproximación al color institucional de la UOH; no
se verificó un Pantone/HEX oficial, así que si tienes el manual de marca a mano,
ajústalo ahí mismo.

Proyecto individual para la asignatura **COM4602 — Introducción a los Repositorios de
Código Distribuido**, Universidad de O'Higgins.

## Funcionalidades

- Vuelo de Barranquín modelado como un **oscilador amortiguado** (resorte + amortiguación)
  que persigue un objetivo de altura recalculado cada cierto tiempo con
  `random.gauss()` (distribución normal), centrado en la mitad de la pantalla y acotado
  a una franja segura lejos del tope y el fondo.
- Estela visual que muestra el recorrido errático del pájaro.
- Control del hueco del barranco con teclado (`↑`/`↓` o `W`/`S`).
- Detección de colisiones círculo–rectángulo y sistema de puntaje.
- Dificultad progresiva: el barranco se mueve más rápido y el hueco se reduce a medida
  que sube el puntaje.
- Pantallas de inicio y de fin de partida, con mejor puntaje guardado en un archivo
  local (`best_score.json`, no versionado).

## Requisitos

- Python 3.9 o superior.
- Pygame 2.5 o superior (ver `requirements.txt`).

## Instalación

```bash
git clone https://github.com/<usuario>/flappy-inverso.git
cd flappy-inverso
python3 -m venv venv
source venv/bin/activate        # en Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

```bash
python3 main.py
```

## Estructura del repositorio

```
flappy-inverso/
├── main.py              # Punto de entrada: bucle principal, estados, dibujo
├── bird.py               # Clase Bird (Barranquín): vuelo con distribución normal
├── gate.py               # Clase Gate (el barranco): movimiento, dibujo, colisiones
├── settings.py            # Constantes de configuración y paleta de colores
├── utils.py                # Función clamp() compartida
├── requirements.txt
├── informe/
│   └── informe.md          # Informe de análisis del repositorio (a convertir a PDF)
├── .gitignore
└── README.md
```

## Uso básico

1. Ejecuta `python3 main.py` y presiona **Espacio** para iniciar la partida.
2. Barranquín comienza a volar solo, rondando el centro de la pantalla de forma
   impredecible.
3. Usa `↑` / `W` para subir el hueco del barranco y `↓` / `S` para bajarlo.
4. Cada vez que Barranquín cruza el hueco sin chocar, sumas un punto.
5. Si Barranquín choca contra el barranco, la partida termina. Presiona **Espacio**
   para volver a jugar, o **Esc** para salir.

## Autor

Arnaldo — estudiante de la Universidad de O'Higgins (UOH).
