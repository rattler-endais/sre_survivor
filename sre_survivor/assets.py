from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "assets" / "images"
SOUNDS_DIR = BASE_DIR / "assets" / "sounds"

def imagen(nombre_archivo):
    return str(IMAGES_DIR / nombre_archivo)

def sonido(nombre_archivo):
    return str(SOUNDS_DIR / nombre_archivo)
