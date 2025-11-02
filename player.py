import pygame
import random
from zombie import spawn_zombie

class Player:
    def __init__(self, grid_size, start_pos=(0,0)):
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

    def get_inner_pos(self):
        return self.pos.x + 10, self.pos.y + 10

    def move(self, direction, grid_width, grid_height):
        if direction == "up":
            self.pos.y -= self.grid_size
        elif direction == "down":
            self.pos.y += self.grid_size
        elif direction == "left":
            self.pos.x -= self.grid_size
        elif direction == "right":
            self.pos.x += self.grid_size

        # Keep inside bounds
        self.pos.x = max(0, min(grid_width - self.grid_size, self.pos.x))
        self.pos.y = max(0, min(grid_height - self.grid_size, self.pos.y))

        self.inner_pos = self.get_inner_pos()
        self.moves += 1

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
