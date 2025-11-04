import pygame
import sys
from player import Player
from zombie import *
from GameMap import *


pygame.init()

# === SETTINGS ===
GRID_SIZE = 100
GRID_WIDTH = 900
GRID_HEIGHT = 900
UI_WIDTH = 200
WINDOW_WIDTH = GRID_WIDTH + UI_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT

BACKGROUND_COLOR = (30, 30, 30)
GRID_COLOR = (80, 80, 80)
UI_COLOR = (45, 45, 45)
TEXT_COLOR = (200, 200, 200)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Turn-Based Grid Game")
font = pygame.font.SysFont(None, 28)
game_map = GameMap(GRID_SIZE, GRID_WIDTH, GRID_HEIGHT)


# === INIT PLAYER & ZOMBIES ===
player = Player(GRID_SIZE)
zombies = []

turn = "player"

spawners = []
for _ in range(3):  # spawn 3 random spawners
    spawn_zombie_spawner(spawners, GRID_SIZE)

# === FUNCTIONS ===
def draw_grid(surface):
    for x in range(0, GRID_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, GRID_HEIGHT))
    for y in range(0, GRID_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (GRID_WIDTH, y))

def draw_ui(surface):
    ui_rect = pygame.Rect(GRID_WIDTH, 0, UI_WIDTH, GRID_HEIGHT)
    pygame.draw.rect(surface, UI_COLOR, ui_rect)

    # Health
    surface.blit(font.render(f"Health: {player.health}", True, TEXT_COLOR), (GRID_WIDTH + 20, 20))
    # Inventory
    surface.blit(font.render("Objects:", True, TEXT_COLOR), (GRID_WIDTH + 20, 60))
    for i, item in enumerate(player.inventory[:8]):
        surface.blit(font.render(f"- {item}", True, TEXT_COLOR), (GRID_WIDTH + 20, 90 + i*25))
    # Turn
    surface.blit(font.render(f"Turn: {turn}", True, TEXT_COLOR), (GRID_WIDTH + 20, GRID_HEIGHT - 50))

# === MAIN LOOP ===
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if turn == "player":
                moved = False
                if event.key == pygame.K_UP:
                    player.move("up", GRID_WIDTH, GRID_HEIGHT,game_map)
                    moved = True
                elif event.key == pygame.K_DOWN:
                    player.move("down", GRID_WIDTH, GRID_HEIGHT,game_map)
                    moved = True
                elif event.key == pygame.K_LEFT:
                    player.move("left", GRID_WIDTH, GRID_HEIGHT,game_map)
                    moved = True
                elif event.key == pygame.K_RIGHT:
                    player.move("right", GRID_WIDTH, GRID_HEIGHT,game_map)
                    moved = True
                elif event.key == pygame.K_e:
                    player.search(zombies)
                    moved = True

                if moved and player.moves >= player.max_moves:
                    turn = "zombie"
                    player.moves = 0
                    print("Zombie turn!")

            elif turn == "zombie":
                
                print("Zombie turn phase 1: movement")
                move_zombies_toward_player(zombies, pygame.Vector2(player.inner_pos), GRID_SIZE)  # phase 2: move old zombies
                
                print("Zombie turn phase 2: spawners")
                spawn_from_spawners(zombies, spawners, GRID_SIZE)  # phase 1: spawn from portals

                reset_zombie_moves(zombies)  # prepare for next turn
                turn = "player"
                print("Back to player turn!")
    # === DRAW ===
    window.fill(BACKGROUND_COLOR)
    game_map.draw(window)
    player.draw(window)
    draw_grid(window)
    draw_spawners(window, spawners)
    draw_zombies(window, zombies)
    draw_ui(window)
    
    pygame.display.flip()
    clock.tick(60)
    

pygame.quit()
sys.exit()
