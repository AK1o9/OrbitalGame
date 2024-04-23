import pygame
import math
import time
from sys import exit
from random import randint
from settings import *
from sprites import Planet, Tower, Meteor, Player

class Game:
    def __init__(self):
        # initial setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption("Orbital")
        self.clock = pygame.time.Clock()
        self.screen_controller = 0  # -1: GAME OVER, 0: MENU, 1: ACTIVE GAME

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # sprites
        self.player = Player(self.all_sprites)
        self.planet = Planet(self.all_sprites)
        self.tower = Tower(self.all_sprites)
        self.meteor = Meteor(self.all_sprites)

        # timer
        # self.obstacle_timer = pygame.USEREVENT + 1
        # pygame.time.set_timer(self.obstacle_timer, 1000)

        # fonts
        self.header_font = pygame.font.Font('assets/fonts/Poppins-Light.ttf', 64)
        self.body_font = pygame.font.Font('assets/fonts/Poppins-Light.ttf', 32)
        self.lives = 3
        self.score = 0

        # text
        self.game_over_surf = self.header_font.render("GAME OVER", False, '#FFFFFF')
        self.game_over_rect = self.game_over_surf.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/6))

        self.play_msg_surf = self.body_font.render("Press 'SPACE' to PLAY", False, '#FFFFFF')
        self.play_msg_rect = self.play_msg_surf.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT*5/6))

        # audio
        # TODO: BG music and score sfx

    def collisions(self):
        return
    
    def add_score(self):
        self.score += 1

    def lose_life(self):
        self.lives -= 1

    def reset_stats(self):
        self.score = 0
        self.lives = 3

    def display_score(self, x, y):
        score_surf = self.header_font.render(f'{self.score}', False, (255,255,255))
        score_rect = score_surf.get_rect(center = (x, y))
        self.screen.blit(score_surf, score_rect)
        
    def display_lives(self, x, y):
        lives_surf = self.header_font.render(f'x {self.lives}', False, (255,255,255))
        lives_rect = lives_surf.get_rect(center = (x, y))
        self.screen.blit(lives_surf, lives_rect)

    def run(self):
        # Attributes for orbital motion
        # player_angle = 0
        # angle_incr = 0.016 # angle is incremented by this value each frame
        # player_speed_multiplier = 5 # the speed of the orbital
        # player_gravity = 0.01 # the pull towards the center

        # player_x = SCREEN_WIDTH/2 - 20
        # player_y = 150
        # player = pygame.Rect(player_x, player_y, 30, 30)

        # Interface 
        # score = 0
        # lives = 3

        # header_font = pygame.font.Font('assets/fonts/Poppins-Light.ttf', 64)
        # body_font = pygame.font.Font('assets/fonts/Poppins-Light.ttf', 32)

        # screen_controller = 0
        # GAME OVER screen -> -1
        # MENU screen -> 0
        # ACTIVE GAME screen -> 1

        
        # Timer
        # start_timer = pygame.USEREVENT + 1
        # pygame.time.set_timer(start_timer, 800)
        # obstacle_timer = pygame.USEREVENT + 2
        
        last_time = time.time()
        running = True
        while running:
            # Delta time
            dt = time.time() - last_time
            last_time = time.time()

            # Event handler/loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running  = False
                if self.screen_controller==1:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print(event.pos)
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            lives = 3
                            self.score = 0
                            # player_gravity = 0
                            self.screen_controller = 1
                        elif event.key == pygame.K_ESCAPE and self.screen_controller==-1:
                            print('esc')
                            lives = 3
                            self.score = 0
                            self.screen_controller = 0
            
            if self.screen_controller == 1:
                # ACTIVE GAME SCREEN

                # Background
                self.screen.fill((0,0,0))

                # Draw sprites
                self.all_sprites.update(dt)
                self.all_sprites.draw(self.screen)

                # Draw surfaces
                self.display_score(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                self.display_lives(SCREEN_WIDTH-80, 40)

            elif self.screen_controller == 0:
                # MENU SCREEN
                # TODO: Add Orbital Logo
                self.screen.fill('Black')
                outer_circle = pygame.draw.circle(self.screen, ((255,255,255)), (360, 450), 132)
                inner_circle = pygame.draw.circle(self.screen, ((0,0,0)), (360, 450), 130)
                self.screen.blit(self.play_msg_surf, self.play_msg_rect)
                if self.score!= 0: self.display_score(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

            else:
                # GAME OVER SCREEN
                self.screen.fill('Black')
                # TODO: Add some idle animation
                outer_circle = pygame.draw.circle(self.screen, ((255,255,255)), (360, 450), 132)
                inner_circle = pygame.draw.circle(self.screen, ((0,0,0)), (360, 450), 130)
                self.screen.blit(self.game_over_surf, self.game_over_rect)
                self.screen.blit(self.play_msg_surf, self.play_msg_rect)
                if self.score!= 0: self.display_score(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

            pygame.display.update()
            self.clock.tick(FRAME_RATE)  # framerate

        pygame.quit()
        exit() 

if __name__ == '__main__':
    game = Game()
    game.run()