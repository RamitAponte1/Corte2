import pygame
import sys
import random
import math
from array import array

pygame.init()

# ================= CONFIGURACIÓN =================
TAM = 50
FILAS, COLUMNAS = 11, 15
ANCHO, ALTO = COLUMNAS * TAM, FILAS * TAM

pantalla = pygame.display.set_mode(
    (ANCHO, ALTO),
    pygame.SCALED | pygame.RESIZABLE
)

pygame.display.set_caption("Bomberman - Bob Esponja")
reloj = pygame.time.Clock()

F_PEQ = pygame.font.Font(None, 28)
F_PANEL = pygame.font.Font(None, 30)
F_GRANDE = pygame.font.Font(None, 70)
F_MEDIA = pygame.font.Font(None, 40)
F_TEXTO = pygame.font.Font(None, 30)

# ================= COLORES =================
NEGRO = (15, 15, 15)
BLANCO = (255, 255, 255)
AMARILLO = (255, 225, 0)
AMARILLO_CLARO = (255, 245, 120)
ROJO = (230, 40, 40)
NARANJA = (255, 120, 0)
GRIS = (90, 90, 90)
GRIS_CLARO = (150, 150, 150)
VERDE = (40, 220, 70)
MORADO = (170, 60, 220)
CAFE = (130, 70, 30)
CELESTE = (50, 210, 240)

COLORES_NIVEL = [
    (40, 100, 180),
    (30, 150, 70),
    (120, 50, 170),
    (170, 90, 40),
    (20, 130, 140),
    (150, 40, 70),
    (60, 60, 150),
    (30, 30, 60),
]

TOTAL_NIVELES = len(COLORES_NIVEL)


# ================= MAPAS =================
def generar_mapa(n):
    rng = random.Random(n * 7 + 3)

    densidad = min(0.30 + 0.04 * n, 0.58)

    seguras = {
        (1, 1),
        (2, 1),
        (1, 2)
    }

    filas = []

    for y in range(FILAS):
        fila = ""

        for x in range(COLUMNAS):

            if x in (0, COLUMNAS - 1) or y in (0, FILAS - 1):
                fila += "1"

            elif x % 2 == 0 and y % 2 == 0:
                fila += "1"

            elif (x, y) in seguras:
                fila += "0"

            else:
                fila += "2" if rng.random() < densidad else "0"

        filas.append(fila)

    return filas


# ================= SONIDOS =================
SONIDO_ACTIVO = True
silenciado = False

