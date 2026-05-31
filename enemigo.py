import pygame

class Enemigo:
    imagen = None
    velocidad = 0
    ancho = 0
    alto = 0

    def __init_subclass__(cls):
        super().__init_subclass__()

        if cls.imagen is not None:
            cls.ancho = cls.imagen.get_width()
            cls.alto = cls.imagen.get_height()

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.imagen = self.__class__.imagen
        self.velocidad = self.__class__.velocidad
        self.ancho = self.__class__.ancho
        self.alto = self.__class__.alto

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

    def mover_hacia(self, objetivo_x, objetivo_y):
        dx = objetivo_x - self.x
        dy = objetivo_y - self.y
        distancia = (dx ** 2 + dy ** 2) ** 0.5

        if distancia > 0:
            self.x += (dx / distancia) * self.velocidad
            self.y += (dy / distancia) * self.velocidad

    def obtener_centro(self):
        return self.x + self.ancho / 2, self.y + self.alto / 2

    def obtener_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)
