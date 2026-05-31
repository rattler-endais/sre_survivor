import pygame
from enemigo import Enemigo
from assets import imagen

class Hacker(Enemigo):
    imagen = pygame.transform.scale(pygame.image.load(imagen("hacker.png")), (84, 100))
    velocidad = 0.5
    vida_maxima = 1
    desaparece_al_colisionar_con_personaje = True

    def __init__(self, x, y):
        super().__init__(x, y)
