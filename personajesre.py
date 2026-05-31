import pygame
from assets import imagen as ruta_imagen

class Personajesre:
    imagen = pygame.transform.scale(pygame.image.load(ruta_imagen("sre.png")), (84, 100))
    imagen_muerto = pygame.transform.scale(pygame.image.load(ruta_imagen("sre_muerto.png")), (100, 50))
    velocidad = 1
    vidas_iniciales = 3
    tiempo_invulnerabilidad = 1000
    ancho = imagen.get_width()
    alto = imagen.get_height()

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cambio_x = 0
        self.cambio_y = 0
        self.vidas = self.__class__.vidas_iniciales
        self.invulnerable_hasta = 0
        self.imagen = self.__class__.imagen
        self.imagen_muerto = self.__class__.imagen_muerto
        self.velocidad = self.__class__.velocidad
        self.ancho = self.__class__.ancho
        self.alto = self.__class__.alto
        self.tiempo_invulnerabilidad = self.__class__.tiempo_invulnerabilidad

    def dibujar(self, pantalla, tiempo_actual, estado_juego):
        if estado_juego == "terminado":
            pantalla.blit(self.imagen_muerto, (self.x, self.y))
            return

        if self.es_invulnerable(tiempo_actual) and (tiempo_actual // 100) % 2 == 0:
            return

        pantalla.blit(self.imagen, (self.x, self.y))

    def iniciar_movimiento_izquierda(self):
        self.cambio_x = -self.velocidad

    def iniciar_movimiento_derecha(self):
        self.cambio_x = self.velocidad

    def iniciar_movimiento_arriba(self):
        self.cambio_y = -self.velocidad

    def iniciar_movimiento_abajo(self):
        self.cambio_y = self.velocidad

    def detener_movimiento_horizontal(self):
        self.cambio_x = 0

    def detener_movimiento_vertical(self):
        self.cambio_y = 0

    def mover(self, ancho_pantalla, alto_pantalla):
        self.x += self.cambio_x
        self.y += self.cambio_y

        if self.x < 0:
            self.x = 0
        elif self.x > ancho_pantalla - self.ancho:
            self.x = ancho_pantalla - self.ancho

        if self.y < 0:
            self.y = 0
        elif self.y > alto_pantalla - self.alto:
            self.y = alto_pantalla - self.alto

    def detener(self):
        self.cambio_x = 0
        self.cambio_y = 0

    def obtener_centro(self):
        return self.x + self.ancho / 2, self.y + self.alto / 2

    def obtener_rect(self):
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)

    def es_invulnerable(self, tiempo_actual):
        return tiempo_actual < self.invulnerable_hasta

    def recibir_golpe(self, tiempo_actual):
        self.vidas -= 1
        self.invulnerable_hasta = tiempo_actual + self.tiempo_invulnerabilidad

    def esta_muerto(self):
        return self.vidas <= 0

    def obtener_ancho_muerto(self):
        return self.imagen_muerto.get_width()

    def obtener_alto_muerto(self):
        return self.imagen_muerto.get_height()