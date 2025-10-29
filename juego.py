import pygame
import random
import threading
import time

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego de Evasión ")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 200, 255)
RED = (255, 60, 60)
BACKGROUND = (20, 20, 40)


font = pygame.font.SysFont("Arial", 30)


player_size = 50
player_x = 400





player_y = 500
player_speed = 6

enemies = []
enemy_size = 40
enemy_speed = 10
spawn_delay = 0.3
max_enemies = 20


score = 0
vidas = 3
running = True
invulnerable = False  


mutex = threading.Lock()
semaforo = threading.Semaphore(max_enemies)


def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_size, player_size))

def draw_enemy(x, y):
    pygame.draw.rect(screen, RED, (x, y, enemy_size, enemy_size))

def generar_enemigos():
    global enemies
    while running:
        semaforo.acquire()
        with mutex:
            enemies.append([random.randint(0, 800 - enemy_size), 0])
        time.sleep(spawn_delay)


def mover_enemigos():
    global enemies, score, running
    while running:
        with mutex:
            for enemy in enemies[:]:
                enemy[1] += enemy_speed
                if enemy[1] > 600:
                    enemies.remove(enemy)
                    score += 1
                    semaforo.release()
        time.sleep(0.03)


t1 = threading.Thread(target=generar_enemigos, daemon=True)
t2 = threading.Thread(target=mover_enemigos, daemon=True)
t1.start()
t2.start()
while running:
    screen.fill(BACKGROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < 800 - player_size:
        player_x += player_speed


    with mutex:
        for enemy in enemies:
            draw_enemy(enemy[0], enemy[1])
            if not invulnerable:
            
                if (player_x < enemy[0] + enemy_size and
                    player_x + player_size > enemy[0] and
                    player_y < enemy[1] + enemy_size and
                    player_y + player_size > enemy[1]):
                    vidas -= 1
                    invulnerable = True
                    player_x = 400
                    player_y = 500
                    enemies.clear()  
                    if vidas <= 0:
                        running = False
                    else:
                
                        pygame.display.update()
                        time.sleep(1)
                        invulnerable = False
                    break  

    # Dibujar jugador y texto
    draw_player(player_x, player_y)
    score_text = font.render(f"Puntos: {score}", True, WHITE)
    vidas_text = font.render(f"Vidas: {vidas}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(vidas_text, (10, 40))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
print(f"Juego terminado. Puntaje final: {score}")
