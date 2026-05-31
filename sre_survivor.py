import pygame
import random
from hacker import Hacker
from teclado import Teclado
from personajesre import Personajesre
from interfaz import Interfaz
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
personaje_sre = Personajesre(358, 480)

# Interfaz
interfaz = Interfaz(ANCHOPANTALLA, ALTOPANTALLA)

# Hacker
hackers = []
ultimo_hacker = 0
tiempo_entre_hackers = 3000

# Teclado
teclados = []
ultimo_disparo_teclado = pygame.time.get_ticks()
tiempo_entre_teclados = 2500

# Boss
boss_img = pygame.image.load(imagen("boss.png"))
boss_img = pygame.transform.scale(boss_img, (138, 150))
boss_x = ANCHOPANTALLA // 2 - boss_img.get_width() // 2
boss_y = (ALTOPANTALLA - boss_img.get_height() - 50)

# Puntaje y tiempo
puntaje = 0
tiempo_inicio = pygame.time.get_ticks()
tiempo_fin = None
estado_juego = "jugando"
sonido_gameover_reproducido = False
sonido_huevo_de_pascua_reproducido = False

def boss(x, y):
    pantalla.blit(boss_img, (x, y))

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

    origen_centro_x, origen_centro_y = personaje_sre.obtener_centro()

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
        t.dibujar(pantalla)

def disparar_teclado():
    hacker_objetivo = obtener_hacker_mas_cercano(personaje_sre.x, personaje_sre.y)

    if hacker_objetivo is not None:
        personaje_centro_x, personaje_centro_y = personaje_sre.obtener_centro()
        origen_x = personaje_centro_x - Teclado.ancho / 2
        origen_y = personaje_centro_y - Teclado.alto / 2
        destino_x, destino_y = hacker_objetivo.obtener_centro()

        dx = destino_x - origen_x
        dy = destino_y - origen_y
        distancia = (dx ** 2 + dy ** 2) ** 0.5

        if distancia > 0:
            teclados.append(Teclado(
                origen_x,
                origen_y,
                (dx / distancia) * Teclado.velocidad,
                (dy / distancia) * Teclado.velocidad
            ))
            sonido_disparo.play()

def mover_teclados():
    # Genera una copia de la lista original
    # Esto evita que la lista original se modifique mientras se itera sobre ella
    copia_teclados = teclados[:]

    for t in copia_teclados:
        t.mover()

        if t.esta_fuera_de_pantalla(ANCHOPANTALLA, ALTOPANTALLA):
            teclados.remove(t)

def mover_hackers():
    # Movimiento de los Hackers hacia el personaje
    for h in hackers:
        h.mover_hacia(personaje_sre.x, personaje_sre.y)

def detectar_colisiones(): # Detecta colisiones entre hackers y teclados
    global hackers, teclados, puntaje

    teclados_sobrevivientes = []
    hackers_sobrevivientes = list(hackers) # Crear una copia de la lista original

    for teclado_actual in teclados:
        teclado_choco = False

        for hacker_actual in hackers_sobrevivientes[:]:
            dx = teclado_actual.x - hacker_actual.x
            dy = teclado_actual.y - hacker_actual.y
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
    global hackers

    if personaje_sre.es_invulnerable(tiempo_actual):
        return

    personaje_rect = personaje_sre.obtener_rect()
    hacker_colisionado = None

    for hacker_actual in hackers:
        hacker_rect = hacker_actual.obtener_rect()

        if personaje_rect.colliderect(hacker_rect): # Si el personaje colisiona con el hacker
            personaje_sre.recibir_golpe(tiempo_actual)
            sonido_vida_perdida.play()
            hacker_colisionado = hacker_actual
            break

    # Se reconstruye la lista de hackers sin el hacker colisionado
    if hacker_colisionado is not None:
        hackers = [
            hacker_actual
            for hacker_actual in hackers
            if hacker_actual is not hacker_colisionado
        ]

def terminar_juego(tiempo_actual):
    global estado_juego, tiempo_fin
    
    estado_juego = "terminado"
    tiempo_fin = tiempo_actual
    personaje_sre.detener()
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

    if personaje_sre.esta_muerto():
        terminar_juego(tiempo_actual)

def dibujar_pantalla_juego(tiempo_actual):
    # Dibujar elementos en la pantalla
    #pantalla.fill((230, 220, 240))
    pantalla.blit(fondo, (0, 0))
    personaje_sre.dibujar(pantalla, tiempo_actual, estado_juego)
    dibujar_hackers()
    dibujar_teclados()
    interfaz.dibujar_vidas(pantalla, personaje_sre.vidas)
    interfaz.dibujar_puntaje(pantalla, puntaje)
    interfaz.dibujar_cronometro(pantalla, tiempo_actual, tiempo_inicio, tiempo_fin)

def obtener_posicion_boss_fin():
    separacion = 15

    personaje_muerto_ancho = personaje_sre.obtener_ancho_muerto()
    personaje_muerto_alto = personaje_sre.obtener_alto_muerto()
    boss_ancho = boss_img.get_width()
    boss_alto = boss_img.get_height()

    boss_x_calculado = personaje_sre.x + personaje_muerto_ancho + separacion

    if boss_x_calculado + boss_ancho > ANCHOPANTALLA:
        boss_x_calculado = personaje_sre.x - boss_ancho - separacion

    boss_y_calculado = personaje_sre.y + personaje_muerto_alto // 2 - boss_alto // 2

    boss_x_calculado = max(0, min(boss_x_calculado, ANCHOPANTALLA - boss_ancho))
    boss_y_calculado = max(0, min(boss_y_calculado, ALTOPANTALLA - boss_alto))

    return boss_x_calculado, boss_y_calculado

def dibujar_pantalla_fin():
    pantalla.blit(fondofin, (0, 0))
    personaje_sre.dibujar(pantalla, tiempo_fin, estado_juego)
    boss_fin_x, boss_fin_y = obtener_posicion_boss_fin()
    boss(boss_fin_x, boss_fin_y)

    interfaz.dibujar_game_over(pantalla, puntaje, tiempo_inicio, tiempo_fin)

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
                personaje_sre.iniciar_movimiento_izquierda()
            if evento.key == pygame.K_RIGHT:
                personaje_sre.iniciar_movimiento_derecha()
            if evento.key == pygame.K_UP:
                personaje_sre.iniciar_movimiento_arriba()
            if evento.key == pygame.K_DOWN:
                personaje_sre.iniciar_movimiento_abajo()
        if estado_juego == "jugando" and evento.type == pygame.KEYUP:
            if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                personaje_sre.detener_movimiento_horizontal()
            if evento.key in (pygame.K_UP, pygame.K_DOWN):
                personaje_sre.detener_movimiento_vertical()

    if estado_juego == "jugando":
        personaje_sre.mover(ANCHOPANTALLA, ALTOPANTALLA)
        actualizar_juego(tiempo_actual)
        dibujar_pantalla_juego(tiempo_actual)
    else: # GAME OVER
        dibujar_pantalla_fin()
        gestionar_sonido_gameover()
        gestionar_huevo_de_pascua()

    pygame.display.update() # Actualizar la pantalla

pygame.quit()
print("Fin del juego")