try:

    pygame.mixer.init(
        frequency=44100,
        size=-16,
        channels=1
    )

    FRECUENCIA_MUSICA = 44100

    # -------------------------------------------------
    # Crear sonidos del juego
    # -------------------------------------------------
    def crear_sonido(frecuencia, duracion, volumen=0.3, final=None):

        fm = 44100
        cantidad = int(fm * duracion)

        datos = array("h")
        fase = 0.0

        for i in range(cantidad):

            if final is None:
                f = frecuencia
            else:
                f = frecuencia + (
                    (final - frecuencia) * i / cantidad
                )

            fase += 2 * math.pi * f / fm

            fade = min(
                1,
                i / 500,
                (cantidad - i) / 500
            )

            datos.append(
                int(
                    32767
                    * volumen
                    * math.sin(fase)
                    * fade
                )
            )

        return pygame.mixer.Sound(buffer=datos)


    sonido_bomba = crear_sonido(
        200,
        0.12,
        0.25,
        120
    )

    sonido_explosion = crear_sonido(
        160,
        0.35,
        0.35,
        40
    )

    sonido_item = crear_sonido(
        500,
        0.18,
        0.25,
        1000
    )

    sonido_dano = crear_sonido(
        300,
        0.30,
        0.30,
        80
    )

    sonido_enemigo = crear_sonido(
        400,
        0.12,
        0.20,
        200
    )

    sonido_nivel = crear_sonido(
        600,
        0.30,
        0.25,
        1200
    )

    sonido_victoria = crear_sonido(
        700,
        0.70,
        0.30,
        1500
    )


    # =================================================
    # MÚSICA DE FONDO
    # =================================================

    def crear_nota(frecuencia, duracion, volumen=0.08):

        cantidad = int(FRECUENCIA_MUSICA * duracion)

        datos = array("h")
        fase = 0.0

        for i in range(cantidad):

            fase += (
                2
                * math.pi
                * frecuencia
                / FRECUENCIA_MUSICA
            )

            # Pequeño fade para evitar golpes de sonido
            fade = min(
                1,
                i / 300,
                (cantidad - i) / 300
            )

            # Onda cuadrada suave estilo retro
            onda = 1 if math.sin(fase) >= 0 else -1

            datos.append(
                int(
                    32767
                    * volumen
                    * onda
                    * fade
                )
            )

        return datos


    # Melodía estilo videojuego retro
    melodia = [

        # Primera parte
        (523, 0.16),
        (659, 0.16),
        (784, 0.16),
        (659, 0.16),

        (523, 0.16),
        (392, 0.16),
        (440, 0.16),
        (523, 0.30),

        # Segunda parte
        (587, 0.16),
        (698, 0.16),
        (880, 0.25),
        (698, 0.16),

        (659, 0.16),
        (523, 0.16),
        (440, 0.16),
        (392, 0.30),

        # Tercera parte
        (523, 0.16),
        (659, 0.16),
        (784, 0.16),
        (988, 0.25),

        (880, 0.16),
        (784, 0.16),
        (659, 0.16),
        (523, 0.30),

        # Cuarta parte
        (440, 0.16),
        (523, 0.16),
        (659, 0.16),
        (784, 0.25),

        (659, 0.16),
        (523, 0.16),
        (440, 0.16),
        (392, 0.35)
    ]


    datos_musica = array("h")

    for frecuencia, duracion in melodia:

        datos_nota = crear_nota(
            frecuencia,
            duracion,
            0.045
        )

        datos_musica.extend(datos_nota)

        # Pequeño espacio entre notas
        silencio = array(
            "h",
            [0] * int(FRECUENCIA_MUSICA * 0.025)
        )

        datos_musica.extend(silencio)


    musica_fondo = pygame.mixer.Sound(
        buffer=datos_musica
    )

    # Volumen general de la música
    musica_fondo.set_volume(0.55)

    # Canal exclusivo para la música
    canal_musica = pygame.mixer.Channel(7)

    musica_activa = True


except Exception:

    SONIDO_ACTIVO = False

    sonido_bomba = None
    sonido_explosion = None
    sonido_item = None
    sonido_dano = None
    sonido_enemigo = None
    sonido_nivel = None
    sonido_victoria = None

    musica_fondo = None
    canal_musica = None
    musica_activa = False


# ================= CONTROL DE SONIDO =================
def reproducir(sonido):

    if SONIDO_ACTIVO and not silenciado and sonido:

        try:
            sonido.play()

        except Exception:
            pass


def actualizar_musica():

    if not canal_musica or not musica_fondo:
        return

    if silenciado or not SONIDO_ACTIVO:

        if canal_musica.get_busy():
            canal_musica.stop()

        return

    if not canal_musica.get_busy():

        canal_musica.play(
            musica_fondo,
            loops=-1
        )


# ================= ÍCONOS =================
def icono_corazon(x, y, s=20, color=ROJO):

    r = s // 4

    pygame.draw.circle(
        pantalla,
        color,
        (x + r, y + r),
        r
    )

    pygame.draw.circle(
        pantalla,
        color,
        (x + 3 * r, y + r),
        r
    )

    pygame.draw.polygon(
        pantalla,
        color,
        [
            (x, y + r + 1),
            (x + 4 * r, y + r + 1),
            (x + 2 * r, y + 4 * r + 2)
        ]
    )


