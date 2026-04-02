import pygame
import numpy as np

# Initialize pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Renderer")

clock = pygame.time.Clock()
running = True

# Function to draw a pixel
def draw_pixel(x, y, color=(255, 255, 255)):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        screen.set_at((int(x), int(y)), color)

vertices = np.array([0, 0, 0])

while running:
    clock.tick(60)  # 60 FPS
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Clear screen
    
    
    
    pygame.display.flip()

pygame.quit()