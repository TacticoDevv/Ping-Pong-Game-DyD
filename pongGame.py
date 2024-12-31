import pygame
import random
import pygame
import numpy as np

# Inicializar Pygame
pygame.init()

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Dimensiones de la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption('Pong Game with Levels')

# Velocidad del juego
reloj = pygame.time.Clock()

# Fuentes
fuente = pygame.font.SysFont(None, 35)

# Sonidos
#rebote_sonido = pygame.mixer.Sound("rebote.wav")
#punto_sonido = pygame.mixer.Sound("rebote.wav")

# Clase de la raqueta
class Raqueta(pygame.sprite.Sprite):
    def __init__(self, color, ancho, alto):
        super().__init__()
        self.image = pygame.Surface([ancho, alto])
        self.image.fill(NEGRO)
        self.image.set_colorkey(NEGRO)
        pygame.draw.rect(self.image, color, [0, 0, ancho, alto])
        self.rect = self.image.get_rect()
        self.velocidad = 0

    def mover_arriba(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
            self.rect.y = 0

    def mover_abajo(self, pixels):
        self.rect.y += pixels
        if self.rect.y > ALTO_PANTALLA - self.rect.height:
            self.rect.y = ALTO_PANTALLA - self.rect.height

# Clase de la pelota
class Pelota(pygame.sprite.Sprite):
    def __init__(self, color, ancho, alto):
        super().__init__()
        self.image = pygame.Surface([ancho, alto])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.velocidad = [3, 3]  # Reducimos la velocidad de la pelota

    def update(self):
        self.rect.x += self.velocidad[0]
        self.rect.y += self.velocidad[1]

        if self.rect.y <= 0 or self.rect.y >= ALTO_PANTALLA - self.rect.height:
            self.velocidad[1] = -self.velocidad[1]
            

# Función para mostrar la puntuación
def mostrar_puntuacion(p1, p2):
    texto = fuente.render(f"Jugador 1: {p1}  Jugador 2: {p2}", True, BLANCO)
    pantalla.blit(texto, [ANCHO_PANTALLA // 4, 10])

# Función para mostrar el menú de selección de nivel
def mostrar_menu():
    pantalla.fill(NEGRO)
    texto = fuente.render("Seleccione Nivel: 1 (Facil), 2 (Medio), 3 (Difícil), 4 (Experto), 5 (Insano)", True, BLANCO)
    pantalla.blit(texto, [ANCHO_PANTALLA // 10, ALTO_PANTALLA // 2])
    pygame.display.flip()

    seleccionando = True
    while seleccionando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return 5
                elif evento.key == pygame.K_2:
                    return 10
                elif evento.key == pygame.K_3:
                    return 15
                elif evento.key == pygame.K_4:
                    return 20
                elif evento.key == pygame.K_5:
                    return 25

pygame.mixer.init()
rebote_sound = pygame.mixer.Sound('rebote.wav')

punto_sonido = pygame.mixer.Sound("/home/tactico/Documentos/Ping Pong Game DyD/myenv/Ring.wav")


# Configuración inicial del juego
def gameLoop():
    velocidad_raqueta_2 = mostrar_menu()
    
    raqueta_1 = Raqueta(BLANCO, 10, 100)
    raqueta_1.rect.x = 30
    raqueta_1.rect.y = (ALTO_PANTALLA // 2) - 50

    raqueta_2 = Raqueta(BLANCO, 10, 100)
    raqueta_2.rect.x = ANCHO_PANTALLA - 40
    raqueta_2.rect.y = (ALTO_PANTALLA // 2) - 50

    pelota = Pelota(BLANCO, 10, 10)
    pelota.rect.x = ANCHO_PANTALLA // 2
    pelota.rect.y = ALTO_PANTALLA // 2

    todas_las_sprites = pygame.sprite.Group()
    todas_las_sprites.add(raqueta_1)
    todas_las_sprites.add(raqueta_2)
    todas_las_sprites.add(pelota)
    # ... resto del código ...

    pelota = Pelota(BLANCO, 10, 10)
    pelota.rect.x = ANCHO_PANTALLA // 2
    pelota.rect.y = ALTO_PANTALLA // 2

    todas_las_sprites = pygame.sprite.Group()
    todas_las_sprites.add(raqueta_1)
    todas_las_sprites.add(raqueta_2)
    todas_las_sprites.add(pelota)

    puntuacion_1 = 0
    puntuacion_2 = 0

    game_over = False

    while not game_over:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            raqueta_1.mover_arriba(7)
        if keys[pygame.K_s]:
            raqueta_1.mover_abajo(7)

        # Mover la raqueta del oponente automáticamente
        if pelota.rect.y < raqueta_2.rect.y:
            raqueta_2.mover_arriba(velocidad_raqueta_2)
        if pelota.rect.y > raqueta_2.rect.y + raqueta_2.rect.height:
            raqueta_2.mover_abajo(velocidad_raqueta_2)

        todas_las_sprites.update()

        if (pelota.rect.left <= raqueta_1.rect.right + 5 and 
            pelota.rect.right >= raqueta_1.rect.left - 5 and 
            pelota.rect.top <= raqueta_1.rect.bottom + 5 and 
            pelota.rect.bottom >= raqueta_1.rect.top - 5):
            pelota.velocidad[0] = -pelota.velocidad[0]
            rebote_sound.play()

        if (pelota.rect.left <= raqueta_2.rect.right + 5 and 
            pelota.rect.right >= raqueta_2.rect.left - 5 and 
            pelota.rect.top <= raqueta_2.rect.bottom + 5 and 
            pelota.rect.bottom >= raqueta_2.rect.top - 5):
            pelota.velocidad[0] = -pelota.velocidad[0]
            rebote_sound.play()


        if pelota.rect.x <= 0:
            puntuacion_2 += 1
            punto_sonido.play() # type: ignore
            pelota.rect.x = ANCHO_PANTALLA // 2
            pelota.rect.y = ALTO_PANTALLA // 2
            pelota.velocidad = [6, 6]
        if pelota.rect.x >= ANCHO_PANTALLA - pelota.rect.width:
            puntuacion_1 += 1
            punto_sonido.play() # type: ignore
            pelota.rect.x = ANCHO_PANTALLA // 2
            pelota.rect.y = ALTO_PANTALLA // 2
            pelota.velocidad = [-6, 6]

        pantalla.fill(NEGRO)
        pygame.draw.line(pantalla, BLANCO, [ANCHO_PANTALLA // 2, 0], [ANCHO_PANTALLA // 2, ALTO_PANTALLA], 5)

        todas_las_sprites.draw(pantalla)

        mostrar_puntuacion(puntuacion_1, puntuacion_2)

        pygame.display.flip()

        reloj.tick(60)

    pygame.quit()

gameLoop()
