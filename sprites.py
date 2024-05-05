import pygame
import math
from random import randint, choice
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Planet(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.original_img = pygame.image.load(
            "assets/images/assetDarkPlanet.png"
        ).convert_alpha()
        self.original_img = pygame.transform.smoothscale_by(self.original_img, 0.5)

        self.image = self.original_img.copy()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        self.angle = 0

        self.mask = pygame.mask.from_surface(self.image)

    def rotate(self, angle_change):
        self.angle += angle_change
        self.image = pygame.transform.rotate(self.original_img, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rotate(0.5)
        return


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        asteroid_no = randint(1, 4)
        self.original_img = pygame.image.load(
            f"assets/images/assetAsteroid{str(asteroid_no)}.png"
        ).convert_alpha()
        self.original_img = pygame.transform.smoothscale_by(self.original_img, 0.25)

        spawn_points = [
            (SCREEN_WIDTH / 2, -80),  # top
            (SCREEN_WIDTH / 2, SCREEN_HEIGHT + 80),  # bottom
            (-80, SCREEN_HEIGHT / 2),  # left
            (SCREEN_WIDTH + 80, SCREEN_HEIGHT / 2),  # right
        ]
        self.spawn_choice = choice(spawn_points)
        print(f"Asteroid spawned @ {self.spawn_choice}")
        self.angle = 0.032
        if self.spawn_choice == spawn_points[0]:
            self.x_direction = 0
            self.y_direction = 1
            self.angle *= -11
        elif self.spawn_choice == spawn_points[1]:
            self.x_direction = 0
            self.y_direction = -1
        elif self.spawn_choice == spawn_points[2]:
            self.x_direction = 1
            self.y_direction = 0
            self.angle *= -0.2
        elif self.spawn_choice == spawn_points[3]:
            self.x_direction = -1
            self.y_direction = 0
            self.angle *= -32

        self.image = self.original_img.copy()
        self.rect = self.image.get_rect(center=(self.spawn_choice))
        self.mask = pygame.mask.from_surface(self.image)

        self.rot_angle = 0

        self.speed_multiplier = 5
        self.direction = 0

        # Orbital properties
        self.orbit_points = []
        self.velocity = [0, 0]
        self.radius = ""
        self.mass = 0

    def move(self, dt):
        if (
            self.rect.x > SCREEN_WIDTH * 3 / 4
            or self.rect.x < SCREEN_WIDTH / 4
            or self.rect.y > SCREEN_HEIGHT * 3 / 4
            or self.rect.y < SCREEN_HEIGHT / 4
        ):
            self.rect.move_ip(self.x_direction, self.y_direction)
            self.mask = pygame.mask.from_surface(self.image)

    def rotate(self, angle_change):
        self.rot_angle += angle_change
        self.image = pygame.transform.rotate(self.original_img, self.rot_angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def orbit(self, dt):
        if (SCREEN_WIDTH / 5 <= self.rect.x <= SCREEN_WIDTH * 4 / 5) and (
            SCREEN_HEIGHT / 6 <= self.rect.y <= SCREEN_HEIGHT * 3 / 4
        ):
            if self.x_direction == 1 or self.y_direction == 1:
                y = int(math.cos(self.angle) * self.speed_multiplier)
                x = int(math.sin(self.angle) * self.speed_multiplier)
            else:
                x = int(math.cos(self.angle) * self.speed_multiplier)
                y = int(math.sin(self.angle) * self.speed_multiplier)
            self.rect.move_ip(x, y)
            if self.x_direction == -1:
                self.angle -= dt * 1.5
            else:
                self.angle -= dt / 2
            self.mask = pygame.mask.from_surface(self.image)

    def destroy(self):
        if (self.rect.centerx < -150 or self.rect.centerx > SCREEN_WIDTH + 150) or (
            self.rect.centery < -150 or self.rect.centery > SCREEN_HEIGHT + 150
        ):
            self.kill()
            print("asteroid deleted.")

    def update(self, dt):
        self.move(dt)
        self.orbit(dt)
        self.rotate(1)
        self.destroy()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.facing_right = choice([True, False])

        img1 = pygame.image.load("assets/images/assetMeteor1.png").convert_alpha()
        img1 = pygame.transform.scale(img1, (50, 50))
        img2 = pygame.image.load("assets/images/assetMeteor2.png").convert_alpha()
        img2 = pygame.transform.scale(img2, (50, 50))
        if not self.facing_right:
            img1 = pygame.transform.flip(img1, True, False)
            img2 = pygame.transform.flip(img2, True, False)
        self.meteor_frames = [img1, img2]
        self.index = 0

        self.image = self.meteor_frames[self.index]
        self.image = pygame.transform.scale(self.image, (50, 50))
        if self.facing_right:
            self.rect = self.image.get_rect(center=(-50, randint(-200, 300)))
        else:
            self.rect = self.image.get_rect(
                center=(SCREEN_WIDTH + 50, randint(-200, 300))
            )
        self.mask = pygame.mask.from_surface(self.image)

    def animate(self, dt):
        self.index += 0.09
        if self.index >= len(self.meteor_frames):
            self.index = 0
        self.image = self.meteor_frames[int(self.index)]
        self.mask = pygame.mask.from_surface(self.image)  # update mask

    def move(self, dt):
        if self.facing_right:
            self.rect.x += 2
        else:
            self.rect.x -= 2
        self.rect.y += 2
        self.mask = pygame.mask.from_surface(self.image)

    def destroy(self, dt):
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
            print("meteor deleted.")

    def update(self, dt):
        self.move(dt)
        self.animate(dt)
        self.destroy(dt)


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.original_img = pygame.image.load(
            "assets/images/assetMoon.png"
        ).convert_alpha()
        self.original_img = pygame.transform.scale(self.original_img, (32, 32))

        self.image = self.original_img.copy()
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH / 2, 150))

        self.mask = pygame.mask.from_surface(self.image)

        self.player_angle = 0
        self.angle_incr = 0.006  # angle is incremented by this value each frame
        self.player_gravity = 0.5  # the pull towards the center
        self.player_rot_angle = 0  # rotatation angle
        self.player_speed_multiplier = 5  # the speed of the orbital
        self.player_max_speed = 7.2  # max orbital speed

        self.player_crash_sound = pygame.mixer.Sound("assets/audio/crashSound.mp3")
        self.player_crash_sound.set_volume(0.5)

    def move(self, dt):
        x_coords = int(math.cos(self.player_angle) * self.player_speed_multiplier)
        y_coords = int(math.sin(self.player_angle) * self.player_speed_multiplier)
        self.rect.move_ip((x_coords, y_coords))
        self.player_angle += dt

    def reset_speed(self):
        self.player_speed_multiplier = 5
        self.player_gravity = 0.5

    def increase_speed(self, dt):
        if self.player_speed_multiplier < self.player_max_speed:
            self.player_speed_multiplier += dt / 5
            self.player_gravity += dt * 2
            self.angle_incr -= dt
            # print(f"Player speed ++ ({self.player_speed_multiplier})")

    def respawn(self):
        self.rect.midbottom = (SCREEN_WIDTH / 2 - 20, 150)
        self.player_angle = 0

    def rotate(self, angle_change):
        self.player_rot_angle += angle_change  # in degrees
        self.image = pygame.transform.rotate(self.original_img, self.player_rot_angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)  # update mask

    def check_input(self, dt):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.player_angle -= 0.03

    def gravity(self, dt):
        self.player_angle += self.player_gravity * dt

    def update(self, dt):
        self.move(dt)
        self.check_input(dt)
        self.gravity(dt)
        self.rotate(-4)

    def destroy(self):
        self.kill()
