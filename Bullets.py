import pygame
from os import path

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

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(bullet_image, (8, 23))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -15

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 35:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, bullet_image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(bullet_image, (8, 23))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = 15

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > WINDOWHEIGHT:
            self.kill()


class Missile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.image = pygame.transform.scale(image, (25, 38))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 35:
            self.kill()