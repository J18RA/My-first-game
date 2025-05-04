import pygame
from settings import ENEMY_SPEED, GROUND_LEVEL, load_enemy, WIDTH
from bullet import Bullet


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = ENEMY_SPEED
        self.velocity_y = 0
        self.gravity = 0.5
        self.direction = -1
        self.player = None

        self.bullets = pygame.sprite.Group()
        self.stop_distance = 200
        self.shoot_timer = 0
        self.shoot_interval = 120
        self.is_stopped = False

        self.run_frames = load_enemy()
        self.current_frame = 0
        self.animation_speed = 0.17
        self.image = self.run_frames[self.current_frame]
        self.rect = self.image.get_rect()

        # The initial position of the enemy outside the screen (right)
        self.rect.center = (WIDTH + 100, GROUND_LEVEL)

    def set_player(self, player):
        self.player = player

    def update(self):
        if self.player is None:
            return

        distance_to_player = abs(self.rect.centerx - self.player.rect.centerx)
        if distance_to_player > self.stop_distance:
            self.is_stopped = False

        # Movement to the player
        if distance_to_player > self.stop_distance:
            if self.rect.x > self.player.rect.x:
                self.rect.x -= self.speed
                self.direction = -1
            else:
                self.rect.x += self.speed
                self.direction = 1

        if distance_to_player <= self.stop_distance:
            self.is_stopped = True

        # Collision checking with ground
        if self.rect.bottom >= GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL
            self.velocity_y = 0

        # Animation
        if not self.is_stopped:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.run_frames):
                self.current_frame = 0
            self.image = self.run_frames[int(self.current_frame)]
        else:  # Static frame when the enemy is stopped
            self.image = self.run_frames[2]

        # Reflect the image if the enemy moves to the left
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

        # Shooting, when enemy is stopped
        if self.is_stopped:
            self.shoot_timer += 1
            if self.shoot_timer >= self.shoot_interval:
                self.shoot()
                self.shoot_timer = 0

    def shoot(self):
        if self.direction == 1:
            bullet = Bullet(self.rect.right, self.rect.centery, self.direction)
        else:
            bullet = Bullet(self.rect.left, self.rect.centery, self.direction)
        self.bullets.add(bullet)
        return bullet
