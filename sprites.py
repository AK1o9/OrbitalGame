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

        self.mask = pygame.mask.from_surface(self.image)

    def rotate(self):
        rotated_img = pygame.transform.rotozoom(self.image, 0.002, 1) 
        self.image = rotated_img

    def update(self, dt):
        # self.rotate()
        return

class Tower(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.image = pygame.image.load('assets/images/assetDarkTower.png').convert_alpha()
        self.image = pygame.transform.smoothscale_by(self.image, 0.5)#pygame.transform.scale(self.image, (100, 250))
        # self.image = pygame.transform.rotate(self.image, randint(0,360))
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 * 0.7))
        self.mask = pygame.mask.from_surface(self.image)

        self.angle = 0.016
        self.angle_incr = 0.008
        self.speed_multiplier = 5

    def move(self, dt):
        self.rect.move_ip(((int(math.cos(self.angle) * self.speed_multiplier)),  (int(math.sin(self.angle) * self.speed_multiplier))))
        self.angle += self.angle_incr
        self.mask = pygame.mask.from_surface(self.image)
    
    def rotate(self, dt):
        rotated_img = pygame.transform.rotozoom(self.image, self.angle*dt, 1)
        self.image = rotated_img
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 * 0.7))
        self.mask = pygame.mask.from_surface(self.image)

    def change_height(self, dt):
        return
    
    def destroy(self, dt):
        self.kill()

    def update(self, dt):
        # self.move(dt)
        # self.rotate(dt)
        return

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        img1 = pygame.image.load('assets/images/assetMeteor1.png').convert_alpha()
        img1 = pygame.transform.scale(img1, (50, 50)) 
        img2 = pygame.image.load('assets/images/assetMeteor2.png').convert_alpha()
        img2 = pygame.transform.scale(img2, (50, 50)) 
        self.meteor_frames = [img1,img2]
        self.index = 0

        self.image = self.meteor_frames[self.index]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center = (-50,randint(-200, 300)))

        self.mask = pygame.mask.from_surface(self.image)

    def animate(self, dt):
        self.index += 0.09
        if self.index >= len(self.meteor_frames):
            self.index = 0
        self.image = self.meteor_frames[int(self.index)]
        self.mask = pygame.mask.from_surface(self.image) # update mask

    def move(self, dt):
        self.rect.x += 2
        self.rect.y += 2
        self.mask = pygame.mask.from_surface(self.image)

    # TODO: delete later
    def reset_pos(self, dt):
        if self.rect.x > SCREEN_WIDTH or self.rect.y > SCREEN_HEIGHT:
            self.rect.center = (-50,-50)

    def destroy(self,dt):
        if self.rect.x > SCREEN_WIDTH and self.rect.y > SCREEN_HEIGHT:
            self.kill()
            print('meteor deleted.')

    def update(self, dt):
        self.move(dt)
        self.animate(dt)
        # self.reset_pos(dt)
        self.destroy(dt)

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        img = pygame.image.load('assets/images/assetMoon.png').convert_alpha()
        img =  pygame.transform.scale(img, (32,32))

        self.image = img
        self.rect = self.image.get_rect(midbottom = (SCREEN_WIDTH/2, 150))

        self.mask = pygame.mask.from_surface(self.image)

        # self.score = 0
        # self.lives = 3

        self.player_angle = 0
        self.angle_incr = 0.006 # angle is incremented by this value each frame
        self.player_gravity = 0.5 # the pull towards the center
        self.player_rotation = 0.1
        self.player_speed_multiplier = 5 # the speed of the orbital
        self.player_max_speed = 12 # max orbital speed
    
    def move(self, dt):
        x_coords = (int(math.cos(self.player_angle) * self.player_speed_multiplier))
        y_coords = (int(math.sin(self.player_angle) * self.player_speed_multiplier))
        self.rect.move_ip((x_coords, y_coords))
        self.player_angle += dt

    def reset_speed(self):
        self.player_speed_multiplier = 5
        self.player_gravity = 0.5
    
    def increase_speed(self, dt):
        if self.player_speed_multiplier <= self.player_max_speed:
            self.player_speed_multiplier += dt/3
            # self.player_angle += dt * self.player_gravity
            self.player_gravity += dt/12
            self.angle_incr *= 1.75
        # print(self.player_speed_multiplier) if self.player_speed_multiplier >= self.player_max_speed else{}
            # print(self.player_speed_multiplier)

    def respawn(self):
        self.rect.midbottom = (SCREEN_WIDTH/2-20, 150)
        # self.lives -= 1
        # print(f'Lives left: {self.lives}')
        self.player_angle = 0

    def rotate(self, dt, img, x, y):
        rotated_img = pygame.transform.rotozoom(self.image, -dt, 1)
        self.image = rotated_img

        # self.image = pygame.transform.rotate(img, self.player_rotation)
        # self.rect =  self.image.get_rect(center = img.get_rect(center = (x, y)).center)

        # self.player_rotation += 0.1
        self.mask = pygame.mask.from_surface(self.image) # update mask
    
    def check_input(self, dt):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.player_angle -= 0.03
        # if key[pygame.K_a]:
        #     self.rect.x -= 3
        # if key[pygame.K_d]:
        #     self.rect.x += 3

    def gravity(self, dt):
        self.player_angle += self.player_gravity * dt

    # def get_score(self, dt):
    #     return self.score
    
    # def get_lives(self, dt):
    #     return self.lives

    def update(self, dt):
        self.move(dt)
        self.increase_speed(dt)
        self.check_input(dt)
        self.gravity(dt)
        # self.rotate( dt, self.image,self.rect.x, self.rect.y)
    
    def destroy(self):
        self.kill() # ~ 