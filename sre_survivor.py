import pygame
import random
from hacker import Hacker
from assets import imagen, sonido

ANCHOPANTALLA = 800
ALTOPANTALLA = 600
print("Inicio de SRE Survivor")
print("Desarrollado por Sr. Muñoz")

# Inicializar a Pygame
pygame.init()

# Sonidos
pygame.mixer.music.load(sonido("MusicaFondo.mp3"))
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)

sonido_disparo = pygame.mixer.Sound(sonido("disparo.mp3"))
sonido_golpe = pygame.mixer.Sound(sonido("golpe.mp3"))
sonido_vida_perdida = pygame.mixer.Sound(sonido("vida_perdida.mp3"))
sonido_gameover = pygame.mixer.Sound(sonido("risamalvada.mp3"))
sonido_gameover_huevo_de_pascua = pygame.mixer.Sound(sonido("sonido_boss_iin.mp3"))

sonido_disparo.set_volume(0.8)
sonido_golpe.set_volume(0.8)
sonido_vida_perdida.set_volume(0.8)
sonido_gameover.set_volume(0.8)
sonido_gameover_huevo_de_pascua.set_volume(0.8)

# Crear la pantalla
pantalla = pygame.display.set_mode((ANCHOPANTALLA, ALTOPANTALLA))
pygame.display.set_caption("SRE Survivor")
icono = pygame.image.load(imagen("iconosre.png"))
pygame.display.set_icon(icono)

# Fondo
fondo = pygame.image.load(imagen("fondosre.png"))
fondo = pygame.transform.scale(fondo, (ANCHOPANTALLA, ALTOPANTALLA))

# Fondo fin del juego
fondofin = pygame.image.load(imagen("fondosrefin.png"))
fondofin = pygame.transform.scale(fondofin, (ANCHOPANTALLA, ALTOPANTALLA))

# Protagonista SRE
personaje_img = pygame.image.load(imagen("sre.png"))
personaje_img = pygame.transform.scale(personaje_img, (84, 100))
personaje_muerto_img = pygame.image.load(imagen("sre_muerto.png"))
personaje_muerto_img = pygame.transform.scale(personaje_muerto_img, (100, 50))
personaje_x = 358
personaje_y = 480
personaje_cambio_x = 0
personaje_cambio_y = 0
velocidad_personaje = 1
vidas = 3
invulnerable_hasta = 0
tiempo_invulnerabilidad = 1000

# Corazones
corazon_img = pygame.image.load(imagen("corazon.png"))
corazon_img = pygame.transform.scale(corazon_img, (32, 32))

# Hacker
hackers = []
ultimo_hacker = 0
tiempo_entre_hackers = 3000

# Teclado
teclado_img = pygame.image.load(imagen("teclado.png"))
teclado_ancho = 80
teclado_alto = int(teclado_img.get_height() * teclado_ancho / teclado_img.get_width())
teclado_img = pygame.transform.scale(teclado_img, (teclado_ancho, teclado_alto))
teclados = []
velocidad_teclado = 1.5
ultimo_disparo_teclado = pygame.time.get_ticks()
tiempo_entre_teclados = 2500

# Boss
boss_img = pygame.image.load(imagen("boss.png"))
boss_img = pygame.transform.scale(boss_img, (138, 150))
boss_x = ANCHOPANTALLA // 2 - boss_img.get_width() // 2
boss_y = (ALTOPANTALLA - boss_img.get_height() - 50)

# Puntaje y tiempo
puntaje = 0
fuente = pygame.font.Font(None, 36) # Usar la fuente predeterminada del sistema
fuente_game_over = pygame.font.Font(None, 96)
fuente_fin = pygame.font.Font(None, 44)
tiempo_inicio = pygame.time.get_ticks()
tiempo_fin = None
estado_juego = "jugando"
sonido_gameover_reproducido = False
sonido_huevo_de_pascua_reproducido = False

