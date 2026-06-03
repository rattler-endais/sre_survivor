import pygame
from sre_survivor.enemigos.enemigo import Enemigo
from sre_survivor.assets import imagen

class Hacker(Enemigo):
    imagen = pygame.transform.scale(pygame.image.load(imagen("hacker.png")), (84, 100))
    velocidad = 3.14
    vida_maxima = 1
    desaparece_al_colisionar_con_personaje = True

    def __init__(self, x, y):
        super().__init__(x, y)
