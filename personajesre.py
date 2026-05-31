import pygame
from assets import imagen as ruta_imagen

def cargar_imagen_personaje(nombre_archivo, alto_objetivo):
    imagen_original = pygame.image.load(ruta_imagen(nombre_archivo))
    ancho_original = imagen_original.get_width()
    alto_original = imagen_original.get_height()
    ancho_objetivo = int(ancho_original * alto_objetivo / alto_original)

    return pygame.transform.scale(imagen_original, (ancho_objetivo, alto_objetivo))

class Personajesre:
    alto = 100
    alto_muerto = 50

    imagenes = {
        "normal": {
            "abajo": cargar_imagen_personaje("sre.png", alto),
            "arriba": cargar_imagen_personaje("sre_up.png", alto),
            "izquierda": cargar_imagen_personaje("sre_left.png", alto),
            "derecha": cargar_imagen_personaje("sre_right.png", alto),
        },
        "ralentizado": {
            "abajo": cargar_imagen_personaje("sre_slow.png", alto),
            "arriba": cargar_imagen_personaje("sre_slow_up.png", alto),
            "izquierda": cargar_imagen_personaje("sre_slow_left.png", alto),
            "derecha": cargar_imagen_personaje("sre_slow_right.png", alto),
        }
    }
    imagen_muerto = cargar_imagen_personaje("sre_muerto.png", alto_muerto)

    velocidad = 1.2
    velocidad_ralentizada = 0.4
    vidas_iniciales = 5
    tiempo_invulnerabilidad = 1000
    tiempo_ralentizacion = 2000

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cambio_x = 0
        self.cambio_y = 0
        self.vidas = self.__class__.vidas_iniciales
        self.invulnerable_hasta = 0
        self.ralentizado_hasta = 0
        self.imagenes = self.__class__.imagenes
        self.imagen_muerto = self.__class__.imagen_muerto
        self.velocidad = self.__class__.velocidad
        self.velocidad_ralentizada = self.__class__.velocidad_ralentizada
        self.alto = self.__class__.alto
        self.tiempo_invulnerabilidad = self.__class__.tiempo_invulnerabilidad
        self.tiempo_ralentizacion = self.__class__.tiempo_ralentizacion

    def obtener_velocidad_actual(self, tiempo_actual):
        if self.esta_ralentizado(tiempo_actual):
            return self.velocidad_ralentizada

        return self.velocidad

    def obtener_estado_imagen(self, tiempo_actual):
        if self.esta_ralentizado(tiempo_actual):
            return "ralentizado"

        return "normal"

    def obtener_direccion_actual(self):
        if self.cambio_y < 0:
            return "arriba"

        if self.cambio_y > 0:
            return "abajo"

        if self.cambio_x < 0:
            return "izquierda"

        if self.cambio_x > 0:
            return "derecha"

        return "abajo"

    def obtener_imagen_actual(self, tiempo_actual):
        estado_imagen = self.obtener_estado_imagen(tiempo_actual)
        direccion = self.obtener_direccion_actual()
        return self.imagenes[estado_imagen][direccion]

    def obtener_ancho_actual(self, tiempo_actual):
        return self.obtener_imagen_actual(tiempo_actual).get_width()

    def obtener_alto_actual(self, tiempo_actual):
        return self.obtener_imagen_actual(tiempo_actual).get_height()

    def dibujar(self, pantalla, tiempo_actual, estado_juego):
        if estado_juego == "terminado":
            pantalla.blit(self.imagen_muerto, (self.x, self.y))
            return

        if self.es_invulnerable(tiempo_actual) and (tiempo_actual // 100) % 2 == 0:
            return

        pantalla.blit(self.obtener_imagen_actual(tiempo_actual), (self.x, self.y))

    def iniciar_movimiento_izquierda(self, tiempo_actual):
        self.cambio_x = -self.obtener_velocidad_actual(tiempo_actual)

    def iniciar_movimiento_derecha(self, tiempo_actual):
        self.cambio_x = self.obtener_velocidad_actual(tiempo_actual)

    def iniciar_movimiento_arriba(self, tiempo_actual):
        self.cambio_y = -self.obtener_velocidad_actual(tiempo_actual)

    def iniciar_movimiento_abajo(self, tiempo_actual):
        self.cambio_y = self.obtener_velocidad_actual(tiempo_actual)

    def detener_movimiento_horizontal(self):
        self.cambio_x = 0

    def detener_movimiento_vertical(self):
        self.cambio_y = 0

    def actualizar_velocidad_movimiento(self, tiempo_actual):
        velocidad_actual = self.obtener_velocidad_actual(tiempo_actual)

        if self.cambio_x < 0:
            self.cambio_x = -velocidad_actual
        elif self.cambio_x > 0:
            self.cambio_x = velocidad_actual

        if self.cambio_y < 0:
            self.cambio_y = -velocidad_actual
        elif self.cambio_y > 0:
            self.cambio_y = velocidad_actual

    def mover(self, ancho_pantalla, alto_pantalla, tiempo_actual):
        self.actualizar_velocidad_movimiento(tiempo_actual)

        self.x += self.cambio_x
        self.y += self.cambio_y

        ancho_actual = self.obtener_ancho_actual(tiempo_actual)
        alto_actual = self.obtener_alto_actual(tiempo_actual)

        if self.x < 0:
            self.x = 0
        elif self.x > ancho_pantalla - ancho_actual:
            self.x = ancho_pantalla - ancho_actual

        if self.y < 0:
            self.y = 0
        elif self.y > alto_pantalla - alto_actual:
            self.y = alto_pantalla - alto_actual

    def detener(self):
        self.cambio_x = 0
        self.cambio_y = 0

    def obtener_centro(self, tiempo_actual=None):
        if tiempo_actual is None:
            imagen_actual = self.imagenes["normal"]["abajo"]
        else:
            imagen_actual = self.obtener_imagen_actual(tiempo_actual)

        return self.x + imagen_actual.get_width() / 2, self.y + imagen_actual.get_height() / 2

    def obtener_rect(self, tiempo_actual=None):
        if tiempo_actual is None:
            imagen_actual = self.imagenes["normal"]["abajo"]
        else:
            imagen_actual = self.obtener_imagen_actual(tiempo_actual)

        return pygame.Rect(
            self.x,
            self.y,
            imagen_actual.get_width(),
            imagen_actual.get_height()
        )

    def es_invulnerable(self, tiempo_actual):
        return tiempo_actual < self.invulnerable_hasta

    def recibir_golpe(self, tiempo_actual):
        self.vidas -= 1
        self.invulnerable_hasta = tiempo_actual + self.tiempo_invulnerabilidad

    def ralentizar(self, tiempo_actual):
        self.ralentizado_hasta = tiempo_actual + self.tiempo_ralentizacion

    def esta_ralentizado(self, tiempo_actual):
        return tiempo_actual < self.ralentizado_hasta

    def esta_muerto(self):
        return self.vidas <= 0

    def obtener_ancho_muerto(self):
        return self.imagen_muerto.get_width()

    def obtener_alto_muerto(self):
        return self.imagen_muerto.get_height()