# player.py — Classe da nave do jogador

import math
import random
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    PLAYER_SPEED, PLAYER_WIDTH, PLAYER_HEIGHT,
    CYAN, LIGHT_CYAN, WHITE, INITIAL_LIVES,
    THRUSTER_PARTICLE_COUNT, THRUSTER_LIFETIME,
    POWERUP_DURATION
)
from bullet import Bullet


class ThrusterParticle:
    def __init__(self, x, y):
        self.x = x + random.uniform(-6, 6)
        self.y = y
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(1.5, 3.5)
        self.lifetime = THRUSTER_LIFETIME
        self.max_lifetime = self.lifetime
        self.size = random.uniform(2, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.size *= 0.92

    def draw(self, screen):
        if self.lifetime <= 0: return
        ratio = self.lifetime / self.max_lifetime
        r, g, b = 255, int(255 * ratio), int(60 * ratio)
        surf = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(surf, (r, g, b, int(200 * ratio)), (int(self.size), int(self.size)), int(self.size))
        screen.blit(surf, (self.x - self.size, self.y - self.size))

    @property
    def alive(self): return self.lifetime > 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        self._draw_ship(self.base_image)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20

        self.lives = INITIAL_LIVES
        self.tilt = 0
        self.target_tilt = 0
        self.thruster_particles = []
        self.glow_timer = 0
        
        # Estado de Power-ups
        self.powerup_type = None
        self.powerup_timer = 0
        self.invincible_timer = 0 # Breve invencibilidade ao ser atingido

        # Estado do Dash
        self.dash_timer = 0
        self.dash_cooldown = 0
        self.dash_direction = 0 # -1 esquerda, 1 direita
        self.last_key_left = False
        self.last_key_right = False
        self.last_tap_left_time = 0
        self.last_tap_right_time = 0

    def _draw_ship(self, surface):
        w, h = PLAYER_WIDTH, PLAYER_HEIGHT
        cx = w // 2
        
        # Asas laterais
        left_wing = [(cx, 10), (0, h - 15), (cx - 8, h - 10)]
        right_wing = [(cx, 10), (w, h - 15), (cx + 8, h - 10)]
        pygame.draw.polygon(surface, (0, 150, 200), left_wing)
        pygame.draw.polygon(surface, (0, 150, 200), right_wing)
        
        # Fuselagem central (corpo principal)
        fuselage = [(cx, 0), (cx - 10, h - 8), (cx + 10, h - 8)]
        pygame.draw.polygon(surface, CYAN, fuselage)
        
        # Motores inferiores
        pygame.draw.rect(surface, (100, 100, 100), (cx - 12, h - 8, 8, 6))
        pygame.draw.rect(surface, (100, 100, 100), (cx + 4, h - 8, 8, 6))
        
        # Cabine / Cockpit
        cockpit = [(cx, 15), (cx - 4, 30), (cx, 35), (cx + 4, 30)]
        pygame.draw.polygon(surface, WHITE, cockpit)
        
        # Detalhes de alta tecnologia (linhas)
        pygame.draw.line(surface, LIGHT_CYAN, (cx, 5), (cx, h - 10), 2)
        
        # Contornos gerais
        pygame.draw.polygon(surface, WHITE, fuselage, 1)
        pygame.draw.polygon(surface, LIGHT_CYAN, left_wing, 1)
        pygame.draw.polygon(surface, LIGHT_CYAN, right_wing, 1)

    def update(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        
        # Detecção de Double Tap para Dash (Janela de 250ms)
        if keys[pygame.K_LEFT] and not self.last_key_left:
            if current_time - self.last_tap_left_time < 250 and self.dash_cooldown <= 0:
                self.dash_timer = 12
                self.dash_direction = -1
                self.dash_cooldown = 40
            self.last_tap_left_time = current_time
            
        if keys[pygame.K_RIGHT] and not self.last_key_right:
            if current_time - self.last_tap_right_time < 250 and self.dash_cooldown <= 0:
                self.dash_timer = 12
                self.dash_direction = 1
                self.dash_cooldown = 40
            self.last_tap_right_time = current_time

        self.last_key_left = keys[pygame.K_LEFT]
        self.last_key_right = keys[pygame.K_RIGHT]

        self.target_tilt = 0
        
        # Aplicação do Movimento e Dash
        if self.dash_timer > 0:
            self.rect.x += self.dash_direction * (PLAYER_SPEED * 3)
            self.target_tilt = 20 * self.dash_direction * -1 # Inclinação forte
            self.dash_timer -= 1
            # Mais partículas para visual do dash
            for _ in range(2):
                self.thruster_particles.append(ThrusterParticle(self.rect.centerx, self.rect.centery))
        else:
            if keys[pygame.K_LEFT]:
                self.rect.x -= PLAYER_SPEED
                self.target_tilt = 8
            if keys[pygame.K_RIGHT]:
                self.rect.x += PLAYER_SPEED
                self.target_tilt = -8
            if keys[pygame.K_UP]:
                self.rect.y -= PLAYER_SPEED
            if keys[pygame.K_DOWN]:
                self.rect.y += PLAYER_SPEED
                
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        self.tilt += (self.target_tilt - self.tilt) * 0.2
        if abs(self.tilt) > 0.5:
            center = self.rect.center
            self.image = pygame.transform.rotate(self.base_image, self.tilt)
            self.rect = self.image.get_rect(center=center)
        else:
            self.image = self.base_image.copy()

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT

        # Partículas e timers
        for _ in range(THRUSTER_PARTICLE_COUNT):
            self.thruster_particles.append(ThrusterParticle(self.rect.centerx, self.rect.bottom - 2))
        for p in self.thruster_particles: p.update()
        self.thruster_particles = [p for p in self.thruster_particles if p.alive]
        
        self.glow_timer += 1
        if self.powerup_timer > 0:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0: self.powerup_type = None
            
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

    def draw_effects(self, screen):
        for p in self.thruster_particles: p.draw(screen)
        
        # Glow especial se tiver power-up ou estiver invencível
        color = (0, 255, 255)
        if self.invincible_timer > 0:
            if (self.invincible_timer // 5) % 2 == 0: return # Piscar
        
        if self.powerup_type == 'triple': color = (50, 100, 255)
        elif self.powerup_type == 'spread': color = (180, 50, 255)
            
        glow_alpha = int(30 + 20 * math.sin(self.glow_timer * 0.1))
        glow_surf = pygame.Surface((self.rect.width + 20, self.rect.height + 20), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surf, (*color, glow_alpha), glow_surf.get_rect())
        screen.blit(glow_surf, (self.rect.x - 10, self.rect.y - 10))

    def shoot(self):
        bullets = []
        if self.powerup_type == 'triple':
            # 3 tiros paralelos
            bullets.append(Bullet(self.rect.centerx, self.rect.top))
            bullets.append(Bullet(self.rect.left, self.rect.centery))
            bullets.append(Bullet(self.rect.right, self.rect.centery))
        elif self.powerup_type == 'spread':
            # 3 tiros em leque (ângulos)
            bullets.append(Bullet(self.rect.centerx, self.rect.top, angle=0))
            bullets.append(Bullet(self.rect.centerx, self.rect.top, angle=-25))
            bullets.append(Bullet(self.rect.centerx, self.rect.top, angle=25))
        else:
            # Tiro normal
            bullets.append(Bullet(self.rect.centerx, self.rect.top))
        return bullets

    def apply_powerup(self, powerup_type):
        if powerup_type == 'life':
            self.lives = min(self.lives + 1, 5)
        else:
            self.powerup_type = powerup_type
            self.powerup_timer = POWERUP_DURATION
