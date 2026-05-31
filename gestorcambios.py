import pygame
from enemigo import Enemigo
from assets import imagen

class GestorCambios(Enemigo):
    imagen = pygame.transform.scale(pygame.image.load(imagen("gestorcambios.png")), (124, 112))
    velocidad = 0.7
    vida_maxima = 2
    desaparece_al_colisionar_con_personaje = False
    tiempo_entre_efectos = 2500
    empuje_al_colisionar = 150
    tiempo_aturdimiento = 1200

    def __init__(self, x, y):
        super().__init__(x, y)
        self.ultimo_efecto = 0
        self.aturdido_hasta = 0

    def puede_aplicar_efecto(self, tiempo_actual):
        return tiempo_actual - self.ultimo_efecto >= self.tiempo_entre_efectos

    def registrar_efecto(self, tiempo_actual):
        self.ultimo_efecto = tiempo_actual

    def esta_aturdido(self, tiempo_actual):
        return tiempo_actual < self.aturdido_hasta

    def aturdir(self, tiempo_actual):
        self.aturdido_hasta = tiempo_actual + self.tiempo_aturdimiento

    def empujar_desde(self, objetivo_x, objetivo_y):
        dx = self.x - objetivo_x
        dy = self.y - objetivo_y
        distancia = (dx ** 2 + dy ** 2) ** 0.5

        if distancia > 0:
            self.x += (dx / distancia) * self.empuje_al_colisionar
            self.y += (dy / distancia) * self.empuje_al_colisionar

    def mover_hacia(self, objetivo_x, objetivo_y, tiempo_actual=None):
        if tiempo_actual is not None and self.esta_aturdido(tiempo_actual):
            return

        super().mover_hacia(objetivo_x, objetivo_y)
