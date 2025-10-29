# bonus
#  Juego de Evasión con Hilos, Mutex y Semáforos (Python + Pygame)

Este proyecto implementa un pequeño **juego de evasión** programado en **Python** utilizando **Pygame**, **hilos (threads)**, **mutex (bloqueos)** y **semaforización** para coordinar la creación y movimiento de enemigos de forma segura y controlada.
<img width="1002" height="790" alt="image" src="https://github.com/user-attachments/assets/38622e1d-2f3a-4eb2-bb8d-ce5e6cc7ee7e" />

---

##  Descripción general

El jugador controla un cuadrado azul que debe **evitar chocar con los enemigos rojos** que caen desde la parte superior de la pantalla.  
Cada vez que un enemigo alcanza la parte inferior sin colisionar, el jugador gana puntos.  
Si el jugador colisiona con un enemigo, **pierde una vida** (tiene 3 en total).  
Cuando se pierden todas las vidas, el juego termina.

El objetivo es **sobrevivir el mayor tiempo posible** y acumular la mayor cantidad de puntos.

---

##  Estructura del juego

### 1. Importación y configuración inicial

```python
import pygame
import random
import threading
import time
```
-pygame: biblioteca para manejar gráficos y eventos del juego.

-random: genera posiciones aleatorias para los enemigos.

-threading: permite ejecutar tareas en paralelo (crear y mover enemigos).

-time: gestiona pausas entre eventos (por ejemplo, tiempo entre enemigos).

---

### 2. Ventana del juego

```python
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego de Evasión")
```
Se crea una ventana de 800x600 píxeles con el título del juego.
También se inicializa el reloj del juego (clock) para controlar los FPS.

---

### 3. Colores y fuentes
```python
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 200, 255)
RED = (255, 60, 60)
BACKGROUND = (20, 20, 40)
font = pygame.font.SysFont("Arial", 30)
```
Se definen los colores en formato RGB y la fuente para mostrar texto (puntuación y vidas).

---

### 4. Parámetros del jugador y enemigos
```python
player_size = 50
player_x = 400
player_y = 500
player_speed = 6

enemy_size = 40
enemy_speed = 10
spawn_delay = 0.3
max_enemies = 20
```
-El jugador es un cuadrado azul controlado con las flechas izquierda/derecha.

-Los enemigos son cuadrados rojos que caen desde arriba.

-spawn_delay controla cada cuánto se genera un nuevo enemigo.

-max_enemies limita la cantidad máxima de enemigos activos a la vez.

---

### 5. Variables globales del juego
```python
score = 0
vidas = 3
running = True
invulnerable = False
```
-score: cantidad de puntos ganados.

-vidas: número de vidas restantes (empieza con 3).

-running: controla el ciclo principal del juego.

-invulnerable: evita perder múltiples vidas instantáneamente tras un choque.

---

### 6. Sincronización con Mutex y Semáforo
```python
mutex = threading.Lock()
semaforo = threading.Semaphore(max_enemies)
```
-Mutex (threading.Lock())

Evita que varios hilos modifiquen la lista enemies al mismo tiempo.
Solo un hilo puede acceder a ella mientras el mutex esté bloqueado.

-Semáforo (threading.Semaphore())

Controla cuántos enemigos pueden existir simultáneamente.
Cada vez que se genera un enemigo, el semáforo resta 1 (acquire()),
y cuando un enemigo desaparece, suma 1 (release()).

Esto asegura que nunca existan más de max_enemies enemigos activos.

---

### 7. Funciones de dibujo
```python
def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_size, player_size))

def draw_enemy(x, y):
    pygame.draw.rect(screen, RED, (x, y, enemy_size, enemy_size))
```
Dibujan el jugador y los enemigos como cuadrados en pantalla.

---

### 8. Generación de enemigos (hilo 1)
```python
def generar_enemigos():
    global enemies
    while running:
        semaforo.acquire()
        with mutex:
            enemies.append([random.randint(0, 800 - enemy_size), 0])
        time.sleep(spawn_delay)

```
-Cada enemigo se genera en una posición X aleatoria.

-Usa el mutex para evitar conflictos al agregar enemigos.

-Usa el semaforo para no superar el límite de enemigos.

-time.sleep(spawn_delay) controla el intervalo entre spawns.

---

### 9. Movimiento de enemigos (hilo 2)
```python
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

```
-Mueve cada enemigo hacia abajo (incrementando su coordenada Y).

-Si un enemigo sale de la pantalla, se elimina y el jugador gana 1 punto.

-Usa mutex y semaforo para sincronizar la modificación de la lista.

---

### 10. Hilos en ejecución
```python
t1 = threading.Thread(target=generar_enemigos, daemon=True)
t2 = threading.Thread(target=mover_enemigos, daemon=True)
t1.start()
t2.start()
```
Se crean dos hilos:

-t1: genera enemigos.

-t2: los mueve y elimina.

Ambos corren en paralelo al bucle principal del juego.

---

### 11. Bucle principal del juego
Controla el movimiento del jugador, las colisiones, y el renderizado:
```python
while running:
    screen.fill(BACKGROUND)
    ...
    draw_player(player_x, player_y)
    ...
    pygame.display.update()
```
Controles:

-(←) Mover a la izquierda.

-(→) Mover a la derecha.

Colisiones:

Cuando un enemigo toca al jugador:

-Se resta una vida.

-Se activa invulnerable para dar un segundo de recuperación.

-Si las vidas llegan a 0, el juego termina.

---

### 12. Textos y puntuación
```python
score_text = font.render(f"Puntos: {score}", True, WHITE)
vidas_text = font.render(f"Vidas: {vidas}", True, WHITE)
screen.blit(score_text, (10, 10))
screen.blit(vidas_text, (10, 40))
```
Muestra el puntaje y las vidas en pantalla durante el juego.

---

### 13. Final del juego
```python
pygame.quit()
print(f"Juego terminado. Puntaje final: {score}")
```
Cuando vidas <= 0, el juego se cierra y se imprime el puntaje final en consola.
