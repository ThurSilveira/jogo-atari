# settings.py — Configurações e constantes do jogo

import math

# Dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Frames por segundo
FPS = 60

# Configurações do Jogador
PLAYER_SPEED = 6
BULLET_SPEED = -10
INITIAL_LIVES = 3

# Dificuldade progressiva — asteroides
ASTEROID_BASE_SPEED = 1.5
ASTEROID_MAX_SPEED = 7.0
ASTEROID_SPEED_PER_SCORE = 0.15

ASTEROID_BASE_SPAWN_RATE = 90
ASTEROID_MIN_SPAWN_RATE = 20
ASTEROID_SPAWN_RATE_DECAY = 3

# Power-ups
POWERUP_SPEED = 2
POWERUP_CHANCE = 0.15  # 15% de chance de dropar ao destruir um asteroide
POWERUP_DURATION = 500 # Frames (aprox 8 segundos)

# Tamanho dos objetos
PLAYER_WIDTH = 48
PLAYER_HEIGHT = 56
BULLET_WIDTH = 4
BULLET_HEIGHT = 14
ASTEROID_MIN_RADIUS = 15
ASTEROID_MAX_RADIUS = 35
POWERUP_SIZE = 30

# Cores (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
LIGHT_CYAN = (120, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 160, 40)
RED = (255, 60, 60)
DEEP_RED = (200, 30, 30)
GRAY = (150, 150, 150)
DARK_GRAY = (80, 80, 80)
MAGENTA = (255, 50, 200)
GREEN = (50, 255, 50)
BLUE = (50, 100, 255)
PURPLE = (180, 50, 255)

# Partículas
EXPLOSION_PARTICLE_COUNT = 12
EXPLOSION_PARTICLE_SPEED = 4
EXPLOSION_LIFETIME = 25
THRUSTER_PARTICLE_COUNT = 2
THRUSTER_LIFETIME = 12

# Título da janela
GAME_TITLE = "⭐ Space Shooter: Skills Edition ⭐"


def get_asteroid_speed(score):
    speed = ASTEROID_BASE_SPEED + (score * ASTEROID_SPEED_PER_SCORE)
    return min(speed, ASTEROID_MAX_SPEED)


def get_spawn_rate(score):
    rate = ASTEROID_BASE_SPAWN_RATE - (score * ASTEROID_SPAWN_RATE_DECAY)
    return max(rate, ASTEROID_MIN_SPAWN_RATE)
