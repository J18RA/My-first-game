import pygame
from settings import BULLET_SIZE, BULLET_SPEED, RED, WIDTH


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface(BULLET_SIZE)
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = BULLET_SPEED * direction
        self.direction = direction

    def update(self, camera):
        self.rect.x += self.speed

        # Destruction of a bullet when it goes beyond the visible area
        visible_left = -camera.camera.left
        visible_right = visible_left + WIDTH

        if self.rect.right < visible_left or self.rect.left > visible_right:
            self.kill()

    # Adjusts the bullet position to account for camera offset
    def apply_camera(self, camera):
        return self.rect.move(camera.camera.topleft)
