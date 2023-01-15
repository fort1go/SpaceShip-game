import pygame, random
from os import path
from Bullets import EnemyBullet
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

class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, enemy_image, bullet_image, sprites_list, bullet_list, bullet_sound, boost_anim):
        super().__init__()
        self.image = pygame.transform.scale(enemy_image, (60, 60))
        self.rect = self.image.get_rect()
        self.sprites = sprites_list
        self.boost_anim = boost_anim
        self.rect.centerx = random.randrange(90, WINDOWWIDTH - 90)
        self.rect.bottom = random.randrange(-150, -20)
        self.bullet_image = bullet_image
        self.bullet_sound = bullet_sound
        self.bullets = bullet_list
        self.shoot_delay = 500
        self.last_shot = pygame.time.get_ticks()
        self.num_of_shots = 2
        self.speedy = 30

    def update(self):
        if self.rect.bottom > 50 and self.rect.bottom < 130:
            for i in range(self.num_of_shots):
                self.shoot()
        if self.rect.bottom <= 120:
            self.rect.bottom += 4
        if self.rect.bottom > 120 and self.rect.bottom < 140:
            self.rect.bottom += 1
        if self.rect.bottom >= 140:
            self.divebomb()
        if (self.rect.top > WINDOWHEIGHT):
            self.rect.centerx = random.randrange(50, WINDOWWIDTH - 50)
            self.rect.y = random.randrange(-200, -50)

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            bullet = EnemyBullet(self.bullet_image, self.rect.centerx, self.rect.bottom)
            self.sprites.add(bullet)
            self.bullets.add(bullet)
            self.bullet_sound.play()
            self.bullet_sound.set_volume(0.2)

    def divebomb(self):
        boost = Boost(self.rect.center, 'boost', self.boost_anim)
        self.sprites.add(boost)
        self.rect.bottom += self.speedy


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, asteroid_img, all_sprites, asteroid_sprites):
        super().__init__()
        self.image_orig = random.choice(asteroid_img)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .90 / 2)
        self.rect.x = random.randrange(-25, WINDOWWIDTH + 25)
        self.rect.y = random.randrange(-200, -100)
        self.speedy = random.randrange(5, 12)
        self.speedx = random.randrange(-2, 2)
        self.angle = 0
        self.rotation_speed = random.randrange(-7, 7)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if (self.rect.top > WINDOWHEIGHT + 10) or (self.rect.left < -self.rect.width) or (
                self.rect.right > WINDOWWIDTH + self.rect.width):
            self.rect.x = random.randrange(0, WINDOWWIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -20)
            self.speedy = random.randrange(3, 10)

    def rotate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > 50:
            self.last_update = current_time
            self.angle = (self.angle + self.rotation_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.angle)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center