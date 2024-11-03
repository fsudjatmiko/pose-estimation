import pygame
from camera import list_cameras

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)
RED = (255, 0, 0)
LIGHT_RED = (255, 182, 193)

# Fonts
font = pygame.font.Font(None, 36)

# Load images from the images folder
image_folder = 'images'
images = [f for f in os.listdir(image_folder) if f.endswith(('png', 'jpg', 'jpeg'))]

def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))
    draw_text(text, x + 10, y + 10, WHITE)

def main_menu(set_mode):
    screen.fill(LIGHT_BLUE)
    draw_text("Pose Estimation", WIDTH // 2 - 100, HEIGHT // 4, BLUE)
    draw_button("Use Image", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, BLUE, LIGHT_BLUE, lambda: set_mode('image_selection'))
    draw_button("Use Camera", WIDTH // 2 - 100, HEIGHT // 2, 200, 50, GREEN, LIGHT_GREEN, lambda: set_mode('camera_selection'))
    draw_button("Quit", WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, RED, LIGHT_RED, quit_app)
    pygame.display.flip()

def image_selection(set_mode):
    screen.fill(LIGHT_BLUE)
    draw_text("Select an Image", WIDTH // 2 - 100, HEIGHT // 4, BLUE)
    margin = 20
    image_size = 100
    columns = 5
    x_offset = (WIDTH - (columns * (image_size + margin))) // 2
    y_offset = HEIGHT // 4 + 50
    for i, img in enumerate(images):
        image = pygame.image.load(os.path.join(image_folder, img))
        image = pygame.transform.scale(image, (image_size, image_size))
        x = x_offset + (i % columns) * (image_size + margin)
        y = y_offset + (i // columns) * (image_size + margin)
        screen.blit(image, (x, y))
        draw_button("Select", x, y + image_size + 5, image_size, 30, BLUE, LIGHT_BLUE, lambda img=img: set_mode('pose_image', img))
    draw_button("Back", 10, 10, 100, 30, RED, LIGHT_RED, lambda: set_mode('menu'))
    pygame.display.flip()

def camera_selection(set_mode):
    screen.fill(LIGHT_BLUE)
    draw_text("Select a Camera", WIDTH // 2 - 100, HEIGHT // 4, BLUE)
    y_offset = HEIGHT // 2 - 50
    cameras = list_cameras()
    for i, cam in enumerate(cameras):
        draw_button(f"Camera {cam}", WIDTH // 2 - 100, y_offset + i * 50, 200, 50, GREEN, LIGHT_GREEN, lambda cam=cam: set_mode('pose_camera', cam))
    draw_button("Back", 10, 10, 100, 30, RED, LIGHT_RED, lambda: set_mode('menu'))
    pygame.display.flip()

def quit_app():
    global running
    running = False