def personaje(x,y, tiempo_actual):
    if estado_juego == "terminado":
        pantalla.blit(personaje_muerto_img, (x, y))
        return

    if tiempo_actual < invulnerable_hasta and (tiempo_actual // 100) % 2 == 0:
        return

    pantalla.blit(personaje_img, (x, y))

def teclado(x, y):
    pantalla.blit(teclado_img, (x, y))

def boss(x, y):
    pantalla.blit(boss_img, (x, y))

def dibujar_vidas():
    for i in range(vidas):
        pantalla.blit(corazon_img, (10 + i * 38, 10))

def crear_hacker():
    posiciones_por_borde = {
        "arriba": {
            "x": random.randrange(0, ANCHOPANTALLA - Hacker.ancho),
            "y": -Hacker.alto
        },
        "abajo": {
            "x": random.randrange(0, ANCHOPANTALLA - Hacker.ancho),
            "y": ALTOPANTALLA
        },
        "izquierda": {
            "x": -Hacker.ancho,
            "y": random.randrange(0, ALTOPANTALLA - Hacker.alto)
        },
        "derecha": {
            "x": ANCHOPANTALLA,
            "y": random.randrange(0, ALTOPANTALLA - Hacker.alto)
        }
    }

    borde = random.choice(list(posiciones_por_borde.keys()))
    posicion = posiciones_por_borde[borde]
    hackers.append(Hacker(posicion["x"], posicion["y"]))

def obtener_hacker_mas_cercano(origen_x, origen_y):
    hacker_mas_cercano = None
    distancia_mas_cercana = None

    origen_centro_x = origen_x + 42
    origen_centro_y = origen_y + 50

    for h in hackers:
        hacker_centro_x, hacker_centro_y = h.obtener_centro()

        dx = hacker_centro_x - origen_centro_x
        dy = hacker_centro_y - origen_centro_y
        distancia = (dx ** 2 + dy ** 2) ** 0.5

        if distancia_mas_cercana is None or distancia < distancia_mas_cercana:
            distancia_mas_cercana = distancia
            hacker_mas_cercano = h

    return hacker_mas_cercano

def dibujar_hackers():
    for h in hackers:
        h.dibujar(pantalla)

def dibujar_teclados():
    for t in teclados:
        teclado(t["x"], t["y"])

def disparar_teclado():
    hacker_objetivo = obtener_hacker_mas_cercano(personaje_x, personaje_y)

    if hacker_objetivo is not None:
        origen_x = personaje_x + 42 - teclado_ancho / 2
        origen_y = personaje_y + 50 - teclado_alto / 2
        destino_x, destino_y = hacker_objetivo.obtener_centro()

        dx = destino_x - origen_x
        dy = destino_y - origen_y
        distancia = (dx ** 2 + dy ** 2) ** 0.5

        if distancia > 0:
            teclados.append({
                "x": origen_x,
                "y": origen_y,
                "velocidad_x": (dx / distancia) * velocidad_teclado,
                "velocidad_y": (dy / distancia) * velocidad_teclado
            })
            sonido_disparo.play()

def mover_teclados():
    # Genera una copia de la lista original
    # Esto evita que la lista original se modifique mientras se itera sobre ella
    copia_teclados = teclados[:]

    for t in copia_teclados:
        t["x"] += t["velocidad_x"]
        t["y"] += t["velocidad_y"]

        if (
            t["x"] < -teclado_ancho or
            t["x"] > ANCHOPANTALLA or
            t["y"] < -teclado_alto or
            t["y"] > ALTOPANTALLA
        ): # Eliminamos los teclados fuera de la pantalla
            teclados.remove(t)

def mover_hackers():
    # Movimiento de los Hackers hacia el personaje
    for h in hackers:
        h.mover_hacia(personaje_x, personaje_y)

def detectar_colisiones(): # Detecta colisiones entre hackers y teclados
    global hackers, teclados, puntaje

    teclados_sobrevivientes = []
    hackers_sobrevivientes = list(hackers) # Crear una copia de la lista original

    for teclado_actual in teclados:
        teclado_choco = False

        for hacker_actual in hackers_sobrevivientes[:]:
            dx = teclado_actual["x"] - hacker_actual.x
            dy = teclado_actual["y"] - hacker_actual.y
            distancia = (dx ** 2 + dy ** 2) ** 0.5

            if distancia < 50: # Si la distancia es menor que el radio del teclado (80x35)
                teclado_choco = True
                puntaje += 1
                sonido_golpe.play()
                hackers_sobrevivientes.remove(hacker_actual)
                break # Salir del bucle interno para evitar colisiones con otros hackers
        if not teclado_choco:
            # Si no choco, agregarlo a la lista de teclados sobrevivientes
            # para que se siga moviendo
            teclados_sobrevivientes.append(teclado_actual)

    hackers = hackers_sobrevivientes
    teclados = teclados_sobrevivientes

def detectar_colisiones_personaje(tiempo_actual):
    global vidas, invulnerable_hasta, hackers

    if tiempo_actual < invulnerable_hasta:
        return

    personaje_rect = pygame.Rect(personaje_x, personaje_y, 84, 100)
    hacker_colisionado = None

    for hacker_actual in hackers:
        hacker_rect = hacker_actual.obtener_rect()

        if personaje_rect.colliderect(hacker_rect): # Si el personaje colisiona con el hacker
            vidas -= 1
            sonido_vida_perdida.play()
            invulnerable_hasta = tiempo_actual + tiempo_invulnerabilidad
            hacker_colisionado = hacker_actual
            break

    # Se reconstruye la lista de hackers sin el hacker colisionado
    if hacker_colisionado is not None:
        hackers = [
            hacker_actual
            for hacker_actual in hackers
            if hacker_actual is not hacker_colisionado
        ]

def dibujar_puntaje():
    texto = fuente.render(f"Puntos: {puntaje}", False, (255, 204, 29))
    pantalla.blit(texto, (650, 10))

def formatear_tiempo(milisegundos):
    segundos_totales = milisegundos // 1000
    minutos = segundos_totales // 60
    segundos = segundos_totales % 60
    return f"{minutos}:{segundos:02d}"

def obtener_tiempo_sobrevivido(tiempo_actual):
    if tiempo_fin is not None:
        return tiempo_fin - tiempo_inicio

    return tiempo_actual - tiempo_inicio

def dibujar_cronometro(tiempo_actual):
    tiempo_sobrevivido = obtener_tiempo_sobrevivido(tiempo_actual)
    texto = fuente.render(f"Tiempo: {formatear_tiempo(tiempo_sobrevivido)}", False, (255, 204, 29))
    rect = texto.get_rect(center=(ANCHOPANTALLA // 2, 25))
    sombra_texto = fuente.render(f"Tiempo: {formatear_tiempo(tiempo_sobrevivido)}", False, (43, 56, 61))
    sombra_rect = texto.get_rect(center=(ANCHOPANTALLA // 2 + 2, 25 + 2))
    pantalla.blit(sombra_texto, sombra_rect)
    pantalla.blit(texto, rect)

def terminar_juego(tiempo_actual):
    global estado_juego, tiempo_fin, personaje_cambio_x, personaje_cambio_y

    estado_juego = "terminado"
    tiempo_fin = tiempo_actual
    personaje_cambio_x = 0
    personaje_cambio_y = 0
    pygame.mixer.music.stop()

def actualizar_juego(tiempo_actual):
    global ultimo_hacker, ultimo_disparo_teclado

    # Movimiento de los hackers
    mover_hackers()

    # Aparición automática de hackers cada 3 segundos
    if tiempo_actual - ultimo_hacker >= tiempo_entre_hackers:
        crear_hacker()
        ultimo_hacker = tiempo_actual

    # Disparo automático de teclados cada segundo
    if tiempo_actual - ultimo_disparo_teclado >= tiempo_entre_teclados:
        disparar_teclado()
        ultimo_disparo_teclado = tiempo_actual

    mover_teclados()
    detectar_colisiones()
    detectar_colisiones_personaje(tiempo_actual)

    if vidas <= 0:
        terminar_juego(tiempo_actual)

def dibujar_pantalla_juego(tiempo_actual):
    # Dibujar elementos en la pantalla
    #pantalla.fill((230, 220, 240))
    pantalla.blit(fondo, (0, 0))
    personaje(personaje_x, personaje_y, tiempo_actual)
    dibujar_hackers()
    dibujar_teclados()
    dibujar_vidas()
    dibujar_puntaje()
    dibujar_cronometro(tiempo_actual)

def obtener_posicion_boss_fin():
    separacion = 15

    personaje_muerto_ancho = personaje_muerto_img.get_width()
    personaje_muerto_alto = personaje_muerto_img.get_height()
    boss_ancho = boss_img.get_width()
    boss_alto = boss_img.get_height()

    boss_x_calculado = personaje_x + personaje_muerto_ancho + separacion

    if boss_x_calculado + boss_ancho > ANCHOPANTALLA:
        boss_x_calculado = personaje_x - boss_ancho - separacion

    boss_y_calculado = personaje_y + personaje_muerto_alto // 2 - boss_alto // 2

    boss_x_calculado = max(0, min(boss_x_calculado, ANCHOPANTALLA - boss_ancho))
    boss_y_calculado = max(0, min(boss_y_calculado, ALTOPANTALLA - boss_alto))

    return boss_x_calculado, boss_y_calculado

def dibujar_pantalla_fin():
    pantalla.blit(fondofin, (0, 0))
    personaje(personaje_x, personaje_y, tiempo_fin)
    #dibujar_hackers()
    #dibujar_teclados()
    #dibujar_puntaje()
    #dibujar_cronometro(tiempo_fin)
    boss_fin_x, boss_fin_y = obtener_posicion_boss_fin()
    boss(boss_fin_x, boss_fin_y)

    texto_game_over = fuente_game_over.render("GAME OVER", False, (255, 0, 0))
    rect_game_over = texto_game_over.get_rect(center=(ANCHOPANTALLA // 2, ALTOPANTALLA // 2 - 80))
    sombra_texto_game_over = fuente_game_over.render("GAME OVER", False, (255, 255, 255))
    sombra_rect_game_over = texto_game_over.get_rect(center=(ANCHOPANTALLA // 2 + 3, ALTOPANTALLA // 2 - 80 + 3))
    pantalla.blit(sombra_texto_game_over, sombra_rect_game_over)
    pantalla.blit(texto_game_over, rect_game_over)

    texto_puntaje = fuente_fin.render(f"Puntaje final: {puntaje}", False, (239, 251, 127))
    rect_puntaje = texto_puntaje.get_rect(center=(ANCHOPANTALLA // 2, ALTOPANTALLA // 2))
    sombra_texto_puntaje = fuente_fin.render(f"Puntaje final: {puntaje}", False, (84, 136, 45))
    sombra_rect_puntaje = texto_puntaje.get_rect(center=(ANCHOPANTALLA // 2 + 2, ALTOPANTALLA // 2 + 2))
    pantalla.blit(sombra_texto_puntaje, sombra_rect_puntaje)
    pantalla.blit(texto_puntaje, rect_puntaje)

    tiempo_sobrevivido = tiempo_fin - tiempo_inicio
    texto_tiempo = fuente_fin.render(f"Tiempo sobrevivido: {formatear_tiempo(tiempo_sobrevivido)}", False, (239, 251, 127))
    rect_tiempo = texto_tiempo.get_rect(center=(ANCHOPANTALLA // 2, ALTOPANTALLA // 2 + 50))
    sombra_texto_tiempo = fuente_fin.render(f"Tiempo sobrevivido: {formatear_tiempo(tiempo_sobrevivido)}", False, (84, 136, 45))
    sombra_rect_tiempo = texto_tiempo.get_rect(center=(ANCHOPANTALLA // 2 + 2, ALTOPANTALLA // 2 + 50 + 2))
    pantalla.blit(sombra_texto_tiempo, sombra_rect_tiempo)
    pantalla.blit(texto_tiempo, rect_tiempo)

def cursor_en_area_huevo_de_pascua():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    area_huevo_de_pascua = pygame.Rect(
            ANCHOPANTALLA - 190,
            ALTOPANTALLA - 180,
            145,
            115
        )
    return area_huevo_de_pascua.collidepoint(mouse_x, mouse_y)

def gestionar_sonido_gameover():
    global sonido_gameover_reproducido

    if not sonido_gameover_reproducido:
        sonido_gameover.play(loops=2)
        sonido_gameover_reproducido = True

def gestionar_huevo_de_pascua():
    global sonido_huevo_de_pascua_reproducido

    if sonido_huevo_de_pascua_reproducido:
        return

    if pygame.mouse.get_pressed()[0] and cursor_en_area_huevo_de_pascua():
        #sonido_gameover.stop()
        sonido_gameover_huevo_de_pascua.play()
        sonido_huevo_de_pascua_reproducido = True



# Loop del juego
se_ejecuta = True
while se_ejecuta:
    tiempo_actual = pygame.time.get_ticks()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        if estado_juego == "jugando" and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                personaje_cambio_x = -velocidad_personaje
            if evento.key == pygame.K_RIGHT:
                personaje_cambio_x = velocidad_personaje
            if evento.key == pygame.K_UP:
                personaje_cambio_y = -velocidad_personaje
            if evento.key == pygame.K_DOWN:
                personaje_cambio_y = velocidad_personaje
        if estado_juego == "jugando" and evento.type == pygame.KEYUP:
            if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                personaje_cambio_x = 0
            if evento.key in (pygame.K_UP, pygame.K_DOWN):
                personaje_cambio_y = 0

    if estado_juego == "jugando":
        # Movimiento del personaje
        personaje_x += personaje_cambio_x
        personaje_y += personaje_cambio_y

        if personaje_x < 0:
            personaje_x = 0
        elif personaje_x > ANCHOPANTALLA - 84:
            personaje_x = ANCHOPANTALLA - 84
        if personaje_y < 0:
            personaje_y = 0
        elif personaje_y > ALTOPANTALLA - 100:
            personaje_y = ALTOPANTALLA - 100

        actualizar_juego(tiempo_actual)
        dibujar_pantalla_juego(tiempo_actual)
    else: # GAME OVER
        dibujar_pantalla_fin()
        gestionar_sonido_gameover()
        gestionar_huevo_de_pascua()

    pygame.display.update() # Actualizar la pantalla

pygame.quit()
print("Fin del juego")
