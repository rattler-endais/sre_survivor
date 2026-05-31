import pygame
from enemigo import Enemigo
from assets import imagen

class GestorCambios(Enemigo):
    imagen = pygame.transform.scale(pygame.image.load(imagen("gestorcambios.png")), (124, 112))
    velocidad = 0.8

    def __init__(self, x, y):
        super().__init__(x, y)
