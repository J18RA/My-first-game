import pygame
from settings import LEVEL_WIDTH


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.level_width = LEVEL_WIDTH

    def apply(self, entity):
        """Move the object to the offset of the camera."""

        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        """Calculate the shift of the camera so that the player is in the center."""

        x = -target.rect.centerx + self.width // 2
        y = -target.rect.centery + self.height // 2

        # Restrictions on the edges of the level (if the level is larger than the screen)
        x = min(0, x)  # Don't move the camera beyond the left border
        x = max(-(self.level_width - self.width), x)  # Don't move the camera behind the right border
        y = min(0, y)  # Don't move the camera beyond the upper border
        y = max(-(self.height - self.height), y)  # Don't move the camera beyond the lower border
        # Update the position of the camera
        self.camera = pygame.Rect(x, y, self.width, self.height)
