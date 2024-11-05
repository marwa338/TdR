import pygame
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nave vs Asteroides")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_BLUE = (0, 0, 128)
BRIGHT_BLUE = (0, 128, 255)
RED = (255, 0, 0)

# Carga de imágenes y escalado
BACKGROUND_IMG = pygame.image.load("fondo.jpg")
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (WIDTH, HEIGHT))
SHIP1_IMG = pygame.image.load("nave1.png")  # Imagen de la primera nave
SHIP1_IMG = pygame.transform.scale(SHIP1_IMG, (50, 50))
SHIP2_IMG = pygame.image.load("nave2.png")  # Imagen de la segunda nave
SHIP2_IMG = pygame.transform.scale(SHIP2_IMG, (50, 50))
ASTEROID_IMG = pygame.image.load("asteroide.png")
ASTEROID_IMG = pygame.transform.scale(ASTEROID_IMG, (50, 50))
GEM_IMG = pygame.image.load("gema.png")
GEM_IMG = pygame.transform.scale(GEM_IMG, (30, 30))

# Carga de sonidos y ajuste de volumen
pygame.mixer.music.load("musica_fondo.mp3")
pygame.mixer.music.set_volume(0.2)  # Ajuste del volumen de la música
pygame.mixer.music.play(-1)
explosion_sound = pygame.mixer.Sound("explosion.wav")
gem_sound = pygame.mixer.Sound("gem.wav")

# Configuración de las naves
ship_x = WIDTH // 2 - 100
ship_y = HEIGHT - 100
ship_speed = 5

ship2_x = WIDTH // 2 + 100  # Segunda nave
ship2_y = HEIGHT - 100
ship2_speed = 5

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
lives1 = 3
lives2 = 3
running = True
game_over = False

# Fuente personalizada y tamaño
font = pygame.font.Font("freesansbold.ttf", 36)  # Usando una fuente más estilizada
button_font = pygame.font.Font("freesansbold.ttf", 48)
title_font = pygame.font.Font("freesansbold.ttf", 72)  # Fuente más grande para el título

# Función para mostrar el texto
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))  # Centrado del texto
    surface.blit(textobj, textrect)

# Función para dibujar botones estilizados
def draw_button(text, font, color, surface, x, y, width, height, border_radius=10):
    button_rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
    pygame.draw.rect(surface, color, button_rect, border_radius=border_radius)
    draw_text(text, font, BLACK, surface, x, y)  # Centrar texto dentro del botón
    return button_rect

# Función para mostrar el botón de inicio
def show_start_screen():
    SCREEN.blit(BACKGROUND_IMG, (0, 0))
    draw_text("Naus en acció", title_font, WHITE, SCREEN, WIDTH // 2, HEIGHT // 3)  # Título
    play_button = draw_button("Play", button_font, BRIGHT_BLUE, SCREEN, WIDTH // 2, HEIGHT // 2, 200, 100)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    waiting = False

# Función para mostrar el botón de volver a jugar
def show_game_over_screen():
    SCREEN.blit(BACKGROUND_IMG, (0, 0))
    draw_text("GAME OVER", font, WHITE, SCREEN, WIDTH // 2, HEIGHT // 3)
    draw_text(f"Score: {score}", font, WHITE, SCREEN, WIDTH // 2, HEIGHT // 2)

    retry_button = draw_button("Tornar a jugar", button_font, BRIGHT_BLUE, SCREEN, WIDTH // 2, HEIGHT // 2 + 100, 300, 100)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(event.pos):
                    waiting = False

# Bucle principal del juego
def game_loop():
    global running, score, lives1, lives2, asteroids, gems, ship_x, ship_y, ship2_x, ship2_y

    # Reiniciar variables
    score = 0
    lives1 = 3
    lives2 = 3
    asteroids = []
    gems = []
    ship_x = WIDTH // 2 - 100
    ship_y = HEIGHT - 100
    ship2_x = WIDTH // 2 + 100
    ship2_y = HEIGHT - 100

    running = True
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

        # Movimiento de la nave 1 (flechas)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and ship_x - ship_speed > 0:
            ship_x -= ship_speed
        if keys[pygame.K_RIGHT] and ship_x + ship_speed < WIDTH - 50:
            ship_x += ship_speed
        if keys[pygame.K_UP] and ship_y - ship_speed > 0:
            ship_y -= ship_speed
        if keys[pygame.K_DOWN] and ship_y + ship_speed < HEIGHT - 50:
            ship_y += ship_speed

        # Movimiento de la nave 2 (WASD)
        if keys[pygame.K_a] and ship2_x - ship2_speed > 0:
            ship2_x -= ship2_speed
        if keys[pygame.K_d] and ship2_x + ship2_speed < WIDTH - 50:
            ship2_x += ship2_speed
        if keys[pygame.K_w] and ship2_y - ship2_speed > 0:
            ship2_y -= ship2_speed
        if keys[pygame.K_s] and ship2_y + ship2_speed < HEIGHT - 50:
            ship2_y += ship2_speed

        # Movimiento de asteroides y gemas
        for asteroid in asteroids:
            asteroid[1] += 5
        for gem in gems:
            gem[1] += 5

        # Comprobación de colisiones para nave 1
        ship_rect = pygame.Rect(ship_x, ship_y, 50, 50)
        for asteroid in asteroids:
            asteroid_rect = pygame.Rect(asteroid[0], asteroid[1], 50, 50)
            if ship_rect.colliderect(asteroid_rect):
                explosion_sound.play()
                lives1 -= 1
                asteroids.remove(asteroid)
                if lives1 == 0:
                    running = False

        for gem in gems:
            gem_rect = pygame.Rect(gem[0], gem[1], 30, 30)
            if ship_rect.colliderect(gem_rect):
                gem_sound.play()
                score += 1
                gems.remove(gem)

        # Comprobación de colisiones para nave 2
        ship2_rect = pygame.Rect(ship2_x, ship2_y, 50, 50)
        for asteroid in asteroids:
            asteroid_rect = pygame.Rect(asteroid[0], asteroid[1], 50, 50)
            if ship2_rect.colliderect(asteroid_rect):
                explosion_sound.play()
                lives2 -= 1
                asteroids.remove(asteroid)
                if lives2 == 0:
                    running = False

        for gem in gems:
            gem_rect = pygame.Rect(gem[0], gem[1], 30, 30)
            if ship2_rect.colliderect(gem_rect):
                gem_sound.play()
                score += 1
                gems.remove(gem)

        # Dibujar fondo
        SCREEN.blit(BACKGROUND_IMG, (0, 0))

        # Dibujar naves
        SCREEN.blit(SHIP1_IMG, (ship_x, ship_y))
        SCREEN.blit(SHIP2_IMG, (ship2_x, ship2_y))

        # Dibujar asteroides y gemas
        for asteroid in asteroids:
            SCREEN.blit(ASTEROID_IMG, (asteroid[0], asteroid[1]))
        for gem in gems:
            SCREEN.blit(GEM_IMG, (gem[0], gem[1]))

        # Mostrar puntuación y vidas
        draw_text(f"Score: {score}", font, WHITE, SCREEN, 100, 50)
        draw_text(f"Lives 1: {lives1}", font, WHITE, SCREEN, 100, 100)
        draw_text(f"Lives 2: {lives2}", font, WHITE, SCREEN, WIDTH - 100, 100)

        pygame.display.flip()
        clock.tick(60)

# Mostrar la pantalla de inicio
show_start_screen()

# Bucle principal
while True:
    game_loop()
    show_game_over_screen()

pygame.quit()








