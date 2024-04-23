import pygame
import math
from sys import exit
from random import randint
from settings import *

def display_score(x,y):
    score_surf = header_font.render(f'{score}', False, (255,255,255))
    score_rect = score_surf.get_rect(center = (x, y))
    screen.blit(score_surf, score_rect)

def display_lives(x,y):
    lives_surf = header_font.render(f'x {lives}', False, (255,255,255))
    lives_rect = lives_surf.get_rect(center = (x, y))
    screen.blit(lives_surf, lives_rect)

def respawn_player():
    global lives, player_angle, player
    player.midbottom = (SCREEN_WIDTH/2-20, 150)
    lives -= 1
    player_angle = 0
    print(f'Lives left: {lives}')

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Orbital")

# Attributes for orbital motion
player_angle = 0
angle_incr = 0.016 # angle is incremented by this value each frame
player_speed_multiplier = 5 # the speed of the orbital
player_gravity = 0.01 # the pull towards the center

player_x = SCREEN_WIDTH/2 - 20
player_y = 150
player = pygame.Rect(player_x, player_y, 30, 30)

clock = pygame.time.Clock()

# Interface 
score = 0
lives = 3

header_font = pygame.font.Font('assets/fonts/Poppins-Light.ttf', 64)
body_font = pygame.font.Font('assets/fonts/Poppins-Light.ttf', 32)

screen_controller = 0
# GAME OVER screen -> -1
# MENU screen -> 0
# ACTIVE GAME screen -> 1

game_over_surf = header_font.render("GAME OVER", False, '#FFFFFF')
game_over_rect = game_over_surf.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/6))

play_msg_surf = body_font.render("Press 'SPACE' to PLAY", False, '#FFFFFF')
play_msg_rect = play_msg_surf.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT*5/6))
 
# Timer
start_timer = pygame.USEREVENT + 1
pygame.time.set_timer(start_timer, 800)
# obstacle_timer = pygame.USEREVENT + 2

running = True
while running:
    # Event handler/loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running  = False
        if screen_controller==1 and start_timer:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lives = 3
                    score = 0
                    # player_gravity = 0
                    screen_controller = 1
                elif event.key == pygame.K_ESCAPE and screen_controller==-1:
                    print('esc')
                    lives = 3
                    score = 0
                    screen_controller = 0
    
    if screen_controller == 1:
        # ACTIVE GAME SCREEN

        # Background
        screen.fill((0,0,0))

        # Shapes / entities / sprites
        # player_circle = pygame.draw.circle(screen, (255,255,255), (player_x, player_y), 15)
        player_ellipse = pygame.draw.ellipse(screen, (255,255,255), player)
        
        outer_circle = pygame.draw.circle(screen, ((255,255,255)), (360,450), 132)
        inner_circle = pygame.draw.circle(screen, ((0,0,0)), (360, 450), 130)
        
        # Orbital movement
        x_orbit = (int(math.cos(player_angle) * player_speed_multiplier))
        y_orbit = (int(math.sin(player_angle) * player_speed_multiplier))
        player.move_ip((x_orbit, y_orbit))
        player_angle += angle_incr
        player_angle += player_gravity
        # pygame.display.update()

        # Gravity
        # player_gravity += 0.002
        # player_angle += player_gravity # Accelerating gravity
        # print(player_angle)

        # x.move_ip(1,0)
        # coord_x +=1

        # If player goes out of bounds, reset player position.
        if player.top > SCREEN_HEIGHT or player.bottom < 0 or player.left > SCREEN_WIDTH+20 or player.right < -20: # Note: SCREEN_HEIGHT is the BOTTOM of the window.
            respawn_player()
            print('collision @ screen border')

        # Controls
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            # player_gravity-=5 # JUMP
            # player_gravity-=0.5 # FLY
            player_angle -= 0.03
            score +=1
        if key[pygame.K_a]:
            player.x -= 3
        if key[pygame.K_d]:
            player.x += 3

        if player.colliderect(inner_circle):
            respawn_player()
            print('collision @ inner circle')#working

        if lives == 0:
            # TODO: Game over screen (includes 'Play Again?' and 'Main Menu' options)
            print("GAME OVER!")
            screen_controller = -1

        # Draw surfaces
        display_score(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        display_lives(SCREEN_WIDTH-80, 40)

    elif screen_controller == 0:
        # MENU SCREEN
        # TODO: Add Orbital Logo
        screen.fill('Black')
        outer_circle = pygame.draw.circle(screen, ((255,255,255)), (360, 450), 132)
        inner_circle = pygame.draw.circle(screen, ((0,0,0)), (360, 450), 130)
        screen.blit(play_msg_surf, play_msg_rect)
        if score!= 0: display_score(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    else:
        # GAME OVER SCREEN
        screen.fill('Black')
        # TODO: Add some idle animation
        outer_circle = pygame.draw.circle(screen, ((255,255,255)), (360, 450), 132)
        inner_circle = pygame.draw.circle(screen, ((0,0,0)), (360, 450), 130)
        screen.blit(game_over_surf, game_over_rect)
        screen.blit(play_msg_surf, play_msg_rect)
        if score!= 0: display_score(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    pygame.display.update()
    clock.tick(FRAME_RATE)  # framerate

pygame.quit()
exit()