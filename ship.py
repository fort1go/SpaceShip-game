import pygame
from Bullets import Bullet, Missile
from os import path
from PowerUp import Boost, Explosion, PowerUp, Shield

img_dir = path.join(path.dirname(__file__), 'images')
sound_dir = path.join(path.dirname(__file__), 'sounds')

WINDOWWIDTH = 480
WINDOWHEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREENYELLOW = (143, 245, 34)
YELLOW = (234, 245, 34)
GREY = (210, 210, 210)
DARKGREY = (93, 94, 94)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
REDORANGE = (245, 103, 32)


class Player(pygame.sprite.Sprite):
    def __init__(self, player_image, bullet_image, missile_image, sprites_list, bullet_list, bullet_sound,
                 missile_sound):
        super().__init__()
        self.image = pygame.transform.scale(player_image, (70, 70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.sprites = sprites_list
        self.rect.centerx = WINDOWWIDTH / 2
        self.rect.bottom = WINDOWHEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.bullet_image = bullet_image
        self.missile_image = missile_image
        self.bullets = bullet_list
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.missile_sound = missile_sound
        self.bullet_sound = bullet_sound
        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.upgrade = 1
        self.upgrade_timer = pygame.time.get_ticks()

    def update(self):
        if self.hidden and (pygame.time.get_ticks() - self.hide_timer > 1500):
            self.hidden = False
            self.rect.centerx = WINDOWWIDTH / 2
            self.rect.bottom = WINDOWHEIGHT - 10
        if self.upgrade >= 2 and pygame.time.get_ticks() - self.upgrade_timer > 4500:
            self.upgrade -= 1
            self.upgrade_timer = pygame.time.get_ticks()
        self.speedx = 0
        self.speedy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.speedx = -9
        if keys[pygame.K_d]:
            self.speedx = +9
        if keys[pygame.K_w]:
            self.speedy = -9
        if keys[pygame.K_s]:
            self.speedy = +9
        if keys[pygame.K_SPACE] and not (self.rect.top > WINDOWHEIGHT):
            self.shoot()
        if self.rect.right > WINDOWWIDTH:
            self.rect.right = WINDOWWIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 200:
            self.rect.top = 200
        if self.rect.bottom > WINDOWHEIGHT - 10 and self.rect.bottom < WINDOWHEIGHT:
            self.rect.bottom = WINDOWHEIGHT - 10
        if self.rect.bottom > WINDOWHEIGHT + 10:
            self.rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT + 100)
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            if self.upgrade == 1:
                bullet = Bullet(self.bullet_image, self.rect.centerx, self.rect.top)
                self.sprites.add(bullet)
                self.bullets.add(bullet)
                self.bullet_sound.play()
            if self.upgrade == 2:
                bullet = Bullet(self.bullet_image, self.rect.centerx, self.rect.top)
                self.sprites.add(bullet)
                self.bullets.add(bullet)
                missile1 = Missile(self.missile_image, self.rect.left, self.rect.centery)
                self.sprites.add(missile1)
                self.bullets.add(missile1)
                self.bullet_sound.play()
                self.missile_sound.play()
            if self.upgrade == 3:
                bullet = Bullet(self.bullet_image, self.rect.centerx, self.rect.top)
                self.sprites.add(bullet)
                self.bullets.add(bullet)
                missile1 = Missile(self.missile_image, self.rect.left, self.rect.centery)
                self.sprites.add(missile1)
                self.bullets.add(missile1)
                missile2 = Missile(self.missile_image, self.rect.right, self.rect.centery)
                self.sprites.add(missile2)
                self.bullets.add(missile2)
                self.bullet_sound.play()
                self.missile_sound.play()

    def upgrade_power(self):
        if self.upgrade >= 3:
            self.upgrade = 3
        elif self.upgrade < 3:
            self.upgrade += 1
        self.upgrade_timer = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT + 100)
        self.hide_timer = pygame.time.get_ticks()
