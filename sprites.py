import pygame
import math
from random import randint
from settings import *
# from main_org import lives, player

class Background(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('../assets/images/assetMoon.png').convert_alpha()
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH/2 - 20, 150))

    def destroy():
        Background.kill() # ~

    def update():
        return
    
class Planet(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('assets/images/assetDarkPlanet.png').convert_alpha()
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    def rotate(self):
        rotated_img = pygame.transform.rotozoom(self.image, 0.002, 1) 
        self.image = rotated_img

    def update(self, dt):
        # self.rotate()
        return

# class Tower(pygame.sprite.Sprite):
#     def __init__(self, groups):
#         super().__init__(groups)

#         self.image = pygame.image.load('assets/images/assetDarkTower.png').convert_alpha()
#         self.image = pygame.transform.scale(self.image, (80, 240))
#         self.rect = self.image.get_rect(center = (SCREEN_WIDTH/2, SCREEN_WIDTH/2))

#         self.angle = 0.032
#         self.angle_incr = 0.016
#         self.speed_multiplier = 10

#     def move(self, dt):
#         self.rect.move_ip(((int(math.cos(self.angle) * self.speed_multiplier)),  (int(math.sin(self.angle) * self.speed_multiplier))))
#         self.angle += self.angle_incr
#         return
    
#     def rotate(self,):
#         rotated_img = pygame.transform.rotozoom(self.image, self.angle, 1)
#         self.image = rotated_img
        

#     def change_height(self, dt):
#         return
    
#     def destroy(self, dt):
#         self.kill()

#     def update(self, dt):
#         self.rotate()
#         return

# class Meteor(pygame.sprite.Sprite):
#     def __init__(self, groups):
#         super().__init__(groups)

#         self.image = pygame.image.load('assets/images/assetMeteor.gif').convert_alpha()
#         self.image = pygame.transform.scale(self.image, (50, 50))
#         self.rect = self.image.get_rect()

#     def move(self, dt):
#         self.rect.x += 2.5
#         self.rect.y += 2.5

#     def destroy(self,dt):
#         if self.rect.x > SCREEN_WIDTH and self.rect.y > SCREEN_HEIGHT:
#             self.kill()
#             print('metoer deleted.')

#     def update(self, dt):
#         self.move(dt)
#         self.destroy(dt)

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        img = pygame.image.load('assets/images/assetMoon.png').convert_alpha()

        self.image = pygame.transform.scale(img, (32,32))
        self.rect = self.image.get_rect(midbottom = (SCREEN_WIDTH/2, 150))

        self.lives = 3
        self.score= 0

        self.player_angle = 0
        self.angle_incr = 0.016 # angle is incremented by this value each frame
        self.player_speed_multiplier = 5 # the speed of the orbital
        self.player_gravity = 0.01 # the pull towards the center
        self.player_rotation = 0

    def check_position(self, dt):
        if self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0 or self.rect.left > SCREEN_WIDTH+20 or self.rect.right < -20: # Note: SCREEN_HEIGHT is the BOTTOM of the window.
            self.respawn(dt)
            print('collision @ screen border')
    
    def move(self, dt):
        x_coords = (int(math.cos(self.player_angle) * self.player_speed_multiplier))
        y_coords = (int(math.sin(self.player_angle) * self.player_speed_multiplier))
        self.rect.move_ip((x_coords, y_coords))
        self.player_angle += self.angle_incr

    def respawn(self, dt):
        self.rect.midbottom = (SCREEN_WIDTH/2-20, 150)
        self.lives -= 1
        self.player_angle = 0
        print(f'Lives left: {self.lives}')

    def rotate(self, img, x, y):
        rotated_img = pygame.transform.rotozoom(self.image, self.player_rotation, 1)
        self.image = rotated_img

        # self.image = pygame.transform.rotate(img, self.player_rotation)
        # self.rect =  self.image.get_rect(center = img.get_rect(center = (x, y)).center)

        self.player_rotation += 0.01
    
    def check_input(self, dt):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.player_angle -= 0.03
            self.score +=1
        # if key[pygame.K_a]:
        #     self.rect.x -= 3
        # if key[pygame.K_d]:
        #     self.rect.x += 3

    def gravity(self, dt):
        self.player_angle += self.player_gravity

    def get_score(self, dt):
        return self.score
    
    def get_lives(self, dt):
        return self.lives

    def update(self, dt):
        self.check_position(dt)
        self.move(dt)
        self.check_input(dt)
        self.gravity(dt)
        # self.rotate(self.image, self.rect.x, self.rect.y)
    
    def destroy():
        Player.kill() # ~ 