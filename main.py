import pygame, sys, random
from pygame import *
import math
from os import path
from PowerUp import Boost, Explosion, PowerUp, Shield
from Bullets import Missile, EnemyBullet, Bullet
from enemy import EnemyShip, Asteroid
from ship import Player

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


pygame.init()
pygame.mixer.init()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Window')


def draw_text(surface, text, size, x, y, color):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def menu():
    pygame.mixer.music.load(path.join(sound_dir, 'SpaceShooter_Theme.wav'))
    pygame.mixer.music.play(-1)

    background = pygame.image.load('images/stars_bg.jpeg').convert()
    background_rect = background.get_rect()

    DISPLAYSURF.blit(background, background_rect)

    pygame.display.update()

    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                break
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()


def draw_lives(surface, x, y, lives, image):
    for i in range(lives):
        img_rect = image.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surface.blit(image, img_rect)


def shield_bar(surface, player_shield):
    if player_shield > 100:
        player_shield_color = GREEN
        player_shield = 100
    elif player_shield > 75:
        player_shield_color = GREEN
    elif player_shield > 50:
        player_shield_color = YELLOW
    else:
        player_shield_color = RED

    pygame.draw.rect(surface, GREY, (5, 5, 104, 24), 3)
    pygame.draw.rect(surface, player_shield_color, (7, 7, player_shield, 20))


