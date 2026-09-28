import pygame
import sys
import random

pygame.init()

# CONFIGURACIÓN
TAM = 50
FILAS, COLUMNAS = 11, 15
ANCHO, ALTO = COLUMNAS * TAM, FILAS * TAM
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Bomberman - Bob Esponja")
reloj = pygame.time.Clock()

# COLORES
NEGRO = (15, 15, 15)
BLANCO = (255, 255, 255)
AMARILLO = (255, 225, 0)
ROJO = (230, 40, 40)
NARANJA = (255, 120, 0)
GRIS = (90, 90, 90)
GRIS_CLARO = (150, 150, 150)
VERDE = (40, 220, 70)

# COLOR DE CADA NIVEL
COLORES_NIVEL = [
    (40, 100, 180),    # Nivel 1 - azul
    (30, 150, 70),     # Nivel 2 - verde
    (120, 50, 170)     # Nivel 3 - morado
]

# MAPAS
niveles = [
[
"111111111111111",
"100220000022001",
"101110111011101",
"100000202000001",
"101011111110101",
"100200000002001",
"101011101110101",
"100000202000001",
"101110111011101",
"100000000000001",
"111111111111111"
],
[
"111111111111111",
"102220000022201",
"101110111011101",
"100020202020001",
"101011111110101",
"100000000000001",
"101110111011101",
"102020202020201",
"101011111110101",
"100000000000001",
"111111111111111"
],
[
"111111111111111",
"102222000222201",
"101110111011101",
"102000202000201",
"101011111110101",
"100200000002001",
"101011111110101",
"102000202000201",
"101110111011101",
"102222000222201",
"111111111111111"
]
]

# JUGADOR
nivel = 0
vidas = 3
jugador_x, jugador_y = 1, 1
bombas_max = 1
alcance = 2

mapa = []
enemigos = []
bombas = []
explosiones = []
items = []

game_over = False
victoria = False


def cargar_nivel():
    global mapa, enemigos, bombas, explosiones, items
    global jugador_x, jugador_y

    mapa = [list(fila) for fila in niveles[nivel]]
    enemigos.clear()
    bombas.clear()
    explosiones.clear()
    items.clear()

    jugador_x, jugador_y = 1, 1

    # Más enemigos en cada nivel
    posiciones = [
        (13, 1), (13, 9), (7, 9),
        (11, 5), (3, 9), (9, 3),
        (5, 5), (11, 9)
    ]

    cantidad = 2 + nivel * 2

    for x, y in posiciones[:cantidad]:
        enemigos.append({
            "x": x,
            "y": y,
            "tiempo": 0
        })


def puede_mover(x, y):
    return (
        0 <= x < COLUMNAS and
        0 <= y < FILAS and
        mapa[y][x] == "0"
    )


def poner_bomba():
    if len(bombas) >= bombas_max:
        return

    bombas.append({
        "x": jugador_x,
        "y": jugador_y,
        "tiempo": pygame.time.get_ticks() + 1500
    })


def explotar(bomba):
    posiciones = [(bomba["x"], bomba["y"])]

    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        for d in range(1, alcance + 1):

            x = bomba["x"] + dx * d
            y = bomba["y"] + dy * d

            if mapa[y][x] == "1":
                break

            posiciones.append((x, y))

            if mapa[y][x] == "2":
                mapa[y][x] = "0"
                break

    explosiones.append({
        "posiciones": posiciones,
        "tiempo": pygame.time.get_ticks() + 400
    })


def mover_enemigos():
    ahora = pygame.time.get_ticks()

    for e in enemigos:
        if ahora - e["tiempo"] < 400:
            continue

        e["tiempo"] = ahora

        direcciones = [(1,0), (-1,0), (0,1), (0,-1)]
        random.shuffle(direcciones)

        for dx, dy in direcciones:
            x = e["x"] + dx
            y = e["y"] + dy

            if puede_mover(x, y):
                e["x"], e["y"] = x, y
                break


def en_explosion(x, y):
    return any(
        (x, y) in e["posiciones"]
        for e in explosiones
    )


