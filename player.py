import pygame
from bullet import Bullet
from settings import PLAYER_SPEED, GROUND_LEVEL, load_player, load_weapon, WEAPONS


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
        self.current_weapon = "weapon1"
        self.weapon_data = self.get_weapon_data("weapon1")
        self.weapon_image = self.weapon_sprites[self.current_weapon]
        self.weapon_rect = self.weapon_image.get_rect()
        self.weapon_offset_x = 15
        self.weapon_offset_y = 32

        self.invincible_timer = 0
        self.is_visible = True  # The player's visibility (for blinking)

    def get_weapon_data(self, weapon_name):
        for weapon in WEAPONS:
            if weapon["name"] == weapon_name:
                return weapon
        return WEAPONS[0]

    def update(self, platforms, boxes, weapon_pickups=None):
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

        # Check for collisions with boxes
        for box in boxes:
            if not box["active"]:
                continue

            if self.velocity_y > 0:
                if (self.rect.colliderect(box["rect"]) and
                        self.rect.bottom <= box["rect"].top + self.velocity_y + 1):
                    self.rect.bottom = box["rect"].top
                    self.velocity_y = 0
                    self.is_jumping = False

            if box["active"] and self.rect.colliderect(box["rect"]):
                if self.rect.right > box["rect"].left > self.rect.left:
                    self.rect.right = box["rect"].left
                elif self.rect.left < box["rect"].right < self.rect.right:
                    self.rect.left = box["rect"].right

        # Check for collisions with ground
        if self.rect.bottom >= GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL
            self.velocity_y = 0
            self.is_jumping = False  # Player on the ground, the jump is completed

        # Check pickup weapon
        if weapon_pickups:
            for pickup in weapon_pickups[:]:
                if self.rect.colliderect(pickup.rect):
                    self.equip_weapon(pickup.weapon_name)
                    weapon_pickups.remove(pickup)

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
        if self.current_weapon and self.is_visible:
            weapon_pos = self.weapon_rect.move(camera.camera.topleft)
            screen.blit(self.weapon_image, weapon_pos)

    def shoot(self):
        bullets = []
        if self.weapon_data:
            for angle in self.weapon_data["bullet_angles"]:
                x = self.rect.right if self.direction == 1 else self.rect.left
                y = self.rect.centery + 5
                bullet = Bullet(x, y, self.direction, angle)
                self.bullets.add(bullet)
                bullets.append(bullet)
        return bullets

    def jump(self):
        if not self.is_jumping:  # Jump is possible only if a player on earth
            self.velocity_y = -10  # Fixed initial jump speed
            self.is_jumping = True

    def equip_weapon(self, weapon_name):
        if any(w["name"] == weapon_name for w in WEAPONS):
            self.current_weapon = weapon_name
            self.weapon_data = self.get_weapon_data(weapon_name)


class WeaponPickup:
    def __init__(self, x, y, weapon_name, weapon_sprites):
        self.rect = pygame.Rect(0, 0, 60, 50)
        self.rect.center = (x, y)
        self.weapon_name = weapon_name
        self.sprite = weapon_sprites[weapon_name]
        self.sprite = pygame.transform.scale(self.sprite, (60, 60))

    def draw(self, screen, camera):
        pos = self.rect.move(camera.camera.topleft)
        screen.blit(self.sprite, pos)