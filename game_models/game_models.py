import pygame
from random import randint
from pygame import mixer


# ship - корабль и огонь
class Ship(pygame.sprite.Sprite):
    def __init__(self, window_width, window_height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load('image/ship.png'), (250, 250))
        self.image.set_colorkey('WHITE')
        self.rect = self.image.get_rect()
        self.rect.x = window_width / 2 - 180
        self.rect.y = window_height - window_height / 2
        self.speed = 5
        self.window_width = window_width
        self.window_height = window_height

        self.last = pygame.time.get_ticks()
        self.last_green = pygame.time.get_ticks()
        self.cooldown = 500
        self.green_cooldown = self.cooldown / 4

        self.ship_check = True

        self.sound_blue = mixer.Sound('sound/blue_gun.mp3')
        self.sound_blue.set_volume(0.11)
        self.sound_green = mixer.Sound('sound/green_gun.mp3')

        self.sound_crush = mixer.Sound('sound/explosion.wav')
        self.sound_crush.set_volume(0.3)

    def check(self):
        if self.ship_check:
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(pygame.image.load('image/ship.png'), (250, 250))
            self.image.set_colorkey('WHITE')
        else:
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(pygame.image.load('image/boom.png'), (250, 250))
            self.image.set_colorkey('WHITE')

    def fire(self, bullets, bullets_green, sound_check):
        self.now = pygame.time.get_ticks()
        self.now_green = pygame.time.get_ticks()
        if self.now - self.last >= self.cooldown:
            self.last = self.now
            bullet = Gun(self)
            bullets.add(bullet)
            if sound_check == 'вкл':
                self.sound_blue.play()

        if self.now_green - self.last_green >= self.green_cooldown:
            bullet_green = GreenGun(self)
            bullets_green.add(bullet_green)
            self.last_green = self.now_green

            bullet_green_2 = GreenGun(self)
            bullet_green_2.rect.x += 195
            bullets_green.add(bullet_green_2)
            if sound_check == 'вкл':
                self.sound_green.play()

    def update(self):
        keys = pygame.key.get_pressed()
        if self.ship_check:
            if keys[pygame.K_a]:
                if self.rect.x > 0 and self.ship_check == True:
                    self.rect.x -= self.speed
            elif keys[pygame.K_d]:
                if self.rect.x < self.window_width - 250 and self.ship_check == True:
                    self.rect.x += self.speed
            if keys[pygame.K_w]:
                if self.rect.y > -10 and self.ship_check == True:
                    self.rect.y -= self.speed
            elif keys[pygame.K_s]:
                if self.rect.y < self.window_height - 250 and self.ship_check == True:
                    self.rect.y += self.speed


# оружие
class Gun(pygame.sprite.Sprite):
    def __init__(self, ship):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('image/snaryad.png'), (30, 50))
        self.image.set_colorkey('WHITE')
        self.rect = self.image.get_rect()
        self.rect.x = ship.rect.x + 112
        self.rect.y = ship.rect.y
        self.speed = 15

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -50:
            self.kill()


# вторичное оружие
class GreenGun(pygame.sprite.Sprite):
    def __init__(self, ship):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('image/greengun.png'), (15, 30))
        self.image.set_colorkey('WHITE')
        self.rect = self.image.get_rect()
        self.rect.x = ship.rect.x + 20
        self.rect.y = ship.rect.y
        self.speed = 25

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -50:
            self.kill()


# астероиды small
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, window_width, window_height, asteroid_group):
        pygame.sprite.Sprite.__init__(self)
        self.change_view('image/asteroid_small.png', 'WHITE', 64, 64)
        self.rotate_image = self.image
        self.window_width = window_width
        self.window_height = window_height
        self.rect = self.image.get_rect()
        self.rect.x = randint(0 + 150, self.window_width - 150)
        self.rect.y = 0
        self.speed = 2
        self.angle = 0
        self.asteroid_group = asteroid_group

        self.is_boss = False

    def spawn_asteroid(self):
        self.asteroid = Asteroid(self.window_width, self.window_height, self.asteroid_group)
        self.rect.x = randint(0 + 150, self.window_width - 150)
        self.rect.y = 0
        self.asteroid_group.add(self.asteroid)

    def change_view(self, image, color, xscale=10, yscale=10):
        self.image = pygame.transform.scale(pygame.image.load(image), (xscale, yscale))
        self.image.set_colorkey(color)

    def update(self, asteroid_check):
        self.rect.y += self.speed
        self.image = pygame.transform.rotate(self.rotate_image, self.angle)
        self.image.set_colorkey('WHITE')
        self.angle += 1
        self.rect.x += randint(0, 2)
        if self.rect.y > self.window_height:
            self.spawn_asteroid()
            self.kill()
        if not asteroid_check:
            self.spawn_asteroid()


class Icon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.scale = 126
        self.image = pygame.transform.scale(pygame.image.load('image/boom_icon.png'), (self.scale, self.scale))
        self.image.set_colorkey('WHITE')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Boss(pygame.sprite.Sprite):
    def __init__(self, window_width, window_height):
        pygame.sprite.Sprite.__init__(self)
        self.scale_x = 550
        self.scale_y = self.scale_x / 3
        self.image = pygame.transform.scale(pygame.image.load('image/asteroid_big.png'), (self.scale_x, self.scale_y))
        self.image.set_colorkey('WHITE')
        self.rect = self.image.get_rect()
        self.rect.x = randint(0 + 150, window_width - 150)
        self.rect.y = 0
        self.is_boss = True

        self.speed = 1
        self.hp = 150

    def update(self, window_height):
        self.rect.y += self.speed
        self.rect.x += randint(-2, 0)
        if self.hp <= 0 or self.rect.y > 600:
            self.kill()

    def spawn_asteroid(self, asteroid_group, window_width, window_height):
        self.asteroid = Boss(window_width, window_height)
        self.rect.x = randint(0 + 150, window_width - 150)
        self.rect.y = 0
        asteroid_group.add(self.asteroid)
