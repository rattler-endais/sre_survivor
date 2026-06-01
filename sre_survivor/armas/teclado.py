import pygame
from sre_survivor.assets import imagen

class Teclado:
    imagen_original = pygame.image.load(imagen("teclado.png"))
    ancho = 80
    alto = int(imagen_original.get_height() * ancho / imagen_original.get_width())
    imagen = pygame.transform.scale(imagen_original, (ancho, alto))
    velocidad = 1.5
    daño = 1

    def __init__(self, x, y, velocidad_x, velocidad_y):
        self.x = x
        self.y = y
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y
        self.imagen = self.__class__.imagen
        self.ancho = self.__class__.ancho
        self.alto = self.__class__.alto
        self.daño = self.__class__.daño

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

    def mover(self):
        self.x += self.velocidad_x
        self.y += self.velocidad_y

    def esta_fuera_de_pantalla(self, ancho_pantalla, alto_pantalla):
        return (
            self.x < -self.ancho or
            self.x > ancho_pantalla or
            self.y < -self.alto or
            self.y > alto_pantalla
        )

    def obtener_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)