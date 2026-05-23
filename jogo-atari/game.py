# game.py — Loop principal do jogo Space Shooter: Skills Edition

import sys
import math
import random
import pygame

from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    BLACK, WHITE, CYAN, YELLOW, RED, GRAY, ORANGE, MAGENTA, GREEN, BLUE, PURPLE,
    GAME_TITLE,
    EXPLOSION_PARTICLE_COUNT, EXPLOSION_PARTICLE_SPEED, EXPLOSION_LIFETIME,
    POWERUP_CHANCE,
    get_spawn_rate, get_asteroid_speed
)
from player import Player
from asteroid import Asteroid
from powerup import PowerUp


class ExplosionParticle:
    def __init__(self, x, y, color=None):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, EXPLOSION_PARTICLE_SPEED)
        self.x, self.y = x, y
        self.vx, self.vy = math.cos(angle) * speed, math.sin(angle) * speed
        self.lifetime = EXPLOSION_LIFETIME + random.randint(-5, 5)
        self.max_lifetime = self.lifetime
        self.size = random.uniform(2, 5)
        self.color = color if color else random.choice([(255, 200, 50), (255, 120, 30), (255, 60, 60)])

    def update(self):
        self.x += self.vx; self.y += self.vy
        self.vx *= 0.96; self.vy *= 0.96
        self.lifetime -= 1; self.size *= 0.95

    def draw(self, screen):
        if self.lifetime <= 0: return
        ratio = self.lifetime / self.max_lifetime
        sz = max(1, int(self.size))
        surf = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, int(220 * ratio)), (sz, sz), sz)
        screen.blit(surf, (self.x - sz, self.y - sz))

    @property
    def alive(self):
        return self.lifetime > 0 and self.size >= 0.5

class Star:
    def __init__(self):
        self.x, self.y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
        self.base_brightness = random.randint(80, 220)
        self.size = random.choice([1, 1, 1, 2, 3])
        self.twinkle_speed, self.twinkle_offset = random.uniform(0.02, 0.08), random.uniform(0, math.pi * 2)
        self.timer = 0
    def update(self): self.timer += 1
    def draw(self, screen):
        twinkle = math.sin(self.timer * self.twinkle_speed + self.twinkle_offset)
        brightness = max(0, min(255, int(self.base_brightness + 35 * twinkle)))
        if self.size <= 1: screen.set_at((self.x, self.y), (brightness, brightness, brightness))
        else: pygame.draw.circle(screen, (brightness, brightness, brightness), (self.x, self.y), self.size)

