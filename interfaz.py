import pygame
from assets import imagen

class Interfaz:
    def __init__(self, ancho_pantalla, alto_pantalla):
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla

        self.corazon_img = pygame.image.load(imagen("corazon.png"))
        self.corazon_img = pygame.transform.scale(self.corazon_img, (32, 32))

        self.fuente = pygame.font.Font(None, 36)
        self.fuente_game_over = pygame.font.Font(None, 96)
        self.fuente_fin = pygame.font.Font(None, 44)

    def dibujar_vidas(self, pantalla, vidas):
        for i in range(vidas):
            pantalla.blit(self.corazon_img, (10 + i * 38, 10))

    def dibujar_puntaje(self, pantalla, puntaje):
        texto = self.fuente.render(f"Puntos: {puntaje}", False, (255, 204, 29))
        pantalla.blit(texto, (650, 10))

    def formatear_tiempo(self, milisegundos):
        segundos_totales = milisegundos // 1000
        minutos = segundos_totales // 60
        segundos = segundos_totales % 60
        return f"{minutos}:{segundos:02d}"

    def obtener_tiempo_sobrevivido(self, tiempo_actual, tiempo_inicio, tiempo_fin):
        if tiempo_fin is not None:
            return tiempo_fin - tiempo_inicio

        return tiempo_actual - tiempo_inicio

    def dibujar_cronometro(self, pantalla, tiempo_actual, tiempo_inicio, tiempo_fin):
        tiempo_sobrevivido = self.obtener_tiempo_sobrevivido(
            tiempo_actual,
            tiempo_inicio,
            tiempo_fin
        )

        texto_tiempo = f"Tiempo: {self.formatear_tiempo(tiempo_sobrevivido)}"

        texto = self.fuente.render(texto_tiempo, False, (255, 204, 29))
        rect = texto.get_rect(center=(self.ancho_pantalla // 2, 25))

        sombra_texto = self.fuente.render(texto_tiempo, False, (43, 56, 61))
        sombra_rect = texto.get_rect(center=(self.ancho_pantalla // 2 + 2, 25 + 2))

        pantalla.blit(sombra_texto, sombra_rect)
        pantalla.blit(texto, rect)

    def dibujar_game_over(self, pantalla, puntaje, tiempo_inicio, tiempo_fin):
        texto_game_over = self.fuente_game_over.render("GAME OVER", False, (255, 0, 0))
        rect_game_over = texto_game_over.get_rect(
            center=(self.ancho_pantalla // 2, self.alto_pantalla // 2 - 80)
        )

        sombra_texto_game_over = self.fuente_game_over.render("GAME OVER", False, (255, 255, 255))
        sombra_rect_game_over = texto_game_over.get_rect(
            center=(self.ancho_pantalla // 2 + 3, self.alto_pantalla // 2 - 80 + 3)
        )

        pantalla.blit(sombra_texto_game_over, sombra_rect_game_over)
        pantalla.blit(texto_game_over, rect_game_over)

        texto_puntaje = self.fuente_fin.render(f"Puntaje final: {puntaje}", False, (239, 251, 127))
        rect_puntaje = texto_puntaje.get_rect(
            center=(self.ancho_pantalla // 2, self.alto_pantalla // 2)
        )

        sombra_texto_puntaje = self.fuente_fin.render(f"Puntaje final: {puntaje}", False, (84, 136, 45))
        sombra_rect_puntaje = texto_puntaje.get_rect(
            center=(self.ancho_pantalla // 2 + 2, self.alto_pantalla // 2 + 2)
        )

        pantalla.blit(sombra_texto_puntaje, sombra_rect_puntaje)
        pantalla.blit(texto_puntaje, rect_puntaje)

        tiempo_sobrevivido = tiempo_fin - tiempo_inicio
        texto_tiempo_final = f"Tiempo sobrevivido: {self.formatear_tiempo(tiempo_sobrevivido)}"

        texto_tiempo = self.fuente_fin.render(texto_tiempo_final, False, (239, 251, 127))
        rect_tiempo = texto_tiempo.get_rect(
            center=(self.ancho_pantalla // 2, self.alto_pantalla // 2 + 50)
        )

        sombra_texto_tiempo = self.fuente_fin.render(texto_tiempo_final, False, (84, 136, 45))
        sombra_rect_tiempo = texto_tiempo.get_rect(
            center=(self.ancho_pantalla // 2 + 2, self.alto_pantalla // 2 + 50 + 2)
        )

        pantalla.blit(sombra_texto_tiempo, sombra_rect_tiempo)
        pantalla.blit(texto_tiempo, rect_tiempo)