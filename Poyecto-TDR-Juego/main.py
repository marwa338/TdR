import pygame
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Nave Espacial")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Carga de imágenes
BACKGROUND_IMG = pygame.image.load("fondo.jpg")
SHIP_IMG = pygame.image.load("nave.png")
ASTEROID_IMG = pygame.image.load("asteroide.png")
GEM_IMG = pygame.image.load("gema.png")

# Escalado de imágenes
SHIP_IMG = pygame.transform.scale(SHIP_IMG, (50, 50))
ASTEROID_IMG = pygame.transform.scale(ASTEROID_IMG, (50, 50))
GEM_IMG = pygame.transform.scale(GEM_IMG, (30, 30))

# Carga de sonidos
pygame.mixer.music.load("musica_fondo.mp3")
explosion_sound = pygame.mixer.Sound("explosion.wav")
gem_sound = pygame.mixer.Sound("gem.wav")

# Reproducción de la música de fondo
pygame.mixer.music.play(-1)

# Configuración de la nave
ship_x = WIDTH // 2
ship_y = HEIGHT - 100
ship_speed = 5

# Configuración de asteroides y gemas
asteroids = []
gems = []
ASTEROID_EVENT = pygame.USEREVENT + 1
GEM_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(ASTEROID_EVENT, 1000)
pygame.time.set_timer(GEM_EVENT, 2000)

# Configuración del juego
clock = pygame.time.Clock()
score = 0
running = True

# Función para mostrar el texto
font = pygame.font.Font(pygame.font.get_default_font(), 36)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Función para mostrar la pantalla de inicio
def show_start_screen():
    SCREEN.blit(BACKGROUND_IMG, (0, 0))
    draw_text("Presiona cualquier tecla para comenzar", font, WHITE, SCREEN, WIDTH // 4, HEIGHT // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                waiting = False

# Función para mostrar la pantalla de fin
def show_game_over_screen():
    SCREEN.blit(BACKGROUND_IMG, (0, 0))
    draw_text("GAME OVER", font, WHITE, SCREEN, WIDTH // 3, HEIGHT // 3)
    draw_text(f"Score: {score}", font, WHITE, SCREEN, WIDTH // 3, HEIGHT // 2)
    draw_text("Presiona cualquier tecla para volver a jugar", font, WHITE, SCREEN, WIDTH // 4, HEIGHT // 2 + 50)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                waiting = False

# Mostrar pantalla de inicio
show_start_screen()

# Bucle principal del juego
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == ASTEROID_EVENT:
            asteroid_x = random.randint(0, WIDTH - 50)
            asteroids.append([asteroid_x, -50])
        elif event.type == GEM_EVENT:
            gem_x = random.randint(0, WIDTH - 30)
            gems.append([gem_x, -30])

    # Movimiento de la nave
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ship_x - ship_speed > 0:
        ship_x -= ship_speed
    if keys[pygame.K_RIGHT] and ship_x + ship_speed < WIDTH - 50:
        ship_x += ship_speed

    # Movimiento de asteroides y gemas
    for asteroid in asteroids:
        asteroid[1] += 5
    for gem in gems:
        gem[1] += 5

    # Comprobación de colisiones
    ship_rect = pygame.Rect(ship_x, ship_y, 50, 50)
    for asteroid in asteroids:
        asteroid_rect = pygame.Rect(asteroid[0], asteroid[1], 50, 50)
        if ship_rect.colliderect(asteroid_rect):
            explosion_sound.play()
            running = False
    for gem in gems:
        gem_rect = pygame.Rect(gem[0], gem[1], 30, 30)
        if ship_rect.colliderect(gem_rect):
            gem_sound.play()
            score += 1
            gems.remove(gem)

    # Eliminación de asteroides y gemas fuera de la pantalla
    asteroids = [asteroid for asteroid in asteroids if asteroid[1] < HEIGHT]
    gems = [gem for gem in gems if gem[1] < HEIGHT]

    # Dibujo en la pantalla
    SCREEN.blit(BACKGROUND_IMG, (0, 0))
    SCREEN.blit(SHIP_IMG, (ship_x, ship_y))
    for asteroid in asteroids:
        SCREEN.blit(ASTEROID_IMG, (asteroid[0], asteroid[1]))
    for gem in gems:
        SCREEN.blit(GEM_IMG, (gem[0], gem[1]))
    draw_text(f"Score: {score}", font, WHITE, SCREEN, 10, 10)

    pygame.display.flip()
    clock.tick(30)

# Mostrar pantalla de fin
show_game_over_screen()

pygame.quit()
