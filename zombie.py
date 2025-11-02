import pygame
import random

ZOMBIE_COLOR = (200, 50, 50)
SPAWNER_COLOR = (150, 0, 150)
ZOMBIE_SIZE = 20  # small zombies
ZOMBIE_LIMIT= 30

def spawn_zombie(zombie_list, grid_size, player_inner_pos=None, cell_pos=None):
    """Spawn a small zombie at a random position inside a grid cell."""
    if len(zombie_list) >= ZOMBIE_LIMIT:
        return

    if cell_pos is None:
        gx = random.randint(0, (900 // grid_size) - 1)
        gy = random.randint(0, (900 // grid_size) - 1)
        base_pos = pygame.Vector2(gx * grid_size, gy * grid_size)
    else:
        base_pos = pygame.Vector2(cell_pos[0] * grid_size, cell_pos[1] * grid_size)

    offset_x = random.randint(1, min(70, grid_size - ZOMBIE_SIZE))
    offset_y = random.randint(1, min(70, grid_size - ZOMBIE_SIZE))
    pos = base_pos + pygame.Vector2(offset_x, offset_y)

    if player_inner_pos and pos == pygame.Vector2(player_inner_pos):
        return

    surf = pygame.Surface((ZOMBIE_SIZE, ZOMBIE_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(surf, ZOMBIE_COLOR, (ZOMBIE_SIZE//2, ZOMBIE_SIZE//2), ZOMBIE_SIZE//2)
    # Add "has_moved" flag to track if it should move this turn
    print(pos)
    zombie_list.append({"pos": pos, "surf": surf, "has_moved": False})

def spawn_zombie_spawner(spawner_list, grid_size):
    """Spawn a purple zombie spawner at a random grid cell."""
    gx = random.randint(0, (900 // grid_size) - 1)
    gy = random.randint(0, (900 // grid_size) - 1)
    pos = pygame.Vector2((gx * grid_size)+10, (gy * grid_size)+10)
    radius = grid_size // 2 - 10
    surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    pygame.draw.circle(surf, SPAWNER_COLOR, (radius, radius), radius)
    spawner_list.append({"pos": pos, "surf": surf})

def draw_zombies(surface, zombie_list):
    for z in zombie_list:
        surface.blit(z["surf"], (z["pos"].x, z["pos"].y))

def draw_spawners(surface, spawner_list):
    for s in spawner_list:
        surface.blit(s["surf"], (s["pos"].x, s["pos"].y))

def spawn_from_spawners(zombie_list, spawner_list, grid_size):
    """Spawn zombies from spawners (phase 1 of zombie turn)."""
    for s in spawner_list:
        if len(zombie_list) >= ZOMBIE_LIMIT:
            break
        cell_x = int(s["pos"].x // grid_size)
        cell_y = int(s["pos"].y // grid_size)
        # Spawn the new zombie, it will have has_moved=False
        spawn_zombie(zombie_list, grid_size, cell_pos=(cell_x, cell_y))

def move_zombies_toward_player(zombie_list, player_pos, grid_size):
    """Move only zombies that existed before this turn (has_moved=False)."""
    for z in zombie_list:
        if z["has_moved"]:
            continue  # skip zombies spawned this turn
        z_center = z["pos"] + pygame.Vector2(ZOMBIE_SIZE//2, ZOMBIE_SIZE//2)
        delta = player_pos - z_center
        move_vector = pygame.Vector2(0,0)
        if abs(delta.x) > abs(delta.y):
            move_vector.x = grid_size if delta.x > 0 else -grid_size
        else:
            move_vector.y = grid_size if delta.y > 0 else -grid_size
        z["pos"] += move_vector
        z["has_moved"] = True  # mark that it moved

def reset_zombie_moves(zombie_list):
    """Reset has_moved flag at the end of the zombie turn for next turn."""
    for z in zombie_list:
        z["has_moved"] = False
