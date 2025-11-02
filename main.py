import pygame
import sys

pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Character Movement")

# Colors
BACKGROUND_COLOR = (30, 30, 30)

# Player setup
player_position = pygame.Surface((100, 100))  # placeholder square
player_position.fill((255,255,255))
player_image = pygame.Surface((80,80))
player_image.fill ((0, 200, 255)) 

player_position_pos = pygame.Vector2(0, 0)
player_image_pos = player_position_pos.x+10, player_position_pos.y+10

MOVE_DISTANCE = 100 #DISTANCE

def refreshposition_character(pla):
    pla = player_position_pos.x+10, player_position_pos.y+10
    return pla

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_position_pos.y -= MOVE_DISTANCE
                player_image_pos=refreshposition_character(player_image_pos)
            elif event.key == pygame.K_DOWN:
                player_position_pos.y += MOVE_DISTANCE
                player_image_pos=refreshposition_character(player_image_pos)
            elif event.key == pygame.K_LEFT:
                player_position_pos.x -= MOVE_DISTANCE
                player_image_pos=refreshposition_character(player_image_pos)
            elif event.key == pygame.K_RIGHT:
                player_position_pos.x += MOVE_DISTANCE
                player_image_pos=refreshposition_character(player_image_pos)
                
    # Optional: keep player within window
    player_position_pos.x = max(0, min(WIDTH - player_position.get_width(), player_position_pos.x))
    player_position_pos.y = max(0, min(HEIGHT - player_position.get_height(), player_position_pos.y))
    player_image_pos=refreshposition_character(player_image_pos)
    print(player_image_pos)
    
    # Draw
    window.fill(BACKGROUND_COLOR)
    window.blit(player_position, player_position_pos)
    window.blit(player_image, player_image_pos)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()