def draw_hud(screen, font, font_small, player, score):
    hud_bg = pygame.Surface((240, 85), pygame.SRCALPHA)
    hud_bg.fill((0, 0, 0, 120))
    pygame.draw.rect(hud_bg, (0, 255, 255, 60), hud_bg.get_rect(), 1, border_radius=6)
    screen.blit(hud_bg, (10, 10))

    screen.blit(font.render(f"Score: {score}", True, WHITE), (20, 15))
    
    # Desenhar Vidas (Corações/Naves)
    for i in range(player.lives):
        pygame.draw.circle(screen, RED, (30 + i * 25, 55), 7)
        pygame.draw.polygon(screen, RED, [(23+i*25, 55), (37+i*25, 55), (30+i*25, 65)])

    # Barra de Tempo do Power-up
    if player.powerup_type:
        color = BLUE if player.powerup_type == 'triple' else PURPLE
        width = int(200 * (player.powerup_timer / 500))
        pygame.draw.rect(screen, GRAY, (20, 75, 200, 5))
        pygame.draw.rect(screen, color, (20, 75, width, 5))

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()
    
    fonts = {
        'hud': pygame.font.SysFont("Courier", 26, bold=True),
        'large': pygame.font.SysFont("Courier", 64, bold=True),
        'medium': pygame.font.SysFont("Courier", 28, bold=True),
        'popup': pygame.font.SysFont("Courier", 20, bold=True)
    }

    stars = [Star() for _ in range(120)]
    all_sprites, bullets, asteroids, powerups = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()
    
    player = Player()
    all_sprites.add(player)

    score, spawn_timer, game_over, frame_count = 0, 0, False, 0
    explosions, score_popups, shake_intensity = [], [], 0

    while True:
        clock.tick(FPS)
        frame_count += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r: return run_game()
                    if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
                elif event.key == pygame.K_SPACE:
                    for b in player.shoot():
                        bullets.add(b); all_sprites.add(b)

        if not game_over:
            spawn_timer += 1
            if spawn_timer >= get_spawn_rate(score):
                spawn_timer = 0
                ast = Asteroid(score=score)
                asteroids.add(ast); all_sprites.add(ast)

            all_sprites.update()

            # Colisões: Tiros vs Asteroides
            hits = pygame.sprite.groupcollide(bullets, asteroids, True, True)
            for bullet, asts in hits.items():
                for ast in asts:
                    score += 1
                    for _ in range(EXPLOSION_PARTICLE_COUNT):
                        explosions.append(ExplosionParticle(ast.rect.centerx, ast.rect.centery))
                    shake_intensity = 4
                    score_popups.append({'x': ast.rect.centerx, 'y': ast.rect.centery, 'life': 30})
                    
                    # Chance de Drop
                    if random.random() < POWERUP_CHANCE:
                        pu = PowerUp(ast.rect.centerx, ast.rect.centery)
                        powerups.add(pu); all_sprites.add(pu)

            # Colisões: Player vs PowerUps
            pu_hits = pygame.sprite.spritecollide(player, powerups, True)
            for pu in pu_hits:
                player.apply_powerup(pu.type)
                for _ in range(15):
                    explosions.append(ExplosionParticle(pu.rect.centerx, pu.rect.centery, color=pu.color))

            # Colisões: Player vs Asteroides
            if player.invincible_timer == 0:
                if pygame.sprite.spritecollide(player, asteroids, True):
                    player.lives -= 1
                    player.invincible_timer = 90 # 1.5s invencível
                    shake_intensity = 15
                    for _ in range(20):
                        explosions.append(ExplosionParticle(player.rect.centerx, player.rect.centery, color=RED))
                    if player.lives <= 0: game_over = True

            for ast in asteroids:
                if ast.rect.top > SCREEN_HEIGHT:
                    ast.kill() # Remove o asteroide sem perder o jogo

        # Atualizar Efeitos
        for exp in explosions: exp.update()
        explosions = [e for e in explosions if e.alive]
        for p in score_popups: p['y'] -= 1.5; p['life'] -= 1
        score_popups = [p for p in score_popups if p['life'] > 0]
        shake_intensity *= 0.85

        # Desenhar
        screen.fill(BLACK)
        shake_x, shake_y = (random.randint(-int(shake_intensity), int(shake_intensity)), random.randint(-int(shake_intensity), int(shake_intensity))) if shake_intensity > 0.5 else (0,0)
        
        temp_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for s in stars: s.update(); s.draw(temp_surf)
        for a in asteroids: a.draw_glow(temp_surf)
        if not game_over: player.draw_effects(temp_surf)
        for b in bullets: b.draw_trail(temp_surf)
        all_sprites.draw(temp_surf)
        for e in explosions: e.draw(temp_surf)
        
        screen.blit(temp_surf, (shake_x, shake_y))
        draw_hud(screen, fonts['hud'], None, player, score)
        
        if game_over:
            # Tela de Game Over simplificada
            ov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA); ov.fill((0,0,0,180)); screen.blit(ov, (0,0))
            txt = fonts['large'].render("FIM DE JOGO", True, RED)
            screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)))
            stxt = fonts['medium'].render(f"Score Final: {score}", True, WHITE)
            screen.blit(stxt, stxt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20)))

        pygame.display.flip()

if __name__ == "__main__":
    run_game()