def icono_bomba(cx, cy, r=9):

    pygame.draw.circle(
        pantalla,
        NEGRO,
        (cx, cy + 2),
        r
    )

    pygame.draw.circle(
        pantalla,
        BLANCO,
        (cx, cy + 2),
        r,
        2
    )

    pygame.draw.line(
        pantalla,
        AMARILLO,
        (cx + r // 2, cy - r // 2),
        (cx + r, cy - r),
        2
    )

    pygame.draw.circle(
        pantalla,
        NARANJA,
        (cx + r, cy - r),
        3
    )


def icono_fuego(cx, cy, k=1.0):

    p = [
        (0, -10),
        (7, 0),
        (5, 9),
        (-5, 9),
        (-7, 0)
    ]

    pygame.draw.polygon(
        pantalla,
        NARANJA,
        [
            (cx + a * k, cy + b * k)
            for a, b in p
        ]
    )

    q = [
        (0, -2),
        (4, 4),
        (3, 9),
        (-3, 9),
        (-4, 4)
    ]

    pygame.draw.polygon(
        pantalla,
        AMARILLO,
        [
            (cx + a * k, cy + b * k)
            for a, b in q
        ]
    )


def icono_estrella(cx, cy, r=10, color=AMARILLO):

    pts = []

    for i in range(10):

        ang = -math.pi / 2 + i * math.pi / 5

        rad = r if i % 2 == 0 else r * 0.45

        pts.append(
            (
                cx + rad * math.cos(ang),
                cy + rad * math.sin(ang)
            )
        )

    pygame.draw.polygon(
        pantalla,
        color,
        pts
    )


def icono_sonido(x, y, activo):

    color = BLANCO if activo else GRIS_CLARO

    pygame.draw.polygon(
        pantalla,
        color,
        [
            (x, y + 5),
            (x + 5, y + 5),
            (x + 11, y),
            (x + 11, y + 16),
            (x + 5, y + 11),
            (x, y + 11)
        ]
    )

    if activo:

        pygame.draw.arc(
            pantalla,
            color,
            (x + 8, y + 3, 8, 10),
            -1.0,
            1.0,
            2
        )

        pygame.draw.arc(
            pantalla,
            color,
            (x + 8, y, 14, 16),
            -1.0,
            1.0,
            2
        )

    else:

        pygame.draw.line(
            pantalla,
            ROJO,
            (x + 14, y + 3),
            (x + 22, y + 13),
            3
        )

        pygame.draw.line(
            pantalla,
            ROJO,
            (x + 22, y + 3),
            (x + 14, y + 13),
            3
        )


# ================= ESTADO =================
nivel = 0
vidas = 3
puntuacion = 0

jugador_x = 1
jugador_y = 1

bombas_max = 1
alcance = 2

velocidad_enemigo = 450
invulnerable_hasta = 0

mapa = []
enemigos = []
bombas = []
explosiones = []
items = []

game_over = False
victoria = False
pausa = False
inicio = True


# ================= IMAGEN BOB =================
try:

    IMG_BOB = pygame.transform.scale(
        pygame.image.load("bob.png").convert_alpha(),
        (44, 44)
    )

except Exception:

    IMG_BOB = None


# ================= NIVEL =================
def cargar_nivel():

    global mapa
    global jugador_x
    global jugador_y
    global velocidad_enemigo

    mapa = [
        list(f)
        for f in generar_mapa(nivel)
    ]

    enemigos.clear()
    bombas.clear()
    explosiones.clear()
    items.clear()

    jugador_x = 1
    jugador_y = 1

    velocidad_enemigo = max(
        200,
        450 - nivel * 35
    )

    libres = [
        (x, y)
        for y in range(FILAS)
        for x in range(COLUMNAS)

        if mapa[y][x] == "0"
        and abs(x - 1) + abs(y - 1) >= 8
    ]

    random.shuffle(libres)

    cantidad = min(
        2 + nivel,
        9,
        len(libres)
    )

    for i in range(cantidad):

        x, y = libres[i]

        tipo = "normal"

        if nivel >= 1 and i % 3 == 0:
            tipo = "rapido"

        if nivel >= 3 and i % 4 == 1:
            tipo = "cazador"

        enemigos.append(
            {
                "x": x,
                "y": y,
                "tiempo": pygame.time.get_ticks(),
                "tipo": tipo
            }
        )


# ================= MOVIMIENTO =================
def puede_mover(x, y):

    return (
        0 <= x < COLUMNAS
        and 0 <= y < FILAS
        and mapa[y][x] == "0"
    )


def hay_bomba(x, y):

    return any(
        b["x"] == x and b["y"] == y
        for b in bombas
    )


# ================= BOMBA =================
def poner_bomba():

    if len(bombas) >= bombas_max:
        return

    if hay_bomba(jugador_x, jugador_y):
        return

    bombas.append(
        {
            "x": jugador_x,
            "y": jugador_y,
            "tiempo": pygame.time.get_ticks() + 1500
        }
    )

    reproducir(sonido_bomba)


# ================= EXPLOSIÓN =================
def explotar(bomba):

    posiciones = [
        (bomba["x"], bomba["y"])
    ]

    for dx, dy in [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]:

        for d in range(1, alcance + 1):

            x = bomba["x"] + dx * d
            y = bomba["y"] + dy * d

            if not (
                0 <= x < COLUMNAS
                and 0 <= y < FILAS
            ):
                break

            if mapa[y][x] == "1":
                break

            posiciones.append(
                (x, y)
            )

            if mapa[y][x] == "2":

                mapa[y][x] = "0"

                if random.random() < 0.2:

                    items.append(
                        {
                            "x": x,
                            "y": y,
                            "tipo": random.choice(
                                [
                                    "bomba",
                                    "fuego",
                                    "vida"
                                ]
                            )
                        }
                    )

                break

    explosiones.append(
        {
            "posiciones": posiciones,
            "tiempo": pygame.time.get_ticks() + 500
        }
    )

    reproducir(sonido_explosion)


def en_explosion(x, y):

    return any(
        (x, y) in e["posiciones"]
        for e in explosiones
    )


# ================= ENEMIGOS =================
def mover_enemigos():

    ahora = pygame.time.get_ticks()

    for e in enemigos:

        vel = velocidad_enemigo

        if e["tipo"] == "rapido":
            vel -= 120

        if ahora - e["tiempo"] < vel:
            continue

        e["tiempo"] = ahora

        dirs = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        random.shuffle(dirs)

        if (
            e["tipo"] == "cazador"
            and random.random() < 0.6
        ):

            dirs.sort(
                key=lambda d:
                abs(
                    e["x"] + d[0] - jugador_x
                )
                +
                abs(
                    e["y"] + d[1] - jugador_y
                )
            )

        for dx, dy in dirs:

            x = e["x"] + dx
            y = e["y"] + dy

            if (
                puede_mover(x, y)
                and not hay_bomba(x, y)
            ):

                e["x"] = x
                e["y"] = y

                break


# ================= ITEMS =================
def recoger_items():

    global bombas_max
    global alcance
    global vidas
    global puntuacion

    for item in items[:]:

        if (
            item["x"] == jugador_x
            and item["y"] == jugador_y
        ):

            if item["tipo"] == "bomba":

                bombas_max += 1
                puntuacion += 100

            elif item["tipo"] == "fuego":

                alcance += 1
                puntuacion += 150

            else:

                vidas += 1
                puntuacion += 300

            reproducir(sonido_item)

            items.remove(item)


# ================= DIBUJAR ITEMS =================
def dibujar_items():

    for it in items:

        cx = it["x"] * TAM + TAM // 2
        cy = it["y"] * TAM + TAM // 2

        pygame.draw.circle(
            pantalla,
            BLANCO,
            (cx, cy),
            19
        )

        pygame.draw.circle(
            pantalla,
            NEGRO,
            (cx, cy),
            19,
            2
        )

        if it["tipo"] == "bomba":

            icono_bomba(
                cx,
                cy,
                10
            )

        elif it["tipo"] == "fuego":

            icono_fuego(
                cx,
                cy,
                1.2
            )

        else:

            icono_corazon(
                cx - 10,
                cy - 9,
                20
            )


# ================= DIBUJAR JUGADOR =================
def dibujar_jugador():

    ahora = pygame.time.get_ticks()

    if (
        ahora < invulnerable_hasta
        and ahora // 100 % 2 == 0
    ):
        return

    px = jugador_x * TAM
    py = jugador_y * TAM

    if IMG_BOB:

        pantalla.blit(
            IMG_BOB,
            (px + 3, py + 3)
        )

        return

    pygame.draw.rect(
        pantalla,
        AMARILLO,
        (px + 5, py + 5, 40, 40)
    )

    for ox in (17, 33):

        pygame.draw.circle(
            pantalla,
            BLANCO,
            (px + ox, py + 17),
            6
        )

        pygame.draw.circle(
            pantalla,
            NEGRO,
            (px + ox, py + 17),
            2
        )

    pygame.draw.arc(
        pantalla,
        NEGRO,
        (px + 14, py + 22, 22, 16),
        math.pi,
        2 * math.pi,
        2
    )


# ================= DIBUJAR ENEMIGOS =================
def dibujar_enemigos():

    colores = {
        "normal": (ROJO, 18),
        "rapido": (MORADO, 20),
        "cazador": ((20, 160, 80), 19)
    }

    for e in enemigos:

        cx = e["x"] * TAM + 25
        cy = e["y"] * TAM + 25

        color, radio = colores[e["tipo"]]

        pygame.draw.circle(
            pantalla,
            color,
            (cx, cy),
            radio
        )

        for ox in (-7, 7):

            pygame.draw.circle(
                pantalla,
                BLANCO,
                (cx + ox, cy - 5),
                5
            )

            pygame.draw.circle(
                pantalla,
                NEGRO,
                (cx + ox, cy - 5),
                2
            )


# ================= PANEL =================
def panel():

    pygame.draw.rect(
        pantalla,
        NEGRO,
        (0, 0, ANCHO, 34)
    )

    x = 8

    pantalla.blit(
        F_PANEL.render(
            f"Nivel {nivel + 1}/{TOTAL_NIVELES}",
            True,
            BLANCO
        ),
        (x, 9)
    )

    x = 150

    icono_corazon(
        x,
        8,
        20
    )

    pantalla.blit(
        F_PANEL.render(
            f"x{vidas}",
            True,
            BLANCO
        ),
        (x + 26, 9)
    )

    x = 225

    icono_bomba(
        x + 8,
        17,
        9
    )

    pantalla.blit(
        F_PANEL.render(
            f"x{bombas_max}",
            True,
            BLANCO
        ),
        (x + 24, 9)
    )

    x = 300

    icono_fuego(
        x + 8,
        17,
        1.0
    )

    pantalla.blit(
        F_PANEL.render(
            f"x{alcance}",
            True,
            BLANCO
        ),
        (x + 24, 9)
    )

    x = 375

    icono_estrella(
        x + 8,
        17,
        10
    )

    pantalla.blit(
        F_PANEL.render(
            str(puntuacion),
            True,
            BLANCO
        ),
        (x + 24, 9)
    )

    icono_sonido(
        ANCHO - 32,
        9,
        SONIDO_ACTIVO and not silenciado
    )


# ================= MENSAJES =================
def mostrar_mensaje(
    titulo,
    color,
    subtitulo
):

    sombra = pygame.Surface(
        (ANCHO, ALTO),
        pygame.SRCALPHA
    )

    sombra.fill(
        (0, 0, 0, 150)
    )

    pantalla.blit(
        sombra,
        (0, 0)
    )

    t = F_GRANDE.render(
        titulo,
        True,
        color
    )

    pantalla.blit(
        t,
        (
            ANCHO // 2
            - t.get_width() // 2,
            ALTO // 2 - 70
        )
    )

    t2 = F_PEQ.render(
        subtitulo,
        True,
        BLANCO
    )

    pantalla.blit(
        t2,
        (
            ANCHO // 2
            - t2.get_width() // 2,
            ALTO // 2 + 15
        )
    )


# ================= DIBUJAR JUEGO =================
def dibujar():

    fondo = COLORES_NIVEL[nivel]

    pantalla.fill(NEGRO)

    for y in range(FILAS):

        for x in range(COLUMNAS):

            rect = pygame.Rect(
                x * TAM,
                y * TAM,
                TAM,
                TAM
            )

            c = mapa[y][x]

            if c == "1":

                pygame.draw.rect(
                    pantalla,
                    GRIS,
                    rect
                )

                pygame.draw.rect(
                    pantalla,
                    GRIS_CLARO,
                    rect,
                    3
                )

            elif c == "2":

                pygame.draw.rect(
                    pantalla,
                    CAFE,
                    rect
                )

                pygame.draw.rect(
                    pantalla,
                    (170, 100, 50),
                    rect,
                    3
                )

            else:

                pygame.draw.rect(
                    pantalla,
                    fondo,
                    rect
                )

            pygame.draw.rect(
                pantalla,
                NEGRO,
                rect,
                1
            )

    dibujar_items()

    # Bombas
    for b in bombas:

        cx = b["x"] * TAM + 25
        cy = b["y"] * TAM + 25

        pygame.draw.circle(
            pantalla,
            NEGRO,
            (cx, cy),
            17
        )

        pygame.draw.line(
            pantalla,
            BLANCO,
            (cx + 8, cy - 12),
            (cx + 15, cy - 20),
            3
        )

    # Explosiones
    for e in explosiones:

        for x, y in e["posiciones"]:

            rect = pygame.Rect(
                x * TAM,
                y * TAM,
                TAM,
                TAM
            )

            pygame.draw.rect(
                pantalla,
                NARANJA,
                rect
            )

            pygame.draw.circle(
                pantalla,
                AMARILLO_CLARO,
                rect.center,
                19
            )

            pygame.draw.circle(
                pantalla,
                AMARILLO,
                rect.center,
                12
            )

    dibujar_enemigos()
    dibujar_jugador()
    panel()

    if pausa:

        mostrar_mensaje(
            "PAUSA",
            CELESTE,
            "Presiona P para continuar"
        )

    if game_over:

        mostrar_mensaje(
            "GAME OVER",
            ROJO,
            f"Puntuación: {puntuacion} - Presiona R"
        )

    if victoria:

        mostrar_mensaje(
            "¡GANASTE!",
            VERDE,
            f"¡Completaste los {TOTAL_NIVELES} niveles!  Puntos: {puntuacion}"
        )


# ================= PANTALLA INICIO =================
def dibujar_inicio():

    pantalla.fill(
        COLORES_NIVEL[0]
    )

    for _ in range(15):

        pygame.draw.circle(
            pantalla,
            (60, 130, 210),
            (
                random.randint(0, ANCHO),
                random.randint(0, ALTO)
            ),
            random.randint(5, 15)
        )

    t = F_GRANDE.render(
        "BOMBERMAN",
        True,
        AMARILLO
    )

    pantalla.blit(
        t,
        (
            ANCHO // 2
            - t.get_width() // 2,
            90
        )
    )

    s = F_MEDIA.render(
        "BOB ESPONJA",
        True,
        BLANCO
    )

    pantalla.blit(
        s,
        (
            ANCHO // 2
            - s.get_width() // 2,
            165
        )
    )

    lineas = [

        "Flechas = Mover   |   ESPACIO = Bomba",

        "P = Pausar   |   M = Sonido on/off",

        "",

        "Destruye bloques y elimina a todos los enemigos",

        f"¡Completa los {TOTAL_NIVELES} niveles!",

        "",

        "Presiona ENTER para comenzar"
    ]

    y = 240

    for l in lineas:

        r = F_TEXTO.render(
            l,
            True,
            BLANCO
        )

        pantalla.blit(
            r,
            (
                ANCHO // 2
                - r.get_width() // 2,
                y
            )
        )

        y += 30


# ================= INICIAR =================
cargar_nivel()

# ================= BUCLE PRINCIPAL =================
while True:

    reloj.tick(60)

    # Música de fondo
    actualizar_musica()

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:

            # Pantalla completa
            if evento.key == pygame.K_F11:

                pygame.display.toggle_fullscreen()

                continue

            # Sonido ON/OFF
            if evento.key == pygame.K_m:

                silenciado = not silenciado

                continue

            # Pantalla de inicio
            if inicio:

                if evento.key == pygame.K_RETURN:

                    inicio = False

                continue

            # Reiniciar después de perder o ganar
            if game_over or victoria:

                if evento.key == pygame.K_r:

                    nivel = 0
                    vidas = 3
                    puntuacion = 0

                    bombas_max = 1
                    alcance = 2

                    game_over = False
                    victoria = False

                    cargar_nivel()

                continue

            # Pausa
            if evento.key == pygame.K_p:

                pausa = not pausa

                continue

            if pausa:
                continue

            # Movimiento
            x = jugador_x
            y = jugador_y

            if evento.key == pygame.K_LEFT:

                x -= 1

            elif evento.key == pygame.K_RIGHT:

                x += 1

            elif evento.key == pygame.K_UP:

                y -= 1

            elif evento.key == pygame.K_DOWN:

                y += 1

            # Bomba
            elif evento.key == pygame.K_SPACE:

                poner_bomba()

            # Comprobar movimiento
            if (
                (x, y) !=
                (jugador_x, jugador_y)
                and puede_mover(x, y)
                and not hay_bomba(x, y)
            ):

                jugador_x = x
                jugador_y = y


    # ================= ACTUALIZAR JUEGO =================
    if (
        not inicio
        and not game_over
        and not victoria
        and not pausa
    ):

        ahora = pygame.time.get_ticks()

        # Bombas
        for b in bombas[:]:

            if ahora >= b["tiempo"]:

                explotar(b)

                bombas.remove(b)


        # Bombas que explotan por reacción
        for b in bombas[:]:

            if en_explosion(
                b["x"],
                b["y"]
            ):

                explotar(b)

                bombas.remove(b)


        # Eliminar explosiones viejas
        for e in explosiones[:]:

            if ahora >= e["tiempo"]:

                explosiones.remove(e)


        # Mover enemigos
        mover_enemigos()


        # Eliminar enemigos alcanzados
        for e in enemigos[:]:

            if en_explosion(
                e["x"],
                e["y"]
            ):

                enemigos.remove(e)

                puntuacion += 250

                reproducir(
                    sonido_enemigo
                )


        # Recoger objetos
        recoger_items()


        # Comprobar daño
        golpeado = (
            en_explosion(
                jugador_x,
                jugador_y
            )
            or
            any(
                e["x"] == jugador_x
                and e["y"] == jugador_y
                for e in enemigos
            )
        )


        if (
            golpeado
            and ahora >= invulnerable_hasta
        ):

            vidas -= 1

            reproducir(
                sonido_dano
            )

            invulnerable_hasta = (
                ahora + 2000
            )

            jugador_x = 1
            jugador_y = 1

            if vidas <= 0:

                game_over = True


        # Pasar de nivel
        if not enemigos and not game_over:

            if nivel < TOTAL_NIVELES - 1:

                nivel += 1

                puntuacion += 500

                reproducir(
                    sonido_nivel
                )

                cargar_nivel()

            else:

                victoria = True

                reproducir(
                    sonido_victoria
                )


    # ================= DIBUJAR =================
    if inicio:

        dibujar_inicio()

    else:

        dibujar()


    pygame.display.flip()