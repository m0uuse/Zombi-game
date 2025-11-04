import pygame
import random
from zombie import spawn_zombie

class Player:
    def __init__(self, grid_size, start_pos=(0, 0)):
        self.grid_size = grid_size
        self.pos = pygame.Vector2(start_pos)
        self.inner_pos = self.get_inner_pos()
        self.outline = pygame.Surface((grid_size, grid_size))
        self.outline.fill((255, 255, 255))
        self.sprite = pygame.Surface((grid_size - 20, grid_size - 20))
        self.sprite.fill((0, 200, 255))
        self.health = 4
        self.inventory = []
        self.moves = 0
        self.max_moves = 3
        self.facing = "down"  # default direction

    def get_inner_pos(self):
        return self.pos.x + 10, self.pos.y + 10

    def move(self, direction, grid_width, grid_height, game_map=None):
        """Move player if not blocked by a wall or door."""
        old_pos = pygame.Vector2(self.pos)
        gx = int(self.pos.x // self.grid_size)
        gy = int(self.pos.y // self.grid_size)
        tx, ty = gx, gy

        if direction == "up":
            ty -= 1
            self.facing = "up"
        elif direction == "down":
            ty += 1
            self.facing = "down"
        elif direction == "left":
            tx -= 1
            self.facing = "left"
        elif direction == "right":
            tx += 1
            self.facing = "right"

        # Check if within bounds
        if tx < 0 or ty < 0 or tx >= (grid_width // self.grid_size) or ty >= (grid_height // self.grid_size):
            return  # out of bounds

        # Check walls/doors before moving
        if game_map and game_map.is_wall_between(gx, gy, tx, ty):
            print("You bump into a wall!")
            return
        if game_map and game_map.is_door_between(gx, gy, tx, ty):
            print("There’s a door blocking your way!")
            return

        # Move if not blocked
        self.pos.x = tx * self.grid_size
        self.pos.y = ty * self.grid_size
        self.inner_pos = self.get_inner_pos()
        self.moves += 1

    def attack(self, game_map):
        """Attack in front of the player — can break doors."""
        gx = int(self.pos.x // self.grid_size)
        gy = int(self.pos.y // self.grid_size)
        tx, ty = gx, gy

        if self.facing == "up":
            ty -= 1
        elif self.facing == "down":
            ty += 1
        elif self.facing == "left":
            tx -= 1
        elif self.facing == "right":
            tx += 1

        if game_map and game_map.is_door_between(gx, gy, tx, ty):
            broke = game_map.break_door_between(gx, gy, tx, ty)
            if broke:
                print("💥 You broke down the door!")
            else:
                print("You hit the door! (still standing)")
        else:
            print("You swing at nothing...")

    def search(self, zombies):
        """Random search action."""
        outcome = random.choice(["item", "zombie"])
        if outcome == "item":
            item = random.choice(["Medkit", "Ammo", "Key", "Coin"])
            self.inventory.append(item)
            print(f"Player found: {item}")
        else:
            spawn_zombie(zombies, self.grid_size, self.inner_pos)
            print("A zombie appeared!")

    def draw(self, surface):
        surface.blit(self.outline, self.pos)
        surface.blit(self.sprite, self.inner_pos)
