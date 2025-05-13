import pygame
import sys
from settings import WIDTH, HEIGHT, load_backgrounds, load_landscape, load_boxes, BOX_HP, WEAPON_PICKUPS, load_weapon
from player import Player, WeaponPickup
from enemies import Enemy
from camera import Camera

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

backgrounds = load_backgrounds()
sky_background = backgrounds["sky"]
mountains_background = backgrounds["mountains"]
clouds_background = backgrounds["clouds"]
trees_background = backgrounds["trees"]

landscapes = load_landscape()
ground = landscapes["ground"]
platforms = landscapes["platforms"]

boxes = load_boxes()

weapon_sprites = load_weapon()
weapon_pickups = [WeaponPickup(weapon["center_x"], weapon["center_y"], weapon["weapon_name"], weapon_sprites)
                  for weapon in WEAPON_PICKUPS]

clouds_offset = 0
PARALLAX_CLOUDS_SPEED = 0.3

camera = Camera(WIDTH, HEIGHT)

font = pygame.font.Font(None, 36)

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

enemies = pygame.sprite.Group()
enemy = Enemy()
enemy.set_player(player)
enemies.add(enemy)
all_sprites.add(enemy)

player_health = 100
score = 0

# The main cycle of the game
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.jump()
            if event.key == pygame.K_SPACE:
                bullet = player.shoot()
                player.bullets.add(bullet)

    # Player management
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if player.rect.left > 0:
            player.rect.x -= player.speed
    if keys[pygame.K_RIGHT]:
        if player.rect.right < camera.level_width:
            player.rect.x += player.speed

    camera.update(player)

    clouds_offset -= PARALLAX_CLOUDS_SPEED
    if clouds_offset <= -WIDTH:  # Seamless scrolling
        clouds_offset = 0

    player.update(platforms, boxes)
    enemies.update()
    player.bullets.update(camera)
    enemy.bullets.update(camera)

    # Checking and adjusting the player's position
    if player.rect.left < 0:  # The left edge of the screen
        player.rect.left = 0
    if player.rect.right > camera.level_width:  # The right edge of the screen
        player.rect.right = camera.level_width

    for pickup in weapon_pickups[:]:
        if player.rect.colliderect(pickup.rect):
            player.equip_weapon(pickup.weapon_name)
            weapon_pickups.remove(pickup)

    # Checking clashes of player bullets with enemies
    for bullet in player.bullets:
        hits = pygame.sprite.spritecollide(bullet, enemies, True)  # Remove the enemy when the bullet enters
        if hits:
            bullet.kill()  # Remove bullet
            score += 10

    for bullet in player.bullets:
        # Checking clashes of player bullets with box
        for box in boxes:
            if box["active"] and bullet.rect.colliderect(box["rect"]):
                box["hp"] -= 1
                bullet.kill()
                if box["hp"] <= 0:
                    box["active"] = False
                break

    # Checking the clashes of the enemy bullet with the player
    for bullet in enemy.bullets:
        if pygame.sprite.collide_rect(bullet, player):
            if player.invincible_timer <= 0:  # Player is vulnerable
                player_health -= 10
                player.invincible_timer = 60  # Activate invulnerability for 1 second (60 frames)
                bullet.kill()
                if player_health <= 0:
                    running = False

    # Checking the player's clashes with enemies
    if player.invincible_timer <= 0:
        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            player_health -= 10
            player.invincible_timer = 100
            if player_health <= 0:
                running = False

    screen.fill((0, 0, 0))

    """Rendering background layers, sprites and camera in mind"""

    screen.blit(sky_background, (0, 0))

    mountains_width = mountains_background.get_width()
    mountains_parallax_factor = 0.01
    mountains_offset = (camera.camera.left * mountains_parallax_factor) % mountains_width
    screen.blit(mountains_background, (mountains_offset - mountains_width, 0))
    screen.blit(mountains_background, (mountains_offset, 0))

    screen.blit(clouds_background, (clouds_offset, 0))
    screen.blit(clouds_background, (clouds_offset + WIDTH, 0))

    trees_width = trees_background.get_width()
    trees_offset = camera.camera.left % trees_width
    screen.blit(trees_background, (trees_offset - trees_width, 0))
    screen.blit(trees_background, (trees_offset, 0))

    ground_width = ground.get_width()
    ground_offset = camera.camera.left % ground_width
    screen.blit(ground, (ground_offset - trees_width, 0))
    screen.blit(ground, (ground_offset, 0))

    # Draw platforms
    for platform in platforms:
        sprite_pos = (
            platform["rect"].x + platform["sprite_offset_x"] + camera.camera.left,
            platform["rect"].y + platform["sprite_offset_y"] + camera.camera.top
        )
        screen.blit(platform["sprite"], sprite_pos)

    for pickup in weapon_pickups:
        pickup.draw(screen, camera)

    # Draw boxes
    for box in boxes:
        if box["active"]:
            sprite_index = BOX_HP - box["hp"]
            if sprite_index < len(box["sprites"]) and box["sprites"][sprite_index]:
                sprite_pos = (
                    box["rect"].x + box["sprite_offset_x"] + camera.camera.left,
                    box["rect"].y + box["sprite_offset_y"] + camera.camera.top
                )
                screen.blit(box["sprites"][sprite_index], sprite_pos)

    for sprite in all_sprites:
        if sprite == player:
            if player.is_visible:
                screen.blit(sprite.image, camera.apply(sprite))
        else:
            screen.blit(sprite.image, camera.apply(sprite))

    for bullet in player.bullets:
        screen.blit(bullet.image, bullet.apply_camera(camera))

    for bullet in enemy.bullets:
        screen.blit(bullet.image, bullet.apply_camera(camera))

    player.draw_weapon(screen, camera)

    # Display health and score
    health_text = font.render(f"Health: {player_health}", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 50))

    # Screen refresh
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
