from .config import get_levels

def get_level(hours: float) -> str:
    """Повертає назву рівня для заданої кількості годин."""
    levels = sorted(get_levels(), key=lambda x: x[0])
    for threshold, name in reversed(levels):
        if hours >= threshold:
            return name
    return levels[0][1] if levels else "Новачок"
