"""
Utilidades compartidas por bird.py y gate.py.
Equivalente a la sección "2. Utilidades" de la primera versión.

Nota: para la distribución normal del vuelo NO reinventamos la
transformada de Box-Muller a mano; usamos random.gauss(mean, stdDev) de
la librería estándar de Python, que ya la implementa internamente.
Se usa directamente en bird.py.
"""


def clamp(value, minimum, maximum):
    """Limita `value` para que quede dentro de [minimum, maximum]."""
    return max(minimum, min(maximum, value))
