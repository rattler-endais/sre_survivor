import random
import pygame
from sre_survivor.assets import imagen as ruta_imagen
from sre_survivor.enemigos.enemigo import Enemigo


def cargar_imagen_vampiremail(nombre_archivo, ancho_objetivo):
    imagen_original = pygame.image.load(
        ruta_imagen(f"enemigos/boss_email/{nombre_archivo}")
    )
    ancho_original = imagen_original.get_width()
    alto_original = imagen_original.get_height()
    alto_objetivo = int(alto_original * ancho_objetivo / ancho_original)

    return pygame.transform.scale(
        imagen_original,
        (ancho_objetivo, alto_objetivo)
    )


class VampireMail(Enemigo):
    ancho_objetivo = 60

    imagenes = [
        cargar_imagen_vampiremail("boss_email_vampiremail_1.png", ancho_objetivo),
        cargar_imagen_vampiremail("boss_email_vampiremail_2.png", ancho_objetivo),
        cargar_imagen_vampiremail("boss_email_vampiremail_3.png", ancho_objetivo),
        cargar_imagen_vampiremail("boss_email_vampiremail_4.png", ancho_objetivo),
        cargar_imagen_vampiremail("boss_email_vampiremail_5.png", ancho_objetivo),
        cargar_imagen_vampiremail("boss_email_vampiremail_6.png", ancho_objetivo),
        cargar_imagen_vampiremail("boss_email_vampiremail_7.png", ancho_objetivo),
        cargar_imagen_vampiremail("boss_email_vampiremail_8.png", ancho_objetivo),
    ]

    imagen = imagenes[0]
    velocidad = 3.77
    vida_maxima = 1
    puntos = 2
    desaparece_al_colisionar_con_personaje = True

    def __init__(self, x, y, velocidad_x, velocidad_y, ancho_pantalla, alto_pantalla, imagen):
        super().__init__(x, y)
        self.imagen = imagen
        self.ancho = self.imagen.get_width()
        self.alto = self.imagen.get_height()
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla

    @classmethod
    def crear_desde_borde_aleatorio(cls, ancho_pantalla, alto_pantalla):
        imagen = random.choice(cls.imagenes)
        ancho = imagen.get_width()
        alto = imagen.get_height()

        borde = random.choice(["arriba", "abajo", "izquierda", "derecha"])

        if borde == "arriba":
            x = random.randrange(0, ancho_pantalla - ancho)
            y = -alto
            velocidad_x = 0
            velocidad_y = cls.velocidad

        elif borde == "abajo":
            x = random.randrange(0, ancho_pantalla - ancho)
            y = alto_pantalla
            velocidad_x = 0
            velocidad_y = -cls.velocidad

        elif borde == "izquierda":
            x = -ancho
            y = random.randrange(0, alto_pantalla - alto)
            velocidad_x = cls.velocidad
            velocidad_y = 0

        else:
            x = ancho_pantalla
            y = random.randrange(0, alto_pantalla - alto)
            velocidad_x = -cls.velocidad
            velocidad_y = 0

        return cls(
            x,
            y,
            velocidad_x,
            velocidad_y,
            ancho_pantalla,
            alto_pantalla,
            imagen
        )

    def mover_hacia(self, objetivo_x, objetivo_y, tiempo_actual=None):
        self.x += self.velocidad_x
        self.y += self.velocidad_y

    def esta_fuera_de_pantalla(self):
        return (
            self.x < -self.ancho or
            self.x > self.ancho_pantalla or
            self.y < -self.alto or
            self.y > self.alto_pantalla
        )

    def esta_derrotado(self):
        return super().esta_derrotado() or self.esta_fuera_de_pantalla()