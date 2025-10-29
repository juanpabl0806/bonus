# bonus
#  Juego de Evasión con Hilos, Mutex y Semáforos (Python + Pygame)

Este proyecto implementa un pequeño **juego de evasión** programado en **Python** utilizando **Pygame**, **hilos (threads)**, **mutex (bloqueos)** y **semaforización** para coordinar la creación y movimiento de enemigos de forma segura y controlada.

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
´´´

-pygame: biblioteca para manejar gráficos y eventos del juego.

-random: genera posiciones aleatorias para los enemigos.

-threading: permite ejecutar tareas en paralelo (crear y mover enemigos).

-time: gestiona pausas entre eventos (por ejemplo, tiempo entre enemigos).
