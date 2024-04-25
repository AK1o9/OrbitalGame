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

        # timer
        self.meteor_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.meteor_timer, 7800)
        # TODO: tower_timer

        # sprite groups & setup
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.player = Player(self.all_sprites)
        self.planet = Planet([self.all_sprites, self.collision_sprites])
        Tower([self.all_sprites, self.collision_sprites])
        # Meteor([self.all_sprites, self.collision_sprites])

        # fonts
        self.header_font = pygame.font.Font('assets/fonts/Poppins-Light.ttf', 64)
        self.body_font = pygame.font.Font('assets/fonts/Poppins-Light.ttf', 32)
        self.lives = 3
        self.score = 0
        self.start_time = 0

        # title
        self.title_img = pygame.image.load('assets/images/title_logo.png').convert_alpha()
        self.title_img = pygame.transform.smoothscale_by(self.title_img, 0.5)
        self.title_rect = self.title_img.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/6))

        # text
        self.game_over_surf = self.header_font.render("GAME OVER", True, '#FFFFFF')
        self.game_over_rect = self.game_over_surf.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/6))

        self.prev_score_surf = self.body_font.render("SCORE", True, '#FFFFFF')
        self.prev_score_rect = self.prev_score_surf.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT * 5/11 - 30))

        self.play_msg_surf = self.body_font.render("Press 'SPACE' to PLAY", True, '#FFFFFF')
        self.play_msg_rect = self.play_msg_surf.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT*5/6))

        # audio
        # TODO: BG music and score sfx

    def collisions(self):
        if pygame.sprite.spritecollide(self.player, self.collision_sprites, False, pygame.sprite.collide_mask) or self.player.rect.top > SCREEN_HEIGHT or self.player.rect.bottom < 0 or self.player.rect.left > SCREEN_WIDTH+20 or self.player.rect.right < -20:
            print("Collision!")
            self.lose_life()
    
    def add_score(self):
        self.score += 1

    def lose_life(self):
        if self.lives != 0:
            self.lives -= 1
            self.player.respawn()
        else:
            self.screen_controller = -1

    def reset_stats(self):
        self.lives = 3
        self.start_time = pygame.time.get_ticks()

    def display_score(self, x, y):
        if self.screen_controller == 1:
            self.score = (pygame.time.get_ticks() - self.start_time) // 1000
        score_surf = self.header_font.render(f'{self.score}', True, (255,255,255))
        score_rect = score_surf.get_rect(center = (x, y))
        self.screen.blit(score_surf, score_rect)
        
    def display_lives(self, x, y):
        lives_surf = self.header_font.render(f'x {self.lives}', True, (255,255,255))
        lives_rect = lives_surf.get_rect(center = (x, y))
        self.screen.blit(lives_surf, lives_rect)

    def run(self):
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
                    if event.type == self.meteor_timer:
                        Meteor([self.all_sprites, self.collision_sprites])
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.reset_stats()
                            self.screen_controller = 1
                            self.player.reset_speed()
                            self.player.respawn()
                        elif event.key == pygame.K_ESCAPE and self.screen_controller==-1:
                            print('esc')
                            self.screen_controller = 0
            
            if self.screen_controller == 1:
                # ACTIVE GAME SCREEN

                # Background
                self.screen.fill((0,0,0))

                # Draw sprites
                self.all_sprites.update(dt)
                self.collisions()
                self.all_sprites.draw(self.screen)

                # Draw surfaces
                self.display_score(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                self.display_lives(SCREEN_WIDTH/10 * 9, SCREEN_HEIGHT/20)

            elif self.screen_controller == 0:
                # MENU SCREEN
                # TODO: Add Orbital Logo
                self.screen.fill('Black')
                outer_circle = pygame.draw.circle(self.screen, ((255,255,255)), (360, 450), 132)
                inner_circle = pygame.draw.circle(self.screen, ((0,0,0)), (360, 450), 130)
                self.screen.blit(self.title_img, self.title_rect)
                self.screen.blit(self.play_msg_surf, self.play_msg_rect)
                if self.score!= 0: self.display_score(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

            else:
                # GAME OVER SCREEN
                self.screen.fill('Black')
                # TODO: Add some idle animation
                # outer_circle = pygame.draw.circle(self.screen, ((255,255,255)), (360, 450), 132)
                # inner_circle = pygame.draw.circle(self.screen, ((0,0,0)), (360, 450), 130)
                inner_rect, outer_rect = pygame.Rect(0,0,500,100), pygame.Rect(0,0,495,105)
                inner_rect.center, outer_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/6), (SCREEN_WIDTH/2, SCREEN_HEIGHT/6) 
                pygame.draw.rect(self.screen, 'white', inner_rect)
                pygame.draw.rect(self.screen, 'black', outer_rect)
                self.screen.blit(self.game_over_surf, self.game_over_rect)
                self.screen.blit(self.prev_score_surf, self.prev_score_rect)
                self.screen.blit(self.play_msg_surf, self.play_msg_rect)
                if self.score!= 0: self.display_score(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

            pygame.display.update()
            self.clock.tick(FRAME_RATE)  # framerate

        pygame.quit()
        exit() 

if __name__ == '__main__':
    game = Game()
    game.run()