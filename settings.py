import os.path
import pygame

WIDTH = 800
HEIGHT = 600

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

LEVEL_WIDTH = 3200

PLATFORMS = [
    {"center_x": 250, "center_y": 510, "width": 120, "height": 80},
    {"center_x": 450, "center_y": 510, "width": 120, "height": 80},
]

BOX_PATH = os.path.join("assets", "level1", "box")
BOX_STATES = ["box.png", "broken_box1.png", "broken_box2.png", "box_destroyed"]
BOX_HP = 3
BOXES = [
    {"center_x": 600, "center_y": 520, "width": 60, "height": 60},
    {"center_x": 800, "center_y": 520, "width": 60, "height": 60},
]

WEAPON_PATH = os.path.join("assets", "weapons")
WEAPONS = [
    {"name": "weapon1", "sprite": "weapon1.png", "bullet_count": 1, "bullet_angles": [0]},
    {"name": "weapon2", "sprite": "weapon2.png", "bullet_count": 3, "bullet_angles": [-30, 0, 30]}
]
WEAPON_PICKUPS = [
    {"center_x": 800, "center_y": 520, "weapon_name": "weapon2"}
]

"""Load and return sprites."""


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


def load_boxes():
    boxes_list = []
    for box_data in BOXES:
        box_states = []
        for state in BOX_STATES:
            if state == "box_destroyed":
                box_states.append(None)
            else:
                state_path = os.path.join(BOX_PATH, state)
                box_sprite = pygame.image.load(state_path).convert_alpha()

                if box_sprite.get_width() != box_data["width"] or box_sprite.get_height() != box_data["height"]:
                    box_sprite = pygame.transform.scale(box_sprite, (box_data["width"], box_data["height"]))
                box_states.append(box_sprite)

        box_rect = pygame.Rect(0, 0, box_data["width"], box_data["height"])
        box_rect.center = (box_data["center_x"], box_data["center_y"])

        boxes_list.append({
            "sprites": box_states,
            "rect": box_rect,
            "hp": BOX_HP,
            "sprite_offset_x": (box_data["width"] - box_states[0].get_width()) // 2,
            "sprite_offset_y": (box_data["height"] - box_states[0].get_height()) // 2,
            "active": True
        })

    return boxes_list


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
    for weapon in WEAPONS:
        weapon_path = os.path.join("assets", "weapons", weapon["sprite"])
        weapon_sprites[weapon["name"]] = pygame.image.load(weapon_path).convert_alpha()
    return weapon_sprites
