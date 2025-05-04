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
GROUND_LEVEL = HEIGHT - 50

PLAYER_SPRITES = os.path.join("assets", "player")
ENEMY_1_SPRITES = os.path.join("assets", "enemies", "enemy_1")
WEAPON_SPRITES = os.path.join("assets", "weapons")

LEVEL_WIDTH = 3200


def load_backgrounds():
    """Load and return all background layers."""

    sky_background = pygame.image.load(os.path.join(BACKGROUND_PATH, "sky-background.png")).convert()
    mountains_background = pygame.image.load(os.path.join(BACKGROUND_PATH, "mountains-background.png")).convert_alpha()
    clouds_background = pygame.image.load(os.path.join(BACKGROUND_PATH, "clouds-background.png")).convert_alpha()
    trees_background = pygame.image.load(os.path.join(BACKGROUND_PATH, "trees-background.png")).convert_alpha()
    ground_background = pygame.image.load(os.path.join(BACKGROUND_PATH, "ground-background.png")).convert_alpha()

    return {
        "sky": sky_background,
        "mountains": mountains_background,
        "clouds": clouds_background,
        "trees": trees_background,
        "ground": ground_background,
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
