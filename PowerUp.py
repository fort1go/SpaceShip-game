import pygame, random

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

class Boost(pygame.sprite.Sprite):
    def __init__(self, center, b_type, boost_anim):
        super().__init__()
        self.b_type = b_type
        self.boost_anim = boost_anim
        self.image = boost_anim[self.b_type][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 35

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.frame_rate:
            self.last_update = current_time
            self.frame += 1
            if self.frame == len(self.boost_anim[self.b_type]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.boost_anim[self.b_type][self.frame]
                self.rect = self.image.get_rect()
                self.rect.midtop = center


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, ex_type, explosion_anim):
        super().__init__()
        self.ex_type = ex_type
        self.explosion_anim = explosion_anim
        self.image = explosion_anim[self.ex_type][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.frame_rate:
            self.last_update = current_time
            self.frame += 1
            if self.frame == len(self.explosion_anim[self.ex_type]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.ex_type][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center, powerup_images):
        super().__init__()
        self.type = random.choice(['shield', 'missile'])
        self.image = powerup_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 6

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > WINDOWHEIGHT + 10:
            self.kill()


class Shield(pygame.sprite.Sprite):
    def __init__(self, image, center, player):
        super().__init__()
        self.image = pygame.transform.scale(image, (85, 85))
        self.center = center
        self.rect = self.image.get_rect(center=(self.center))
        self.player = player

    def update(self):
        self.rect.centerx = self.player.rect.centerx
        self.rect.centery = self.player.rect.centery

        if self.player.shield <= 30:
            self.rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT + 115)
        elif self.player.shield > 30:
            self.rect.centerx = self.player.rect.centerx
            self.rect.centery = self.player.rect.centery