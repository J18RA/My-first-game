import os.path
import pygame

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

PLAYER_SPEED = 1.1
BULLET_SPEED = 10
ENEMY_SPEED = 0.9

PLAYER_SIZE = (60, 80)
BULLET_SIZE = (10, 5)
ENEMY_SIZE = (10, 80)

BACKGROUND_PATH = os.path.join("assets", "level1", "background")
LANDSCAPE_PATH = os.path.join("assets", "level1", "landscape")
GROUND_LEVEL = HEIGHT - 50

PLAYER_SPRITES = os.path.join("assets", "player")
ENEMY_1_SPRITES = os.path.join("assets", "enemies", "enemy_1")
WEAPON_SPRITES = os.path.join("assets", "weapons")

LEVEL_WIDTH = 3200

PLATFORMS = [
    {"center_x": 250, "center_y": 510, "width": 120, "height": 80},
    {"center_x": 450, "center_y": 510, "width": 120, "height": 80},
]


def load_backgrounds():
    """Load and return all background layers."""

    sky_background = pygame.image.load(os.path.join(BACKGROUND_PATH, "sky-background.png")).convert()
    mountains_background = pygame.image.load(os.path.join(BACKGROUND_PATH, "mountains-background.png")).convert_alpha()
    clouds_background = pygame.image.load(os.path.join(BACKGROUND_PATH, "clouds-background.png")).convert_alpha()
    trees_background = pygame.image.load(os.path.join(BACKGROUND_PATH, "trees-background.png")).convert_alpha()

    return {
        "sky": sky_background,
        "mountains": mountains_background,
        "clouds": clouds_background,
        "trees": trees_background
    }


def load_landscape():
    """Load and return all landscape layers."""

    ground = pygame.image.load(os.path.join(LANDSCAPE_PATH, "ground.png")).convert_alpha()

    platforms = []
    for platform in PLATFORMS:
        plat_sprite = pygame.image.load(os.path.join(LANDSCAPE_PATH, "middle_ground.png")).convert_alpha()

        if (plat_sprite.get_width() != platform["width"] or
                plat_sprite.get_height() != platform["height"]):
            plat_sprite = pygame.transform.scale(
                plat_sprite,
                (platform["width"], platform["height"])
            )

        plat_rect = pygame.Rect(0, 0, platform["width"], platform["height"])
        plat_rect.center = (platform["center_x"], platform["center_y"])

        platforms.append({
            "sprite": plat_sprite,
            "rect": plat_rect,
            "sprite_offset_x": (platform["width"] - plat_sprite.get_width()) // 2,
            "sprite_offset_y": (platform["height"] - plat_sprite.get_height()) // 2
        })

    return {
        "ground": ground,
        "platforms": platforms
    }


"""Load and return sprites."""
def load_player():
    frames = []

    for frame_name in sorted(os.listdir(PLAYER_SPRITES)):
        frame_path = os.path.join(PLAYER_SPRITES, frame_name)
        frame = pygame.image.load(frame_path).convert_alpha()
        frames.append(frame)

    return frames


def load_enemy():
    frames = []

    for frame_name in sorted(os.listdir(ENEMY_1_SPRITES)):
        frame_path = os.path.join(ENEMY_1_SPRITES, frame_name)
        frame = pygame.image.load(frame_path).convert_alpha()
        frames.append(frame)

    return frames


def load_weapon():
    weapon_sprites = {}
    for weapon_name in os.listdir(WEAPON_SPRITES):
        weapon_path = os.path.join(WEAPON_SPRITES, weapon_name)
        weapon_sprites[weapon_name] = pygame.image.load(weapon_path).convert_alpha()

    return weapon_sprites