def main():
    background = pygame.image.load('images/stars_bg.jpeg').convert()
    background_rect = background.get_rect()
    planet = pygame.image.load('images/planet.png').convert()
    planet = pygame.transform.scale(planet, (400, 400))
    planet.set_colorkey(BLACK)
    planet_rect = planet.get_rect(center=(70, 70))

    black_bar = pygame.Surface((WINDOWWIDTH, 35))

    player_img = pygame.image.load('images/player.png').convert()
    life_player_img = pygame.transform.scale(player_img, (25, 25))
    life_player_img.set_colorkey(BLACK)
    bullet_img = pygame.image.load('images/laser_red.png').convert()
    enemy_bullet_img = pygame.image.load('images/laser_purple.png').convert()
    missile_img = pygame.image.load('images/missile.png').convert_alpha()
    energy_shield= pygame.image.load('images/energy_shield.png').convert_alpha()
    enemy_img = pygame.image.load('images/spacecraft_enemy.png').convert_alpha()

    asteroid_images = []
    asteroid_list = [
        'asteroid_medium2.png',
        'asteroid_medium1.png',
        'asteroid_medium3.png',
        'asteroid_big1.png',
        'asteroid_tiny.png'
    ]

    for image in asteroid_list:
        asteroid_images.append(pygame.image.load(path.join(img_dir, image)).convert_alpha())

    explosion_anim = {}
    explosion_anim['large'] = []
    explosion_anim['small'] = []
    explosion_anim['ship'] = []
    for i in range(5):
        filename = 'explosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
        image_lg = pygame.transform.scale(img, (75, 75))
        explosion_anim['large'].append(image_lg)
        image_sm = pygame.transform.scale(img, (45, 45))
        explosion_anim['small'].append(image_sm)

    for i in range(10):
        filename = 'ship_explosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(BLACK)
        image_player = pygame.transform.scale(img, (100, 100))
        explosion_anim['ship'].append(image_player)

    boost_anim = {}
    boost_anim['boost'] = []
    for i in range(8):
        filename = 'boost0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
        boost_img = pygame.transform.scale(img, (50, 50))
        boost_anim['boost'].append(boost_img)

    powerup_images = {}
    powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield.png')).convert_alpha()
    powerup_images['shield'] = pygame.transform.scale(powerup_images['shield'], (35, 35))
    powerup_images['missile'] = pygame.image.load(path.join(img_dir, 'missile_powerup.png')).convert_alpha()
    powerup_images['missile'] = pygame.transform.scale(powerup_images['missile'], (45, 45))

    bullet_sound = pygame.mixer.Sound(path.join(sound_dir, 'laser.wav'))
    bullet_sound.set_volume(0.25)
    enemy_bullet_sound = pygame.mixer.Sound(path.join(sound_dir, 'enemy_laser.wav'))
    missile_sound = pygame.mixer.Sound(path.join(sound_dir, 'rocket.ogg'))
    missile_sound.set_volume(0.15)
    large_expl = pygame.mixer.Sound(path.join(sound_dir, 'large_explosion.wav'))
    small_expl = pygame.mixer.Sound(path.join(sound_dir, 'small_explosion.wav'))
    ship_expl = pygame.mixer.Sound(path.join(sound_dir, 'explosion_ship.wav'))
    ship_expl.set_volume(0.4)

    running = True
    show_menu = True
    while running:
        if show_menu:
            menu()
            pygame.time.delay(1500)

            pygame.mixer.music.fadeout(1500)

            pygame.mixer.music.load(path.join(sound_dir, 'SpaceShooter_Theme2.mp3'))
            pygame.mixer.music.play(-1)

            show_menu = False

            all_active_sprites = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            enemy_bullets = pygame.sprite.Group()
            asteroids = pygame.sprite.Group()
            powerups = pygame.sprite.Group()
            enemy_ships = pygame.sprite.Group()

            player = Player(player_img, bullet_img, missile_img, all_active_sprites,
                            bullets, bullet_sound, missile_sound)
            shield = Shield(energy_shield, player.rect.center, player)
            all_active_sprites.add(player, shield)

            for i in range(2):
                enemy_ship = EnemyShip(enemy_img, enemy_bullet_img, all_active_sprites,
                                       enemy_bullets, enemy_bullet_sound, boost_anim)
                all_active_sprites.add(enemy_ship)
                enemy_ships.add(enemy_ship)

            for i in range(7):
                new_asteroid = Asteroid(asteroid_images, all_active_sprites, asteroids)
                all_active_sprites.add(new_asteroid)
                asteroids.add(new_asteroid)
            score = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()

        all_active_sprites.update()

        asteroid_hit = pygame.sprite.groupcollide(asteroids, bullets, True, pygame.sprite.collide_circle)

        for hit in asteroid_hit:
            score += 50 - hit.radius
            large_expl.play()
            large_expl.set_volume(0.1)
            expl = Explosion(hit.rect.center, 'large', explosion_anim)
            all_active_sprites.add(expl)
            if random.random() > 0.92:
                powerup = PowerUp(hit.rect.center, powerup_images)
                all_active_sprites.add(powerup)
                powerups.add(powerup)
            new_asteroid = Asteroid(asteroid_images, all_active_sprites, asteroids)
            all_active_sprites.add(new_asteroid)
            asteroids.add(new_asteroid)

        enemy_hit = pygame.sprite.groupcollide(enemy_ships, bullets, True, pygame.sprite.collide_circle)
        for hit in enemy_hit:
            score += 75
            ship_expl.play()
            ship_expl.set_volume(0.1)
            expl = Explosion(hit.rect.center, 'ship', explosion_anim)
            all_active_sprites.add(expl)
            if random.random() > 0.85:
                powerup = PowerUp(hit.rect.center, powerup_images)
                all_active_sprites.add(powerup)
                powerups.add(powerup)
            new_ship = EnemyShip(enemy_img, enemy_bullet_img, all_active_sprites, enemy_bullets,
                                 enemy_bullet_sound, boost_anim)
            all_active_sprites.add(new_ship)
            enemy_ships.add(new_ship)
        player_hit_by_bullet = pygame.sprite.spritecollide(player, enemy_bullets, True)

        for hit in player_hit_by_bullet:
            player.shield -= 5
            if player.shield <= 0:
                ship_expl.play()
                expl_ship = Explosion(player.rect.center, 'ship', explosion_anim)
                all_active_sprites.add(expl_ship)
                player.hide()
                player.lives -= 1
                player.shield = 100

        player_hit = pygame.sprite.spritecollide(player, asteroids, True)

        for hit in player_hit:
            player.shield -= random.randint(10, 25)
            small_expl.play()
            small_expl.set_volume(0.1)
            expl = Explosion(hit.rect.center, 'small', explosion_anim)
            all_active_sprites.add(expl)
            new_asteroid = Asteroid(asteroid_images, all_active_sprites, asteroids)
            all_active_sprites.add(new_asteroid)
            asteroids.add(new_asteroid)
            if player.shield <= 0:
                ship_expl.play()
                expl_ship = Explosion(player.rect.center, 'ship', explosion_anim)
                all_active_sprites.add(expl_ship)
                player.hide()
                player.lives -= 1
                player.shield = 100

        player_hit_by_ship = pygame.sprite.spritecollide(player, enemy_ships, True)

        for hit in player_hit_by_ship:
            player.shield -= 35
            ship_expl.play()
            ship_expl.set_volume(0.1)
            expl = Explosion(hit.rect.center, 'ship', explosion_anim)
            all_active_sprites.add(expl)
            new_ship = EnemyShip(enemy_img, enemy_bullet_img, all_active_sprites, enemy_bullets,
                                 enemy_bullet_sound, boost_anim)
            all_active_sprites.add(new_ship)
            enemy_ships.add(new_ship)
            if player.shield <= 0:
                ship_expl.play()
                expl_ship = Explosion(player.rect.center, 'ship', explosion_anim)
                all_active_sprites.add(expl_ship)
                player.hide()
                player.lives -= 1
                player.shield = 100

        powerup_hit = pygame.sprite.spritecollide(player, powerups, True)

        for hit in powerup_hit:
            if hit.type == 'shield':
                score += 100
                player.shield += 20
                if player.shield >= 100:
                    player.shield = 100
            if hit.type == 'missile':
                score += 50
                player.upgrade_power()

        if player.lives == 0 and not expl_ship.alive():
            pygame.mixer.music.stop()
            show_menu = True

        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(background, background_rect)
        DISPLAYSURF.blit(planet, planet_rect)

        all_active_sprites.draw(DISPLAYSURF)
        DISPLAYSURF.blit(black_bar, (0, 0))
        pygame.draw.rect(DISPLAYSURF, GREY, (0, 0, WINDOWWIDTH, 35), 3)
        shield_bar(DISPLAYSURF, player.shield)

        draw_text(DISPLAYSURF, "SCORE", 12, WINDOWWIDTH / 2, 2, WHITE)
        draw_text(DISPLAYSURF, str(score), 25, WINDOWWIDTH / 2, 12, WHITE)

        draw_lives(DISPLAYSURF, WINDOWWIDTH - 100, 5, player.lives, life_player_img)

        pygame.time.Clock().tick(60)
        pygame.display.flip()


if __name__ == "__main__":
    main()
