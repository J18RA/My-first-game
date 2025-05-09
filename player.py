import pygame
from bullet import Bullet
from settings import PLAYER_SPEED, GROUND_LEVEL, load_player, load_weapon


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.speed = PLAYER_SPEED
        self.velocity_y = 0
        self.gravity = 0.45
        self.is_jumping = False
        self.direction = 1
        self.bullets = pygame.sprite.Group()
        self.is_stopped = None

        self.run_frames = load_player()
        self.current_frame = 0
        self.animation_speed = 0.17
        self.image = self.run_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (100, GROUND_LEVEL)

        self.weapon_sprites = load_weapon()
        self.current_weapon = "weapon1.png"

        self.weapon_image = self.weapon_sprites[self.current_weapon]
        self.weapon_rect = self.weapon_image.get_rect()

        self.weapon_offset_x = 15
        self.weapon_offset_y = 32

        self.invincible_timer = 0
        self.is_visible = True  # The player's visibility (for blinking)

    def update(self, platforms):
        # Updating the timer of invulnerability
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            # Blinking: Change visibility every 10 frames
            if self.invincible_timer % 10 == 0:
                self.is_visible = not self.is_visible
        else:
            self.is_visible = True

        # Horizontal movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = -1
            self.is_stopped = False
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = 1
            self.is_stopped = False
        else:
            self.is_stopped = True

        # Gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Check for collisions with platforms
        for platform in platforms:
            if self.velocity_y > 0:  # Falling
                if (self.rect.colliderect(platform["rect"]) and
                        self.rect.bottom <= platform["rect"].top + self.velocity_y + 1):
                    self.rect.bottom = platform["rect"].top
                    self.velocity_y = 0
                    self.is_jumping = False

        # Collision checking with ground
        if self.rect.bottom >= GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL
            self.velocity_y = 0
            self.is_jumping = False  # Player on the ground, the jump is completed

        # Animation
        if not self.is_stopped:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.run_frames):
                self.current_frame = 0
            self.image = self.run_frames[int(self.current_frame)]

            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)
        else:  # # Static frame when the player is stopped
            self.image = self.run_frames[2]

            # Reflect the image if the enemy moves to the left
            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)

        self.update_weapon()

    def update_weapon(self):
        if self.current_weapon:
            self.weapon_image = self.weapon_sprites[self.current_weapon]
            if self.direction == -1:
                self.weapon_image = pygame.transform.flip(self.weapon_image, True, False)

            # Weapon position, taking into account displacement
            if self.direction == 1:
                self.weapon_rect.midbottom = (
                    self.rect.centerx + self.weapon_offset_x,
                    self.rect.centery + self.weapon_offset_y,
                )
            else:
                self.weapon_rect.midbottom = (
                    self.rect.centerx - self.weapon_offset_x,
                    self.rect.centery + self.weapon_offset_y,
                )

    def draw_weapon(self, screen, camera):
        if self.current_weapon:
            weapon_pos = self.weapon_rect.move(camera.camera.topleft)
            screen.blit(self.weapon_image, weapon_pos)

    def shoot(self):
        if self.direction == 1:
            bullet = Bullet(self.rect.right, self.rect.centery + 5, self.direction)
        else:
            bullet = Bullet(self.rect.left, self.rect.centery + 5, self.direction)
        self.bullets.add(bullet)
        return bullet

    def jump(self):
        if not self.is_jumping:  # Jump is possible only if a player on earth
            self.velocity_y = -10  # Fixed initial jump speed
            self.is_jumping = True

    def equip_weapon(self, weapon_name):
        if weapon_name in self.weapon_sprites:
            self.current_weapon = weapon_name
