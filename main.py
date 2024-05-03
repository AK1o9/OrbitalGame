import pygame
import math  # noqa: F401
import time
from sys import exit
from random import randint  # noqa: F401
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, FRAME_RATE, WHITE, BLACK
from sprites import Planet, Meteor, Player, Asteroid


class Game:
    def __init__(self):
        # initial setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Orbital")
        self.clock = pygame.time.Clock()
        self.screen_controller = 0  # -1: GAME OVER, 0: MENU, 1: ACTIVE GAME

        # timer
        self.meteor_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.meteor_timer, 7800)
        self.asteroid_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.asteroid_timer, 5000)

        # sprite groups & setup
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.menu_sprites = pygame.sprite.Group()

        self.player = Player([self.all_sprites, self.menu_sprites])
        self.planet = Planet(
            [self.all_sprites, self.collision_sprites, self.menu_sprites]
        )
        self.meteors = []
        self.asteroids = []

        # fonts
        self.header_font = pygame.font.Font("assets/fonts/Poppins-Light.ttf", 64)
        self.body_font = pygame.font.Font("assets/fonts/Poppins-Light.ttf", 32)
        self.lives = 3
        self.score = 0
        self.start_time = 0

        self.score_checkpoints = [
            25,
            50,
            80,
        ]  # checkpoints in which the game difficulty increases

        # title
        self.title_img = pygame.image.load(
            "assets/images/title_logo.png"
        ).convert_alpha()
        self.title_img = pygame.transform.smoothscale_by(self.title_img, 0.5)
        self.title_rect = self.title_img.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6)
        )

        # text
        self.game_over_surf = self.header_font.render("GAME OVER", True, WHITE)
        self.game_over_rect = self.game_over_surf.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6)
        )

        self.prev_score_surf = self.body_font.render("SCORE", True, WHITE)
        self.prev_score_rect = self.prev_score_surf.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 5 / 11 - 30)
        )

        self.play_msg_surf = self.body_font.render("Press 'SPACE' to PLAY", True, WHITE)
        self.play_msg_rect = self.play_msg_surf.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 5 / 6)
        )

        # audio
        # TODO: BG music and score sfx

    def collisions(self):
        if (
            pygame.sprite.spritecollide(
                self.player, self.collision_sprites, False, pygame.sprite.collide_mask
            )
            or self.player.rect.top > SCREEN_HEIGHT + 140
            or self.player.rect.bottom < -140
            or self.player.rect.left > SCREEN_WIDTH + 140
            or self.player.rect.right < -140
        ):
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
        score_surf = self.header_font.render(f"{self.score}", True, WHITE)
        score_rect = score_surf.get_rect(center=(x, y))
        self.screen.blit(score_surf, score_rect)

    def display_lives(self, x, y):
        lives_surf = self.header_font.render(f"x {self.lives}", True, WHITE)
        lives_rect = lives_surf.get_rect(center=(x, y))
        self.screen.blit(lives_surf, lives_rect)

    def reduce_timers(self):
        if self.score == self.score_checkpoints[0]:
            pygame.time.set_timer(self.meteor_timer, 4500)
            pygame.time.set_timer(self.asteroid_timer, 4000)
        elif self.score == self.score_checkpoints[1]:
            pygame.time.set_timer(self.meteor_timer, 3200)
            pygame.time.set_timer(self.asteroid_timer, 3600)

    def increase_player_speed(self, dt):
        if self.score >= self.score_checkpoints[2]:
            self.player.increase_speed(dt)

    def restart(self):
        # reset score & lives
        self.reset_stats()
        # reset timers
        pygame.time.set_timer(self.meteor_timer, 7800)
        pygame.time.set_timer(self.asteroid_timer, 5000)

        # reset player abilities
        self.player.reset_speed()
        self.player.respawn()
        # change screen
        self.screen_controller = 1
        # clear obstacles
        if self.meteors and self.asteroids:
            for meteor in self.meteors:
                meteor.kill()
            for asteroid in self.asteroids:
                asteroid.kill()

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
                    running = False
                if self.screen_controller == 1:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print(event.pos)
                    if event.type == self.meteor_timer:
                        self.meteors.append(
                            Meteor([self.all_sprites, self.collision_sprites])
                        )
                    if event.type == self.asteroid_timer:
                        self.asteroids.append(
                            Asteroid([self.all_sprites, self.collision_sprites])
                        )
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.restart()
                        elif (
                            event.key == pygame.K_ESCAPE
                            and self.screen_controller == -1
                        ):
                            print("Inpt: esc")
                            self.screen_controller = 0

            if self.screen_controller == 1:
                # ACTIVE GAME SCREEN

                # Background
                self.screen.fill(BLACK)
                # Draw sprites
                self.all_sprites.update(dt)
                self.collisions()
                self.all_sprites.draw(self.screen)

                # Draw surfaces
                self.display_score(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                self.display_lives(SCREEN_WIDTH / 10 * 9, SCREEN_HEIGHT / 20)

                # Reset attributes (which were edited in the MENU SCREEN below )
                self.player.player_gravity = 0.5

                # Gameplay progression
                self.reduce_timers()
                self.increase_player_speed(dt)

            elif self.screen_controller == 0:
                # MENU SCREEN
                self.screen.fill(BLACK)
                self.player.rect.move(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
                self.menu_sprites.draw(self.screen)
                self.player.player_gravity = 0
                self.menu_sprites.update(dt)
                self.screen.blit(self.title_img, self.title_rect)
                self.screen.blit(self.play_msg_surf, self.play_msg_rect)
                if self.score != 0:
                    self.display_score(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

            else:
                # GAME OVER SCREEN
                self.screen.fill(BLACK)
                # TODO: Add some idle animation (Optional)
                inner_rect, outer_rect = (
                    pygame.Rect(0, 0, 500, 100),
                    pygame.Rect(0, 0, 495, 105),
                )
                inner_rect.center, outer_rect.center = (
                    (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6),
                    (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6),
                )
                pygame.draw.rect(self.screen, WHITE, inner_rect)
                pygame.draw.rect(self.screen, BLACK, outer_rect)
                self.screen.blit(self.game_over_surf, self.game_over_rect)
                self.screen.blit(self.prev_score_surf, self.prev_score_rect)
                self.screen.blit(self.play_msg_surf, self.play_msg_rect)
                if self.score != 0:
                    self.display_score(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

            pygame.display.update()
            self.clock.tick(FRAME_RATE)  # framerate

        pygame.quit()
        exit()


if __name__ == "__main__":
    game = Game()
    game.run()