def dibujar():
    fondo = COLORES_NIVEL[nivel]
    pantalla.fill(NEGRO)

    # MAPA
    for y in range(FILAS):
        for x in range(COLUMNAS):

            rect = pygame.Rect(
                x*TAM, y*TAM, TAM, TAM
            )

            if mapa[y][x] == "1":
                pygame.draw.rect(pantalla, GRIS, rect)
                pygame.draw.rect(pantalla, GRIS_CLARO, rect, 3)

            elif mapa[y][x] == "2":
                pygame.draw.rect(pantalla, (130,70,30), rect)

            else:
                pygame.draw.rect(pantalla, fondo, rect)

            pygame.draw.rect(pantalla, NEGRO, rect, 1)

    # BOMBAS
    for b in bombas:
        pygame.draw.circle(
            pantalla, NEGRO,
            (b["x"]*TAM+25, b["y"]*TAM+25), 17
        )

    # EXPLOSIONES
    for e in explosiones:
        for x, y in e["posiciones"]:
            rect = pygame.Rect(
                x*TAM, y*TAM, TAM, TAM
            )
            pygame.draw.rect(pantalla, NARANJA, rect)
            pygame.draw.circle(
                pantalla, AMARILLO,
                rect.center, 17
            )

    # ENEMIGOS
    for e in enemigos:
        pygame.draw.circle(
            pantalla, ROJO,
            (e["x"]*TAM+25, e["y"]*TAM+25), 18
        )
        pygame.draw.circle(
            pantalla, BLANCO,
            (e["x"]*TAM+18, e["y"]*TAM+19), 5
        )
        pygame.draw.circle(
            pantalla, BLANCO,
            (e["x"]*TAM+32, e["y"]*TAM+19), 5
        )

    # BOB ESPONJA
    try:
        bob = pygame.image.load("bob.png").convert_alpha()
        bob = pygame.transform.scale(bob, (44,44))
        pantalla.blit(
            bob,
            (jugador_x*TAM+3, jugador_y*TAM+3)
        )
    except:
        pygame.draw.rect(
            pantalla, AMARILLO,
            (jugador_x*TAM+3, jugador_y*TAM+3, 44, 44)
        )

    # INFORMACIÓN
    fuente = pygame.font.Font(None, 28)
    texto = fuente.render(
        f"Nivel: {nivel+1}  Vidas: {vidas}  Bombas: {bombas_max}  Fuego: {alcance}",
        True, BLANCO
    )
    pantalla.blit(texto, (8, 5))

    # GAME OVER
    if game_over:
        mostrar_mensaje("GAME OVER", ROJO, "Presiona R para reiniciar")

    # VICTORIA
    if victoria:
        mostrar_mensaje("¡GANASTE!", VERDE, "Completaste los 3 niveles")


def mostrar_mensaje(titulo, color, subtitulo):
    fuente = pygame.font.Font(None, 75)
    texto = fuente.render(titulo, True, color)

    pantalla.blit(
        texto,
        (
            ANCHO//2 - texto.get_width()//2,
            ALTO//2 - 60
        )
    )

    fuente2 = pygame.font.Font(None, 30)
    texto2 = fuente2.render(subtitulo, True, BLANCO)

    pantalla.blit(
        texto2,
        (
            ANCHO//2 - texto2.get_width()//2,
            ALTO//2 + 20
        )
    )


cargar_nivel()

# BUCLE PRINCIPAL
while True:

    reloj.tick(60)

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:

            if game_over or victoria:

                if evento.key == pygame.K_r:
                    nivel = 0
                    vidas = 3
                    bombas_max = 1
                    alcance = 2
                    game_over = victoria = False
                    cargar_nivel()

            else:

                x, y = jugador_x, jugador_y

                if evento.key == pygame.K_LEFT:
                    x -= 1
                elif evento.key == pygame.K_RIGHT:
                    x += 1
                elif evento.key == pygame.K_UP:
                    y -= 1
                elif evento.key == pygame.K_DOWN:
                    y += 1
                elif evento.key == pygame.K_SPACE:
                    poner_bomba()

                if puede_mover(x, y):
                    jugador_x, jugador_y = x, y

    if not game_over and not victoria:

        ahora = pygame.time.get_ticks()

        # Explosión de bombas
        for b in bombas[:]:
            if ahora >= b["tiempo"]:
                explotar(b)
                bombas.remove(b)

        # Quitar explosiones
        for e in explosiones[:]:
            if ahora >= e["tiempo"]:
                explosiones.remove(e)

        mover_enemigos()

        # Eliminar enemigos
        enemigos[:] = [
            e for e in enemigos
            if not en_explosion(e["x"], e["y"])
        ]

        # Jugador golpeado
        golpeado = en_explosion(jugador_x, jugador_y)

        for e in enemigos:
            if e["x"] == jugador_x and e["y"] == jugador_y:
                golpeado = True

        if golpeado:
            vidas -= 1
            jugador_x, jugador_y = 1, 1

            if vidas <= 0:
                game_over = True

        # Siguiente nivel
        if not enemigos:
            if nivel < 2:
                nivel += 1
                cargar_nivel()
            else:
                victoria = True

    dibujar()
    pygame.display.flip()

