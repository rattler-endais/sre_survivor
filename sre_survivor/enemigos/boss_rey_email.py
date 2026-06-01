import pygame
from sre_survivor.assets import imagen as ruta_imagen
from sre_survivor.enemigos.enemigo import Enemigo

"""Imagen inicial quieto    boss_email_idle.png
Movimiento 1    boss_email_move_1.png
Movimiento 2    boss_email_move_2.png
Movimiento 3    boss_email_move_3.png
Daño 50%    boss_email_damage_50.png
Daño 80%    boss_email_damage_80.png
Daño 90%    boss_email_damage_90.png
Explosión frame 1   boss_email_explosion_1.png
Explosión frame 2   boss_email_explosion_2.png
Explosión frame 3   boss_email_explosion_3.png
Explosión frame 4   boss_email_explosion_4.png
Explosión frame 5   boss_email_explosion_5.png
Imagen que tapa la pantalla boss_email_overlay.png
Muerte frame 1  boss_email_death_1.png
Muerte frame 2  boss_email_death_2.png
Muerte frame 3  boss_email_death_3.png
Muerte frame 4  boss_email_death_4.png"""

def cargar_imagen_boss(nombre_archivo, tamaño):
    return pygame.transform.scale(
        pygame.image.load(ruta_imagen(f"enemigos/boss_email/{nombre_archivo}")),
        tamaño
    )


