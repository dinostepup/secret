import pygame
import math
import random
import os  # For handling paths

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("You are my baby sunshineeeee 💖")

# Colors
PINK = (255, 105, 180)
DARK_PINK = (255, 20, 147)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)

# Font settings
font = pygame.font.Font(None, 70)  # Text size
angle = 0  # Rotation angle

# Get the current script directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Load images using relative paths
dino_image = pygame.image.load(os.path.join(current_directory, "assets", "images", "dino.webp"))
scaled_dino = pygame.transform.scale(dino_image, (40, 40))  # Resize

background_image = pygame.image.load(os.path.join(current_directory, "assets", "images", "seal.png"))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Resize

# Heart function
def heart_function(t):
    x = 16 * math.sin(t) ** 3
    y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
    return x * 20 + WIDTH // 2, -y * 20 + HEIGHT // 2

# Generate heart points
heart_points = [heart_function(t) for t in [i * 0.1 for i in range(0, 63)]]

dinos = [(-40, -40)] * 50
indexes = [random.randint(0, len(heart_points) - 1) for _ in range(50)]

def render_3d_text(text, font, center_x, center_y, angle):
    """ Renders a rotating 3D text effect centered on screen. """
    base_text = font.render(text, True, WHITE)

    # Rotate the text
    rotated_text = pygame.transform.rotate(base_text, angle)
    text_rect = rotated_text.get_rect(center=(center_x, center_y))

    # Shadow effect (depth)
    for i in range(5, 0, -1):
        shadow = pygame.transform.rotate(font.render(text, True, DARK_PINK), angle)
        shadow_rect = shadow.get_rect(center=(center_x + i, center_y + i))
        screen.blit(shadow, shadow_rect)

    # Outer glow effect
    outline_offset = 3
    for dx in [-outline_offset, 0, outline_offset]:
        for dy in [-outline_offset, 0, outline_offset]:
            if dx != 0 or dy != 0:
                outline = pygame.transform.rotate(font.render(text, True, GOLD), angle)
                outline_rect = outline.get_rect(center=(center_x + dx, center_y + dy))
                screen.blit(outline, outline_rect)

    # Render main text
    screen.blit(rotated_text, text_rect)

# Initialize Pygame mixer
pygame.mixer.init()

# Load and play background music using relative path
pygame.mixer.music.load(os.path.join(current_directory, "assets", "music", "cute.mp3"))
pygame.mixer.music.play(-1)  # -1 means loop forever

# Main game loop
running = True
while running:
    screen.blit(background_image, (0, 0))

    # Rotate text at center
    render_3d_text("Dino loves Seal!!!", font, WIDTH // 2, HEIGHT // 2, angle)
    angle -= 15  # Smooth rotation

    # Move dinosaurs along heart shape
    for i in range(50):
        dinos[i] = heart_points[indexes[i]]
        screen.blit(scaled_dino, (dinos[i][0] - 20, dinos[i][1] - 20))
        indexes[i] = (indexes[i] + 1) % len(heart_points)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    pygame.time.delay(50)

pygame.quit()