class BossEmail(Enemigo):
    tamaño = (130, 130)

    imagen = cargar_imagen_boss("boss_email_idle.png", tamaño)
    velocidad = 0.15
    vida_maxima = 20
    puntos = 10
    desaparece_al_colisionar_con_personaje = False

    nombre = "REY DEL CORREO ELECTRÓNICO"
    tamaño_fuente_nombre = 13
    color_nombre = (180, 139, 202)
    color_sombra_nombre = (0, 0, 0)

    tiempo_espera_inicial = 2500
    tiempo_por_frame_movimiento = 180
    tiempo_por_frame_explosion = 180
    tiempo_overlay = 5000
    tiempo_por_frame_muerte = 180

    imagen_idle = cargar_imagen_boss("boss_email_idle.png", tamaño)

    imagenes_movimiento = [
        cargar_imagen_boss("boss_email_move_1.png", tamaño),
        cargar_imagen_boss("boss_email_move_2.png", tamaño),
        cargar_imagen_boss("boss_email_move_3.png", tamaño),
    ]

    imagen_damage_50 = cargar_imagen_boss("boss_email_damage_50.png", tamaño)
    imagen_damage_80 = cargar_imagen_boss("boss_email_damage_80.png", tamaño)
    imagen_damage_90 = cargar_imagen_boss("boss_email_damage_90.png", tamaño)

    imagenes_explosion = [
        cargar_imagen_boss("boss_email_explosion_1.png", tamaño),
        cargar_imagen_boss("boss_email_explosion_2.png", tamaño),
        cargar_imagen_boss("boss_email_explosion_3.png", tamaño),
        cargar_imagen_boss("boss_email_explosion_4.png", tamaño),
        cargar_imagen_boss("boss_email_explosion_5.png", tamaño),
    ]

    imagen_overlay = pygame.image.load(
        ruta_imagen("enemigos/boss_email/boss_email_overlay.png")
    )

    imagenes_muerte = [
        cargar_imagen_boss("boss_email_death_1.png", tamaño),
        cargar_imagen_boss("boss_email_death_2.png", tamaño),
        cargar_imagen_boss("boss_email_death_3.png", tamaño),
        cargar_imagen_boss("boss_email_death_4.png", tamaño),
    ]

    def __init__(self, x, y, centro_pantalla_x, centro_pantalla_y):
        super().__init__(x, y)
        self.centro_pantalla_x = centro_pantalla_x
        self.centro_pantalla_y = centro_pantalla_y
        self.estado = "apareciendo"
        self.tiempo_creacion = pygame.time.get_ticks()
        self.tiempo_inicio_estado = self.tiempo_creacion
        self.overlay_visible_hasta = 0
        self.puede_eliminarse = False
        # Se crea la fuente en el init de la clase porque requiere que se haya ejecutado pygame.init() previamente
        # Si se intenta crear la fuente al importar la clase, pygame no estará inicializado y se producirá un error "pygame.error: font not initialized"
        self.fuente_nombre = pygame.font.SysFont(
            "arial",
            self.tamaño_fuente_nombre,
            bold=True
        )

    def cambiar_estado(self, nuevo_estado, tiempo_actual):
        self.estado = nuevo_estado
        self.tiempo_inicio_estado = tiempo_actual

    def obtener_imagen_por_vida(self):
        porcentaje_vida_perdida = 1 - self.vida / self.vida_maxima

        if porcentaje_vida_perdida >= 0.9:
            return self.imagen_damage_90

        if porcentaje_vida_perdida >= 0.8:
            return self.imagen_damage_80

        if porcentaje_vida_perdida >= 0.5:
            return self.imagen_damage_50

        return self.imagen_idle

    def obtener_imagen_movimiento(self, tiempo_actual):
        indice = (
            (tiempo_actual - self.tiempo_inicio_estado)
            // self.tiempo_por_frame_movimiento
        ) % len(self.imagenes_movimiento)

        return self.imagenes_movimiento[indice]

    def obtener_imagen_explosion(self, tiempo_actual):
        indice = (
            tiempo_actual - self.tiempo_inicio_estado
        ) // self.tiempo_por_frame_explosion

        if indice >= len(self.imagenes_explosion):
            return None

        return self.imagenes_explosion[indice]

    def obtener_imagen_muerte(self, tiempo_actual):
        indice = (
            tiempo_actual - self.tiempo_inicio_estado
        ) // self.tiempo_por_frame_muerte

        if indice >= len(self.imagenes_muerte):
            self.puede_eliminarse = True
            return self.imagenes_muerte[-1]

        return self.imagenes_muerte[indice]

    def mover_hacia(self, objetivo_x, objetivo_y, tiempo_actual=None):
        if tiempo_actual is None:
            return

        if self.estado == "apareciendo":
            if tiempo_actual - self.tiempo_inicio_estado >= self.tiempo_espera_inicial:
                self.cambiar_estado("moviendose", tiempo_actual)
            return

        if self.estado != "moviendose":
            return

        objetivo_x = self.centro_pantalla_x - self.ancho / 2
        objetivo_y = self.centro_pantalla_y - self.alto / 2

        dx = objetivo_x - self.x
        dy = objetivo_y - self.y
        distancia = (dx ** 2 + dy ** 2) ** 0.5

        if distancia <= self.velocidad:
            self.x = objetivo_x
            self.y = objetivo_y
            self.cambiar_estado("explotando", tiempo_actual)
            return

        if distancia > 0:
            self.x += (dx / distancia) * self.velocidad
            self.y += (dy / distancia) * self.velocidad

    def actualizar(self, tiempo_actual):
        if self.estado == "explotando":
            duracion_explosion = len(self.imagenes_explosion) * self.tiempo_por_frame_explosion

            if tiempo_actual - self.tiempo_inicio_estado >= duracion_explosion:
                self.overlay_visible_hasta = tiempo_actual + self.tiempo_overlay
                self.cambiar_estado("pantalla_inundada", tiempo_actual)

        elif self.estado == "pantalla_inundada":
            if tiempo_actual >= self.overlay_visible_hasta:
                self.cambiar_estado("reposo", tiempo_actual)

        elif self.estado == "muriendo":
            self.obtener_imagen_muerte(tiempo_actual)

    def recibir_golpe(self, daño):
        if self.estado == "muriendo":
            return

        super().recibir_golpe(daño)

        if self.vida <= 0:
            self.vida = 0
            self.estado = "muriendo"
            self.tiempo_inicio_estado = pygame.time.get_ticks()

    def esta_derrotado(self):
        return self.vida <= 0 and self.puede_eliminarse

    def obtener_imagen_actual(self, tiempo_actual):
        if self.estado == "apareciendo":
            return self.obtener_imagen_por_vida()

        if self.estado == "moviendose":
            return self.obtener_imagen_movimiento(tiempo_actual)

        if self.estado == "explotando":
            imagen_explosion = self.obtener_imagen_explosion(tiempo_actual)

            if imagen_explosion is not None:
                return imagen_explosion

            return self.obtener_imagen_por_vida()

        if self.estado == "muriendo":
            return self.obtener_imagen_muerte(tiempo_actual)

        return self.obtener_imagen_por_vida()

    def dibujar(self, pantalla, tiempo_actual=None):
        if tiempo_actual is None:
            tiempo_actual = pygame.time.get_ticks()

        self.imagen = self.obtener_imagen_actual(tiempo_actual)
        pantalla.blit(self.imagen, (self.x, self.y))

        if self.estado != "muriendo":
            self.dibujar_nombre(pantalla)
            self.dibujar_barra_vida(pantalla)

    def dibujar_nombre(self, pantalla):
        texto_sombra = self.fuente_nombre.render(self.nombre, True, self.color_sombra_nombre)
        texto = self.fuente_nombre.render(self.nombre, True, self.color_nombre)

        x_texto = self.x + self.ancho / 2 - texto.get_width() / 2
        y_texto = self.y - 30

        pantalla.blit(texto_sombra, (x_texto + 2, y_texto + 2))
        pantalla.blit(texto, (x_texto, y_texto))

    def dibujar_barra_vida(self, pantalla):
        margen = 6
        alto_barra = 8
        ancho_barra = self.ancho
        x_barra = self.x
        y_barra = self.y - alto_barra - margen

        porcentaje_vida = max(0, self.vida / self.vida_maxima)
        ancho_vida = int(ancho_barra * porcentaje_vida)

        pygame.draw.rect(
            pantalla,
            (27, 27, 32),
            (x_barra, y_barra, ancho_barra, alto_barra)
        )

        pygame.draw.rect(
            pantalla,
            (144, 72, 185),
            (x_barra, y_barra, ancho_vida, alto_barra)
        )

        pygame.draw.rect(
            pantalla,
            (170, 109, 202),
            (x_barra, y_barra, ancho_barra, alto_barra),
            1
        )

    def debe_bloquear_generacion_enemigos(self):
        return self.estado not in ("muriendo",)

    def debe_dibujar_overlay(self, tiempo_actual):
        return self.estado == "pantalla_inundada" and tiempo_actual < self.overlay_visible_hasta

    def dibujar_overlay(self, pantalla):
        overlay = pygame.transform.scale(
            self.imagen_overlay,
            pantalla.get_size()
        )
        pantalla.blit(overlay, (0, 0))
